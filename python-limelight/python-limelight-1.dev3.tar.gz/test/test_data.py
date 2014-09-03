# -*- coding: utf-8 -*-

import re
import datetime

from copy import copy
from random import randrange

from unittest import TestCase

A_YEAR_FROM_NOW = datetime.datetime.today() + datetime.timedelta(days=randrange(365, 365 * 3))

test_user = dict(
    first_name="Ignacio",
    last_name="Vergara",
    phone_number="9566397841",
    email_address="joselaverga%d@hotmail.com" % randrange(0, 3000, 3),
)

test_partial = dict(
    pk=1,
    first_name=test_user['first_name'],
    last_name=test_user['last_name'],
    phone_number=test_user['phone_number'],
    email_address=test_user['email_address']
)

test_credit_card = dict(
    type="Visa",
    number=4444585412324564,
    expires_0=re.sub('0', '', A_YEAR_FROM_NOW.strftime('%m')),
    expires_1=A_YEAR_FROM_NOW.strftime('%Y'),
    ccv=randrange(0, 999),
    first_name=test_user['first_name'],
    last_name=test_user['last_name']
)

test_credit_card_decline = dict(
    type=test_credit_card['type'],
    number=4447895462215544,
    expires_0=test_credit_card['expires_0'],
    expires_1=test_credit_card['expires_1'],
    ccv=test_credit_card['ccv'],
    first_name=test_credit_card['first_name'],
    last_name=test_credit_card['last_name']
)

test_address = dict(
    pk=1,
    first_name=test_user['first_name'],
    last_name=test_user['last_name'],
    street="74 Tudela St.",
    city="Brownsville",
    state="TX",
    postal_code="78526",
    country="US"
)

test_order = dict(**test_user)
test_order.update(test_address)
test_order.update(test_credit_card)
test_order.pop('pk', None)


class TestData(TestCase):
    def test_data_is_valid(self):
        """Validate test data"""
        for datum in copy(locals()).values():
            if isinstance(datum, dict):
                self.assertTrue(all(v for v in datum.values()))