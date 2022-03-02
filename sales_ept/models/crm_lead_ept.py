from odoo import fields,models
from odoo.exceptions import ValidationError, UserError

class CRM_Lead(models.Model):
    _name="crm.lead.ept"
    _description="CRM Lead model"

    partner_id = fields.Many2one(comodel_name='res.partner.ept', string="Partner", help="Partner data will fetch if exist")
    order_ids = fields.One2many(comodel_name='sale.order.ept', inverse_name='lead_id', readonly=True,
                                string="Order No.", help="Order number will be display if once generated")
    team_id = fields.Many2one(comodel_name='crm.team.ept', string="Team Member",
                              help="CRM Team member id field")
    user_id = fields.Many2one(comodel_name='res.users', string="Sales Person", required=True)
    lead_line_ids = fields.One2many(comodel_name='crm.lead.line.ept', inverse_name='lead_id',
                                    string="Lead Lines", help="To identify lead for which product")
    state = fields.Selection(selection=[('New', 'New'), ('Qualified', 'Qualified'), ('Proposition', 'Proposition'),
                                        ('Won', 'Won'), ('Lost', 'Lost')], default='New')
    won_date = fields.Date(string="Won Date", readonly=True, help="Date field which is identify when lead should be converted to sales")
    lost_reason = fields.Text(string="Lost Reason", help="Reason for lead lost")
    next_followup_date = fields.Date(string="Next Followup Date", help="Next followup date field")
    partner_name = fields.Char(string="Partner Name", help="Partner name field of CRM")
    partner_email = fields.Char(string="E-Mail", help="E-Mail field of CRM")
    country_id = fields.Many2one(comodel_name = 'res.country.ept', string="Country", help="Fetch data over module of localization")
    state_id = fields.Many2one(comodel_name ='res.state.ept', string="State", help="Fetch data over module of localization")
    city_id = fields.Many2one(comodel_name ='res.city.ept', string="City", help="Fetch city data over module of localization")
    partner_phone_number = fields.Char(string="Phone Number", help="Phone Number field of CRM")

    def move_to_qualified(self):
        self.state = "Qualified"

    def move_to_proposition(self):
        self.state = "Proposition"

    def move_to_won(self):
        self.state = "Won"
        self.won_date = fields.Date.today()

    def move_to_lost(self):
        self.state = "Lost"

    def generate_partner(self):
        if not self.partner_name:
            raise UserError("Partner name can't left blank")
        else:
            partner = self.env['res.partner.ept']
            partner_data = {
                "name": self.partner_name,
                "country_id": self.country_id.id,
                "state_id": self.state_id.id,
                "city_id": self.city_id.id,
                "email": self.partner_email,
                "phone": self.partner_phone_number,
                "address_type": "Invoice"
            }
            new_record = partner.create(partner_data)
            self.partner_id = new_record.id

    def generate_quotation(self):
        if not self.partner_id and self.partner_name:
            raise UserError("Partner name can't left blank")
        elif not self.lead_line_ids:
            raise UserError("Product data can't left blank")
        else:
            sales_order_line_data = []
            sale_order_line = self.env['sale.order.line.ept']
            for line in self.lead_line_ids:
                product_data = sale_order_line.new({'product': line.product_id})
                product_data.on_change_product()
                sales_order_line_data.append((0, 0, {
                    "product": line.product_id.id,
                    "name_description": line.name,
                    "quantity": line.expected_sell_qty,
                    "unit_price": product_data.product.cost_price,
                    "state": "Draft",
                    "uom_id": product_data.product.uom_id.id
                }))
            sales_order = self.env['sale.order.ept']

            partner_data = sales_order.new({'partner_id': self.partner_id})
            partner_data.on_change_partner()
            sale_order_data = {
                "partner_id": self.partner_id.id,
                "partner_invoice_id": partner_data.partner_invoice_id.id,
                "partner_shipping_id": partner_data.partner_shipping_id.id,
                "sales_person": self.user_id.id,
                "state": "Draft",
                "order_line": sales_order_line_data
            }
            last_inserted_record = sales_order.create(sale_order_data)


            # sales_order = self.env['sale.order.ept']
            # sale_order_data = {
            #     "partner_id": self.partner_id.id,
            #     "partner_invoice_id": self.partner_id.id,
            #     "partner_shipping_id": self.partner_id.id,
            #     "sales_person": self.user_id.id,
            #     "state": "Draft"
            # }
            # last_inserted_record = sales_order.create(sale_order_data)
            #
            # sale_order_line = self.env['sale.order.line.ept']
            # for line in self.lead_line_ids:
            #     product_data = sale_order_line.new({'product': line.product_id})
            #     product_data.on_change_product()
            #     sale_order_line_data = {
            #         "order_line_id": last_inserted_record.id,
            #         "product": line.product_id.id,
            #         "name_description": line.name,
            #         "quantity": line.expected_sell_qty,
            #         "unit_price": product_data.product.cost_price,
            #         "state": "Draft",
            #         "uom_id": product_data.product.uom_id.id
            #     }
            #     sale_order_line.create(sale_order_line_data)

