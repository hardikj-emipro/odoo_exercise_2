# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Student & Course Demo",
    'version': "1.0",
    'author': 'Emipro Technologies Pvt. Ltd.',
    'category': "Sales/Sales",
    'description': """
    2nd Programme of Exercise 2.
    """,
    'depends': ['sales_team'],
    'data': ['security/ir.model.access.csv',
             'views/course_demo.xml',
             'views/student_demo.xml'],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False
}
