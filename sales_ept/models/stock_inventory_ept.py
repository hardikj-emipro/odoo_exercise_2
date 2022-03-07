from odoo import fields,models,api

class Stock_Inventory(models.Model):
    _name="stock.inventory.ept"
    _description="Stock Inventory"

    name=fields.Char(string="Inventory Name", required=True, help="Inventory Name field")
    state = fields.Selection(selection=[('Draft', 'Draft'), ('In-Progress', 'In-Progress'), ('Done', 'Done'),
                                        ('Cancelled', 'Cancelled')], default='Draft')
    location_id=fields.Many2one(
        comodel_name="stock.location.ept",
        string="Location",
        required=True,
        help="M2O for location field"
    )
    inventory_date=fields.Date(string="Inventory Date", default=fields.Date.today(), help="Inventory Date Field")
    inventory_line_ids = fields.One2many(
        comodel_name="stock.inventory.line.ept",
        inverse_name="inventory_id",
        string="Inventory Line",
        help="Inventory line data"
    )
    stock_move_ids=fields.One2many(
        comodel_name = "stock.move.ept",
        readonly=True,
        inverse_name="stock_inventory_id",
        help="O2M field with stock move model"
    )

    def btn_start_inventory(self):
        self.state = "In-Progress"
        for line in self.inventory_line_ids:
            line.available_quantity = line.product_id.with_context(location_id = self.location_id).product_stock

    def btn_validate_inventory(self):
        adjustment_location = self.env['stock.location.ept'].search([('name', '=', "Adjustment Location")])
        stock_location = self.env['stock.location.ept'].search([('name', '=', "Stock Location")])
        for line in self.inventory_line_ids:
            if line.difference > 0:
                description = line.product_id.name + ":" + stock_location.name + "->" + adjustment_location.name
                stock_move = self.env['stock.move.ept'].create({
                    "name": description,
                    "product_id": line.product_id.id,
                    "uom_id": line.product_id.uom_id.id,
                    "source_location_id": stock_location.id,
                    "destination_location_id": adjustment_location.id,
                    "qty_to_deliver": abs(line.difference),
                    "qty_to_done": abs(line.difference),
                    "state":"Done",
                    "stock_inventory_id": self.id
                })
            elif line.difference < 0:
                description = line.product_id.name + ":" + adjustment_location.name + "->" + stock_location.name
                stock_move = self.env['stock.move.ept'].create({
                    "name": description,
                    "product_id": line.product_id.id,
                    "uom_id": line.product_id.uom_id.id,
                    "source_location_id": adjustment_location.id,
                    "destination_location_id": stock_location.id,
                    "qty_to_deliver": abs(line.difference),
                    "qty_to_done": abs(line.difference),
                    "state": "Done",
                    "stock_inventory_id": self.id
                })
        self.state = "Done"
