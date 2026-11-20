# Copyright (C) 2026 - Scalizer (<https://www.scalizer.fr>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Scalizer Webhook Extra Payload',
    'version': '20.0.1.0.0',
    'author': 'Scalizer',
    'website': 'https://www.scalizer.fr',
    'summary': "Add a configurable Python expression to extend native webhook server action payloads",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'category': 'Generic Modules/Scalizer',
    'complexity': 'easy',
    'description': '''
This module adds an "Extra Payload (Python Expression)" field on the native
Odoo webhook server action (`ir.actions.server`, "Send Webhook Notification").

The expression is evaluated in a restricted (`safe_eval`) context with
`record`, `user` and `env` available, and its result (a dict) is merged into
the webhook payload alongside the standard `_model`/`_id`/`_action` and the
fields selected in `Fields`.

Lets an administrator send data that is not a field of the triggering record,
such as the id of the user who triggered the action
(`{'user_id': user.id}`), without any code change.
    ''',
    'demo': [
    ],
    'images': [
        'static/description/icon.png',
    ],
    'data': [
        'views/ir_actions_server_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
