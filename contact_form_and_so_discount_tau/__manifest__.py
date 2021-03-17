# -*- coding: utf-8 -*-

{
'name': 'contact_form_and_so_discount_tau',
'version': '14.0.1.0',
'author': 'OdooHK-TAU',
'description': 'Change contact form and SO discount',
'depends': [
            'sale_management',
            'contacts',
            'account_followup',
            'purchase',
        ],
'data': [
        'data/contact_form_data.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
    ],
}
