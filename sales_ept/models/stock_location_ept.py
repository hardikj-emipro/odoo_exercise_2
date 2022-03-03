from odoo import fields,models,api

class Stock_Location(models.Model):
    _name = "stock.location.ept"
    _description = "Stock Location"

    name = fields.Char(string="Name", required=True, help="Location name field")
    parent_id = fields.Many2one(comodel_name="stock.location.ept", string="Parent Location",
                                help="Id of this model will be use in parent id field")
    location_type = fields.Selection(selection=[('Vendor', 'Vendor'), ('Customer', 'Customer'), ('Internal', 'Internal'),
                                          ('Inventory Loss', 'Inventory Loss'), ('Production', 'Production'), ('Transit', 'Transit'),
                                                ('View', 'View')],
                                     default='Draft')
    is_scrap_location = fields.Boolean(string="Is Scrap Location", help="To identify scrap location")