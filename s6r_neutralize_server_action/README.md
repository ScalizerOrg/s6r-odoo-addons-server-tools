Scalizer Neutralize Server Action
===============

This module lets an administrator configure an ordered list of server actions to run automatically right after a database neutralization (odoo.sh duplicate/restore, `odoo neutralize` command), on top of the standard neutralization.

It patches `odoo.modules.neutralize.neutralize_database` via a `post_load` hook: the standard neutralization always runs first and is left untouched, then the configured `neutralize.action` lines are executed in order. With no line configured, the module has no effect.


## Usage

1. Enable developer mode.
2. Go to `Settings > Technical > Automation > Neutralize Server Actions`.
3. Add a line: pick an existing `ir.actions.server` and a `Sequence` to control the execution order.
4. Uncheck `Active` to temporarily disable a line without deleting it.

The referenced server actions run with the same privileges and semantics as any other `ir.actions.server` (e.g. a "Execute Python Code" action can reactivate specific `ir.cron` records via `write({'active': True})`, since `ir.cron.toggle()` is itself blocked on a neutralized database).

## Configuration

No specific configuration required.

## Authors

* Scalizer

## Contributors

* David Halgand ([Github](https://github.com/halgandd))

## Maintainers

This module is maintained by [Scalizer](https://www.scalizer.fr).

![Scalizer](./static/description/logo.png)
