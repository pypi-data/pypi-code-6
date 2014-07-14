# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import base64
import json
import time

import requests


ENDPOINT = 'http://logstash.openstack.org/api'


def _GET(path):
    r = requests.get(ENDPOINT + path)

    if r.status_code != requests.codes.ok:
        print('Got HTTP %s, retrying...' % r.status_code)
        # retry once
        r = requests.get(ENDPOINT + path)

    try:
        return r.json()
    except Exception:
        raise SystemExit(r.text)


def _encode(q):
    """Encode a JSON dict for inclusion in a URL."""
    return base64.b64encode(json.dumps(q))


def _unix_time_in_microseconds():
    return int(time.time() * 1000)


def query(q, days):
    search = {
        'search': q,
        'fields': [],
        'offset': 0,
        'timeframe': str(days * 86400),
        'graphmode': 'count',
        'time': {
            'user_interval': 0},
        'stamp': _unix_time_in_microseconds()}
    return _GET('/search/%s' % _encode(search))
