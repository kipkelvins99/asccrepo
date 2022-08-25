from odoo import api, fields, models, _


class SummaryReport(models.AbstractModel):
    _name = 'report.payroll_reports.summary_report'

    # @api.model
    def _get_report_values(self, docids, data=None):
        # docs = self.env['hr.employee'].browse(data['context']['active_ids'])
        # print(self.env['hr.employee'].browse(data['context']['active_ids']), 'docs')
        return {
            'doc_ids': docids,
            'doc_model': 'hr.employee',
            # 'docs': docs,
            'data': data,
        }
