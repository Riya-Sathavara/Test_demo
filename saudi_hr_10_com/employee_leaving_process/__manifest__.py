# -*- coding: utf-8 -*-
{
    'name': "Employee Leaving Process(EOS)",

    'summary': """
        Manage Employee Leaving Process and EOS
""",

    'description': """
	Module Contains Below Employee Leaving Process for Saudi HR.
		Employee Leaving Process\n
		Employee Clearance Process\n
		EOS (End of Service Benefits)\n
        
    """,

    'author': "Aktiv Software",
    'website': "http://www.aktivsoftware.com",

    'category': 'Employees',
    'version': '0.1',

    'depends': ['saudi_base', 'saudi_it', 'hr_payroll'],

    'data': [
        'data/payroll_data.xml',
        'data/employee_leaving_process_data.xml',
        'security/employee_leaving_process_security.xml',
        'security/ir.model.access.csv',
        'views/hr_payroll_view.xml',
        'views/employee_leaving_process_view.xml',
        'views/employee_clearance_process_view.xml',
        'views/end_of_service_benefit_view.xml',
    ],
}

