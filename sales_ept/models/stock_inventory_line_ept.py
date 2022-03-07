from odoo import fields,models,api

class Stock_Inventory_Line(models.Model):
    _name="stock.inventory.line.ept"
    _description="Stock Inventory Line"

    product_id = fields.Many2one(
        comodel_name="product.ept",
        string="Product",
        help="Product Name field from Product Model"
    )
    available_quantity=fields.Float(string="System Quantity", readonly=True, help="Available Quantity Field")
    counted_product_quantity=fields.Float(string="Counted Quantity", help="User will input for actual quantity")
    difference=fields.Float(string="Difference", help="System will calculate", store=False, compute="calculate_stock")
    inventory_id=fields.Many2one(
        comodel_name="stock.inventory.ept",
        string="Inventory",
        help="M2O field with Inventory model"
    )

    @api.depends('counted_product_quantity')
    def calculate_stock(self):
        for line in self:
            line.difference = (line.counted_product_quantity - line.available_quantity)
