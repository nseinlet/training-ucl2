# -*- coding: utf-8 -*-
{
    'name': "openacademy",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail', 'board', 'website'],

    # always loaded
    'data': [
        'security/res.groups.csv',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/course.xml',
        'views/session.xml',
        'views/partner.xml',
        'views/inscription.xml',
        'views/entity.xml',
        'views/menu.xml',
        'templates.xml',
        'data/respartnercategory.xml',
        'views/wizard.xml',
        'views/wizard2.xml',
        'views/reports.xml',
        'views/dashboard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}