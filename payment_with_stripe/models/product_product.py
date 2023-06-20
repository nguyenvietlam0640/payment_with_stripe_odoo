from odoo import fields, models, api


class ProductProduct(models.Model):
    
    _inherit = 'product.product'
    order_line_ids = fields.One2many('payment_with_stripe.order_line', 'product_product_id')
