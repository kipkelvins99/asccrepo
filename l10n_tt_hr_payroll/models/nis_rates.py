from odoo import api, fields, models, _


class NISRates(models.Model):
    _name = 'nis.rates'
    _description = 'NIS Rates'

    nis_deductible_percentage = fields.Integer('% Deductible')
    nis_maximum_age = fields.Integer('Maximum Age')
    nis_minimum_age = fields.Integer('Minimum Age')
    nis_employee_gl_account_number = fields.Char('Employee Acc No')
    nis_employer_gl_account_number = fields.Char('Employer Acc No')
    nis_show_full_salary = fields.Boolean('Show Full Salary')
