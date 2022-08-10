from odoo import api, fields, models, _


class HealthSurchargeRates(models.Model):
    _name = 'health.surcharge.rates'
    _description = 'Health Surcharge Rates'
    _rec_name = 'id'

    health_surcharge_minimum_age = fields.Integer('Minimum Age')
    health_surcharge_maximum_age = fields.Integer('Maximum Age')
    # health_surcharge_taxable_range = fields.Many2one()
    health_surcharge_account_number = fields.Char('Account No')
    health_line_ids = fields.One2many('health.surcharge.rates.lines', 'health_id')


class HealthSurchargeRatesLines(models.Model):
    _name = 'health.surcharge.rates.lines'
    _description = 'Health Surcharge Rates'
    _rec_name = 'id'

    health_id = fields.Many2one('health.surcharge.rates')
    range_from = fields.Integer('Minimum Age')
    range_to = fields.Integer('Maximum Age')
    percentage_rate = fields.Float('Rate')
