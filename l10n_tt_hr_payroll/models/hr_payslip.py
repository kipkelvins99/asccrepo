# -*- coding: utf-8 -*-
import time
import babel
from odoo import models, fields, api, tools, _
from datetime import datetime


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    health_rate = fields.Float(string="Health", compute='_compute_health_deduction')
    paye_rate = fields.Float(string="Paye", compute='_compute_paye_deduction')
    nis_rate = fields.Float(string="NIS", compute='_compute_nis_deduction')

    @api.depends('struct_id', 'date_from', 'date_to', 'employee_id', 'contract_id')
    def _compute_paye_deduction(self):
        res_config_details = self.env['ir.config_parameter'].sudo()
        paye_personal_deduction = res_config_details.get_param('l10n_tt_hr_payroll.paye_personal_deduction')
        paye_senior_citizen_deduction = res_config_details.get_param('l10n_tt_hr_payroll.paye_senior_citizen_deduction')
        paye_mortgage_limit = res_config_details.get_param('l10n_tt_hr_payroll.paye_mortgage_limit')
        paye_tertiary_education_limit = res_config_details.get_param('l10n_tt_hr_payroll.paye_tertiary_education_limit')
        paye_account_number = res_config_details.get_param('l10n_tt_hr_payroll.paye_account_number')
        paye_senior_citizen_age = res_config_details.get_param('l10n_tt_hr_payroll.paye_senior_citizen_age')
        paye_alimony_limit = res_config_details.get_param('l10n_tt_hr_payroll.paye_alimony_limit')
        paye_other_annuities_limit = res_config_details.get_param('l10n_tt_hr_payroll.paye_other_annuities_limit')
        self.paye_rate = 0.0
        for data in self:
            if (not data.employee_id) or (not data.date_from) or (not data.date_to):
                return
            # if data.input_line_ids.input_type_id:
            #     data.input_line_ids = [(5, 0, 0)]
            # loan_line = data.struct_id.input_line_type_ids.filtered(
            #     lambda x: x.code == 'paye')
            get_amount = self.env['hr.contract'].search([
                ('employee_id', '=', data.employee_id.id),
                # ('state', '=', 'approve')
            ], limit=1)
            basic_sal_year = get_amount.wage * 12
            # basic_sal_week = (get_amount.wage * 12) / 52
            # if loan_line:
            if str(basic_sal_year) < paye_personal_deduction:
                data.paye_rate = 0.0

            elif paye_personal_deduction < str(basic_sal_year) <= '100000':
                data.paye_rate = get_amount.wage * (25 / 100)

            elif str(basic_sal_year) > '100000':
                data.paye_rate = get_amount.wage * (30 / 100)

    @api.depends('struct_id', 'date_from', 'date_to', 'employee_id', 'contract_id')
    def _compute_health_deduction(self):
        self.health_rate = 0.0
        health_age = self.env['health.surcharge.rates'].search([], limit=1)
        res_config_details = self.env['ir.config_parameter'].sudo()
        health_surcharge_minimum_age = res_config_details.get_param('l10n_tt_hr_payroll.health_surcharge_minimum_age')
        health_surcharge_maximum_age = res_config_details.get_param('l10n_tt_hr_payroll.health_surcharge_maximum_age')
        health_surcharge_account_number = res_config_details.get_param(
            'l10n_tt_hr_payroll.health_surcharge_account_number')
        nis_maximum_age = res_config_details.get_param('l10n_tt_hr_payroll.nis_maximum_age')
        nis_minimum_age = res_config_details.get_param('l10n_tt_hr_payroll.nis_minimum_age')
        for data in self:
            get_amount = self.env['hr.contract'].search([
                ('employee_id', '=', data.employee_id.id),
                # ('state', '=', 'approve')
            ], limit=1)
            if (not data.employee_id) or (not data.date_from) or (not data.date_to):
                return
            basic_sal_week = (get_amount.wage * 12) / 52
            if health_surcharge_minimum_age and health_surcharge_maximum_age:
                if health_surcharge_minimum_age < str(data.employee_id.age) < health_surcharge_maximum_age:
                    if basic_sal_week < 109:
                        data.health_rate = 4.8 * 4
                    else:
                        data.health_rate = 8.25 * 4
            else:
                if health_age.health_surcharge_minimum_age < str(data.employee_id.age) < health_age.health_surcharge_maximum_age:
                    if basic_sal_week < 109:
                        data.health_rate = 4.8 * 4
                    else:
                        data.health_rate = 8.25 * 4

    @api.depends('struct_id', 'employee_id', 'contract_id')
    def _compute_nis_deduction(self):
        self.nis_rate = 0.0
        amount = 0.0
        nis_age = self.env['nis.rates'].search([], limit=1)
        res_config_details = self.env['ir.config_parameter'].sudo()
        nis_deductible_percentage = res_config_details.get_param('l10n_tt_hr_payroll.nis_deductible_percentage')
        nis_maximum_age = res_config_details.get_param('l10n_tt_hr_payroll.nis_maximum_age')
        nis_minimum_age = res_config_details.get_param('l10n_tt_hr_payroll.nis_minimum_age')
        nis_employee_gl_account_number = res_config_details.get_param(
            'l10n_tt_hr_payroll.nis_employee_gl_account_number')
        nis_employer_gl_account_number = res_config_details.get_param(
            'l10n_tt_hr_payroll.nis_employer_gl_account_number')
        for data in self:
            if (not data.employee_id) or (not data.date_from) or (not data.date_to):
                return
            get_amount = self.env['hr.contract'].search([
                ('employee_id', '=', data.employee_id.id),
                # ('state', '=', 'approve')
            ], limit=1)
            basic_sal_week = (get_amount.wage * 12) / 52
            nis_rates = self.env['nis.rates'].search([])

            for line in nis_rates.nis_line_ids:
                monthly_earn = line.monthly_earnings.split()
                if nis_minimum_age and nis_maximum_age:
                    if nis_minimum_age < str(data.employee_id.age) < nis_maximum_age:
                        if monthly_earn[0] < str(get_amount.wage) < monthly_earn[2]:
                            if monthly_earn[2] != 'over':
                                amount = line.employees_weekly_contri
                                data.nis_rate = float(amount) * 5
                            elif monthly_earn[2] == 'over' and str(get_amount.wage) > monthly_earn[2]:
                                amount = line.employees_weekly_contri
                                data.nis_rate = float(amount) * 5
                else:
                    if nis_age.nis_minimum_age < str(data.employee_id.age) < nis_age.nis_maximum_age:
                        if monthly_earn[0] < str(get_amount.wage) < monthly_earn[2]:
                            if monthly_earn[2] != 'over':
                                amount = line.employees_weekly_contri
                                data.nis_rate = float(amount) * 5
                            elif monthly_earn[2] == 'over' and str(get_amount.wage) > monthly_earn[2]:
                                amount = line.employees_weekly_contri
                                data.nis_rate = float(amount) * 5
