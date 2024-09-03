# -*- coding: utf-8 -*-
{
    'name': "demo_external_sync",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'demo_base','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/example_view.xml',
        'views/product_template_view.xml',
        'views/product_product_view.xml',
        'views/product_sync_view.xml',
    ],

    'installable': True,
    'application': True,

    'controllers': [
        'controllers/example_controller.py'
    ],
}

