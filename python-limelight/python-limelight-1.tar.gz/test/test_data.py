# -*- coding: utf-8 -*-

import datetime

from copy import copy
from random import randrange, choice

from unittest import TestCase

A_YEAR_FROM_NOW = datetime.datetime.today() + datetime.timedelta(days=randrange(365, 365 * 3))

test_user = dict(
    first_name="Ignacio",
    last_name="Vergara",
    phone="9566397841",
    email="joselaverga%d@hotmail.com" % randrange(0, 3000, 3),
)

test_partial = dict(
    pk=1,
    first_name=test_user['first_name'],
    last_name=test_user['last_name'],
    phone=test_user['phone'],
    email=test_user['email']
)

test_credit_card = dict(
    credit_card_type="visa",
    credit_card_number='4444585412324564',
    expiration_date=A_YEAR_FROM_NOW,
    cvv=randrange(100, 9999),
    billing_first_name=test_user['first_name'],
    billing_last_name=test_user['last_name']
)

test_credit_card_decline = dict(
    credit_card_type=test_credit_card['credit_card_type'],
    credit_card_number='4447895462215544',
    expiration_date=A_YEAR_FROM_NOW,
    cvv=test_credit_card['cvv'],
    billing_first_name=test_credit_card['billing_first_name'],
    billing_last_name=test_credit_card['billing_last_name']
)

test_address = dict(
    pk=1,
    shipping_address1="74 Tudela St.",
    shipping_city="Brownsville",
    shipping_state="TX",
    shipping_zip="78526",
    shipping_country="US"
)

test_order = dict(**test_user)
test_order.update(test_address)
test_order.update(test_credit_card)
test_order.pop('pk', None)
test_order['billing_same_as_shipping'] = True
test_order['shipping_id'] = 1
test_order['upsell_count'] = False
test_order['product_id'] = 43
test_order['campaign_id'] = 29
test_order['ip_address'] = choice(['127.0.0.1', '::1'])


class TestData(TestCase):
    def test_data_is_valid(self):
        """Validate test data"""
        for datum in copy(locals()).values():
            if isinstance(datum, dict):
                self.assertTrue(all(v for v in datum.values()))