from odoo import fields, models


class ResPartnerTag(models.Model):
    _inherit = "res.partner"

    def _default_category(self):
        return self.env['res.partner.category'].browse(self._context.get('category_id'))

    category_id = fields.Many2many('res.partner.category',
                                   column1='partner_id',
                                   column2='category_id', string='Tags',
                                   default=_default_category,required=True)
