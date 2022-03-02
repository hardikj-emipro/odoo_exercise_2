from odoo import fields,models

from odoo import api


class CRM_Lead_Lines(models.Model):
    _name="crm.lead.line.ept"
    _description="CRM Lead Line Model"

    product_id = fields.Many2one(comodel_name="product.ept", string="Product",
                          help="Product from product model")
    name = fields.Char(string="Product Description", help="Description will fetch from product master")
    expected_sell_qty = fields.Float(string="Quantity", digit=(6,2), help="Quantity field from lead lines")
    uom_id = fields.Many2one(comodel_name="product.uom.ept", string="Unit",
                             help="Unit from product unit model")
    lead_id = fields.Many2one(comodel_name="crm.lead.ept", string="Lead Id",
                              help="Lead id field many2one")

    @api.onchange('product_id')
    def on_change_product(self):
        if self.product_id:
            name = self.product_id.product_description
            if not name:
                name = self.product_id.name
            self.name = name
            self.uom_id = self.product_id.uom_id.id
            self.expected_sell_qty = 1
