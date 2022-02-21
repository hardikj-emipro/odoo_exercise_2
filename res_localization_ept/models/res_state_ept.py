from odoo import fields,models

class State_Demo(models.Model):
    _name="res.state.ept"
    _description="Localization state demo with table relationship concepts"

    name=fields.Char(string="State Name", help="State Name Field of localization version 2 module")
    state_code = fields.Char(string="State Code", help="Short code for state like GJ or 24 for Gujarat")
    country_id = fields.Many2one('res.country.ept', string="Country", ondelete="set null")
    city_ids = fields.One2many('res.city.ept', 'state_id', string="City of state", help="Display number of cities available in each state")