from odoo import fields,models,api

class Purchase_Order(models.Model):
    _name="purchase.order.ept"
    _description="Purchase Order"

    warehouse_id=fields.Many2one(
        comodel_name="stock.warehouse.ept",
        string="Warehouse",
        help="Fetch data of warehouse model"
    )
    partner_id=fields.Many2one(
        comodel_name="res.partner.ept",
        string="Vendor/Supplier",
        help="Data fetch from partner model"
    )
    order_date=fields.Date(string="Date", default=fields.Date.today(), help="Default today's date")
    name=fields.Char(string="Order Number", help="Auto generated Order Number", readonly=True)
    state = fields.Selection(selection=[('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Done', 'Done'),
                                        ('Cancelled', 'Cancelled')], default='Draft')
    purchase_order_line_ids=fields.One2many(
        comodel_name="purchase.order.line.ept",
        inverse_name="purchase_order_id",
        string="Order Line",
        help="One2many field for manage oder lines"
    )
    picking_ids = fields.One2many(
        comodel_name="stock.picking.ept",
        inverse_name="purchase_order_id",
        string="Stock Picking Data",
        help="O2M field picking_ids"
    )

    @api.model
    def create(self,vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order')
        purchase_order_data = super(Purchase_Order, self).create(vals)
        return purchase_order_data

    def confirm_purchase_order(self):
        self.state = "Confirmed"
        stock_move_line_data = []
        location = self.env['stock.location.ept']
        vendor_location = location.search([('name', '=', 'Vendor')])
        for line in self.purchase_order_line_ids:
            line.state = "Confirmed"
            modified_product_name = line.product_id.name + ":" + vendor_location.name + "->" + self.warehouse_id.stock_location_id.name
            stock_move_line_data.append((0, 0,
                                         {
                                             "name": modified_product_name,
                                             "product_id": line.product_id.id,
                                             "uom_id": line.uom_id.id,
                                             "source_location_id": vendor_location.id,
                                             "destination_location_id": self.warehouse_id.stock_location_id.id,
                                             "qty_to_deliver": line.quantity,
                                             "state": "Draft",
                                             "purchase_line_id": line.id,
                                         }
                                         ))
        stock_picking = self.env['stock.picking.ept']
        stock_picking_data = {
            "partner_id": self.partner_id.id,
            "state": "Draft",
            "purchase_order_id": self.id,
            "transaction_type": "In",
            "move_ids": stock_move_line_data
        }
        last_record_of_stock_picking = stock_picking.create(stock_picking_data)
        return last_record_of_stock_picking