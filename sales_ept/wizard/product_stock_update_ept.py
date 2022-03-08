from odoo import fields,models,api

class Product_Stock_Update(models.TransientModel):
    _name = "product.stock.update.ept"
    _description = "To update stock for each product"

    location_id = fields.Many2one(
        comodel_name = "stock.location.ept",
        string = "Location",
        help = "TO Update stock product wise"
    )

    available_stock = fields.Float(string="System Quantity", help="Available Quantity Field")

    counted_quantity = fields.Float(string="Counted Quantity", required = True, help="User will input for actual quantity")

    difference_quantity = fields.Float(string="Difference", help="System will calculate", store=False,
                                       compute="calculate_stock")


    @api.onchange('location_id')
    def on_change_location(self):
        if self.location_id:
            product_ids = self.env.context.get('active_ids')
            product_id = self.env['product.ept'].browse(product_ids[0])
            self.available_stock = product_id.with_context(location_id=self.location_id.ids).product_stock

    @api.depends('counted_quantity')
    def calculate_stock(self):
        for line in self:
            line.difference_quantity = (line.counted_quantity - line.available_stock)

    def btn_update_stock_click(self):
        product_ids = self.env.context.get('active_ids')
        product_id = self.env['product.ept'].browse(product_ids[0])
        stock_inventory_line_data = []
        stock_inventory_line = {
            "product_id": product_id.id,
            "available_quantity": self.available_stock,
            "counted_product_quantity": self.counted_quantity,
        }
        stock_inventory_line_data.append((0,0,stock_inventory_line))
        stock_inventory = self.env['stock.inventory.ept'].create(
            {
                "name": product_id.name + " - " + "Stock Update",
                "location_id": self.location_id.id,
                "inventory_line_ids": stock_inventory_line_data
            }
        )
        stock_inventory.btn_validate_inventory()