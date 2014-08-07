# coding=utf8

"""This module provides a hook function `send_to_hipchat`, it sends message
to a hipchat room once an anomalous datapoint was detected. To enable it,
set `hooks.enable` to `true`, and add `bell.hooks.hipchat` to `hooks.modules`
::
    [hooks]
    enable = true
    modules = ["bell.hooks.hipchat"]

then add the following section to `configs.toml`::

    [hooks.hipchat]
    roomId = 12345
    token = "your-hipchat-api-token"
    weburl = "http://bell.example.com"

pip requirements:
    * requests
"""


import requests
from datetime import datetime
from bell.configs import configs
from bell.events import on_anomaly_detected


room_id = configs['hooks']['hipchat']['roomId']
token = configs['hooks']['hipchat']['token']
weburl = configs['hooks']['hipchat']['weburl']


api_url = ('http://api.hipchat.com/v1/rooms/message?'
           'format=json&auth_token=%s') % token

pattern = ('{series}: <a href="{web}/{series}/around/{timestamp}">'
           '{datetime}</a>, {value}')


@on_anomaly_detected
def send_to_hipchat(datapoint):
    series, (timestamp, value) = datapoint
    datetime_obj = datetime.fromtimestamp(timestamp)
    datetime_str = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    message = pattern.format(web=weburl, series=series, value=value,
                             datetime=datetime_str, timestamp=timestamp)
    data = {'room_id': room_id, 'from': 'Bell', 'message': message}
    return requests.post(api_url, data=data)
