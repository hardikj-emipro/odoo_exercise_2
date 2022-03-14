from builtins import super
from odoo import fields,models

class CRM_Lead(models.Model):
    _name = "crm.lead"
    _inherit = 'crm.lead'


    def action_new_quotation(self):
        tag_id = self.env.ref("sale_order_extended.crm_tag_new_value").id
        action = super(CRM_Lead, self).action_new_quotation()
        action['context']['default_lead_id'] = self.id
        action['context']['default_tag_ids'] += [(4, tag_id, 0)]
        return action


