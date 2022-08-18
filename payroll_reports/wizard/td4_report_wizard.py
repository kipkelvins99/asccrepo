from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta,date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class td4ReportWizard(models.TransientModel):
    _name = 'td4.report.wizard'
    _description = 'TD4 Report'

    employee_ids = fields.Many2many('hr.employee', string='Employees', required=1)
    year = fields.Selection([(str(y), str(y)) for y in range(1990, datetime.now().year+1)], 'Year', required=True)

    def preview_report(self):
        # last_week = date(self, 12, 28)
        # print(last_week, 'lasttttt')
        # total_weeks = last_week.isocalendar()[1]
        # print(total_weeks, '/////////////////')
        year_select = int(self.year)
        next_year_date = datetime(year_select + 1, 1, 1)
        last_day = next_year_date - timedelta(days=4)
        total_weeks = last_day.isocalendar()[1]
        data = {'year': self.year, 'total_weeks': total_weeks}
        lst = []
        for rec in self.employee_ids:
            report = self.env['hr.employee'].search([('id', '=', rec.id)])
            print(report.address_id.street, '000000')
            name = report._get_report_base_filename()
            employee_address = report.address_home_id.street
            employer_address = report.address_id.street
            remuneration_before = report.contract_id.wage * 12
            obj = self.env['td4.edit'].create(
                {
                    'employee_name': name,
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
        return {
            'name': "TD4 Report",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'td4.edit',
            'domain': [('id', 'in', lst)],
            # 'view_id': self.env.ref('module.view_id').id,
            'target': 'current'

        }



