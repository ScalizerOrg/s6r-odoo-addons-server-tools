# Copyright 2024 Scalizer (https://www.scalizer.fr)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models, api, Command
from odoo.tools.safe_eval import safe_eval
from odoo.addons.base.models.ir_model import SAFE_EVAL_BASE


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(BaseModel, self).create(vals_list)
        tag_ids = self.env['model.tag'].search([('model', '=', self._name)])
        for rec in res:
            rec._apply_tags(tag_ids)
        return res

    def write(self, vals):
        res = super(BaseModel, self).write(vals)
        tag_ids = self.env['model.tag'].search([('model', '=', self._name)])
        if any(field in tag_ids.mapped('trigger_field_ids.name') for field in vals):
            self._apply_tags(tag_ids)
        return res

    def _apply_tags(self, tag_ids):
        for tag in tag_ids:
            res = []
            local_dict = {'self': self, 'res': res}
            safe_eval(tag.compute_tags_method, SAFE_EVAL_BASE, local_dict, mode='exec', nocopy=True)
            res = local_dict['res']
            if res:
                tags = self.env[tag.tag_field_id.relation].search([('name', 'in', res)])
                self[tag.tag_field_id.name] = [Command.set(tags.ids)]
