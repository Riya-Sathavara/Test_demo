# -*- coding: utf-8 -*-
{
    'name': "Admin Operations",

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

    'depends': ['hr', 'hr_expense'],

    'data': [
             'security/ir.model.access.csv',
             'data/admin_operations_data.xml',
             'security/admin_operation_security.xml',
             'views/ticket_type_view.xml',
             'views/purpose_of_travel_view.xml',
             'views/flight_booking_view.xml',
             'views/hotel_type_view.xml',
             'views/hotel_booking_view.xml',
             'views/ticket_details_view.xml',
    ],
}
