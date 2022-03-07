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
             'views/sale_order_ept.xml',
             'views/crm_team_ept.xml',
             'views/crm_lead_ept.xml',
             'views/stock_warehouse_ept.xml',
             'views/stock_location_ept.xml',
             'views/purchase_order_ept.xml',
             'views/stock_picking_ept.xml',
             'views/stock_inventory_ept.xml'
             ],
    'demo': ['data/ir_sequence_data.xml'],
    'installable': True,
    'application': False,
    'auto_install': False
}
