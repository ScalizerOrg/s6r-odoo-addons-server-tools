Scalizer Webhook Extra Payload
===============

Adds an "Extra Payload (Python Expression)" field on the native Odoo webhook server action (`ir.actions.server`, "Send Webhook Notification"). The expression is evaluated in a restricted (`safe_eval`) context and its result, a dict, is merged into the webhook payload alongside the standard `_model`/`_id`/`_action` and the selected `Fields`.

This lets an administrator send data that isn't a field of the triggering record (e.g. the id of the user who triggered the action) without writing any code.

**Technical note**: Odoo core builds and sends the webhook payload in a single method (`_run_action_webhook`) with no dedicated extension point, and that method has changed shape across major Odoo versions (17.0/18.0 synchronous vs 19.0+ postcommit/postrollback). This module therefore duplicates the full method rather than extending a hook — re-check it against `odoo/addons/base/models/ir_actions.py` on every major Odoo upgrade.

**Security note**: the `Extra Payload` field is restricted to `base.group_system` and its expression runs through `safe_eval`, but the evaluation context includes `env`, giving ORM read access beyond the action's own model. Only trusted administrators should be allowed to edit server actions.


## Usage

1. Enable developer mode.
2. Go to `Settings > Technical > Automation > Server Actions`.
3. Open a server action with `Action To Do` set to `Send Webhook Notification`.
4. Fill in `Extra Payload` with a Python expression returning a dict, evaluated with `record` (the triggering record), `user` (the current `res.users`) and `env` available, e.g. `{'user_id': user.id}`.

## Configuration

No specific configuration required.

## Authors

* Scalizer

## Maintainers

This module is maintained by [Scalizer](https://www.scalizer.fr).

![Scalizer](./static/description/logo.png)
