from odoo import fields,models

class Account_Tax(models.Model):
    _name = "account.tax.ept"
    _description = "Account Model"

    name = fields.Char(string="Tax Name", help="Name of tax slab")
    tax_use = fields.Selection(selection=[('None', 'None'), ('Sales', 'Sales'), ('Purchase', 'Purchase')],
                     default='None')
    tax_value = fields.Float(string="Amount", help="Tax Amount")
    tax_amount_type = fields.Selection(selection=[('Percentage', 'Percentage'), ('Fixed', 'Fixed')],
                     default='Percentage')
