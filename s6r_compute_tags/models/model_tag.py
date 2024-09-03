# -*- coding: utf-8 -*-
# Copyright 2024 Scalizer (https://www.scalizer.fr)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models

DEFAULT_PYTHON_CODE = """# Available variables:
#  - env: Odoo Environment on which the action is triggered
#  - model: Odoo Model of the record on which the action is triggered; is a void recordset
#  - record: record on which the action is triggered; may be void
#  - records: recordset of all records on which the action is triggered in multi-mode; may be void
#  - time, datetime, dateutil, timezone: useful Python libraries
#  - float_compare: Odoo function to compare floats based on specific precisions
#  - log: log(message, level='info'): logging function to record debug information in ir.logging table
#  - UserError: Warning Exception to use with raise
#  - Command: x2Many commands namespace
# To return an action, assign: action = {...}\n\n\n\n"""



class ModelTag(models.Model):
    _name = 'model.tag'
    _description = 'This model can add or remove tags to any model based on a Python eval'

    name = fields.Char("Name")
    model_id = fields.Many2one("ir.model", string="Model")
    model = fields.Char(related='model_id.model', string="Model name")
    tag_field_id = fields.Many2one("ir.model.fields", string="Tag Field", domain="[('model_id', '=', model_id)]")
    trigger_field_ids = fields.Many2many("ir.model.fields", string="Trigger Tag Field", domain="[('model_id', '=', model_id)]")
    compute_tags_method = fields.Text(string='Python Code', groups='base.group_system',
                       default=DEFAULT_PYTHON_CODE,
                       help="Write Python code that the action will execute. Some variables are "
                            "available for use; help about python expression is given in the help tab.")