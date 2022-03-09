from odoo import fields,models

class Sale_Order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'
    _description = 'Inheritance Demo'

    lead_id = fields.Many2one(
        comodel_name = 'crm.lead',
        string='Lead',
        help = 'Inherited from crm.lead model'
    )