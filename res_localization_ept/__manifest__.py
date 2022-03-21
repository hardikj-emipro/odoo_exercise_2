# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Localization Demo Version 2",
    'version': "1.0",
    'author': 'Emipro Technologies Pvt. Ltd.',
    'category': "Sales/Sales",
    'description': """
    1st Programme of Exercise 2.
    """,
    'depends': ['sales_team'],
    'data': ['security/ir.model.access.csv',
             'views/country_demo.xml',
             'views/state_demo.xml',
             'views/city_demo.xml',
             'report/country_report.xml',
             'report/country_report_template.xml'],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False
}
