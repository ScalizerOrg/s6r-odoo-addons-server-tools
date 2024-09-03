# -*- coding: utf-8 -*-
# Copyright (C) 2024 - Scalizer (<https://www.scalizer.fr>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Scalizer Compute Tags',
    'version': '16.0.1.0.1',
    'author': 'Scalizer',
    'website': 'https://www.scalizer.fr',
    'summary': "Add and remove tags with python evals on any model",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'category': 'Generic Modules/Scalizer',
    'complexity': 'easy',
    'description': '''
This module adds and removes tags with python evals on any model
    ''',
    'qweb': [
    ],
    'demo': [
    ],
    'images': [
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Data
        # Views
        'views/model_tag_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
