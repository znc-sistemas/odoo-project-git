# -*- coding: utf-8 -*-
{
    'name': "Project Git Integration",

    'summary': """
        Odoo Project integration with git repositories push webhooks""",

    'description': """Registers work progress in project tasks using commit messages marked with #TASK_ID, and time spent with THH:MM.

Push webhook URL: /project_git/push
    """,

    'author': "ZNC Sistemas",
    'website': "http://znc.com.br",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Project',
    'version': '0.1',
    'license': 'Other OSI approved licence',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
    # 'external_dependencies': {
    #     'python': ['python-dateutil'],
    # }
}
