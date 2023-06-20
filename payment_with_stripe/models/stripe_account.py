

from odoo import fields, models, api


class StripeAccount(models.Model):
    _name = 'payment_with_stripe.account'
    
    secret_api_key = fields.Char(string='Stripe key api', require=True)
    order_ids = fields.One2many('payment_with_stripe.order', 'payment_account_id')                              
    
    _sql_constraints = [
        ('check_name_unique',
         'UNIQUE(name)',
         'Name account must be unique'),
        
        ('check_secret_key_unique',
         'UNIQUE(secret_api_key)',
         'Secret key must be unique'),
        
        ('check_secret_key_not_null',
         'CHECK (secret_api_key IS NOT NULL)',
         'Secret key must not be empty'),
        ]

    def _set_default_name(self):
        return f'KEY #{self.search_count([])+1}'

    name = fields.Char(string='Key name', default=_set_default_name)

    
