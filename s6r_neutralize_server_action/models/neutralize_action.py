from odoo import fields, models


class NeutralizeAction(models.Model):
    _name = 'neutralize.action'
    _description = 'Server action to run after a database neutralization'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10, help="Determines the execution order after the neutralization.")
    action_id = fields.Many2one(
        'ir.actions.server', string="Server Action", required=True, ondelete='restrict',
        help="Server action to execute after the neutralization.",
    )
    name = fields.Char(related='action_id.name', store=True)
    active = fields.Boolean(default=True, help="Uncheck to temporarily disable this line without deleting it.")
