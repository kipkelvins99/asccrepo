from odoo import models, fields
from datetime import date, datetime, timedelta


class CrmTimeline(models.Model):
    _inherit = 'crm.lead'

    def action_timeline_expire(self):
        # print("function")
        # print(self.search([('stage_id', '=', 2)]))
        # print(self.search([('stage_id', '=', 2), ('date_last_stage_update', '<=', datetime.now()-timedelta(days=8))]))
        crm_leads = self.search([])
        for lead in crm_leads:
            if lead.stage_id.id == self.env.ref('crm_timeline.stage_lead1').id:
                lead.stage_id = self.env.ref(
                    'crm_timeline.stage_lead6').id and lead.date_last_stage_update <= datetime.now() - timedelta(days=4)
                print(lead.stage_id, 'lead')
            if lead.stage_id.id == self.env.ref(
                    'crm_timeline.stage_lead2').id and lead.date_last_stage_update <= datetime.now() - timedelta(
                days=10):
                lead.stage_id = self.env.ref('crm_timeline.stage_lead6').id
            if lead.stage_id.id == self.env.ref(
                    'crm_timeline.stage_lead3').id and lead.date_last_stage_update <= datetime.now() - timedelta(
                days=7):
                lead.stage_id = self.env.ref('crm_timeline.stage_lead6').id
            if lead.stage_id.id == self.env.ref(
                    'crm_timeline.stage_lead4').id and lead.date_last_stage_update <= datetime.now() - timedelta(
                days=1):
                lead.stage_id = self.env.ref('crm_timeline.stage_lead6').id

    def action_activity_due(self):
        crm_leads = self.search([])
        for lead in crm_leads:
            if lead.activity_date_deadline:
                print(lead, lead.activity_date_deadline)
                team_manager = lead.user_id.sale_team_id.user_id.partner_id
                if lead.activity_date_deadline < date.today() and team_manager:
                    print(lead.user_id.sale_team_id.user_id.partner_id, 'le')
                    notification_ids = [((0, 0, {
                        'res_partner_id': team_manager.id,
                        'notification_type': 'inbox'}))]
                    # second_notification_ids = [((0, 0, {
                    #     'res_partner_id': lead.user_id.id,
                    #     'notification_type': 'inbox'
                    # }))]
                    print(notification_ids)
                    ch = self.env['mail.channel'].channel_get([team_manager.id])
                    print(ch, 'chh')
                    ch_obj = self.env['mail.channel'].browse(ch["id"])
                    b = ch_obj.message_post(
                        body='Hello <br> The MR %s missed the activity for the lead %s</br>' % (
                            lead.user_id.name, lead.name),
                        # body='Hello <br> The MR %s needs to approve.' % (order.name),
                        subject=lead.name,
                        message_type='notification',
                        notification_ids=notification_ids,
                        partner_ids=[team_manager.id],
                        subtype_xmlid='mail.mt_comment',
                        notify_by_email=False,
                    )
# second_notification_ids = [((0, 0, {
#                         'res_partner_id': lead.user_id.id,
#                         'notification_type': 'inbox'
#                     }))]
#
#                     ch = self.env['mail.channel'].channel_get([team_manager.id])
#                     ch_obj = self.env['mail.channel'].browse(ch["id"])
#                     second_ch = self.env['mail.channel'].channel_get([lead.user_id.id])
#                     second_ch_obj = self.env['mail.channel'].browse(second_ch["id"])
#
#
#                     b = ch_obj.message_post(
#                         body='Hello <br> The MR %s missed the activity for the lead %s</br>' % (
#                             lead.user_id.name, lead.name),
#                         subject=self.name,
#                         message_type='notification',
#                         notification_ids=notification_ids,
#                         partner_ids=[team_manager.id],
#                         subtype_xmlid='mail.mt_comment',
#                         notify_by_email=False)
#                     self.message_post(
#                         body='Approved the requested MR %s' % self.name,
#                         subject=self.name,
#                         partner_ids=[team_manager.id],
#                         subtype_id=self.env['ir.model.data'].xmlid_to_res_id(
#                             'mail.mt_comment'),
#                         notify_by_email=False)
#                     self.env['mail.mail'].sudo().create({
#                         'email_from': self.env.company.email,
#                         'author_id': self.env.user.partner_id.id,
#                         'body_html': 'Hello <br> The MR %s missed the activity for the lead %s</br>' % (
#                             lead.user_id.name, lead.name),
#                         'subject': 'MR Request to Approve',
#                         'email_to': team_manager.email
#                     }).send(auto_commit=False)
#
#                     m = second_ch_obj.message_post(
#                         body='Hello <br> The MR %s missed the activity for the lead %s</br>' % (
#                             lead.user_id.name, lead.name),
#                         subject=self.name,
#                         message_type='notification',
#                         notification_ids=second_notification_ids,
#                         partner_ids=[lead.user_id.id],
#                         subtype_xmlid='mail.mt_comment',
#                         notify_by_email=False)
#                     self.message_post(
#                         body='Hello <br> The MR %s missed the activity for the lead %s</br>' % (
#                             lead.user_id.name, lead.name),
#                         subject=self.lead.name,
#                         partner_ids=[lead.user_id.id],
#                         subtype_id=self.env['ir.model.data'].xmlid_to_res_id(
#                             'mail.mt_comment'),
#                         notify_by_email=False)
#                     self.env['mail.mail'].sudo().create({
#                         'email_from': self.env.company.email,
#                         'author_id': self.env.user.partner_id.id,
#                         'body_html': 'Hello <br> The MR %s missed the activity for the lead %s</br>' % (
#                             lead.user_id.name, lead.name),
#                         'subject': 'MR Request to Approve',
#                         'email_to': lead.user_id.email
#                     }).send(auto_commit=False)