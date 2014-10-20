# -*- coding: utf-8 -*-
import os
import random
import string
from codecs import open


class TestTask(object):

    def __init__(self, root_dir):
        self.id = "".join([random.choice(string.ascii_letters) for __ in range(15)])
        self.root_dir = root_dir

    def __call__(self, key):
        with open(os.path.join(self.root_dir, self.id), 'w', encoding='utf-8') as f:
            f.write(key)

    def validate(self, key):
        try:
            with open(os.path.join(self.root_dir, self.id), 'r', encoding='utf-8') as f:
                read_key = f.read()
                if key != read_key:
                    raise AssertionError("Invalid key")
        except IOError:
            raise AssertionError("No such file")
