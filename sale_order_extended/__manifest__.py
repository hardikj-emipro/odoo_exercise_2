# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Sales Management Extended EPT",
    'version': "1.0",
    'author': 'Emipro Technologies Pvt. Ltd.',
    'category': "Sales/Sales",
    'description': """
    4th Programme of Exercise 2.
    """,
    'depends': [
            'sale_crm',
	        'mail',
            'product'
            ],
    'data': ['security/ir.model.access.csv',
             'data/sample_data.xml',
             'views/sale_order.xml',
             'views/product_product.xml',
             'views/sale_order_line.xml'],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False
}
