from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'

    bir_file_number = fields.Char('BIR File Number')
    nis_number = fields.Char('NIS Number')
    number_of_weeks_at_8_25 = fields.Float('Number of weeks at $8.25')
    number_of_weeks_at_4_80 = fields.Float('Number of weeks at $4.80')

    # def write(self, vals):
    #     res = super(HrEmployee, self).write(vals)
    #     if vals.get('number_of_weeks_at_8_25') and self.number_of_weeks_at_4_80:
    #         raise ValidationError("You can not select Number of weeks at $8.25 and Number of weeks at $4.80 at once.")
    #
    #     if vals.get('number_of_weeks_at_4_80') and self.number_of_weeks_at_8_25:
    #         raise ValidationError("You can not select Number of weeks at $8.25 and Number of weeks at $4.80 at once.")
    #
    #     return res

    def _get_report_base_filename(self):
        """This function is used for to get the report file name"""

        # self.ensure_one()
        return 'TD4 Report-%s' % (self.name)

    def get_remuneration(self):
        """This function returns the value for Remuneration before Deduction"""
        return round(self.contract_id.wage * 12)

    def get_total_deduction(self, year):
        """The function return the value for Total Deductions as per TD1"""
        # deduction_year = self.deduction_year_ids.filtered(lambda d: d.year == str(year))
        # # print(year,'year')
        # if deduction_year:
        #     return deduction_year.deduction_amount
        # else:
        return 0

    def calculate_gross_earnings(self):
        """The function return the gross earnings"""
        # Gross Earnings = Remuneration before deduction + Commissions + Taxable allowances \
        # + Travelling + other + Income related to previous years paid in current year + \
        # Savings Plan withdrawals of Contributions made by company.

        gross_earning = (self.contract_id.wage * 12) + 0 + 0 + 0 + 0 + 0 + 0 + 0

        return round(gross_earning)

    def get_national_insurance_deduction(self, weeks, year):
        """The function returns the National insurance deducted"""

        # National Insurance deducted = Employee's weekly contribution rate x number of
        # the 52 weeks worked (Round to nearest) No cent value.
        print(self, 'employees')
        payslip = self.env['hr.payslip'].search([('state', '!=', 'cancel'), ('employee_id', '=', self.id)])
        nis_amount = 0.0
        for line in payslip.line_ids:
            if line.salary_rule_id.id == 18 and str(line.date_from.year) == str(year):
                nis_amount += line.total

        return abs(nis_amount)

    def get_income_tax_deduction(self, gross_earning, total_deduction_as_per_td1, year):
        """The function returns the income tax deduction"""
        # Gross Earnings - Total Deductions as per TD1 * 0.25

        paye_amount = 0.0
        nis_amount = 0.0
        basic_salary = 0.0
        allowances = 0.0
        income_received_to_date = 0.0
        sum_of_monthly_additions = 0.0
        projected_income = 0.0
        no_of_payslips_in_year = 0
        no_of_payslips_left_year = 0

        payslip = self.env['hr.payslip'].search([('state', '!=', 'cancel'), ('employee_id', '=', self.id)])


        for pay in payslip:
            if str(pay.date_from.year) == str(year):
                no_of_payslips_in_year += 1
            no_of_payslips_left_year = 12 - no_of_payslips_in_year

            for line in pay.line_ids:

                if line.salary_rule_id.id == 1 and str(line.date_from.year) == str(year):
                    basic_salary += line.total
                if line.category_id.id == 2 and str(line.date_from.year) == str(year):
                    allowances += line.total
                income_received_to_date = basic_salary + allowances
                projected_income = (self.contract_id.wage) * no_of_payslips_left_year


        # Income Received to Date = (Sum of all Salary received to date (taken from this year's payslips)) +
        # (Sum of all additions received to date (taken from this year's payslips)
        # Projected Income = (Basic Salary + (Sum of Monthly Additions)) *Number of months left in the year
        # Annual Income = Projected Income + Income Received to Date
        # Deductions paid to Date = (Sum of all Deductions (taken from this year's payslips. This includes 70% of NIS))
        # Projected Deductions = (Sum of Monthly Deductions (This includes 70 % of NIS)) *Number of months left in the year
        # Annual Deductions = Projected Deductions + Deductions paid to Date + Personal Allowance
        # Annual Taxable Income = Annual Income - Annual Deductions
        # Annual PAYE = Annual Taxable Income * PAYE Rate(0.25 or 0.3)
        # Monthly PAYE = (Annual PAYE - PAYE paid to date) / (Number of months left in the year)

        return abs(paye_amount)

    def get_health_surcharge_deducted(self, year):
        """The function return the health surcharge calculation"""
        # Number of weeks at $8.25 or Number of weeks at $4.80
        # if self.number_of_weeks_at_8_25:
        #     return round(int(weeks) * 8.25)
        # elif self.number_of_weeks_at_4_80:
        #     return round(int(weeks) * 4.80)
        # else:
        #     return 0

        payslip = self.env['hr.payslip'].search([('state', '!=', 'cancel'), ('employee_id', '=', self.id)])
        health_amount = 0.0
        for line in payslip.line_ids:
            if line.salary_rule_id.id == 17 and str(line.date_from.year) == str(year):
                health_amount += line.total
        return abs(health_amount)
