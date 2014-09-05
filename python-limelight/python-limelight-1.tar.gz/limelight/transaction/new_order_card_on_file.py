# -*- coding: utf-8 -*-

from voluptuous import Required, Optional, All, Length, Any

from ..request import TransactionMethod


class NewOrderCardOnFile(TransactionMethod):
    __name__ = 'NewOrderCardOnFile'
    schema = {Required('tran_type'): 'Sale',
              Optional('click_id'): All(str, Length(max=255)),
              Required('product_id'): int,
              Required('campaign_id'): int,
              Required('shipping_id'): int,
              Required('upsell_count'): bool,
              Optional('upsell_product_ids'): [int],
              Optional('notes'): All(str, Length(max=512)),
              Optional('preserve_force_gateway'): bool,
              Optional('created_by'): All(str, Length(max=100)),
              Optional('force_subscription_cycle'): bool,
              Optional('recurring_days'): int,
              Optional('subscription_week'): Any(1, 2, 3, 4, 5),
              Optional('subscription_day'): Any(1, 2, 3, 4, 5, 6, 7),
              Optional('master_order_id'): int,
              Optional('promo_code'): All(str, Length(max=100)),
              Optional('temp_customer_id'): All(str, Length(max=32)), }