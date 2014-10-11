# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re

from six import string_types

from ..cache import read_url
from .. import decode_html
from ..utils import datetime


def cleanup(key, data, data_type):
    if data:
        if isinstance(data[0], string_types):
            #FIXME: some types need strip_tags
            #data = [strip_tags(decode_html(p)).strip() for p in data]
            data = [decode_html(p).strip() for p in data]
        elif isinstance(data[0], list) or isinstance(data[0], tuple):
            data = [cleanup(key, p, data_type) for p in data]
        while len(data) == 1 and not isinstance(data, string_types):
            data = data[0]
        if data_type == 'list' and isinstance(data, string_types):
            data = [data, ]
    elif data_type != 'list':
        data = ''
    return data

class SiteParser(dict):
    baseUrl = ''
    regex = {}

    def get_url(self, page):
        return "%s%s" % (self.baseUrl, page)

    def read_url(self, url, timeout):
        if not url in self._cache:
            self._cache[url] = read_url(url, timeout=timeout, unicode=True)
        return self._cache[url]

    def __init__(self, timeout=-1):
        self._cache = {}
        for key in self.regex:
            url = self.get_url(self.regex[key]['page'])
            data = self.read_url(url, timeout)
            if isinstance(self.regex[key]['re'], string_types):
                data = re.compile(self.regex[key]['re'], re.DOTALL).findall(data)
                data = cleanup(key, data, self.regex[key]['type'])
            elif callable(self.regex[key]['re']):
                data = self.regex[key]['re'](data)
            else:
                for r in self.regex[key]['re']:
                    if callable(r):
                        f = r
                    else:
                        f = re.compile(r, re.DOTALL).findall
                    if isinstance(data, string_types):
                        data = f(data)
                    else:
                        data = [f(d) for d in data]
                        data = cleanup(key, data, self.regex[key]['type'])
            def apply_f(f, data):
                if data and isinstance(data[0], list):
                    data = [f(d) for d in data]
                else:
                    data = f(data)
                return data
            if self.regex[key]['type'] == 'float' and data:
                data = apply_f(float, data)
            elif self.regex[key]['type'] == 'int' and data:
                data = apply_f(int, data)
            elif self.regex[key]['type'] == 'date':
                parse_date = lambda d: d and datetime.strptime('-'.join(d), '%m-%d-%Y').strftime('%Y-%m-%d')
                data = apply_f(parse_date, data)
            if data:
                self[key] = data

