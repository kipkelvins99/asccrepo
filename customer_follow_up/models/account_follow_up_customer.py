import dateutil.utils

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.tools.misc import formatLang, format_date, get_lang
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from itertools import chain
from datetime import datetime as dt


class AccountFollowupCustomer(models.AbstractModel):
    _inherit = 'account.followup.report'

    _depends = {
        'account.move.line': [
            'id',
            'move_id',
            'name',
            'account_id',
            'journal_id',
            'company_id',
            'currency_id',
            'analytic_account_id',
            'display_type',
            'date',
            'debit',
            'credit',
            'balance',
        ],
    }

    def _get_columns_name(self, options):
        headers = [
            {'style': 'display:none;'},
            {'name': _('Date'), 'class': 'date',
             'style': 'text-align:center; width:15%; white-space:nowrap;'},
            {'name': _('Due Date'), 'class': 'date',
             'style': 'text-align:center; white-space:nowrap;'},
            {'name': _('Source Document'),
             'style': 'text-align:center; white-space:nowrap;'},
            {'name': _('Communication'),
             'style': 'text-align:right; white-space:nowrap;'},
            {'name': _('Expected Date'), 'class': 'date',
             'style': 'white-space:nowrap;'},
            {'name': _('Excluded'), 'class': 'date',
             'style': 'white-space:nowrap;'},
            {'name': _('Amount'), 'class': 'number',
             'style': 'text-align:right; white-space:nowrap;'},
            {'name': _('Total Due'), 'class': 'number o_price_total',
             'style': 'text-align:right; white-space:nowrap;'},
            {'name': _('Balance'), 'class': 'number o_price_total',
             'style': 'text-align:right; white-space:nowrap;'},
        ]
        if self.env.context.get('print_mode'):
            headers = headers[:5] + headers[
                                    7:]  # Remove the 'Expected Date' and 'Excluded' columns
        return headers

    def _get_lines(self, options, line_id=None):
        """
        Override
        Compute and return the lines of the columns of the follow-ups report.
        """
        # Get date format for the lang
        new_fun = self.report_new(options)
        partner = options.get('partner_id') and self.env['res.partner'].browse(
            options['partner_id']) or False
        if not partner:
            return []

        lang_code = partner.lang if self._context.get(
            'print_mode') else self.env.user.lang or get_lang(self.env).code
        lines = []
        li = []
        res = {}
        today = fields.Date.today()
        line_num = 0
        running_bal = 0
        for l in partner.unreconciled_aml_ids.sorted():
            if l.company_id == self.env.company:
                if self.env.context.get('print_mode') and l.blocked:
                    continue
                currency = l.currency_id or l.company_id.currency_id
                if currency not in res:
                    res[currency] = []
                res[currency].append(l)
        for currency, aml_recs in res.items():
            total = 0
            total_issued = 0
            for aml in aml_recs:
                amount = aml.amount_residual_currency if aml.currency_id else aml.amount_residual
                li.append(amount)
                running_bal = li[0] + running_bal
                format_float = "{:.2f}".format(running_bal)
                date_due = format_date(self.env, aml.date_maturity or aml.date,
                                       lang_code=lang_code)
                total += not aml.blocked and amount or 0
                is_overdue = today > aml.date_maturity if aml.date_maturity else today > aml.date
                is_payment = aml.payment_id
                if is_overdue or is_payment:
                    total_issued += not aml.blocked and amount or 0
                if is_overdue:
                    date_due = {'name': date_due, 'class': 'color-red date',
                                'style': 'white-space:nowrap;text-align:center;color: red;'}
                if is_payment:
                    date_due = ''
                move_line_name = self._format_aml_name(aml.name,
                                                       aml.move_id.ref,
                                                       aml.move_id.name)
                total_amoun = aml.move_id.amount_total_signed
                # print(aml.move_id.name,'amlllllll')
                format_new_date = format_date(self.env, aml.date,
                                              lang_code=lang_code)
                if self.env.context.get('print_mode'):
                    move_line_name = {'name': move_line_name,
                                      'style': 'text-align:right; white-space:normal;'}
                    format_new_date = {'name': format_new_date,
                                       'style': 'text-align:right;'}
                amount = formatLang(self.env, amount, currency_obj=currency)
                total_amoun = formatLang(self.env, total_amoun,
                                         currency_obj=currency)
                line_num += 1
                expected_pay_date = format_date(self.env,
                                                aml.expected_pay_date,
                                                lang_code=lang_code) if aml.expected_pay_date else ''
                invoice_origin = aml.move_id.invoice_origin or ''
                if len(invoice_origin) > 43:
                    invoice_origin = invoice_origin[:40] + '...'
                columns = [
                    # format_date(self.env, aml.date, lang_code=lang_code),
                    format_new_date,
                    date_due,
                    invoice_origin,
                    move_line_name,
                    (expected_pay_date and expected_pay_date + ' ') + (
                            aml.internal_note or ''),
                    {'name': '', 'blocked': aml.blocked},
                    total_amoun,
                    amount,
                    format_float,
                ]
                if self.env.context.get('print_mode'):
                    columns = columns[:4] + columns[6:]
                lines.append({
                    'id': aml.id,
                    'account_move': aml.move_id,
                    # 'name': aml.move_id.name,
                    # 'caret_options': 'followup',
                    'move_id': aml.move_id.id,
                    'type': is_payment and 'payment' or 'unreconciled_aml',
                    'unfoldable': False,
                    'columns': [type(v) == dict and v or {'name': v} for v in
                                columns],
                })
                li.pop(0)
            total_due = formatLang(self.env, total, currency_obj=currency)
            line_num += 1
            lines.append({
                'id': line_num,
                'name': '',
                'class': 'total',
                'style': 'border-top-style: double',
                'unfoldable': False,
                'level': 4,
                'columns': [{'name': v} for v in [''] * (
                    5 if self.env.context.get('print_mode') else 6) + [
                                total >= 0 and _('Total Due') or '',
                                total_due]],
            })
            # Add an empty line after the total to make a space between two currencies
            line_num += 1
            lines.append({
                'id': line_num,
                'name': '',
                'class': '',
                'style': 'border-bottom-style: none',
                'unfoldable': False,
                'level': 0,
                'columns': [{} for col in columns],
            })
        # Remove the last empty line
        if lines:
            lines.pop()
        return lines

    def _get_report_name(self):
        """
        Override
        Return the name of the report
        """
        return _('Customer Statement')

    def report_new(self, options):
        partner = options.get('partner_id') and self.env['res.partner'].browse(
            options['partner_id']) or False
        account_move = self.env['account.move'].search([('partner_id', '=', partner.id)])
        amount_total = 0.0
        difference_in_days = 0.0
        total = round(partner.total_due, 2)
        record = []
        record.extend([{'symbol': self.env.company.currency_id.symbol}])
        for move in account_move:
            if move:
                account_payment = self.env['account.payment'].search(
                    [('partner_id', '=', partner.id), ('move_id', '=', move.id)])
                if move.invoice_date_due:
                    invoice_due = move.invoice_date_due
                    today_date = date.today()
                    difference_in_days = (today_date - invoice_due).days
                if account_payment:
                    for pay in account_payment:
                        self.env.cr.execute('''select sum(amount_residual)  as current
                                   from account_move
                                   where DATE(invoice_date_due) >= DATE(NOW())
                                   and state = 'posted'
                                   and partner_id = '%s'  ''' % partner.id)

                        current_rec = self.env.cr.dictfetchall()
                        if current_rec == [{'current': None}]:
                            record.extend([{'current': 0.0}])
                            if move.date == date.today() and move.date == pay.date and pay.is_reconciled is False and pay.payment_type == 'inbound':
                                amount_total = 0.0
                                amount_total += move.amount_total
                                current = float(record[1]['current']) - amount_total
                                record[1]['current'] = current
                        elif current_rec != [{'current': None}]:
                            record.extend(current_rec)
                            if move.date == date.today() and move.date == pay.date and pay.is_reconciled is False and pay.payment_type == 'inbound':
                                amount_total = 0.0
                                amount_total += move.amount_total
                                current = round(float(record[1]['current']) - amount_total, 2)
                                record[1]['current'] = current
                        self.env.cr.execute('''select sum(amount_residual) as due1
                                            from account_move
                                            WHERE (date(now()) - invoice_date_due ) between 1 and 30
                                            and state = 'posted'
                                            AND partner_id = '%s'  ''' % partner.id)
                        due1 = self.env.cr.dictfetchall()
                        if due1 == [{'due1': None}]:
                            record.extend([{'due1': 0.0}])
                            if move.date == pay.date and pay.is_reconciled is False and 0 < difference_in_days <= 30 and pay.payment_type == 'inbound':
                                amount_total = 0.0
                                amount_total += pay.amount
                                due1 = round(float(record[2]['due1']) - amount_total, 2)
                                record[2]['due1'] = due1
                        elif due1 != [{'due1': None}]:
                            record.extend(due1)
                            if move.date == pay.date and pay.is_reconciled is False and pay.payment_type == 'inbound' and 0 < difference_in_days <= 30:
                                amount_total = 0.0
                                amount_total += pay.amount
                                due1 = round(float(record[2]['due1']) - amount_total, 2)
                                record[2]['due1'] = due1
                        self.env.cr.execute('''select sum(amount_residual) as due2
                                            from account_move
                                            WHERE (date(now()) - invoice_date_due ) between 30 and 60
                                            and state = 'posted'
                                            AND partner_id = '%s' ''' % partner.id)
                        due2 = self.env.cr.dictfetchall()
                        if due2 == [{'due2': None}]:
                            record.extend([{'due2': 0.0}])
                            if move.date == pay.date and pay.is_reconciled is False and pay.payment_type == 'inbound' and 30 < difference_in_days <= 60:
                                amount_total = 0.0
                                amount_total += pay.amount
                                due2 = round(float(record[3]['due2']) - amount_total, 2)
                                record[3]['due2'] = due2
                        elif due2 != [{'due2': None}]:
                            record.extend(due2)
                            if move.date == pay.date and pay.is_reconciled is False and pay.payment_type == 'inbound' and 30 < difference_in_days <= 60:
                                amount_total = 0.0
                                amount_total += pay.amount
                                due2 = round(float(record[2]['due2']) - amount_total, 2)
                                record[3]['due2'] = due2
                        self.env.cr.execute('''select sum(amount_residual) as due3
                                            from account_move
                                            WHERE
                                            (date(now()) - invoice_date_due ) between 60
                                            and  90
                                            and state = 'posted'
                                            AND partner_id = '%s'  ''' % partner.id)
                        due3 = self.env.cr.dictfetchall()
                        if due3 == [{'due3': None}]:
                            record.extend([{'due3': 0.0}])
                            if move.date == pay.date and pay.is_reconciled is False and pay.payment_type == 'inbound' and 60 < difference_in_days <= 90:
                                amount_total = 0.0
                                amount_total += pay.amount
                                due3 = round(float(record[4]['due3']) - amount_total, 2)
                                record[4]['due3'] = due3
                        elif due3 != [{'due3': None}]:
                            record.extend(due3)
                            if move.date == pay.date and pay.is_reconciled is False and pay.payment_type == 'inbound' and 60 < difference_in_days <= 90:
                                amount_total = 0.0
                                amount_total += pay.amount
                                due3 = round(float(record[4]['due3']) - amount_total, 2)
                                record[4]['due3'] = due3
                        self.env.cr.execute('''select  sum(amount_residual) as due4
                                                    from account_move
                                                    WHERE
                                                    (date(now()) - invoice_date_due ) between 90
                                                    and  120
                                                    and state = 'posted'
                                                    AND partner_id = '%s'  ''' % partner.id)
                        due4 = self.env.cr.dictfetchall()
                        if due4 == [{'due4': None}]:
                            record.extend([{'due4': 0.0}])
                            if move.date == pay.date and pay.is_reconciled is False and pay.payment_type == 'inbound' and 90 < difference_in_days <= 120:
                                amount_total = 0.0
                                amount_total += pay.amount
                                due4 = round(float(record[5]['due4']) - amount_total, 2)
                                record[5]['due4'] = due4
                        elif due4 != [{'due4': None}]:
                            record.extend(due4)
                            if move.date == pay.date and pay.is_reconciled is False and pay.payment_type == 'inbound' and 90 < difference_in_days <= 120:
                                amount_total = 0.0
                                amount_total += pay.amount
                                due4 = round(float(record[5]['due4']) - amount_total, 2)
                                record[5]['due4'] = due4
                        self.env.cr.execute('''select sum(amount_residual) as due5
                                                    from account_move
                                                    WHERE
                                                    (date(now()) - invoice_date_due ) > 120
                                                    and state = 'posted'
                                                    AND partner_id = '%s'  ''' % partner.id)
                        due5 = self.env.cr.dictfetchall()
                        if due5 == [{'due5': None}]:
                            record.extend([{'due5': 0.0}])
                            if move.date == pay.date and pay.is_reconciled is False and pay.payment_type == 'inbound' and difference_in_days > 120:
                                amount_total = 0.0
                                amount_total += pay.amount
                                due5 = round(float(record[6]['due5']) - amount_total, 2)
                                record[6]['due5'] = due5
                        elif due5 != [{'due5': None}]:
                            record.extend(due5)
                            if move.date == pay.date and pay.is_reconciled is False and pay.payment_type == 'inbound' and difference_in_days <= 30:
                                amount_total = 0.0
                                amount_total += pay.amount
                                due5 = round(float(record[6]['due5']) - amount_total, 2)
                                record[6]['due5'] = due5
                        # total = round(float(record[1]['current']) + float(record[2]['due1']) + float(record[3]['due2']) + float(record[4]['due3']) + float(record[5]['due4']) + float(record[6]['due5']), 2)
                        if not total:
                            record.extend([{'total': 0.0}])
                        else:
                            record.extend([{'total': total}])
                else:
                    self.env.cr.execute('''select sum(amount_residual)  as current
                                                       from account_move
                                                       where DATE(invoice_date_due) >= DATE(NOW())
                                                       and state = 'posted'
                                                       and partner_id = '%s'  ''' % partner.id)

                    current_rec = self.env.cr.dictfetchall()
                    if current_rec == [{'current': None}]:
                        record.extend([{'current': 0.0}])
                    else:
                        record.extend(current_rec)
                    self.env.cr.execute('''select sum(amount_residual) as due1
                                                                from account_move
                                                                WHERE (date(now()) - invoice_date_due ) between 1 and 30
                                                                and state = 'posted'
                                                                AND partner_id = '%s'  ''' % partner.id)
                    due1 = self.env.cr.dictfetchall()
                    if due1 == [{'due1': None}]:
                        record.extend([{'due1': 0.0}])

                    else:
                        record.extend(due1)

                    self.env.cr.execute('''select sum(amount_residual) as due2
                                                                from account_move
                                                                WHERE (date(now()) - invoice_date_due ) between 30 and 60
                                                                and state = 'posted'
                                                                AND partner_id = '%s' ''' % partner.id)
                    due2 = self.env.cr.dictfetchall()
                    if due2 == [{'due2': None}]:
                        record.extend([{'due2': 0.0}])

                    else:
                        record.extend(due2)

                    self.env.cr.execute('''select sum(amount_residual) as due3
                                                                from account_move
                                                                WHERE
                                                                (date(now()) - invoice_date_due ) between 60
                                                                and  90
                                                                and state = 'posted'
                                                                AND partner_id = '%s'  ''' % partner.id)
                    due3 = self.env.cr.dictfetchall()
                    if due3 == [{'due3': None}]:
                        record.extend([{'due3': 0.0}])

                    else:
                        record.extend(due3)

                    self.env.cr.execute('''select  sum(amount_residual) as due4
                                                                        from account_move
                                                                        WHERE
                                                                        (date(now()) - invoice_date_due ) between 90
                                                                        and  120
                                                                        and state = 'posted'
                                                                        AND partner_id = '%s'  ''' % partner.id)
                    due4 = self.env.cr.dictfetchall()
                    if due4 == [{'due4': None}]:
                        record.extend([{'due4': 0.0}])

                    else:
                        record.extend(due4)
                    self.env.cr.execute('''select sum(amount_residual) as due5
                                                                        from account_move
                                                                        WHERE
                                                                        (date(now()) - invoice_date_due ) > 120
                                                                        and state = 'posted'
                                                                        AND partner_id = '%s'  ''' % partner.id)
                    due5 = self.env.cr.dictfetchall()
                    if due5 == [{'due5': None}]:
                        record.extend([{'due5': 0.0}])

                    else:
                        record.extend(due5)

                    # total = round(float(record[1]['current']) + float(record[2]['due1']) + float(record[3]['due2']) + float(record[4]['due3']) + float(record[5]['due4']) + float(record[6]['due5']), 2)
                    if not total:
                        record.extend([{'total': 0.0}])
                    else:
                        record.extend([{'total': total}])
        return record
