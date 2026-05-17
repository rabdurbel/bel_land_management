from odoo import fields, models


class Product(models.Model):
    _inherit = 'product.template'

    rel_property_id = fields.Many2one('property.property')
