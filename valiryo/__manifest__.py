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
    ],
    'data': [
        'views/product_template.xml', 
        'views/sale_order.xml',
        'report/sale_order.xml',
        'report/purchase.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

