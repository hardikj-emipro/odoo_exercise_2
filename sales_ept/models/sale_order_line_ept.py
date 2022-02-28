from odoo import fields,models

from odoo import api


class Sale_Order_Lines(models.Model):
    _name="sale.order.line.ept"
    _description="Sales Order Lines"
    _rec_name = "order_line_id"

    order_line_id=fields.Many2one(comodel_name='sale.order.ept',
                                 string="Order Number",
                                 help="Order Lines Reference with Sales Order")
    product=fields.Many2one(comodel_name='product.ept',
                            string="Product",
                            help="Product data from Product Model")
    name_description=fields.Text(string="Product Description",
                                 help="Product Description Field")
    quantity=fields.Float(string="Quantity",
                          help="Quantity Fields")
    unit_price=fields.Float(string="Price",
                            help="Unit Price or Sales Price field")
    state = fields.Selection(selection=[('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Done', 'Done'),
                                        ('Cancelled', 'Cancelled')], default='Draft',
                             string="Status")
    uom_id=fields.Many2one(comodel_name='product.uom.ept',
                           string="Unit",
                           help="Unit field")

    subtotal_without_tax = fields.Float(string="Sub Total", compute='compute_subtotal_without_tax', store=True)

    # def compute_subtotal_without_tax(self):
    #     for line in self:
    #         line.subtotal_without_tax = line.quantity * line.unit_price

    @api.depends('quantity', 'unit_price')
    def compute_subtotal_without_tax(self):
        for line in self:
            line.subtotal_without_tax = line.quantity * line.unit_price

    @api.onchange('product')
    def on_change_product(self):
        self.unit_price = self.product.sale_price
        self.quantity = 1


