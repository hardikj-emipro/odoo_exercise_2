from odoo import fields,models,api

class Stock_Move(models.Model):
    _name="stock.move.ept"
    _description="Sotck Movement"

    name=fields.Char(string="Description", help="Display Product Description with source & destination")
    product_id=fields.Many2one(
        comodel_name="product.ept",
        string="Product",
        help="display product"
    )
    uom_id=fields.Many2one(
        comodel_name="product.uom.ept",
        string="Unit",
        help="display Unit data"
    )
    source_location_id=fields.Many2one(
        comodel_name="stock.location.ept",
        string="Source Location",
        help="Display source location"
    )
    destination_location_id=fields.Many2one(
        comodel_name="stock.location.ept",
        string="Destination Location",
        help="Display destination location"
    )
    qty_to_deliver=fields.Float(string="Demand", help="Expected Quantity")
    qty_to_done = fields.Float(string="Done Quantity", help="Actual Quantity")
    state = fields.Selection(selection=[('Draft', 'Draft'), ('Done', 'Done'),
                                        ('Cancelled', 'Cancelled')], default='Draft')
    sale_line_id=fields.Many2one(
        comodel_name="sale.order.line.ept",
        string = "Sale Order Line",
        help="Get data from sale order model"
    )
    purchase_line_id=fields.Many2one(
        comodel_name="purchase.order.line.ept",
        string="Purchase Order Line",
        help="Get data from purchase order model"
    )
    stock_inventory_id=fields.Many2one(
        comodel_name="stock.inventory.ept",
        string="Stock Inventory",
        help="Data fetch from Stock Inventory Model"
    )
    picking_id=fields.Many2one(
        comodel_name="stock.picking.ept",
        string="Stock Picking",
        help="Data fetch from Stock Picking Model"
    )