{
    'name': 'Pago Masivo de Proveedores',
    'version': '14.0.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'live_test_url': 'https://www.ganemo.co/demo',
    'description': "This module issues the txt files for the massive payment of suppliers",
    'depends': [
        'l10n_pe_edi',
        'base_spot',
        'account',
        'type_bank_accounts',
        'account_batch_payment',
    ],
    'data': [
        'views/account_batch_payment.xml',
    ],
    'installable': True,
    'auto_install': False,
}
