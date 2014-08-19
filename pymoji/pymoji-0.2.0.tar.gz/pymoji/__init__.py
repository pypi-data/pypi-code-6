# -*- encoding: utf-8 -*-

import re

from pymoji.utils import Singleton, ensure_unicode, get_package_version
from pymoji.resources import load_soft_bank_resources, load_moji_resources

__all__ = ['PyMoji']
__version__ = get_package_version()


class PyMoji(object):

    __metaclass__ = Singleton

    def __init__(self):
        self.moji_resources = load_moji_resources()
        self.soft_bank_resources = load_soft_bank_resources()
        self.soft_bank_r = re.compile(r'(%s)' % '|'.join(self.soft_bank_resources.keys()))
        self.encode_r = re.compile(r'(%s)' % '|'.join(self.moji_resources.keys()))
        self.moji_resources_reversed = {message: code for code, message in self.moji_resources.items()}
        self.encode_r = re.compile(r'(%s)' % '|'.join(self.moji_resources.keys()))
        self.decode_r = re.compile(r'(%s)' % '|'.join([re.escape(message) for message in self.moji_resources_reversed.keys()]))

    def encode(self, text):
        text = self.soft_bank_r.sub(lambda m: self.soft_bank_resources[m.group()], ensure_unicode(text))
        return self.encode_r.sub(lambda m: self.moji_resources[m.group()], text)

    def decode(self, text):
        return self.decode_r.sub(lambda m: self.moji_resources_reversed[m.group()], ensure_unicode(text))
