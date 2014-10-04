# Copyright 2014 VEXXHOST, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import requests

import manage2


class License(object):

    def __init__(self, id, info):
        # List licenses prepend license ID with "L", remove that.
        self.id = id.replace('L', '')
        self._info = info

    def expire(self, reason=None):
        r = requests.get('%s/XMLlicenseExpire.cgi' % manage2.API_ENDPOINT,
                         params={'liscid': self.id, 'reason': reason},
                         auth=manage2.auth)
        return r.status_code == 200

    def __getattr__(self, name):
        if name in self._info:
            return self._info[name]
        raise AttributeError

    def __repr__(self):
        return '<manage2.License object at %s> JSON: %s' % (self.id, str(self))

    def __str__(self):
        return json.dumps(self._info, sort_keys=True, indent=2)

    @classmethod
    def all(cls, only_expired=False):
        params = {'output': 'json'}
        if only_expired:
            params['expired'] = True

        r = requests.get('%s/XMLlicenseInfo.cgi' % manage2.API_ENDPOINT,
                         params=params, auth=manage2.auth).json()

        if r['status'] != 1:
            raise RuntimeError(r['reason'])
        return [License(id, info) for id, info in r['licenses'].iteritems()]

    @classmethod
    def retrieve(cls, ip_address):
        r = requests.get('%s/XMLRawlookup.cgi' % manage2.API_ENDPOINT,
                         params={'ip': ip_address, 'output': 'json'},
                         auth=manage2.auth).json()

        if r['status'] != '1':
            raise RuntimeError(r['reason'])
        return License(r['licenseid'], r)

    @classmethod
    def activate(cls, ip_address, package_id, group_id):
        r = requests.get('%s/XMLlicenseAdd.cgi' % manage2.API_ENDPOINT,
                         params={'ip': ip_address, 'packageid': package_id,
                                 'groupid': group_id, 'output': 'json'},
                         auth=manage2.auth).json()

        if r['status'] != 1:
            raise RuntimeError(r['reason'])
        return cls.retrieve(ip_address)
