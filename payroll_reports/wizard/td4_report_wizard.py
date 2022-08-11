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

    def print_report(self):
        last_week = date(self, 12, 28)
        total_weeks = last_week.isocalendar()[1]
        data = {'year': self.year, 'total_weeks': total_weeks}
        return self.env.ref('payroll_reports.employee_td4_report').report_action(self.employee_ids, data=data)

