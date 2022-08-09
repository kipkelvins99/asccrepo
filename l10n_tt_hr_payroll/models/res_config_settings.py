from odoo import fields, models, api
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    nis_deductible_percentage = fields.Integer(string='% Deductible')
    nis_maximum_age = fields.Integer(string='Maximum Age')
    nis_minimum_age = fields.Integer(string='Minimum Age')
    nis_employee_gl_account_number = fields.Char(string='Employee Acc No')
    nis_employer_gl_account_number = fields.Char(string='Employer Acc No')
    nis_show_full_salary = fields.Boolean(string='Show Full Salary')

    paye_personal_deduction = fields.Float(string='Personal Deduction')
    paye_senior_citizen_deduction = fields.Float(string='Senior Citizen Deduction ')
    paye_mortgage_limit = fields.Float(string='Mortgage Limit')
    paye_tertiary_education_limit = fields.Float(string='Tertiary Education Limit')
    paye_account_number = fields.Char(string='Account No')
    paye_senior_citizen_age = fields.Integer(string='Senior Citizen Age')
    paye_alimony_limit = fields.Float(string='Alimony limit')
    paye_other_annuities_limit = fields.Float(string='Other Annuities limit')

    health_surcharge_minimum_age = fields.Integer(string='Minimum Age')
    health_surcharge_maximum_age = fields.Integer(string='Maximum Age')
    health_surcharge_account_number = fields.Char(string='Account No')

    # set_values method
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('l10n_tt_hr_payroll.nis_deductible_percentage', self.nis_deductible_percentage)
        # self.env['ir.config_parameter'].sudo().set_param('l10n_tt_hr_payroll.product_bom', self.product_bom)
        return res

    # get_values method
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        # with_user = self.env['ir.config_parameter'].sudo()
        nis_deductible_percentage = self.env['ir.config_parameter'].sudo().get_param('l10n_tt_hr_payroll.nis_deductible_percentage')
        # product_bom = self.env['ir.config_parameter'].sudo().get_param('l10n_tt_hr_payroll.product_bom')
        res.update(
            # product_bom_ids=[(6, 0, literal_eval(nis_deductible_percentage))] if nis_deductible_percentage else False,
            nis_deductible_percentage=nis_deductible_percentage
        )
        return res
