{
    'name': 'RUC Validation SUNAT',
    'version': '14.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Consult RUC, DNI and complete contacts automatically from SUNAT, using a private consultation service https://apiperu.dev.',
    'category': 'Accounting',
    'depends': [
        'document_type_validation',
        'l10n_pe_catalog',
        'first_and_last_name',
        'l10n_pe_vat_validation',
        'l10n_country_filter'
    ],
    'data': [
        'views/partner_views.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 4.00
}
