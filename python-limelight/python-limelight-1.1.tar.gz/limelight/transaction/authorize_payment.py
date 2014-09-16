# -*- coding: utf-8 -*-

from voluptuous import Required, Optional, All, Length

from ..request import TransactionMethod
from ..validation_functions import (email_address, ip_address, country_code,
                                    credit_card_number, accepted_payment_type,
                                    expiration_date, decimal)


class AuthorizePayment(TransactionMethod):
    __name__ = 'authorize_payment'
    schema = {Required('billing_first_name'): All(str, Length(min=1, max=64)),
              Optional('billing_last_name'): All(str, Length(min=1, max=64)),
              Required('billing_address1'): All(str, Length(min=1, max=64)),
              Required('billing_address2'): All(str, Length(min=1, max=64)),
              Required('billing_city'): All(str, Length(max=32)),
              Required('billing_state'): All(str, Length(max=32)),
              Required('billing_zip'): All(int, Length(max=10)),
              Required('billing_country'): All(str, country_code, Length(max=2)),
              Required('phone'): All(int, Length(max=18)),
              Required('email'): All(email_address, Length(max=96)),
              Required('credit_card_type'): All(str, accepted_payment_type),
              Required('credit_card_number'): All(credit_card_number, Length(max=20)),
              Required('expiration_date'): All(expiration_date, Length(4)),
              Required('cvv'): All(str, Length(min=3, max=4)),
              Required('ip_address'): All(ip_address, Length(max=15)),
              Required('product_id'): int,
              Required('campaign_id'): int,
              Optional('auth_amount'): decimal,
              Optional('cascade_enabled'): bool,
              Optional('save_customer'): bool, }