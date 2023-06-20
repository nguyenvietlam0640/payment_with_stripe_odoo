

from odoo import fields, models, api
from odoo.exceptions import ValidationError  


class OrderLine(models.Model):
    _name = 'payment_with_stripe.order_line'
    
    name = fields.Char(string='Order line name', default='Orderline')
    quantity = fields.Integer()
    currency_id = fields.Many2one('res.currency', related='order_id.currency_id' , string='Order line currency')
    total = fields.Monetary(currency_field='currency_id', compute='_compute_total')
    product_product_id = fields.Many2one('product.product', ondelete='cascade', require=True)
    product_template_id = fields.Many2one('product.template', ondelete='cascade', related='product_product_id.product_tmpl_id')
    order_id = fields.Many2one('payment_with_stripe.order', ondelete='cascade', readonly=True)
    
    _sql_constraints = [
        ('check_name_unique',
         'UNIQUE(name)',
         'Name orderline must be unique'),
        
        ('check_quantity_not_negative',
         'CHECK(quantity>0)',
         'quantity must greater than zero'),
        ]
    
    @api.depends('quantity', 'product_product_id')
    def _compute_total(self):
        for r in self:
            r.total = r.quantity * r.product_product_id.list_price
    
