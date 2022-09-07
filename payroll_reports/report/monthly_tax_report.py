from odoo import models, _


class TaxReport(models.AbstractModel):
    _name = 'report.payroll_reports.monthly_tax_report'

    def _get_report_values(self, docids, data):
        docs = self.env['hr.employee'].search([('id', 'in', data['employee_ids'])])
        company = self.env.company
        res = {
            'doc_ids': docids,
            'doc_model': 'hr.employee',
            'data': data,
            'company': company.name,
            'docs': docs,
            'summary_report_data': self.summary_report_data(data),
        }
        return res

    def summary_report_data(self, data):
        employees = self.env['hr.employee'].browse(data['employee_ids'])
        payslip = self.env['hr.payslip'].search(
            [('employee_id', 'in', data['employee_ids'])])
        departments = self.env['hr.department'].search([])
        main_lines = []
        values = []
        lines = []
        if data['employee_ids']:
            for department in departments:
                total_paye_amount = 0.0
                total_hsur_amount = 0.0
                total_amount = 0.0
                sub_total =0.0
                employee_count = 0
                employee_paye_count = 0
                employee_hsur_count = 0
                for employee in employees:

                    pay_lines = payslip.line_ids.filtered(
                        lambda x: str(x.date_from.month) == data['month'] and x.employee_id.id == employee.id and department == employee.department_id)
                    if pay_lines:
                        paye_rate_lines = pay_lines.filtered(
                            lambda x: x.code == self.env.ref('l10n_tt_hr_payroll.hr_rule_paye').code
                                      )
                        total_paye_amount += abs(paye_rate_lines.total)
                        hsur_rate_lines = pay_lines.filtered(
                            lambda x: x.code == self.env.ref('l10n_tt_hr_payroll.hr_rule_health_surcharge').code)
                        total_hsur_amount += abs(hsur_rate_lines.total)
                        sub_total = abs(paye_rate_lines.total) + abs(hsur_rate_lines.total)
                        total_amount = total_paye_amount + total_hsur_amount
                        sub_line_tuple = (employee, abs(paye_rate_lines.total), abs(hsur_rate_lines.total), sub_total)
                        lines.append(sub_line_tuple)
                        employee_count += 1
                        if paye_rate_lines.total != 0:
                            employee_paye_count += 1
                        if hsur_rate_lines.total != 0:
                            employee_hsur_count += 1
                department_tuple = (department, total_paye_amount, total_hsur_amount, total_amount, employee_count,
                                    employee_paye_count, employee_hsur_count)
                main_lines.append(department_tuple)
        values.append({
            'main_lines': main_lines,
            'lines': lines,
        })
        print('values', values)
        return values
