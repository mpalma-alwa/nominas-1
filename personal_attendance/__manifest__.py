# -*- coding: utf-8 -*-
# Copyright (C) 2022 Kevin Sander <lodhur@web.de>
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Personal Attendance",

    'summary': """
        Working hours of logged in person""",

    'description': """
        The hr.attendance module will be extended by one menu entry "My working time". The logged in user has the 
        possibility to see his own working hours. 
        Depending on his rights he is unable or able to change his working hours.         
    """,

    'author': "K. Sander",
    'website': "https://github.com/Fikom/odoo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '14.0',
    "license": "LGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_attendance'],
    'installable': True,

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/attendance.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
