from odoo import fields,models

class Partner(models.Model):
    _name="res.partner.ept"
    _description="Cross module sample demo"

    name=fields.Char(string="Name", required=True, help="Name field for partner")
    street_1=fields.Char(string="Street 1", help="stree1 of address field")
    street_2=fields.Char(string="Street 2", help="stree2 of address field")
    country_id = fields.Many2one('res.country.ept', string="Country", help="Fetch data over module of localization")
    state_id=fields.Many2one('res.state.ept', string="State", help="Fetch data over module of localization")
    city_id=fields.Many2one('res.city.ept', string="City", help="Fetch city data over module of localization")
    zip_code=fields.Char(string="Zip Code", help="Zip code field for partner model")
    email=fields.Char(string="E-Mail", help="E-Mail address of partner")
    mobile=fields.Char(string="Mobile No.", help="Mobile Number of partner")
    phone=fields.Char(string="Phone No.", help="Phone Number of partner")
    photo=fields.Image(string="Image", help="Image field of partner model")
    website=fields.Char(string="Website", help="Website of partner")
    is_active=fields.Boolean(string="Is Active", default=True, help="Is active or not field by default is True")
    parent_id=fields.Many2one('res.partner.ept', string="Parent", help="Data of this field came from id of same model")
    child_ids=fields.One2many('res.partner.ept','parent_id', string="Child", help="Data of this field came from parent_id of same model")
    address_type = fields.Selection(selection=[('Invoice', 'Invoice'), ('Shipping', 'Shipping'), ('Contact', 'Contact')])

    # def copy(self):
    #     default={'name': self.name+"-Copy"}
    #     new_record = super(Partner, self).copy(default)
    #     return new_record

    def duplicate_the_country(self):
        print(self.country_id.copy())