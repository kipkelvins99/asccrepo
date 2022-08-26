from odoo import api, fields, models, _


class SummaryReport(models.AbstractModel):
    _name = 'report.payroll_reports.summary_report'

    # @api.model
    def _get_report_values(self, docids, data):
        # docs = self.env['hr.employee'].browse(data['context']['active_ids'])
        docs = self.env['hr.employee'].search([])
        # print(self.env['hr.employee'].browse(data['year']), 'docs')
        return {
            'doc_ids': docids,
            'doc_model': 'hr.employee',
            # 'docs': docs,
            'data': data,
            'summary_report_data': self.summary_report_data('year'),
        }

    def summary_report_data(self, year):
        # year = self.env['td4.report.wizard'].search([], limit=1).mapped('year')
        # print(self.env['hr.employee'].browse(data['year']), 'iiiiiiiiiiiiiiii')
        total_remuneration = 0.0
        total_commissions = 0.0
        taxable_travel = 0.0
        previous_year_income = 0.0
        other_taxable_allowances = 0.0
        total_benefits = 0.0
        total_gross_earnings = 0.0
        non_taxable_travel = 0.0
        other_non_taxable_allowances = 0.0
        other_before_deductions = 0.0
        total_before_tax_pension = 0.0
        total_after_tax_pension = 0.0
        total_nis = 0.0
        total_health_surcharge = 0.0
        total_paye = 0.0
        allowances = 0.0
        employer_contributions = 0.0
        no_of_non_paye_employees = 0
        no_of_paye_employees = 0
        no_of_non_hsur_employees = 0
        no_of_hsur_employees = 0
        no_of_non_nis_employees = 0
        no_of_nis_employees = 0
        gross_of_non_taxable_employees = 0.0
        employees = self.env['hr.employee'].search([])
        no_of_employees = self.env['hr.employee'].search_count([])
        year = self.env['td4.report.wizard'].search([]).mapped('year')
        company = self.env.company
        res_config_details = self.env['ir.config_parameter'].sudo()
        personal_deduction = res_config_details.get_param('l10n_tt_hr_payroll.paye_personal_deduction')
        health_surcharge_minimum_age = res_config_details.get_param('l10n_tt_hr_payroll.health_surcharge_minimum_age')
        health_surcharge_maximum_age = res_config_details.get_param('l10n_tt_hr_payroll.health_surcharge_maximum_age')
        nis_maximum_age = res_config_details.get_param('l10n_tt_hr_payroll.nis_maximum_age')
        nis_minimum_age = res_config_details.get_param('l10n_tt_hr_payroll.nis_minimum_age')

        for employee in employees:
            emp_annual_salary = employee.contract_id.wage*12
            if emp_annual_salary < float(personal_deduction):
                no_of_non_paye_employees += 1

            else:
                no_of_paye_employees += 1
            if health_surcharge_minimum_age < str(employee.age) < health_surcharge_maximum_age:
                print(employee)
                no_of_non_hsur_employees += 1
            else:
                no_of_hsur_employees += 1
            if nis_minimum_age < str(employee.age) < nis_maximum_age:
                no_of_non_nis_employees += 1
            else:
                no_of_nis_employees += 1
            payslip = self.env['hr.payslip'].search([('state', '!=', 'cancel'), ('employee_id', '=', employee.id)])
            if payslip:
                total_remuneration += employee.contract_id.wage * 12
                for line in payslip.line_ids:

                    if line.code == 'TA':
                        taxable_travel += line.total
                    elif line.code != 'TA':
                        other_taxable_allowances += line.total
                    # if line.code == 'BASIC' and str(line.date_from.year) == str(year):
                    #     basic_salary += line.total
                    if line.code == 'PAYE':
                        total_paye += line.total
                    # print(no_of_paye_employees, 'payeee')
                    if line.code == 'HSLR':
                        total_health_surcharge += line.total
                    if line.code == 'NIS':
                        total_nis += line.total
                    if line.category_id.code == 'ALW':
                        allowances += line.total
                    # if line.category_id.code == 'DED' and str(line.date_from.year) == str(year):
                    #     deductions += line.total
                total_gross_earnings += (employee.contract_id.wage * 12) + allowances

        values = {
            'total_remuneration': round(total_remuneration, 2),
            'taxable_travel': round(taxable_travel, 2),
            'other_taxable_allowances': round(other_taxable_allowances, 2),
            'total_paye': round(abs(total_paye), 2),
            'total_health_surcharge': round(abs(total_health_surcharge), 2),
            'total_nis': round(abs(total_nis), 2),
            'total_gross_earnings': round(total_gross_earnings, 2),
            'company_name': company.name,
            'no_of_employees': no_of_employees,
            'no_of_non_paye_employees': no_of_non_paye_employees,
            'no_of_paye_employees': no_of_paye_employees,
            'no_of_non_hsur_employees': no_of_non_hsur_employees,
            'no_of_hsur_employees': no_of_hsur_employees,
            'no_of_non_nis_employees': no_of_non_nis_employees,
            'no_of_nis_employees': no_of_nis_employees,
            'gross_of_non_taxable_employees': allowances,
            'total_commissions': total_commissions,
            'previous_year_income': previous_year_income,
            'total_benefits': total_benefits,
            'non_taxable_travel': non_taxable_travel,
            'other_non_taxable_allowances': other_non_taxable_allowances,
            'other_before_deductions': other_before_deductions,
            'total_before_tax_pension': total_before_tax_pension,
            'total_after_tax_pension': total_after_tax_pension,
            'employer_contributions': employer_contributions,

        }
        # print(values, 'values')
        return values
