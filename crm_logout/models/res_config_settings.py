from odoo import fields, models, api


class IdleTimer(models.TransientModel):
    _inherit = 'res.config.settings'

    idle_time_limit = fields.Float(string="Idle time limit")
    next_question_limit = fields.Float(string="Move to next question limit")

    @api.model
    def get_values(self):
        res = super(IdleTimer, self).get_values()
        res['idle_time_limit'] = self.env['ir.config_parameter'].sudo(). \
            get_param('idle_time_limit_id')
        res['next_question_limit'] = self.env['ir.config_parameter'].sudo(). \
            get_param('next_question_limit_id')
        # print(res['idle_time_limit'], 'time')
        print(res)
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('idle_time_limit_id',
                                                         self.idle_time_limit)
        self.env['ir.config_parameter'].sudo().set_param(
            'next_question_limit_id', self.next_question_limit)
        super(IdleTimer, self).set_values()

    def idle_timer(self):
        vals = {
            'idle_time_limit': self.idle_time_limit,
            'next_question_limit': self.next_question_limit}
        return vals
