from odoo import fields,models,api

class Sale_Order_Line(models.Model):
    _name="sale.order.line"
    _inherit="sale.order.line"

    @api.onchange('product_uom_qty')
    def on_change_quantity(self):
        for line in self.order_id.order_line:
            if line.product_id.id == self.product_id.deposite_product_id.id:
                self.order_id.action_manage_deposite(self.env['sale.order.line'].browse(line.ids[0]))
                break
