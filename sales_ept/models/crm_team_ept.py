from odoo import fields,models

class CRM_Team(models.Model):
    _name = "crm.team.ept"
    _description = "Sales Module upgraded with CRM"

    name=fields.Char(string="Name", help="Name field of CRM")
    team_lead=fields.Many2one(comodel_name='res.users',string="Team Leader", help="Many 2 one filed with res.users")