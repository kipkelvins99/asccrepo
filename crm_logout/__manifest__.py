# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Afra K (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

{
    'name': 'CRM IDLE LOGOUT',
    'version': '15.0.1.0.1',
    'summary': """CRM""",
    'description': 'CRM',
    'category': 'Warehouse Management',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base', 'crm', 'sale_management', 'purchase'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/account_data.xml',
        'views/res_config_settings_view.xml',
        'views/crm_lead_views.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'crm_logout/static/src/xml/crm_logout.xml',
        ],
        'web.assets_backend': [
            'crm_logout/static/src/js/crm_logout.js',
        ],

    },

    # 'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
