{
    'name': 'Pagos masivos de detracciones',
    'version': '14.0.2.0.0',
    'author': 'Ganemo, Unoobi',
    'website': 'https://www.ganemo.co',
    'live_test_url': 'https://www.ganemo.co/demo',
    'summary': 'This module allows us to make massive payments of detractions.',
    'category': 'Accounting',
    'depends': ['l10n_pe_edi',
                'base_spot',
                'account',
                'account_batch_payment'
                ],
    'data': [
        'views/account_move.xml',
        'views/account_payment.xml',
        'views/account_batch_payment.xml',
        'wizard/account_payment_register.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 299.00
}
