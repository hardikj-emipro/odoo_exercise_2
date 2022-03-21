from odoo import fields,models,api

class Sale_Order_Line(models.Model):
    _name="sale.order.line"
    _inherit="sale.order.line"


    profit_value = fields.Float(string="Profit Value", compute="compute_profit_value", store=True)
    profit_percentage = fields.Float(string="Profit(%)")
    warehouse_ept_id = fields.Many2one(
        comodel_name = "stock.warehouse",
        string = "Warehouse EPT"
    )

    def _prepare_procurement_values(self, group_id=False):
        existing_val = super(Sale_Order_Line, self)._prepare_procurement_values(group_id = group_id)
        if self.warehouse_ept_id:
            existing_val.update({'warehouse_id': self.warehouse_ept_id})
        return existing_val


    def compute_profit_value(self):
        for line in self:
            if not line.profit_value:
                line.profit_value = line.product_id.list_price - line.product_id.standard_price
                line.profit_percentage = line.profit_value * 100 / line.product_id.list_price


    @api.onchange('product_uom_qty')
    def on_change_quantity(self):
        pass
        # for line in self.order_id.order_line:
        #     if line.product_id.id == self.product_id.deposite_product_id.id:
        #         self.order_id.action_manage_deposite(self.env['sale.order.line'].browse(line.ids[0] if line.ids else 0))
        #         break
