# -*- coding: utf-8 -*-
{
    'name': "saudi_it",

    'summary': """
    IT Stand for Infermation Technology
       """,

    'description': """
       Basically this module Contains Below IT operation for Saudi HR.
        Equipment Request\n
        Employee Registration\n
        Employee Deregistration\n
    """,

    'author': "Aktiv Software",
    'website': "http://www.aktivsoftware.com",

    'category': 'Employees',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['saudi_base','maintenance'],

    # always loaded
    'data': [
        'security/saudi_it_security.xml',
        'security/ir.model.access.csv',
        'data/saudi_it_data.xml',
        'views/equipment_request_views.xml',
        'views/employee_registration_views.xml',
        'views/employee_deregistration_views.xml',
	   'views/hr_employee_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
