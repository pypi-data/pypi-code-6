# -*- coding: utf-8 -*-

import os
import json
import codecs

class ConfigReader(object):
    def __init__(self, path = None):
        self.path = os.path.abspath(path) if path is not None else None;

        if os.path.exists(path):
            x = codecs.open(path, encoding='utf-8')
            self.data = json.load(x)
            x.close()
        else:
            self.data = {}

    def put(self, k, v=None):
        self.data[k] = v

    def get(self, k, v=None):
        return self.data.get(k, v)

    def delete(self, k):
        if k in self.data:
            del self.data[k]

    def update(self, dict):
        if dict is not None:
            self.data.update(dict)

    def save(self):
        if not os.path.exists(os.path.dirname(self.path)):
            dir_path = os.path.dirname(self.path)
            os.makedirs(dir_path)

        x = codecs.open(self.path, 'w+', encoding='utf-8')
        json.dump(self.data, x)
        x.close()
