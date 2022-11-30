from odoo import api, fields, models, _


class Lead(models.Model):
    _inherit = 'res.partner'

    is_agent = fields.Boolean('Is Agent')
