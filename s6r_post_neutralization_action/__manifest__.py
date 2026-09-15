# Copyright (C) 2026 - Scalizer (<https://www.scalizer.fr>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Scalizer Post Neutralization Action',
    'version': '19.0.1.0.0',
    'author': 'Scalizer',
    'website': 'https://www.scalizer.fr',
    'summary': "Run a configurable, ordered list of server actions right after a database neutralization",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'category': 'Generic Modules/Scalizer',
    'complexity': 'easy',
    'description': '''
This module lets an administrator configure an ordered list of server
actions to run automatically right after the database has been
neutralized (odoo.sh duplicate/restore, `odoo neutralize` command), on
top of the standard neutralization.
    ''',
    'demo': [
    ],
    'images': [
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/post_neutralization_action_views.xml',
    ],
    'post_load': 'post_load_neutralize_patch',
    'auto_install': False,
    'installable': True,
    'application': False,
}
