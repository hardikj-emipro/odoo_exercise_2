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

    tax_ids = fields.Many2many(
        comodel_name="account.tax.ept",
        string="Tax",
        help="Load only sales type tax",
        domain="[('tax_use','=','Sales')]"
    )

    subtotal_with_tax = fields.Float(
        string="Sub total with tax",
        help="Calculate Total with tax",
        digit=(6,2),
        compute="calculate_sub_total_with_tax"
    )

    stock_move_ids=fields.One2many(
        comodel_name="stock.move.ept",
        inverse_name="sale_line_id",
        string = "Stock Move Data"
    )

    delivered_qty = fields.Float(string="Delivered Quantity", store=False, compute="compute_delivered_quantity",
                                 help="Compute Field for count delivered quantity")

    cancelled_qty = fields.Float(string="Cancelled Quantity", store=False, compute="compute_cancelled_quantity",
                                 help="Compute Field for count cancelled quantity")

    warehouse_id = fields.Many2one(
        comodel_name = "stock.warehouse.ept",
        string = "Warehouse",
        help = "Warehouse wise stock movement process"
    )

    def compute_delivered_quantity(self):
        stock_move = self.env['stock.move.ept']
        for line in self:
            total_delivered = 0
            stock_moves = stock_move.search([('sale_line_id','=',line.id),('state', '=' , 'Done')])
            for stock_move in stock_moves:
                total_delivered += stock_move.qty_to_done
        self.delivered_qty = total_delivered

    def compute_cancelled_quantity(self):
        stock_move = self.env['stock.move.ept']
        for line in self:
            total_cancelled = 0
            stock_moves = stock_move.search([('sale_line_id', '=', line.id), ('state', '=', 'Cancelled')])
            for stock_move in stock_moves:
                total_cancelled += stock_move.qty_to_done
        self.cancelled_qty = total_cancelled

    @api.depends('quantity', 'unit_price')
    def compute_subtotal_without_tax(self):
        for line in self:
            line.subtotal_without_tax = line.quantity * line.unit_price

    @api.depends('quantity', 'unit_price')
    def calculate_sub_total_with_tax(self):
        for line in self:
            if line.product.tax_ids.tax_amount_type == "Percentage":
                line.subtotal_with_tax = line.subtotal_without_tax + (line.subtotal_without_tax * line.tax_ids.tax_value) / 100
            else:
                line.subtotal_with_tax = line.subtotal_without_tax +  line.tax_ids.tax_value

    @api.onchange('product')
    def on_change_product(self):
        if self.product:
            self.unit_price = self.product.sale_price
            self.tax_ids = self.product.tax_ids.ids
            self.quantity = 1


