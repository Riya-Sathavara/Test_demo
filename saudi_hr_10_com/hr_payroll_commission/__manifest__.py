# -*- coding: utf-8 -*-
{
    'name': "hr_payroll_commission",

    'summary': """
        Payroll Commisions""",

    'description': """
            Payroll Commisions
    """,

    'author': "Active Software",
    'website': "http://www.aktivsoftware.com",

    'category': 'Human Resources',
    'version': '0.1',

    'depends': ['base', 'hr_payroll', 'account'],

    'data': [
        'views/hr_contract_view.xml',
        'views/hr_payroll_view.xml',
        'data/hr.salary.rule.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
