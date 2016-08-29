{
    'name': 'Qweb report test',
    'summary' : '',
    'version': '1.0',
    'category': 'sale',
    'website': '',
    'complexity': "normal",
    'sequence': 20,
    'description': """

""",

    # Dependencies
    'depends': ['purchase'],
    'external_dependencies': {},

    'data': [
        'report/purchase_report_test.xml',
        'report/report_header.xml',
        'report/inherit_purchase_report.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'active':True,
    'auto_install': False,
}
