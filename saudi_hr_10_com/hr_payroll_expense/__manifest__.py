# -*- coding: utf-8 -*-

{
    'name': 'Expense - Payroll',
    'summary': 'Payroll Expense',
    'description': """
       Basically this module Contains Below Expence operation for Saudi HR.
        
    """,

    'category': 'Employees',
    'author': "Aktiv Software",
    'website': "http://www.aktivsoftware.com",
    'depends': [
        'hr_payroll',
        'hr_expense'
    ],
    'version': '0.1',
    'auto_install': False,
    'data': [
        'views/hr_contract_view.xml',
        'views/hr_payroll_view.xml',
        'data/hr.salary.rule.category.xml',
        'data/hr.salary.rule.xml',
    ],
    'installable': True
}
