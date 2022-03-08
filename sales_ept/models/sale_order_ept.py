from odoo import fields, models

from odoo import api


class Sale_Order(models.Model):
    _name = "sale.order.ept"
    _description = "Sale Order"
    _rec_name = "order_number"

    order_number = fields.Char(string="Order No.", help="Order number for each separate order", readonly=True)
    partner_id = fields.Many2one(comodel_name='res.partner.ept', required=True,
                                 string="Customer", help="Customer data loaded from partner model with filter")
    partner_invoice_id = fields.Many2one(comodel_name='res.partner.ept',
                                         required=True, string="Invoice", help="Invoice customer data "
                                                                               "loaded based on main customer")
    partner_shipping_id = fields.Many2one(comodel_name='res.partner.ept',
                                          required=True, string="Shipping", help="Shipping customer data "
                                                                                 "loaded based on main customer")
    order_date=fields.Date(string="Order Date", default=fields.Date.today(), help="Date of order")
    sales_person=fields.Many2one(comodel_name='res.users', string="Sales Person", help="This data is "
                                                                                       "loaded from res.users model")
    state=fields.Selection(selection=[('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Done', 'Done'),
                                          ('Cancelled', 'Cancelled')], default='Draft')
    order_line=fields.One2many(comodel_name='sale.order.line.ept',inverse_name='order_line_id',
                                string="Order Line",help="This data is from order model")

    total_weight=fields.Float(string="Total Weight", digits=(6,2), compute="compute_total_weight", store=False, help="Display total weight", readonly=True)
    total_volume=fields.Float(string="Total Volume", digits=(6,2), compute="compute_total_volume", store=False, help="Display total volume", readonly=True)
    order_total = fields.Float(string="Order Amount", compute="compute_order_total", store=True, help="Store order amount data")
    lead_id = fields.Many2one(comodel_name="crm.lead.ept", string="Lead Id",
                              help="Lead id field many2one")
    warehouse_id=fields.Many2one(
        comodel_name="stock.warehouse.ept",
        string="Warehouse",
        help="Data fetch from warehouse model"
    )
    picking_ids=fields.One2many(
        comodel_name="stock.picking.ept",
        inverse_name="sale_order_id",
        string="Stock Picking Data",
        help="O2M field picking_ids"
    )

    delivery_order_count = fields.Integer(store=False, help="Total Delivery Orders", compute="compute_delivery_order")

    stock_move_count = fields.Integer(store=False, help="Total Move Orders", compute="compute_move_orders")

    def compute_delivery_order(self):
        tmp_count = 0
        for id in self.picking_ids:
            tmp_count += 1
        self.delivery_order_count = tmp_count

    def compute_move_orders(self):
        tmp_count = 0
        for id in self.picking_ids.move_ids:
            tmp_count += 1
        self.stock_move_count = tmp_count


    @api.depends('order_line.product')
    def compute_total_weight(self):
        for order in self:
            total_weight = 0
            for line in order.order_line:
                total_weight += line.product.weight
            order.total_weight = total_weight

    @api.depends('order_line.product')
    def compute_total_volume(self):
        for order in self:
            total_volume = 0
            for line in order.order_line:
                total_volume += line.product.volume
            order.total_volume = total_volume

    @api.depends('order_line.subtotal_without_tax')
    def compute_order_total(self):
        for order in self:
            order_total = 0
            for line in order.order_line:
                order_total += line.subtotal_without_tax
            order.order_total = order_total

    @api.onchange('partner_id')
    def on_change_partner(self):
        if self.partner_id:
            partner_invoice = self.partner_id.child_ids.filtered(lambda child: child.address_type == 'Invoice')
            partner_shipping = self.partner_id.child_ids.filtered(lambda child: child.address_type == 'Shipping')

            if not partner_invoice:
                self.partner_invoice_id = self.partner_id
            else:
                self.partner_invoice_id = partner_invoice[0]

            if not partner_shipping:
                self.partner_shipping_id = self.partner_id
            else:
                self.partner_shipping_id = partner_shipping[0]

    @api.model
    def create(self,vals):
        vals['order_number'] = self.env['ir.sequence'].next_by_code('sale.order')
        sale_order_data = super(Sale_Order, self).create(vals)
        return sale_order_data

    # def confirm_sale_order(self):
    #     self.state = "Confirmed"
    #     stock_move_line_data = []
    #     location = self.env['stock.location.ept']
    #     customer_location = location.search([('name', '=', 'Customer')])
    #     for line in self.order_line:
    #         line.state = "Confirmed"
    #         modified_product_name = line.product.name + ":" + self.warehouse_id.stock_location_id.name + "->" + customer_location.name
    #         stock_move_line_data.append((0,0,
    #             {
    #                 "name": modified_product_name,
    #                 "product_id": line.product.id,
    #                 "uom_id": line.uom_id.id,
    #                 "source_location_id": self.warehouse_id.stock_location_id.id,
    #                 "destination_location_id": customer_location.id,
    #                 "qty_to_deliver": line.quantity,
    #                 "state": "Draft",
    #                 "sale_line_id": line.id,
    #             }
    #         ))
    #     stock_picking = self.env['stock.picking.ept']
    #     stock_picking_data = {
    #         "partner_id": self.partner_id.id,
    #         "state": "Draft",
    #         "sale_order_id": self.id,
    #         "transaction_type": "Out",
    #         "move_ids":stock_move_line_data
    #     }
    #     last_record_of_stock_picking = stock_picking.create(stock_picking_data)
    #     return last_record_of_stock_picking

    def confirm_sale_order(self):
        self.state = "Confirmed"
        stock_move_line_data = []
        location = self.env['stock.location.ept']
        customer_location = location.search([('name', '=', 'Customer')])
        list_warehouse_id = []

        for line in self.order_line:
            if line.warehouse_id.id == False:
                list_warehouse_id.append(self.warehouse_id.id)
            elif line.warehouse_id.id not in list_warehouse_id:
                list_warehouse_id.append(line.warehouse_id.id)

        tmp_warehouse_id = list(dict.fromkeys(list_warehouse_id))

        for id in tmp_warehouse_id:
            stock_move_line_data = []
            order_lines = False
            if id == self.warehouse_id.id:
                order_lines = self.order_line.filtered(lambda line: line.warehouse_id.id == self.warehouse_id.id or line.warehouse_id.id == False)
            else:
                order_lines = self.order_line.filtered(
                    lambda line: line.warehouse_id.id == id)
            for line in order_lines:
                    stock_location_name = line.warehouse_id.stock_location_id.name if line.warehouse_id else self.warehouse_id.stock_location_id.name
                    line.state = "Confirmed"
                    modified_product_name = line.product.name + ":" + stock_location_name + "->" + customer_location.name
                    stock_move_line_data.append((0, 0,
                                             {
                                                 "name": modified_product_name,
                                                 "product_id": line.product.id,
                                                 "uom_id": line.uom_id.id,
                                                 "source_location_id": self.warehouse_id.stock_location_id.id,
                                                 "destination_location_id": customer_location.id,
                                                 "qty_to_deliver": line.quantity,
                                                "sale_line_id": line.id
                                            }
                                            ))
            stock_picking = self.env['stock.picking.ept']
            stock_picking_data = {
                "partner_id": self.partner_id.id,
                "sale_order_id": self.id,
                "transaction_type": "Out",
                "move_ids": stock_move_line_data
            }
            last_record_of_stock_picking = stock_picking.create(stock_picking_data)
        return last_record_of_stock_picking

    def btn_open_delivery_orders(self):
        action = {
            'name': "Delivery orders",
            'res_model': 'stock.picking.ept',
            'type': 'ir.actions.act_window'
        }
        if len(self.picking_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.picking_ids[0].id
            })
        else:
            action.update({
                'name': "Delivery orders",
                'domain': [('id', 'in', self.picking_ids.ids)],
                'view_mode': 'tree'
            })
        return action

    def btn_open_stock_moves(self):
        action = {
            'name': "Stock Move",
            'res_model': 'stock.move.ept',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.picking_ids.move_ids.ids)],
            'view_mode': 'tree'
        }
        return action


