odoo.define('stock_barcode.SalesOrderClientAction', function (require) {
'use strict';

const core = require('web.core');
const PickingClientAction = require('stock_barcode.picking_client_action');
const ViewsWidget = require('stock_barcode.ViewsWidget');

const _t = core._t;

const SalesOrderClientAction = PickingClientAction.extend({
    custom_events: Object.assign({}, PickingClientAction.prototype.custom_events, {
        'print_sales_order': '_onPrintSalesOrder',
    }),


    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Handles the `print_picking_batch` OdooEvent.
     * It makes an RPC call to the method 'action_print'.
     *
     * @private
     * @param {OdooEvent} ev
     */
    _onPrintSalesOrder: function (ev) {
        ev.stopPropagation();
        this._printReport(this.currentState.actionSalesOrderReportBarcodes);
    },
});

core.action_registry.add('stock_barcode_picking_client_action', SalesOrderClientAction);

return SalesOrderClientAction;

});
