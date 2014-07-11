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
