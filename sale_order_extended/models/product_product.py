from odoo import fields,models

class Product_Product(models.Model):
    _name="product.product"
    _inherit = "product.product"

    deposite_product_id = fields.Many2one(
        comodel_name="product.product",
        string = "Deposite Product",
        help="Many2one Relation with same model"
    )
    deposite_product_qty = fields.Integer(string="Deposite Quantity", help="Quantity for deposite product")

