{
    "name": "APSCO Sales Order Barcode",
    "version": "1.0",
    "description": "APSCO Sales Order Barcode",
    "summary": "APSCO Sales Order Barcode",
    "author": "Marc Gaston-Johnston",
    "website": "www.pingtt.com",
    "license": "LGPL-3",
    "depends": [
        "sale",
        "stock",
    ],
    "data": [
        "report/sales_order_barcode_report.xml",
        "views/assets.xml",
    ],
    'qweb': ['static/src/xml/qweb_templates.xml'],
    "auto_install": False,
    "installable": True,
    "application": False,
    "assets": {},
}
