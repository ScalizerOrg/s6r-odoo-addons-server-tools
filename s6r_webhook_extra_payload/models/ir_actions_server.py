import json
import logging

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class IrActionsServer(models.Model):
    _inherit = 'ir.actions.server'

    webhook_extra_payload = fields.Text(
        string="Extra Payload (Python Expression)",
        groups='base.group_system',
        help="Python expression evaluated in a restricted context (safe_eval) with "
             "'record' (the triggering record), 'user' (the current res.users) and "
             "'env' available. Must return a dict, merged into the webhook payload. "
             "Example: {'user_id': user.id}",
    )

    def _run_action_webhook(self, eval_context=None):
        """Send a post request with a read of the selected field on active_id.

        Odoo core (odoo/addons/base/models/ir_actions.py) builds and sends the
        webhook payload in this same method, with no dedicated hook to extend
        it, and the method body has changed shape across major versions
        (17.0/18.0 synchronous vs 19.0+ postcommit/postrollback). This override
        therefore duplicates the full method rather than extending a clean
        extension point: re-check it against Odoo core on every major upgrade.
        """
        record = self.env[self.model_id.model].browse(self.env.context.get('active_id'))
        url = self.webhook_url
        if not record:
            return
        if not url:
            raise UserError(_("I'll be happy to send a webhook for you, but you really need to give me a URL to reach out to..."))
        vals = {
            '_model': self.model_id.model,
            '_id': record.id,
            '_action': f'{self.name}(#{self.id})',
        }
        if self.webhook_field_ids:
            # you might think we could use the default json serializer of the requests library
            # but it will fail on many fields, e.g. datetime, date or binary
            # so we use the json.dumps serializer instead with the str() function as default
            vals.update(record.read(self.webhook_field_ids.mapped('name'), load=None)[0])
        if self.webhook_extra_payload:
            self._merge_webhook_extra_payload(vals, record)
        json_values = json.dumps(vals, sort_keys=True, default=str)
        _logger.info("Webhook call to %s", url)
        _logger.debug("POST JSON data for webhook call: %s", json_values)

        @self.env.cr.postrollback.add
        def _add_post_rollback():
            _logger.warning("Webhook call to %s - cancelled due to a rollback", url)

        @self.env.cr.postcommit.add
        def _add_post_commit():
            _logger.debug("Webhook call to %s - start", url)
            import requests  # noqa: PLC0415
            try:
                # 'send and forget' strategy, and avoid locking the user if the webhook
                # is slow or non-functional (we still allow for a 1s timeout so that
                # if we get a proper error response code like 400, 404 or 500 we can log)
                response = requests.post(url, data=json_values, headers={'Content-Type': 'application/json'}, timeout=1)
                response.raise_for_status()
                _logger.info("Webhook call to %s - succeeded", url)
            except requests.exceptions.ReadTimeout:
                _logger.warning("Webhook call timed out after 1s - it may or may not have failed. "
                                "If this happens often, it may be a sign that the system you're "
                                "trying to reach is slow or non-functional.")
            except requests.exceptions.RequestException as e:
                _logger.warning("Webhook call failed: %s", e)

    def _compute_webhook_sample_payload(self):  # pylint: disable=missing-return
        """Also reflect ``webhook_extra_payload`` in the sample payload preview."""
        super()._compute_webhook_sample_payload()
        for action in self:
            if action.state != 'webhook' or not action.webhook_extra_payload:
                continue
            sample_record = self.env[action.model_id.model].with_context(active_test=False).search([], limit=1)
            if not sample_record:
                continue
            payload = json.loads(action.webhook_sample_payload)
            action._merge_webhook_extra_payload(payload, sample_record)
            action.webhook_sample_payload = json.dumps(payload, indent=4, sort_keys=True, default=str)

    def _merge_webhook_extra_payload(self, vals, record):
        """Evaluate ``webhook_extra_payload`` and merge its result into ``vals``."""
        self.ensure_one()
        try:
            extra_vals = safe_eval(
                self.webhook_extra_payload,
                {'record': record, 'user': self.env.user, 'env': self.env},
            )
        except Exception:
            _logger.exception("Failed to evaluate the webhook extra payload of action %s, ignored.", self.id)
            return
        if isinstance(extra_vals, dict):
            vals.update(extra_vals)
        else:
            _logger.error(
                "The webhook extra payload of action %s did not evaluate to a dict, ignored.", self.id,
            )
