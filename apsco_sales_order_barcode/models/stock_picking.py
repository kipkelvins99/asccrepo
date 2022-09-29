from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_barcode_view_state(self):
        pickings = super(StockPicking, self).get_barcode_view_state()
        for picking in pickings:
            picking['actionSalesOrderReportBarcodes'] = self.env.ref(
                'apsco_sales_order_barcode.sales_order_barcode_report_id').id
        return pickings
