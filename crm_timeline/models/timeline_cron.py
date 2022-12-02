from odoo import models, fields
from datetime import datetime, timedelta


class CrmTimeline(models.Model):
    _inherit = 'crm.lead'

    def action_timeline_expire(self):
        # print("function")
        # print(self.search([('stage_id', '=', 2)]))
        # print(self.search([('stage_id', '=', 2), ('date_last_stage_update', '<=', datetime.now()-timedelta(days=8))]))
        crm_leads = self.search([])
        for lead in crm_leads:
            if lead.stage_id.id == 1 and lead.date_last_stage_update <= datetime.now()-timedelta(days=4):
                lead.stage_id = 5
            if lead.stage_id.id == 2 and lead.date_last_stage_update <= datetime.now()-timedelta(days=10):
                lead.stage_id = 5
            if lead.stage_id.id == 3 and lead.date_last_stage_update <= datetime.now()-timedelta(days=7):
                lead.stage_id = 5
            if lead.stage_id.id == 4 and lead.date_last_stage_update <= datetime.now()-timedelta(days=1):
                lead.stage_id = 5
