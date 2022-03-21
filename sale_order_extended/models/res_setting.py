from odoo import fields,models,api

class Res_Setting(models.TransientModel):
    _inherit = "res.config.settings"

    default_date_format = fields.Selection(string="Date Format", selection=[('ddMMyyyy', 'DD/MM/YYYY'), ('mmDDyyyy', 'MM/DD/YYYY')], default="ddMMyyyy", default_model="sale.order")

