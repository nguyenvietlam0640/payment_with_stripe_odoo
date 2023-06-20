from odoo import fields, models, api


class ProductProduct(models.Model):
   
    _inherit = 'product.template'
    order_line_ids = fields.One2many('payment_with_stripe.order_line', 'product_template_id')
