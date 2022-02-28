from odoo import models,fields

class Product_UOM_Category(models.Model):
    _name="product.uom.category.ept"
    _description="TO manage unit for product like Kg., Ltr. etc."

    name=fields.Char(string="Unit Category Name", help="Category of unit of unit model")
    uom_ids=fields.One2many('product.uom.ept', 'unit_category_id', string="Unit", help="To identify which unit is in which category")