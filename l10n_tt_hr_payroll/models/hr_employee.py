from odoo import api, fields, models
from datetime import date, timedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'

    date_of_birth = fields.Date(string="Date Of Birth", required=True)
    age = fields.Char(string="Age", compute="compute_age", store=True)

    @api.depends('date_of_birth')
    def compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                rec.age = (date.today() - rec.date_of_birth) // timedelta(days=365)
