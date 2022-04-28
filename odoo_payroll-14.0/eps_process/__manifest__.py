{
    'name': 'employee eps management',
    'version': '14.0.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'description': "This module allows you to manage the hiring process and eps control",
    'live_test_url': 'https://www.ganemo.co/demo',
    'category': 'Payroll',
    'license': 'Other proprietary',

    'depends': [
        'hr_payroll',
        'localization_menu',
    ],
    'data': {
        'security/ir.model.access.csv',
        'views/eps_credit_calculation.xml'
    },
    'installable': True,
    'auto_install': False,
}