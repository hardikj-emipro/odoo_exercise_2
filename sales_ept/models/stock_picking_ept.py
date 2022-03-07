from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError

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

    back_order_id = fields.Many2one(
        comodel_name="stock.picking.ept",
        string="Partial Order",
        help="To manage partial delivery"
    )

    @api.model
    def create(self, vals):
        if vals.get("transaction_type") == "Out":
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.picking.out')
        else:
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.picking.in')
        last_stock_picking_record = super(Stock_Picking, self).create(vals)
        return last_stock_picking_record

    def validate_stock(self):
        stock_move_line_data = []
        for line in self.move_ids:
            tmp_balance = (line.qty_to_deliver - line.qty_to_done)
            if tmp_balance != 0:
                if line.qty_to_done <= line.qty_to_deliver:
                    stock_move_line_data.append((0, 0,
                                             {
                                                 "name": line.name,
                                                 "product_id": line.product_id.id,
                                                 "uom_id": line.uom_id.id,
                                                 "source_location_id": line.source_location_id.id,
                                                 "destination_location_id": line.destination_location_id.id,
                                                 "qty_to_deliver": tmp_balance,
                                                 "qty_to_done": 0,
                                                 "sale_line_id": line.sale_line_id.id or False,
                                                 "purchase_line_id": line.purchase_line_id.id or False,
                                             }
                                             ))

                    line.write({"state": "Done" , "qty_to_deliver": line.qty_to_done})
                    if line.qty_to_done == 0:
                        line.unlink()
            else:
                line.write({"state": "Done", "qty_to_done": line.qty_to_deliver})


        if stock_move_line_data:
            stock_picking = self.env['stock.picking.ept']
            stock_picking_data = {
                "partner_id": self.partner_id.id,
                "sale_order_id": self.sale_order_id.id or False,
                "purchase_order_id":self.purchase_order_id or False,
                "transaction_type": self.transaction_type,
                "move_ids": stock_move_line_data,
                "back_order_id": self.id
            }
            last_record_of_stock_picking = stock_picking.create(stock_picking_data)
            self.state = "Done"
        else:
            raise UserError("Kindly enter valid quantity in done quantity")
        return last_record_of_stock_picking
