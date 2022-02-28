from odoo import fields,models

class Product_EPT(models.Model):
    _name="product.ept"
    _description="This model is part of sales and it is connected with product category and sales"

    category_id = fields.Many2one('product.category.ept', string="Product Category",
                                  help="Product will be categorized product category wise")
    name=fields.Char(string="Product Name", help="Product Name field of product.ept model")
    sku=fields.Char(string="SKU", help="Product sku field which is identify to particular product code wise")
    weight=fields.Float(string="Weight", help="To store weight of each product")
    length=fields.Float(string="Length", help="To store length of each product")
    volume=fields.Float(string="Volume", help="To store volume of each product")
    width=fields.Float(string="Width", help="To store width of each product")
    barcode=fields.Char(string="Barcode Character", help="To store character of barcode particular product wise")
    product_type = fields.Selection(selection=[('Storable', 'Storable'), ('Consumable', 'Consumable'), ('Service', 'Service')])
    sale_price = fields.Float(string="Sale Price", help="Sales price field of product model")
    cost_price=fields.Float(string="Purchase Price", help="Purchase price field of product model")
    uom_id = fields.Many2one('product.uom.ept', string="Unit", help="Unit for product will use in sales and purchase transaction")
    product_description=fields.Text(string="Description", help="Product description field of product model")


