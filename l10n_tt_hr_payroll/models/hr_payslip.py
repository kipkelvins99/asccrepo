# -*- coding: utf-8 -*-
import time
import babel
from odoo import models, fields, api, tools, _
from datetime import datetime


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    loan_line_id = fields.Many2one('hr.loan.line', string="Loan Installment", help="Loan installment")


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    health_rate = fields.Float(string="Health", compute='_compute_deductions')
    paye_rate = fields.Float(string="Paye", compute='_compute_deductions')

    @api.depends('struct_id', 'date_from', 'date_to', 'employee_id', 'contract_id')
    def _compute_deductions(self):
        self.health_rate = 0.0
        self.paye_rate =0.0
        for data in self:

            if (not data.employee_id) or (not data.date_from) or (not data.date_to):
                return

            if data.input_line_ids.input_type_id:
                print('input_type_id')
                data.input_line_ids = [(5, 0, 0)]

            loan_line = data.struct_id.input_line_type_ids.filtered(
                lambda x: x.code == 'paye')
            get_amount = self.env['hr.contract'].search([
                ('employee_id', '=', data.employee_id.id),
                # ('state', '=', 'approve')
            ], limit=1)
            basic_sal_year = get_amount.wage * 12
            basic_sal_week = (get_amount.wage * 12) / 52
            if loan_line:

                print(basic_sal_year)
                if basic_sal_year < 84000:
                    data.paye_rate = 0.0

                elif 84000 < basic_sal_year <= 100000:
                    data.paye_rate = get_amount.wage * (25 / 100)

                elif basic_sal_year > 100000:
                    data.paye_rate = get_amount.wage * (30 / 100)
                print(data.paye_rate)

            health_rate = data.struct_id.input_line_type_ids.filtered(
                    lambda x: x.code == 'hlsr')
            if health_rate:
                if basic_sal_week < 109:
                    data.health_rate = get_amount.wage * (4.8/100)

                else:
                    data.health_rate = get_amount.wage * (8.25/100)
                print(data.health_rate, 'amount_week')


class HrPayslipInputType(models.Model):
    _inherit = 'hr.payslip.input.type'

    input_id = fields.Many2one('hr.salary.rule')