import io
import os
import string
import random

from orm.api import Api


def login(self):
    self.api = Api(os.environ['CONFINE_SERVER_API'])
    self.api.username = os.environ['CONFINE_USER']
    self.api.password = os.environ['CONFINE_PASSWORD']
    self.api.login()


def random_ascii(length):
    return ''.join([random.choice(string.hexdigits) for i in range(0, length)])

def fake_file(name):
    fake_file = io.StringIO()
    content = unicode(random_ascii(100))
    fake_file.name = name
    fake_file.write(content)
    fake_file.seek(0)
    return fake_file, content
