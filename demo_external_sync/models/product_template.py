# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    demo_id = fields.Char(string="demo ID", readonly=True)
    is_synced = fields.Boolean(string="Is Synced", default=False, readonly=True)

    def write(self, vals):
        if 'is_synced' not in vals:
            vals['is_synced'] = False

        return super(ProductTemplate, self).write(vals)

    @api.model
    def create(self, vals):
        if 'is_synced' not in vals:
            vals['is_synced'] = False
            
        return super(ProductTemplate, self).create(vals)

    def sync_templates(self):
        for template in self:
            template.is_synced = True
            # template.product_variant_ids.sync_products()

    def sync_selected(self):
        self.sync_templates()