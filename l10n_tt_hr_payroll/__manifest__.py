{
    'name': 'Payroll - Trinidad and Tobago',
    'version': '14.0.1.0.1',
    'summary': 'To handle the TD4 report in payroll',
    'author': 'Cybrosys Techno solutions',
    'company': 'Cybrosys Techno Solutions',
    'depends': ['base', 'hr_payroll'],
    'maintainer': 'Cybrosys Techno Solutions',
    'data': [
        'security/ir.model.access.csv',
        'data/hr_payroll_data.xml',
        'views/health_surcharge_rates.xml',
        'views/nis_rates.xml',
        'views/paye_rates.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}