# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    demo_id = fields.Char(string="demo ID", readonly=True)
    is_synced = fields.Boolean(string="Is Synced", default=False, readonly=True)

    def write(self, vals):
        if 'is_synced' not in vals:
            vals['is_synced'] = False

        return super(ProductProduct, self).write(vals)

    @api.model
    def create(self, vals):
        if 'is_synced' not in vals:
            vals['is_synced'] = False

        return super(ProductProduct, self).create(vals)

    def sync_products(self):
        for product in self:
            product.is_synced = True
