# -*- coding: utf-8 -*-
{
    'name': "Saudi GR",

    'summary': """
	GR Stand for General Resource management for Saudi HR.        
""",

    'description': """
        Basically this module Contains Below GR operation for Saudi HR.
		VISA Request\n
		Iqama\n
		Sponsorship Transfer\n
		Operation Request\n
		Recruiter VISA Request\n
		Employee GOSI\n
    """,

    'author': "Aktiv Software",
    'website': "http://www.aktivsoftware.com",

    'category': 'Employees',
    'version': '0.1',

    'depends': ['saudi_base'],

    'data': [
        'security/saudi_gr_security.xml',
        'security/ir.model.access.csv',
        'data/saudi_gr_data.xml',
        'views/gr_operation_config_view.xml',
        'views/visa_request_view.xml',
        'views/visa_iqama_view.xml',
        'views/sponsorship_transfer_view.xml',
        'views/other_operation_view.xml',
        'views/employee_gosi_view.xml',
        'views/hr_employee_view.xml',
    ],
}
