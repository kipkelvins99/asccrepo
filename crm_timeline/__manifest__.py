{
    'name': 'CRM TIMELINE',
    'version': '15.0.1.0.1',
    'summary': """CRM""",
    'description': 'CRM',
    'category': 'Warehouse Management',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base', 'crm', 'sale_management', 'purchase'],
    'data': [
        'views/crm_timeline_cron_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
