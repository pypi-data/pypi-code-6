# -*- coding: utf-8 -*-

from voluptuous import Required, Optional, Any, All, Length

from ..request import TransactionMethod
from ..validation_functions import ip_address, country_code, email_address


class NewProspect(TransactionMethod):
    __name__ = 'NewProspect'
    schema = {Optional('first_name'): All(str, Length(max=64)),
              Optional('last_name'): All(str, Length(max=64)),
              Optional('address1'): All(str, Length(max=64)),
              Optional('address2'): All(str, Length(max=64)),
              Optional('city'): All(str, Length(max=32)),
              Optional('state'): All(str, Length(max=32)),
              Optional('zip'): All(Any(str, int), Length(max=10)),
              Optional('country'): All(str, country_code, Length(2)),
              Optional('phone'): All(str, Length(max=18)),
              Required('email'): All(str, email_address, Length(max=96)),
              Required('ip_address'): All(str, ip_address, Length(max=15)),
              Optional('AFID'): All(str, Length(max=255)),
              Optional('SID'): All(str, Length(max=255)),
              Optional('AFFID'): All(str, Length(max=255)),
              Optional('C1'): All(str, Length(max=255)),
              Optional('C2'): All(str, Length(max=255)),
              Optional('C3'): All(str, Length(max=255)),
              Optional('AID'): All(str, Length(max=255)),
              Optional('OPT'): All(str, Length(max=255)),
              Optional('click_id'): All(str, Length(max=255)),
              Required('campaign_id'): int,
              Optional('notes'): All(str, Length(max=512)), }