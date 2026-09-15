import logging

import odoo.modules.neutralize
from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

_PATCHED_ATTR = '_s6r_post_neutralization_action_patched'


def _run_configured_server_actions(cursor):
    env = api.Environment(cursor, SUPERUSER_ID, {})
    if 'post.neutralization.action' not in env.registry:
        return

    lines = env['post.neutralization.action'].search([('active', '=', True)])
    executed = 0
    for line in lines:
        try:
            line.action_id.run()
            executed += 1
        except Exception:
            _logger.exception(
                "Post neutralization action failed (post.neutralization.action id=%s, action_id=%s)",
                line.id, line.action_id.id,
            )
    _logger.info("Post neutralization action: %s/%s configured action(s) executed", executed, len(lines))


def post_load_neutralize_patch():
    original_neutralize_database = odoo.modules.neutralize.neutralize_database
    if getattr(original_neutralize_database, _PATCHED_ATTR, False):
        return

    def neutralize_database(cursor):
        original_neutralize_database(cursor)
        # Commit the standard neutralization before running our own actions,
        # so it is preserved even if a configured server action fails.
        cursor.commit()
        _run_configured_server_actions(cursor)

    setattr(neutralize_database, _PATCHED_ATTR, True)
    odoo.modules.neutralize.neutralize_database = neutralize_database
