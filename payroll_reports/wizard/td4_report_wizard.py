from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta,date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class td4ReportWizard(models.TransientModel):
    _name = 'td4.report.wizard'
    _description = 'TD4 Report'

    date_start = fields.Date('Start Period', required=True,
                             default=lambda self: (fields.Date.today() - relativedelta(years=1)).replace(month=1,
                                                                                                         day=1),
                             help="Start date of the period to consider.")
    date_end = fields.Date('End Period', required=True,
                           default=lambda self: (fields.Date.today() - relativedelta(years=1)).replace(month=12,
                                                                                                       day=31),
                           help="End date of the period to consider.")
    employee_ids = fields.Many2many('hr.employee', string='Employees', required=1)
    year = fields.Selection([(str(y), str(y)) for y in range(1970, datetime.now().year+1)], 'Year', required=True)

    def print_report(self):

        if self.date_end.year != self.date_start.year:
            raise ValidationError("Invalid year selected")

        total_weeks = self.weeks_for_year(self)
        data = {'year': self.year, 'total_weeks': total_weeks}
        return self.env.ref('payroll_reports.employee_td4_report').report_action(self.employee_ids, data=data)

    def weeks_for_year(self,year):
        print(self,year, 'oooo')
        last_week = date(year, 12, 28)
        print(last_week.isocalendar()[1], 'last week')
        return last_week.isocalendar()[1]