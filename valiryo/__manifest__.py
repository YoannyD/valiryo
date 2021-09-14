# -*- coding: utf-8 -*-
# © 2021 Ingetive - <info@ingetive.com>
{
    'name': "Valiryo",
    'summary': """""",
    'description': """""",
    'author': "Ingetive",
    'website': "http://ingetive.com",
    'category': 'Uncategorized',
    'version': '13.0.1.0.1',
    'depends': [
        'base',
        'product',
        'sale',
        'purchase',
        'account',
        'account_reports',
    ],
    'data': [
        'report/sale_order.xml',
        'report/purchase.xml',
        'report/account_move.xml',
        'report/productos_factura.xml',
        'report/purchasequotation.xml',
        'views/res_config_settings.xml', 
        'views/product_template.xml', 
        'views/sale_order.xml',  
        'views/stock_picking.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

