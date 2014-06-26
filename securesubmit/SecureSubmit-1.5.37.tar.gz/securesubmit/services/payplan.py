"""
    payplan.py

    This module represents the pay plan service.

    :copyright: (c) Heartland Payment Systems. All rights reserved.
"""

import requests
import json
from securesubmit.entities.payplan import HpsPayPlanCustomer


class HpsPayPlanService(object):
    _service_config = None
    _headers = None

    def __init__(self, config):
        self._service_config = config

        self._headers = {'content-type': 'json/application',
                         'SiteID': str(self._service_config.site_id),
                         'LicenseID': str(self._service_config.license_id),
                         'DeviceID': str(self.service_config.device_id),
                         'Password': self.service_config.password,
                         'UserName': self.service_config.username}


class HpsPayPlanCustomerService(HpsPayPlanService):
    pass

    def read(self, customer_key):
        response = requests.get('Customer/' + customer_key,
                                headers=self._headers)

        return HpsPayPlanCustomer.from_dto(response)

    def create(self, options):
        data = json.encode(options)
        response = requests.post('Customer',
                                 data=data,
                                 headers=self._headers)

        return HpsPayPlanCustomer.from_dto(response)

    def update(self, options):
        data = json.encoder(options)
        response = requests.put('Customer',
                                data=data,
                                headers=self._headers)

        return HpsPayPlanCustomer.from_dto(response)

    def delete(self, customer_key):
        requests.delete('Customer/' + customer_key,
                        headers=self._headers)