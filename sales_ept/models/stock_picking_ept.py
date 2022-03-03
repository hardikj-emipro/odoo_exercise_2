from odoo import fields,models,api

class Stock_Picking(models.Model):
    _name = "stock.picking.ept"
    _description="Stock Picking"

    name=fields.Char(string="Transaction Number", help="Automatically generated while insert data")
    partner_id = fields.Many2one(
        comodel_name="res.partner.ept",
        string="Partner",
        help="Shipping partner or vendor information will be set"
    )
    state = fields.Selection(selection=[('Draft', 'Draft'), ('Done', 'Done'),
                                        ('Cancelled', 'Cancelled')], default='Draft')
    sale_order_id = fields.Many2one(
        comodel_name="sale.order.ept",
        string="Sale Order",
        help="Data will fetch from sale order model"
    )

    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order.ept",
        string="Purchase Order",
        help="Data will fetch from purchase order model"
    )

    transaction_type=fields.Selection(selection=[('In', 'In'), ('Out', 'Out')], default='In')

    move_ids=fields.One2many(
        comodel_name="stock.move.ept",
        inverse_name="picking_id",
        string="Move stock",
        help="This will store information about product stock"
    )

    transaction_date = fields.Date(string="Date", default=fields.Date.today(), help="Store today's date")

    @api.model
    def create(self, vals):
        if vals.get("transaction_type") == "Out":
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.picking.out')
        else:
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.picking.in')
        last_stock_picking_record = super(Stock_Picking, self).create(vals)
        return last_stock_picking_record
