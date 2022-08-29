from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class td4ReportWizard(models.TransientModel):
    _name = 'td4.report.wizard'
    _description = 'TD4 Report'

    employee_ids = fields.Many2many('hr.employee', string='Employees')
    year = fields.Selection([(str(y), str(y)) for y in range(1990, datetime.now().year+1)], 'Year', required=True)

    def preview_report(self):
        year_select = int(self.year)
        next_year_date = datetime(year_select + 1, 1, 1)
        last_day = next_year_date - timedelta(days=4)
        total_weeks = last_day.isocalendar()[1]
        data = {'year': self.year, 'total_weeks': total_weeks}
        lst = []

        employees = self.env['hr.employee'].search([])
        if self.employee_ids:
            for report in self.employee_ids:
                payslip = self.env['hr.payslip'].search([('employee_id', '=', report.id)])
                if payslip:
                    name = report._get_report_base_filename()
                    employee_address = report.address_home_id.street
                    employer_address = report.address_id.street
                    remuneration_before = report.contract_id.wage * 12
                    obj = self.env['td4.edit'].create(
                        {
                            'year': self.year,
                            'name': name,
                            'employee_name': report.name,
                            'employee_address': employee_address,
                            'employer_name': report.company_id.partner_id.name,
                            'employer_address': employer_address,
                            'employee_bir_number': report.bir_file_number,
                            'employee_nis_number': report.nis_number,
                            'employer_paye_number': report.company_id.paye_file_number,
                            'employer_bir_number': report.company_id.bir_file_number,
                            'total_deductions': report.get_income_tax_deduction(self.year)['deductions'],
                            'week_employed': total_weeks,
                            'remuneration_before': remuneration_before,
                            'commissions': '',
                            'taxable_allowance': report.get_income_tax_deduction(self.year)['allowances'],
                            'travel_allowance': report.get_income_tax_deduction(self.year)['travel_allowance'],
                            'other_allowance': report.get_income_tax_deduction(self.year)['other_allowance'],
                            'income_relate_previous': '',
                            'saving_plan': '',
                            'gross_earnings': report.get_income_tax_deduction(self.year)['gross_earning'],
                            'employer_contribution': '',
                            'travel_dispensation': '',
                            'employee_contribution': '',
                            'nis_deduction': report.get_national_insurance_deduction(total_weeks, self.year),
                            'paye_deduction': report.get_income_tax_deduction(self.year)['annual_paye'],
                            'no_of_weeks_health': total_weeks,
                            'no_of_weeks_at_8_25': '',
                            'no_of_weeks_at_4_80': '',
                            'health_deductions': report.get_health_surcharge_deducted((data['year'])),
                        })
                    lst.append(obj.id)
        else:
            for employee in employees:
                payslip = self.env['hr.payslip'].search([('employee_id', '=', employee.id)])
                if payslip:
                    name = employee._get_report_base_filename()
                    employee_address = employee.address_home_id.street
                    employer_address = employee.address_id.street
                    remuneration_before = employee.contract_id.wage * 12
                    obj = self.env['td4.edit'].create(
                        {
                            'year': self.year,
                            'name': name,
                            'employee_name': employee.name,
                            'employee_address': employee_address,
                            'employer_name': employee.company_id.partner_id.name,
                            'employer_address': employer_address,
                            'employee_bir_number': employee.bir_file_number,
                            'employee_nis_number': employee.nis_number,
                            'employer_paye_number': employee.company_id.paye_file_number,
                            'employer_bir_number': employee.company_id.bir_file_number,
                            'total_deductions': employee.get_income_tax_deduction(self.year)['deductions'],
                            'week_employed': total_weeks,
                            'remuneration_before': remuneration_before,
                            'commissions': '',
                            'taxable_allowance': employee.get_income_tax_deduction(self.year)['allowances'],
                            'travel_allowance': employee.get_income_tax_deduction(self.year)['travel_allowance'],
                            'other_allowance': employee.get_income_tax_deduction(self.year)['other_allowance'],
                            'income_relate_previous': '',
                            'saving_plan': '',
                            'gross_earnings': employee.get_income_tax_deduction(self.year)['gross_earning'],
                            'employer_contribution': '',
                            'travel_dispensation': '',
                            'employee_contribution': '',
                            'nis_deduction': employee.get_national_insurance_deduction(total_weeks, self.year),
                            'paye_deduction': employee.get_income_tax_deduction(self.year)['annual_paye'],
                            'no_of_weeks_health': total_weeks,
                            'no_of_weeks_at_8_25': '',
                            'no_of_weeks_at_4_80': '',
                            'health_deductions': employee.get_health_surcharge_deducted((data['year'])),
                        })
                    lst.append(obj.id)

        return {
            'name': "TD4 Report",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'td4.edit',
            'domain': [('id', 'in', lst)],
            'target': 'current'

        }

    def report_summary(self):

        data = {'year': self.year, 'employee_ids': self.employee_ids.ids}
        return self.env.ref('payroll_reports.employee_summary_report').report_action(self.employee_ids, data=data)
