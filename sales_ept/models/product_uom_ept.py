from odoo import fields,models

class Product_UOM(models.Model):
    _name="product.uom.ept"
    _description="Management of unit"

    name=fields.Char(string="Unit Name", help="Unit field of unit master")
    unit_category_id = fields.Many2one('product.uom.category.ept', string="Unit Category", help="Unit category id from unit category model")
