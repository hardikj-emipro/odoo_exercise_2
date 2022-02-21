from odoo import models,fields

class City_Demo(models.Model):
    _name="res.city.ept"
    _description="Localization city demo with table relationship concepts"

    name=fields.Char(string="City Name", help="City name Field of localization version 2 module")
    state_id=fields.Many2one('res.state.ept', string="State", help="State field id from state model", ondelete="set null")
