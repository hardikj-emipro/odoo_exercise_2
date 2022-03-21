from odoo import fields,models

class Sale_Order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    lead_id = fields.Many2one(
        comodel_name = 'crm.lead',
        string='Lead',
        help = 'Inherited from crm.lead model'
    )

    is_all_picking_completed = fields.Boolean(string="Order Done", default=False, compute="get_done_orders", search="get_done_orders")

    total_profit = fields.Float(string="Total Profit", compute="compute_total_profit")
    total_profit_percentage = fields.Float(string="Total Profit Percentage")

    date_format = fields.Selection(string="Date Format",
                                   selection=[('ddMMyyyy', 'DD/MM/YYYY'), ('mmDDyyyy', 'MM/DD/YYYY')],
                                   default="ddMMyyyy")

    def compute_total_profit(self):
        total_profit = 0
        for line in self.order_line:
            total_profit += line.profit_value
        self.total_profit = total_profit
        self.total_profit_percentage = self.total_profit * 100 / self.amount_untaxed

    def get_done_orders(self, operator=False, value=False):
        sql = "select id from sale_order where id not in (select sale_id from stock_picking where state not in ('done', 'cancel') and sale_id is not null group by sale_id);"
        self._cr.execute(sql)
        res = list(map(lambda lst: lst[0], self._cr.fetchall()))
        sale_orders = self.browse(res)
        sale_orders.is_all_picking_completed = True
        remaining_orders = self - sale_orders
        remaining_orders.is_all_picking_completed = False
        return [("id", "in", res)]


    def action_confirm(self):
        # new_product_id = self.env.ref("sale_order_extended.shipping_product_service")
        # sale_order_line = self.order_line.create({
        #     "product_id": new_product_id.id,
        #     "name":new_product_id.name,
        #     "product_uom_qty": 1,
        #     "price_unit": new_product_id.list_price,
        #     "order_id": self.id
        # })
        action = super(Sale_Order, self).action_confirm()
        return action

    def action_confirm_validate(self):
        self.action_confirm()
        self.picking_ids.move_lines._set_quantities_to_reservation()
        self.picking_ids.with_context(cancel_backorder=False)._action_done()

    def action_manage_deposite(self, current_obj = False):
        deposite_product_list = []
        for line in self.order_line:
            if line.product_id.deposite_product_id.id\
                    and line.product_id.deposite_product_id.id not in self.order_line.product_id.ids:
                deposite_product_list.append({
                    "product_id": line.product_id.deposite_product_id.id,
                    "name": line.product_id.deposite_product_id.name,
                    "product_uom_qty": line.product_id.deposite_product_qty,
                    "price_unit": line.product_id.deposite_product_id.list_price,
                    "order_id": self.id
                })
                sale_order_line = self.order_line.create(deposite_product_list)
            else:
                if current_obj:
                    sale_order_line = current_obj
                    sale_order_line.product_uom_qty += line.product_id.deposite_product_qty
                    break
                sale_order_line.product_uom_qty += line.product_id.deposite_product_qty
        return sale_order_line

    def action_collect_products(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale_order_extended.action_sale_order_line")
        action["domain"] = [("id","not in",self.order_line.ids), ("product_id","in",self.order_line.product_id.ids),
                            ("move_ids", "=", "assigned")]
        return action




