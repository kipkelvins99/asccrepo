from odoo import api, fields, models, _


class Lead(models.Model):
    _inherit = 'crm.lead'

    @api.onchange('stage_id')
    def onchange_stage(self):
        print(self.stage_id, 'print')
        if self.stage_id == self.env.ref('crm_timeline.stage_lead1'):
            print(self.stage_id, self._origin.id, self.user_id.id, 'ssssss')
            self.activity_schedule(
                res_id=self._origin.id,
                res_model_id=self.env['ir.model'].search([('model', '=', 'crm.lead')]).id,

                activity_type_id=self.env.ref('crm_timeline.mail_activity_data_lead_email').id,
                # summary=activity_type.summary,
                user_id=self.user_id.id,
                date_deadline=self.create_date
            )

        if self.stage_id == self.env.ref('crm_timeline.stage_lead2'):
            self.activity_schedule(
                res_id=self._origin.id,
                res_model_id=self.env['ir.model'].search([('model', '=', 'crm.lead')]).id,
                activity_type_id=self.env.ref('crm_timeline.mail_activity_data_lead_email').id,
                # summary=activity_type.summary,
                user_id=self.user_id.id,
                date_deadline=self.date_last_stage_update
            )
        if self.stage_id == self.env.ref('crm_timeline.stage_lead3'):
            self.activity_schedule(
                res_id=self._origin.id,
                res_model_id=self.env['ir.model'].search([('model', '=', 'crm.lead')]).id,
                activity_type_id=self.env.ref('crm_timeline.mail_activity_data_lead_email').id,
                # summary=activity_type.summary,
                user_id=self.user_id.id,
                date_deadline=self.date_last_stage_update
            )
        if self.stage_id == self.env.ref('crm_timeline.stage_lead4'):
            self.activity_schedule(
                res_id=self._origin.id,
                res_model_id=self.env['ir.model'].search([('model', '=', 'crm.lead')]).id,
                activity_type_id=self.env.ref('crm_timeline.mail_activity_data_lead_email').id,
                # summary=activity_type.summary,
                user_id=self.user_id.id,
                date_deadline=self.date_last_stage_update
            )
        if self.stage_id == self.env.ref('crm_timeline.stage_lead5'):
            self.activity_schedule(
                res_id=self._origin.id,
                res_model_id=self.env['ir.model'].search([('model', '=', 'crm.lead')]).id,
                activity_type_id=self.env.ref('crm_timeline.mail_activity_data_lead_email').id,
                # summary=activity_type.summary,
                user_id=self.user_id.id,
                date_deadline=self.date_last_stage_update
            )
        if self.stage_id == self.env.ref('crm_timeline.stage_lead6'):
            self.activity_schedule(
                res_id=self._origin.id,
                res_model_id=self.env['ir.model'].search([('model', '=', 'crm.lead')]).id,
                activity_type_id=self.env.ref('crm_timeline.mail_activity_data_lead_email').id,
                # summary=activity_type.summary,
                user_id=self.user_id.id,
                date_deadline=self.date_last_stage_update
            )

