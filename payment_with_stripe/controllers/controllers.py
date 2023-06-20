from odoo import http
from werkzeug.utils import redirect
import jwt
from odoo.exceptions import ValidationError 


class PaymentWithStripe(http.Controller):

    @http.route('/payment_with_stripe/success/', auth='public')
    def success(self, **kw):
        token = http.request.params.get('token')
        if not token:
            raise ValidationError('Missing token')
        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except:
            raise ValidationError('Invalid token')
        print(payload['order'])
        order = http.request.env['payment_with_stripe.order'].browse([int(payload['order'])])
        
        order.status = 'su'
        return '<h1 style="color: green; text-align: center; margin-top: 100px;">success<h1>'
        
    @http.route('/payment_with_stripe/cancel/', auth='public')
    def cancel(self, **kw):
        token = http.request.params.get('token')
        if not token:
            raise ValidationError('Missing token')
        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except:
            raise ValidationError('Invalid token')
        print(payload['order'])
        order = http.request.env['payment_with_stripe.order'].browse([int(payload['order'])])
        
        order.status = 'ca'
        return '<h1 style="color: orange; text-align: center; margin-top: 100px;">cancel<h1>'
        
