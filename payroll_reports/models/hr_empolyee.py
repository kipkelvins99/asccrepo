from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'

    bir_file_number = fields.Char('BIR File Number')
    nis_number = fields.Char('NIS Number')
    deduction_year_ids = fields.One2many('deduction.years', 'employee_id', string='Deduction')
    basic_salary = fields.Float('Basic Salary')
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
        self.ensure_one()
        return 'TD4 Report-%s' % (self.name)

    def get_remuneration(self):
        """This function returns the value for Remuneration before Deduction"""
        return round(self.contract_id.wage * 12)

    def get_total_deduction(self, year):
        """The function return the value for Total Deductions as per TD1"""
        deduction_year = self.deduction_year_ids.filtered(lambda d: d.year == str(year))
        # print(year,'year')
        if deduction_year:
            return deduction_year.deduction_amount
        else:
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

        payslip = self.env['hr.payslip.line'].search(
            [('employee_id', '=', self.id), ('salary_rule_id', '=', 18)])
        nis_amount = 0.0
        for line in payslip:
            if str(line.date_from.year) == str(year):
                nis_amount += line.amount
        return abs(nis_amount)

    def get_income_tax_deduction(self, gross_earning, total_deduction_as_per_td1, year):
        """The function returns the income tax deduction"""
        # Gross Earnings - Total Deductions as per TD1 * 0.25
        payslip = self.env['hr.payslip.line'].search(
            [('employee_id', '=', self.id), ('salary_rule_id', '=', 16)])
        paye_amount = 0.0
        for line in payslip:
            if str(line.date_from.year) == str(year):
                paye_amount += line.amount
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

        payslip = self.env['hr.payslip.line'].search([('employee_id', '=', self.id), ('salary_rule_id', '=', 17)])
        health_amount = 0.0
        for line in payslip:
            if str(line.date_from.year) == str(year):
                health_amount += line.amount
        return abs(health_amount)


class DeductionYears(models.Model):
    _name = 'deduction.years'
    _description = 'Deduction Years'

    def _get_years(self):
        return [(str(i), i) for i in range(2020, fields.Date.today().year + 10, 1)]

    year = fields.Selection(selection='_get_years', string='Year', required=True,
                            default=lambda x: str(fields.Date.today().year - 1))

    deduction_amount = fields.Float('Deduction', compute='_compute_deduction', store=True)
    employee_id = fields.Many2one('hr.employee')

    # @api.depends()
    # def _compute_deduction(self, year):
    #     print('_compute_deduction', year)


# class NationalInsuranceContribution(models.Model):
#     _name = 'national.insurance.contribution'
#
#     earning_range = fields.Char('Monthly Earnings')
#     contribution_rate = fields.Float("Employee's weekly contribution rate")
