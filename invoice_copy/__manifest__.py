# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "invoice_copy",
    'summary': "Mark invoice as copy after original print",
    'version': '14.0.1.0',
    'author': 'OdooHK-FJA',
    'depends': ['account', 'point_of_sale'],
    'data': [
        'data/account_move.xml',
        'views/account_invoice_send_views.xml',
        'views/report_invoice.xml',
    ],
    'qweb': [
        'static/src/xml/OrderReceipt.xml',
    ],
}
