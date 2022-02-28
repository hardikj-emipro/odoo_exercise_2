from odoo import models,fields

class Product_Category(models.Model):
    _name="product.category.ept"
    _description="Sales Module Demo"

    name=fields.Char(string="Category Name", help="Category field of product category model")
    parent_id = fields.Many2one('product.category.ept', string="Parent Category", help="Parent category field of product category model")
