from odoo import fields,models

class Country(models.Model):
    _name="res.country.ept"
    _description="Localization country demo with table relationship concepts"

    name=fields.Char(string="Country Name", help="Country Name field of localization module")
    short_code=fields.Char(string="Short Code", help="Country code like US for America")
    state_ids=fields.One2many('res.state.ept', 'country_id', string="State of Country", help="Display number of state from state model")

    _sql_constraints = [
        ('unique_country_code', 'unique(short_code)', 'Country code must be unique...')
    ]