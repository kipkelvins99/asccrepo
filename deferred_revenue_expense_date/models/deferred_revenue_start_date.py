import calendar
from dateutil.relativedelta import relativedelta
from math import copysign

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero, float_round


class DeferredRevenueStartDate(models.Model):
    _inherit = 'account.asset'

    recognize_on_first = fields.Boolean(string='Recognize On 1st?')

    def _recompute_board(self, depreciation_number, starting_sequence,
                         amount_to_depreciate, depreciation_date,
                         already_depreciated_amount, amount_change_ids):
        self.ensure_one()
        residual_amount = amount_to_depreciate
        # Remove old unposted depreciation lines. We cannot use unlink() with One2many field
        move_vals = []
        prorata = self.prorata and not self.env.context.get("ignore_prorata")
        if amount_to_depreciate != 0.0:
            for asset_sequence in range(starting_sequence + 1,
                                        depreciation_number + 1):
                while amount_change_ids and amount_change_ids[
                    0].date <= depreciation_date:
                    if not amount_change_ids[0].reversal_move_id:
                        residual_amount -= amount_change_ids[0].amount_total
                        amount_to_depreciate -= amount_change_ids[
                            0].amount_total
                        already_depreciated_amount += amount_change_ids[
                            0].amount_total
                    amount_change_ids[0].write({
                        'asset_remaining_value': float_round(residual_amount,
                                                             precision_rounding=self.currency_id.rounding),
                        'asset_depreciated_value': amount_to_depreciate - residual_amount + already_depreciated_amount,
                    })
                    amount_change_ids -= amount_change_ids[0]
                amount = self._compute_board_amount(asset_sequence,
                                                    residual_amount,
                                                    amount_to_depreciate,
                                                    depreciation_number,
                                                    starting_sequence,
                                                    depreciation_date)
                prorata_factor = 1
                move_ref = self.name + ' (%s/%s)' % (
                    prorata and asset_sequence - 1 or asset_sequence,
                    self.method_number)
                if prorata and asset_sequence == 1:
                    move_ref = self.name + ' ' + _('(prorata entry)')
                    first_date = self.prorata_date
                    if int(self.method_period) % 12 != 0:
                        month_days = \
                            calendar.monthrange(first_date.year,
                                                first_date.month)[
                                1]
                        days = month_days - first_date.day + 1
                        prorata_factor = days / month_days
                    else:
                        total_days = (
                                             depreciation_date.year % 4) and 365 or 366
                        days = (self.company_id.compute_fiscalyear_dates(
                            first_date)['date_to'] - first_date).days + 1
                        prorata_factor = days / total_days
                amount = self.currency_id.round(amount * prorata_factor)
                if float_is_zero(amount,
                                 precision_rounding=self.currency_id.rounding):
                    continue
                residual_amount -= amount
                move_vals.append(self.env[
                    'account.move']._prepare_move_for_asset_depreciation({
                    'amount': amount,
                    'asset_id': self,
                    'move_ref': move_ref,
                    'date': depreciation_date,
                    'asset_remaining_value': float_round(residual_amount,
                                                         precision_rounding=self.currency_id.rounding),
                    'asset_depreciated_value': amount_to_depreciate - residual_amount + already_depreciated_amount,
                }))

                depreciation_date = depreciation_date + relativedelta(
                    months=+int(self.method_period))
                # datetime doesn't take into account that the number of days is not the same for each month
                if int(self.method_period) % 12 != 0:
                    max_day_in_month = \
                        calendar.monthrange(depreciation_date.year,
                                            depreciation_date.month)[1]
                    if self.recognize_on_first:
                        depreciation_date = depreciation_date.replace(
                            day=1)
                    else:
                        depreciation_date = depreciation_date.replace(
                            day=max_day_in_month)
        return move_vals
