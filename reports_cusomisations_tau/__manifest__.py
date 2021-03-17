# -*- coding: utf-8 -*-

{
'name': "reports_cusomisations_tau",
'version': '14.0.1.0',
'author': 'OdooHK-TAU',
'description': 'Reports customisation',
'depends': ['purchase', 'account', 'sale', 'point_of_sale', 'hr'],
'data': [
    'views/account_move.xml',
    'views/purchase_order.xml',
    'views/pos_assets.xml',
    'views/pos_config.xml',
    'reports/invoice_report.xml',
    'reports/purchase_order_reports.xml',
    'reports/sale_order_reports.xml',
    ],

'qweb': [
    'static/src/xml/OrderReceipt.xml',
    ],
}
