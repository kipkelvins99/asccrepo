odoo.define('stock_barcode_sales_order.SettingsWidget', function (require) {
'use strict';

const SettingsWidget = require('stock_barcode.SettingsWidget');

SettingsWidget.include({
    events: Object.assign({}, SettingsWidget.prototype.events, {
        'click .o_print_sales_order': '_onClickPrintSalesOrder',
    }),

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Handles the click on the `print picking batch` button.
     * This is specific to the `stock.picking.batch` model.
     *
     * @private
     * @param {MouseEvent} ev
     */
    _onClickPrintSalesOrder: function (ev) {
        ev.stopPropagation();
        this.trigger_up('print_sales_order');
    },
});

});
