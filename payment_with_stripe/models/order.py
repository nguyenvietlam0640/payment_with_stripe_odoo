
from odoo.exceptions import ValidationError 
from odoo import fields, models, api
import datetime
import stripe
import jwt
status_list = [('su', 'Success'), ('wa', 'Wait for checkout'), ('ca', 'Cancel'), ('fa', 'Fail')]

domain = 'http://localhost:8015'


def generate_order_token(order):
    payload = {
        'order': order,
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token


class Order(models.Model):
    _name = 'payment_with_stripe.order'
    status = fields.Selection(status_list, default='wa', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Order Currency', default=2)
    total = fields.Monetary(currency_field='currency_id', compute='_compute_total', store=True)
    
    shipping_fee = fields.Monetary(currency_field='currency_id')
    
    payment_account_id = fields.Many2one('payment_with_stripe.account', ondelete='restrict', require=True)                              
    order_line_ids = fields.One2many('payment_with_stripe.order_line', 'order_id', require=True) 
    payment_url = fields.Text(readonly=True, store=True)

    _sql_constraints = [
        ('check_account_not_null',
         'CHECK(payment_account_id IS NOT NULL)',
         'Stripe account must provided'),
        
    ]
    
    def _set_default_name(self):
        return f'Order #{self.search_count([])+1}'

    name = fields.Char(string='Order name', default=_set_default_name)
    
    @api.depends('shipping_fee', 'order_line_ids')
    def _compute_total(self):
        for r in self:
            total = 0
            for orderline in r.order_line_ids:
                total += orderline.total
            r.total = total + r.shipping_fee
    
    def generate_checkout_session(self):
        for r in self:
            stripe.api_key = r.payment_account_id.secret_api_key
            try:
                line_items = [{
                    'price_data': {
                        'currency': str(r.currency_id.name).lower(),
                        'unit_amount': int(orderline.product_product_id.list_price * 100),
                        'product_data': {
                            'name': orderline.product_template_id.name,
                        },
                    },
                    'quantity': int(orderline.quantity),
                } for orderline in r.order_line_ids]
                # order = [{'id': item['book']['id'], 'quantity':item['quantity']}
                #          for item in request.data['cart']['items']]
                checkout_session = stripe.checkout.Session.create(
                    line_items=line_items,
                    mode='payment',
                    success_url=f'{domain}/payment_with_stripe/success?token={generate_order_token(r.id)}',
                    cancel_url=f'{domain}/payment_with_stripe/cancel?token={generate_order_token(r.id)}',
                    # success_url=f'{domain}/payment_with_stripe/success/?order={generate_order_token(request.data["user"],order)}',
                    # cancel_url=f'{domain}cancel',
                    phone_number_collection={
                        'enabled': True
                    },
                    shipping_address_collection={
                        "allowed_countries": ["VN"]},
                    shipping_options=[
                        {
                            "shipping_rate_data": {
                                "type": "fixed_amount",
                                "fixed_amount": {"amount": int(r.shipping_fee), "currency": str(r.currency_id.name).lower()},
                                "display_name": "Shipping fee",
                                "delivery_estimate": {
                                    "minimum": {"unit": "business_day", "value": 10},
                                    "maximum": {"unit": "business_day", "value": 15},
                                },
                            },
                        },
                    ],
    
                )
                r.payment_url = checkout_session.url
            
            except Exception as e:
                raise ValidationError(e)
            
  
