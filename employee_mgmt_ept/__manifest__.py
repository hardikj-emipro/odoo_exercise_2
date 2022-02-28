# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "HR",
    'version': "1.0",
    'author': 'Emipro Technologies Pvt. Ltd.',
    'category': "Sales/Sales",
    'description': """
    3rd Programme of Exercise 2.
    """,
    'depends': ['sales_team'],
    'data': ['security/hr_security.xml',
             'security/ir.model.access.csv',
             'views/employee_department.xml',
             'views/employee_shift.xml',
             'views/employee.xml',
             'views/employee_leave_ept.xml'],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False
}
