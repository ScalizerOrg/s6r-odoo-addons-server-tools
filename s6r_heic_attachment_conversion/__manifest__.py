# Copyright 2025 Scalizer (<https://www.scalizer.fr>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Scalizer HEIC Attachment Conversion',
    'version': '19.0.1.0.0',
    'author': 'Scalizer',
    'website': 'https://www.scalizer.fr',
    'summary': "HEIC Image Attachment Conversion",
    'sequence': 0,
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'external_dependencies': {
        'python': ['pillow-heif'],
    },
    'category': 'Generic Modules/Scalizer',
    'complexity': 'easy',
    'description': '''
This module converts HEIC image file to PNG or JPEG on attachment creation
    ''',
    'qweb': [
    ],
    'demo': [
    ],
    'images': [
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
