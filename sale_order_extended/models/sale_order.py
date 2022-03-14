from odoo import fields,models

class Sale_Order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    lead_id = fields.Many2one(
        comodel_name = 'crm.lead',
        string='Lead',
        help = 'Inherited from crm.lead model'
    )

    def action_confirm(self):
        new_product_id = self.env.ref("sale_order_extended.shipping_product_service")
        sale_order_line = self.order_line.create({
            "product_id": new_product_id.id,
            "name":new_product_id.name,
            "product_uom_qty": 1,
            "price_unit": new_product_id.list_price,
            "order_id": self.id
        })
        action = super(Sale_Order, self).action_confirm()
        return action

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
        action["domain"] = [("id","!=",self.id), ("product_id")]
        print(action)




