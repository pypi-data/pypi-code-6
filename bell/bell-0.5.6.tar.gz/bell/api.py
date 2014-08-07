# coding=utf8

import time

import ssdb

from bell.configs import configs

ssdb_host = configs['ssdb']['host']
ssdb_port = configs['ssdb']['port']
ssdb_client = ssdb.SSDBClient(host=ssdb_host, port=ssdb_port)
all_series = configs['ssdb']['allSeries']['hashmap']
series_name_prefix = configs['ssdb']['series']['zsets']['namePrefix']


class SeriesNotFound(Exception):
    pass


def format(keys):
    lst = []
    for key in keys:
        val, stat, _time = key.split(':')
        lst.append((int(_time), float(val), int(stat)))
    return lst


def require_series_exist(func):
    def _func(series, *args, **kwargs):
        if not ssdb_client.hexists(all_series, series):
            raise SeriesNotFound
        return func(series, *args, **kwargs)
    return _func


@require_series_exist
def around(series, timestamp=None, offset=10):
    if timestamp is None:
        timestamp = int(time.time())

    keys = ssdb_client.zkeys(series_name_prefix + series, '',
                             timestamp - offset,
                             timestamp + offset, -1)
    return format(keys)


@require_series_exist
def latest(series):
    lst = ssdb_client.zrrange(series_name_prefix + series, 0, 1)
    keys = lst[-2::-2]
    if keys:
        return format(keys)[0]


@require_series_exist
def now(series):
    timestamp = int(time.time())
    keys = ssdb_client.zkeys(series_name_prefix + series, '',
                             timestamp, timestamp, -1)
    if keys:
        return format(keys)[0]
