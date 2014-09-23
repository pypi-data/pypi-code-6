#!/usr/bin/env python
#-*- coding:utf-8 -*-

from json2xls import Json2Xls

url_or_json = '''[
    {"name": "John", "age": 30, "sex": "male"},
    {"name": "Alice", "age": 18, "sex": "female"}
]'''
Json2Xls('test.xls', url_or_json)
params = {
    'location': u'上海',
    'output': 'json',
    'ak': '5slgyqGDENN7Sy7pw29IUvrZ'
}
Json2Xls('test2.xls', "http://api.map.baidu.com/telematics/v3/weather", params=params)
