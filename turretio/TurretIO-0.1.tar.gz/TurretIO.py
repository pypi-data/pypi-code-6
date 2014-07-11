#!/usr/bin/env python

"""
Copyright 2014 Loop Science

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

__author__ = "Tim Henrich"
__copyright__ = "Copyright 2014, Loop Science"
__credits__ = ["Tim Henrich"]
__license__ = "Apache"
__version__ = "0.1"
__maintainer__ = "Tim Henrich"
__email__ = "tim@loopscience.com"
__status__ = "Production"

import base64, hmac, hashlib, time, json
import requests

DOMAIN='https://api.turret.io'

class CredentialsNotProvided(Exception):
    def __init__(self, message):
        super(CredentialsNotProvided, self).__init__(self, message)

class TurretIO(object):
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def get_secret(self):
        return base64.b64decode(self.secret)

    def build_string_to_sign(self, uri, t, data={}):
        if len(data) is not 0:
            return '%s%s%s' % (uri, data, t)

        return '%s%s' % (uri, t)

    def request(self, uri, t, type, data={}):
        headers = {}
        headers['X-LS-Time'] = t
        headers['X-LS-Key'] = self.key
        headers['X-LS-Auth'] = base64.b64encode(hmac.new(self.get_secret(), self.build_string_to_sign(uri, t, data), hashlib.sha512).digest())
        headers['Content-Type'] = 'text/json'

        if type == 'GET':
            return requests.get('%s%s' % (DOMAIN, uri), headers=headers)

        if type == 'POST':
            return requests.post('%s%s' % (DOMAIN, uri), base64.b64encode(data), headers=headers)

    def GET(self, uri):
        t = int(time.time())
        response = self.request(uri, t, 'GET')
        return response

    def POST(self, uri, data):
        t = int(time.time())
        response = self.request(uri, t, 'POST', json.dumps(data))
        return response

class Account(TurretIO):

    URI = '/latest/account'

    def __init__(self, key, secret):
        super(Account, self).__init__(key, secret)

    def get(self):
        return self.GET(self.URI)

    def set(self, outgoing_method, options={}):
        if outgoing_method == 'turret.io':
            return self.POST('%s/me' % self.URI, {'type':outgoing_method})

        if outgoing_method == 'aws':
            if 'aws_access_key' not in options or 'aws_secret_access_key' not in options:
                raise CredentialsNotProvided('AWS Credentials not provided')

            return self.POST('%s/me' % self.URI, {'type':outgoing_method, 'aws':options})

        if outgoing_method == 'smtp':
            if 'smtp_host' not in options \
            or 'smtp_username' not in options \
            or 'smtp_password' not in options:
                raise CredentialsNotProvided('SMTP credentials not provided')

            return self.POST('%s/me' % self.URI, {'type':outgoing_method, 'smtp':options})

        return None

class Target(TurretIO):

    URI = '/latest/target'

    def __init__(self, key, secret):
        super(Target, self).__init__(key, secret)

    def get(self, name):
        return self.GET('%s/%s' % (self.URI, name))

    def create(self, name, attribute_map):
        return self.POST('%s/%s' % (self.URI, name),
                         {'attributes': attribute_map})

    def update(self, name, attribute_map):
        return self.POST('%s/%s' % (self.URI, name),
                         {'attributes': attribute_map})


class TargetEmail(TurretIO):

    URI = '/latest/target'

    def __init__(self, key, secret):
        super(TargetEmail, self).__init__(key, secret)

    def get(self, target_name, email_id):
        return self.GET('%s/%s/email/%s' % (self.URI, target_name, email_id))

    def create(self, target_name, subject, html_body, plain_body):
        return self.POST('%s/%s/email' % (self.URI, target_name),
            {'subject': subject, 'html': html_body, 'plain': plain_body})

    def update(self, target_name, email_id, subject, html_body, plain_body):
        return self.POST('%s/%s/email/%s' % (self.URI, target_name, email_id),
            {'subject': subject, 'html': html_body, 'plain': plain_body})

    def sendTest(self, target_name, email_id, email_from, recipient):
        return self.POST('%s/%s/email/%s/sendTestEmail' % (self.URI, target_name, email_id),
            {'email_from': email_from, 'recipient': recipient})

    def send(self, target_name, email_id, email_from):
        return self.POST('%s/%s/email/%s/sendEmail' % (self.URI, target_name, email_id),
            {'email_from': email_from})


class User(TurretIO):

    URI = '/latest/user'

    def __init__(self, key, secret):
        super(User, self).__init__(key, secret)

    def get(self, email):
        return self.GET('%s/%s' % (self.URI, email))

    def set(self, email, attribute_map, property_map={}):
        if len(property_map) > 0:
            attribute_map['properties'] = property_map

        return self.POST('%s/%s' % (self.URI, email), attribute_map)


if __name__ == '__main__':
    u = User('d034da2187fb493ca18946383d5feaac', 'lfAopUAPHtVOPf8AzcV/WM3Q9RQsYH+BFdP3YP6VeeSXOqaCs/MpKh2Zu7coJVw2ZYg9EgpwXKIlXqZxZ6PQxsoovXtFQEX62HBwEevYEldfJwYOfHc/vQn48cxJABQ5hZ01thKLhFCNQJH/qBEsOT8INLEr8VmFXQAhx8I93V4doyQJ0cO0u1FzanKC7Gas6DAOL9p5RlqHRtHujy9SX1S8JB6ECAcMhCNlUqpFHBtq2DkqJNLHXo+3FtL15uC57juQoa84ALFU3QxOhbK5kQNekdrBKx6u3PnxdA+whrrYwIAWRnXx1024HCqcOu4nxiEcSEB+Yi3xipPdsBDVneYMfjv2/e1go+jCyaIC/QyBVRs9TkXYG4+12p/YrmzfyXNKGs0M2wlPoInibsUUj2ZaG4vLFa+ZucG23yLSLYCXegSA58P+xIRPkNJb1J25+a98XJuDxEEtu7Hy57xXThlH5E0ZsLmUv4HkktgIvEo2F7PQXS0vTu6tCf3au8+L8bjTFh+rQhsETitoMEoJcYsr2Ez3IDiGxaF74xIXdJrulBwvmBxsdRLEE6UKlAPZveb0adjybyN2n0wsnFQpEgX/X8tnNe6C0ijUYYDTWoeKZzMP1lgA2/CyLRY91kna6yn1qx0B1Ky4c/CDx/1ivqJcgL3duECWEMaa6Zfi5Ys=')
    print u.set('tim@loopscience.com', {'contact_name':'tim', 'tester':'1'}).text
    print u.set('tim@tdinternet.com', {'contact_name':'tim', 'tester':'1'}).text
    print u.set('tim@taskscience.com', {'contact_name':'tim', 'tester':'1'}).text
    print u.set('tim@yardy.co', {'contact_name':'tim', 'tester':'1'}).text
