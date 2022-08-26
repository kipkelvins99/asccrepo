from odoo import api, fields, models, _
import calendar
from datetime import datetime


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'

    bir_file_number = fields.Char('BIR File Number')
    nis_number = fields.Char('NIS Number')
    number_of_weeks_at_8_25 = fields.Float('Number of weeks at $8.25')
    number_of_weeks_at_4_80 = fields.Float('Number of weeks at $4.80')

    def _get_report_base_filename(self):
        """This function is used for to get the report file name"""

        self.ensure_one()
        return 'TD4 Report-%s' % (self.name)

    def get_remuneration(self):
        """This function returns the value for Remuneration before Deduction"""
        return round(self.contract_id.wage * 12)

    def get_national_insurance_deduction(self, weeks, year):
        """The function returns the National insurance deducted"""

        # National Insurance deducted = Employee's weekly contribution rate x number of
        # the 52 weeks worked (Round to nearest) No cent value.
        payslip = self.env['hr.payslip'].search([('state', '!=', 'cancel'), ('employee_id', '=', self.id)])
        nis_amount = 0.0
        for line in payslip.line_ids:
            if line.code == 'NIS' and str(line.date_from.year) == str(year):
                nis_amount += line.total

        return abs(nis_amount)

    def get_income_tax_deduction(self, year):
        """The function returns the income tax deduction"""
        # Gross Earnings - Total Deductions as per TD1 * 0.25
        values = {}
        paye_amount = 0.0
        nis_amount = 0.0
        basic_salary = 0.0
        allowances = 0.0
        income_received_to_date = 0.0
        sum_of_monthly_additions = 0.0
        projected_income = 0.0
        no_of_payslips_in_year = 0
        no_of_payslips_left_year = 0
        annual_income = 0.0
        deductions_paid_to_date = 0.0
        sum_of_all_deductions = 0.0
        projected_deductions = 0.0
        sum_of_monthly_deductions = 0.0
        annual_deductions = 0.0
        deductions = 0.0
        annual_taxable_income = 0.0
        annual_paye = 0.0
        paye_rate =0.0
        monthly_paye = 0.0
        paye_paid_to_date = 0.0
        gross_earning = 0.0
        travel_allowance = 0.0
        other_allowance = 0.0
        total_mondays = 0.0
        payslip = self.env['hr.payslip'].search([('state', '!=', 'cancel'), ('employee_id', '=', self.id)])
        if payslip:
            for pay in payslip:
                total_mondays = len([1 for i in calendar.monthcalendar(pay.date_from.year,
                                                                       pay.date_from.month) if i[0] != 0])
                print("Total Mondays in the Month: ", total_mondays)
                if str(pay.date_from.year) == str(year):
                    no_of_payslips_in_year += 1
                else:
                    no_of_payslips_in_year = 1

                no_of_payslips_left_year = 12 - no_of_payslips_in_year

                if (self.contract_id.wage * 12) <= 100000:
                    paye_rate = 0.25
                else:
                    paye_rate = 0.30
                for line in pay.line_ids:

                    if line.code == 'TA' and str(line.date_from.year) == str(year):
                        travel_allowance += line.total
                    elif line.code != 'TA' and str(line.date_from.year) == str(year):
                        other_allowance += line.total
                    if line.code == 'BASIC' and str(line.date_from.year) == str(year):
                        basic_salary += line.total
                    if line.code == 'PAYE' and str(line.date_from.year) == str(year):
                        paye_paid_to_date += line.total
                    if line.category_id.code == 'ALW' and str(line.date_from.year) == str(year):
                        allowances += line.total
                    if line.category_id.code == 'DED' and str(line.date_from.year) == str(year):
                        deductions += line.total
                sum_of_monthly_additions = allowances / no_of_payslips_in_year
                income_received_to_date = basic_salary + allowances
                projected_income = (self.contract_id.wage + sum_of_monthly_additions) * no_of_payslips_left_year
                annual_income = projected_income + income_received_to_date
                deductions_paid_to_date = abs(deductions)
                sum_of_monthly_deductions = abs(deductions) / no_of_payslips_in_year
                projected_deductions = sum_of_monthly_deductions * no_of_payslips_left_year
                annual_deductions = projected_deductions + deductions_paid_to_date + allowances
                annual_taxable_income = annual_income - annual_deductions
                annual_paye = annual_taxable_income * paye_rate
                monthly_paye = (annual_paye - paye_paid_to_date) / no_of_payslips_left_year
                gross_earning = (self.contract_id.wage * 12) + allowances

        else:
            deductions = 0.0
            annual_paye = 0.0
            gross_earning = (self.contract_id.wage * 12) + allowances
        values = {
            'annual_paye': round(abs(annual_paye), 2),
            'allowances': round(allowances, 2),
            'deductions': abs(deductions),
            'travel_allowance': round(travel_allowance, 2),
            'other_allowance': round(other_allowance, 2),
            'gross_earning': round(gross_earning, 2),

        }
        return values

    def get_health_surcharge_deducted(self, year):
        """The function return the health surcharge calculation"""
        payslip = self.env['hr.payslip'].search([('state', '!=', 'cancel'), ('employee_id', '=', self.id)])
        health_amount = 0.0
        for line in payslip.line_ids:
            if line.code == 'HLSR' and str(line.date_from.year) == str(year):
                health_amount += line.total
        return abs(health_amount)
    #
    # def summary_report_data(self, year):
    #     print('repo')
    #     total_remuneration = 0.0
    #     total_commissions = 0.0
    #     taxable_travel = 0.0
    #     previous_year_income = 0.0
    #     other_taxable_allowances = 0.0
    #     total_benefits = 0.0
    #     total_gross_earnings = 0.0
    #     non_taxable_travel = 0.0
    #     other_non_taxable_allowances = 0.0
    #     other_before_deductions = 0.0
    #     total_before_tax_pension = 0.0
    #     total_after_tax_pension = 0.0
    #     total_nis = 0.0
    #     total_health_surcharge = 0.0
    #     total_paye = 0.0
    #     employer_contributions = 0.0
    #     no_of_employees = 0.0
    #     no_of_non_paye_employees = 0.0
    #     no_of_paye_employees = 0.0
    #     no_of_non_hsur_employees = 0.0
    #     no_of_hsur_employees = 0.0
    #     no_of_non_nis_employees = 0.0
    #     no_of_nis_employees = 0.0
    #     gross_of_non_taxable_employees = 0.0
    #     employees = self.env['hr.employee'].search([])
    #     for employee in employees:
    #         payslip = self.env['hr.payslip'].search([('state', '!=', 'cancel'), ('employee_id', '=', employee.id)])
    #         if payslip:
    #             print('total_remuneration', total_remuneration)
    #             total_remuneration += employee.contract_id.wage * 12
    #             print('total_remuneration', total_remuneration)
    #
    #             values = {
    #                 'total_remuneration': round(total_remuneration, 2),
    #                 # 'allowances': round(allowances, 2),
    #                 # 'deductions': abs(deductions),
    #                 # 'travel_allowance': round(travel_allowance, 2),
    #                 # 'other_allowance': round(other_allowance, 2),
    #                 # 'gross_earning': round(gross_earning, 2),
    #
    #             }
    #             return values