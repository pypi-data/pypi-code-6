# -*- coding: utf-8 -*-
"""CLI for Server Density.
"""

import os
import json
import math
import datetime
import requests
import urlparse


URL_SD = 'https://api.serverdensity.io'
PATH_TOKEN = '~/.sd_token'


def parse_response(response):
    try:
        data = json.loads(response.text)
    except ValueError:
        data = {}

    if response.status_code == 200:
        return data
    else:
        print "Error:"
        print "  %s" % data['message']


def sd_post(path, payload):
    response = requests.post(
        urlparse.urljoin(URL_SD, path),
        headers={
            "content-type": "application/json"
        },
        data=json.dumps(payload)
    )
    return parse_response(response)


def sd_get(path, payload):
    response = requests.get(
        urlparse.urljoin(URL_SD, path),
        params=payload
    )
    return parse_response(response)


def save_token(token):
    try:
        file(os.path.expanduser(PATH_TOKEN), 'w').write(token)
    except IOError:
        print "Unable to save token to %s" % PATH_TOKEN


def get_token():
    try:
        return file(os.path.expanduser(PATH_TOKEN)).read().strip()
    except IOError:
        print "You need an authentication token. " \
              "Run 'sd auth' first"


def auth_user(account, user, password):
    payload = {
        "username": user,
        "password": password,
        "accountName": account,
        "tokenName": 'SD Command line interface',
    }
    data = sd_post('tokens', payload)
    if data:
        print "Authenticated."
        token = data['token_data']['token']
        save_token(token)


def auth_token(token):
    payload = {
        "token": token,
        "fields": json.dumps(['name'])
    }
    data = sd_get('inventory/devices', payload)

    if data:
        print "Token verified."
        save_token(token)


def device_list():
    token = get_token()
    if not token:
        return

    payload = {
        "token": token,
        "fields": json.dumps(['name', 'hostname'])
    }
    data = sd_get('inventory/devices', payload)

    if data:
        for i in data:
            print '%s (%s)' % (i['name'], i['hostname'])


def device_get(subject_id):
    token = get_token()
    if not token:
        return

    payload = {
        "token": token
    }
    data = sd_get('inventory/devices/' + subject_id, payload)

    if data:
        return data['name']


def device_search(name):
    token = get_token()
    if not token:
        return

    payload = {
        "token": token,
        "filter": json.dumps({"name": name, "type": "device"})
    }
    data = sd_get('inventory/resources', payload)

    if data and len(data):
        return data[0]['_id']


def service_list():
    token = get_token()
    if not token:
        return

    payload = {
        "token": token,
        "fields": json.dumps(['name', 'checkUrl', 'currentStatus'])
    }
    data = sd_get('inventory/services', payload)

    if data:
        for i in data:
            print '%s (%s) %s' % (i['name'], i['checkUrl'], i['currentStatus'])


def service_get(subject_id):
    token = get_token()
    if not token:
        return

    payload = {
        "token": token
    }
    data = sd_get('inventory/services/' + subject_id, payload)

    if data:
        return "%s (%s)" % (data['name'], data['checkUrl'])


def alerts_list():
    token = get_token()
    if not token:
        return

    payload = {
        "token": token,
        "closed": 'false'
    }
    data = sd_get('alerts/triggered', payload)

    if not data:
        print "No alerts. Yay!"
        return

    for i in data:
        field = i['config']['fullField']
        if i['config']['subjectType'] == 'device':
            device = device_get(i['config']['subjectId'])
            print "Device: %s - %s" % (device, field)
        elif i['config']['subjectType'] == 'service':
            service = service_get(i['config']['subjectId'])
            print "Service: %s - %s" % (service, field)


def get_bar(value, high=100.0):
    if value == 0:
        return ' '

    bars = ['▁', '▂', '▃', '▅', '▆', '▇']

    x = value * len(bars) / high
    x = int(math.ceil(x))
    x = min(x, len(bars))

    return bars[x - 1]


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def parse_cpu_metrics(data):
    for i in data:
        if i['name'] == 'ALL':
            for j in i['tree']:
                name = j['name']
                values = [x['y'] for x in j['data']]
                if name in ['System', 'User']:
                    print "  %s" % name
                    print "  %s" % ''.join([get_bar(x) for x in values])


def parse_memory_metrics(data):
    for i in data:
        name = i['name']
        values = [x['y'] for x in i['data']]
        if name in ['Physical used', 'Cached used']:
            high = max(values)
            size = sizeof_fmt(high * 1024 * 1024)
            print "  %s (%s max)" % (name, size)
            print "  %s" % ''.join([get_bar(x, high) for x in values])


def parse_network_metrics(data):
    for i in data:
        iface = i['name']
        for j in i['tree']:
            name = j['name']
            values = [x['y'] for x in j['data']]
            if any(values) and 'MB' in name:
                high = max(values)
                size = sizeof_fmt(high * 1024 * 1024)
                print "  %s %s (%s max)" % (iface, name, size)
                print "  %s" % ''.join([get_bar(x) for x in values])


def parse_metrics(data):
    for i in data:
        name = i['name']
        key = i['key']
        values = i['tree']

        if key == 'cpuStats':
            print name
            parse_cpu_metrics(values)
            print
        elif key == 'networkTraffic':
            print name
            parse_network_metrics(values)
            print
        elif key == 'memory':
            print name
            parse_memory_metrics(values)
            print


def get_metrics(name):
    token = get_token()
    if not token:
        return

    subject_id = device_search(name)
    if not subject_id:
        print "No such device name."
        return

    start = datetime.datetime.now().utcnow() - datetime.timedelta(seconds=3600)
    end = datetime.datetime.now().utcnow()

    payload = {
        "token": token,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "filter": json.dumps({'cpuStats': 'all',
                              'memory': 'all',
                              'networkTraffic': 'all'})
    }
    data = sd_get('metrics/graphs/' + subject_id, payload)
    if data:
        parse_metrics(data)
