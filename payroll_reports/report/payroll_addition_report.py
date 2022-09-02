from odoo import models, _


class SummaryReportAdd(models.AbstractModel):
    _name = 'report.payroll_reports.monthly_payroll_addition_report'

    # @api.model
    def _get_report_values(self, docids, data):
        docs = self.env['hr.employee'].search([('id', 'in', data['employee_ids'])])
        company = self.env.company
        # print(data)
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
        categories = self.env['hr.salary.rule'].search([('category_id', '=', 2)])
        employee = self.env['hr.employee'].search([('id', 'in', data['employee_ids'])])
        company = self.env.company
        date = []
        amount = []
        category = []
        total = 0.0
        for deduct in categories:
            category.append(deduct)
        category = self.env['hr.salary.rule'].search([('category_id', '=', 2)])
        payslip = self.env['hr.payslip'].search(
            [('employee_id', 'in', data['employee_ids'])])
        print(payslip, 'payslip')
        payslip_lines = self.env['hr.payslip.line'].search(
            [('employee_id', 'in', data['employee_ids']), ('category_id', '=', 2)])
        lines = []
        category_lst = []
        values = []
        total_ded_ytd = []
        total_amt = 0.0
        total_alw = 0.0
        # for pay in payslip:
        #     print(pay.date_from.month)
        #     if str(pay.date_from.month) <= data['month']:
        #         for line in pay.line_ids:
        #             print(pay.line_ids.code, 'payy')
        for cat in category:
            for line in payslip_lines:
                if str(line.date_from.month) == data['month'] and str(line.date_from.year) == data['year'] and line.code == cat.code:
                    total_amt += abs(line.total)
                    lines.append(line)
                # for employee in data['employee_ids']:
                #     if str(line.date_from.month) <= data['month'] and line.code == cat.code and line.employee_id.id == employee:
                #         print(line)
                #         print(line.code)
                #         print(line.total)
                #         print(line.employee_id.id)
                #         total_alw += abs(line.total)
                # print(total_alw, 'total_alw')
            category_lst.extend([{
                'cat': cat,
                'amount': round(total_amt, 2)
            }])
            amount.append(round(total_amt, 2))
            total_amt = 0.0
            # print(category_lst, '00000000000')
            # for rec in payslip_lines:
            #     for employee in data['employee_ids']:
            #         # print(employee, 'lllllllllllllllllllllllllllllll')
            #         # print(rec.employee_id, 'lllllllllllllllllllllllllllllll')
            #         if str(rec.date_from.month) <= data['month'] and rec.code == cat.code and rec.employee_id.id == employee:
            #             # print(rec.slip_id)
            #             # print(rec.total)
            #             total_ded += rec.total
            #         total_ded_ytd.append(round(total_ded, 2))
            #         # print(total_ded_ytd, 'total')
            # total_ded = 0.0
        values.append({
            'category': category_lst,
            'lines': lines,

        })
        # print(values, 'values')
        return values
