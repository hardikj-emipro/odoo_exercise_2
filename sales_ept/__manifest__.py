# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Sales Management EPT",
    'version': "1.0",
    'author': 'Emipro Technologies Pvt. Ltd.',
    'category': "Sales/Sales",
    'description': """
    4th Programme of Exercise 2.
    """,
    'depends': [
            'sales_team',
            'res_localization_ept'
            ],
    'data': ['security/ir.model.access.csv',
             'views/product_category.xml',
             'views/product_uom_category.xml',
             'views/product_uom_ept.xml',
             'views/product_ept.xml',
             'views/res_partner_ept.xml',
             'views/sale_order_ept.xml'],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False
}
