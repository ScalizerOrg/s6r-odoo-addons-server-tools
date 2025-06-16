# Copyright 2024 Scalizer (https://www.scalizer.fr)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models, api, Command, fields
from odoo.tools.safe_eval import safe_eval
from odoo.addons.base.models.ir_model import SAFE_EVAL_BASE


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(BaseModel, self).create(vals_list)
        if not self.env.context.get('skip_tag_computation'):
            tag_ids = self.env['model.tag'].search([('model', '=', self._name)])
            for rec in res:
                rec._apply_tags(tag_ids)
        return res

    def write(self, vals):
        res = super(BaseModel, self).write(vals)
        if not self.env.context.get('skip_tag_computation'):
            tag_ids = self.env['model.tag'].search([('model', '=', self._name)])
            if any(field in tag_ids.mapped('trigger_field_ids.name') for field in vals):
                self._apply_tags(tag_ids)
        return res

    def unlink(self):
        tag_ids = self.env['model.tag'].search([('model', '=', self._name), ('compute_on_unlink', '=', True)])
        for tag_id in tag_ids:
            self._apply_tags(tag_id)
        return super(BaseModel, self).unlink()

    def _apply_tags(self, tag_ids):
        for rec in self:
            for tag in tag_ids:
                res = []
                local_dict = {
                    'self': rec,
                    'res': res,
                    'Date': fields.Date,
                    'dynamic_unlink': rec.env.context.get('dynamic_unlink', False)
                }
                safe_eval(tag.compute_tags_method, SAFE_EVAL_BASE, local_dict, mode='exec', nocopy=True)
                res = local_dict['res']
                if res:
                    tags = rec.env[tag.tag_field_id.relation].search([('name', 'in', res)])
                    rec.with_context(skip_tag_computation=True)[tag.tag_field_id.name] = [Command.set(tags.ids)]
