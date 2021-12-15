# -*- coding: utf-8 -*-
# © 2021 Ingetive - <info@ingetive.com>
{
    'name': "Valiryo",
    'summary': """""",
    'description': """""",
    'author': "Ingetive",
    'website': "http://ingetive.com",
    'category': 'Uncategorized',
    'version': '15.0.1.0.1',
    'depends': [
        'base',
        'mail',
        'product',
        'sale',
        'purchase',
        'account',
        'account_reports',
    ],
    'data': [
        'security/valiryo_security.xml',
        'report/sale_order.xml',
        'report/purchase.xml',
        'report/account_move.xml',
        #'report/productos_factura.xml',
        'report/purchasequotation.xml',
        'views/product_template.xml', 
        'views/sale_order.xml',  
        'views/stock_picking.xml',
        'views/account_move.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'valiryo/static/src/js/**/*',
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'Other proprietary',
}

