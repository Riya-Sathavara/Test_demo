# -*- coding: utf-8 -*-
{
    'name': "saudi_base",

    'summary': """
	Base Module for Saudi HR.        
""",

    'description': """
        Module provide base functionality for all modules in saudi HR.
    """,

    'author': "Aktiv Software",
    'website': "http://www.aktivsoftware.com",

    'category': 'Employees',
    'version': '0.1',

    'depends': ['hr'],

    'data': [
	'security/saudi_base_security.xml',
        # 'security/ir.model.access.csv',
	'views/base_operation_config_view.xml',
        'views/hr_employee_view.xml',
    ],
}
