from odoo import fields,models,api

class Purchase_Order_Lines(models.Model):
    _name="purchase.order.line.ept"
    _description="Purchase Order Line"

    purchase_order_id=fields.Many2one(
        comodel_name="purchase.order.ept",
        string="Purchase Order",
        help="For reference many2one field"
    )
    product_id=fields.Many2one(
        comodel_name="product.ept",
        string="Product",
        help="Fetch data from product model"
    )
    name=fields.Char(string="Description", help="Product Description")
    quantity=fields.Float(string="Quantity", help="Quantity Field")
    cost_price=fields.Float(string="Price", help="Price Field")
    state = fields.Selection(selection=[('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Done', 'Done'),
                                        ('Cancelled', 'Cancelled')], default='Draft')
    uom_id=fields.Many2one(
        comodel_name="product.uom.ept",
        string="Unit",
        help="Unit name will be loaded from unit model"
    )