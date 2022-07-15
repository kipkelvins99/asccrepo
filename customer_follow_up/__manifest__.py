{
    'name': 'Customer Followup Report',
    'version': '14.0.1.0.1',
    'summary': 'To handle the followup report in customer followup report',
    'author': 'Cybrosys Techno solutions',
    'company': 'Cybrosys Techno Solutions',
    'depends': ['base', 'account_followup', 'account', 'account_reports'],
    'maintainer': 'Cybrosys Techno Solutions',
    'data': [
        'views/follow_up_template.xml',
        'views/report_followup_new.xml',
        'views/follow_up_assets.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
