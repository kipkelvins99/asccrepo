from odoo import fields, models


class StockReturnPickingUpdatedLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    to_refund = fields.Boolean(string="Update quantities on SO/PO",
                               default=False,
                               help='Trigger a decrease of the delivered/received quantity in the associated Sale Order/Purchase Order')
