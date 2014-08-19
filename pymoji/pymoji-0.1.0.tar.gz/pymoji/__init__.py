# -*- encoding: utf-8 -*-

import re

from pymoji.utils import Singleton, ensure_unicode
from pymoji.resources.nature import NATURE_MOJI_RESOURCES
from pymoji.resources.objects import OBJECTS_MOJI_RESOURCES
from pymoji.resources.people import PEOPLE_MOJI_RESOURCES
from pymoji.resources.places import PLACES_MOJI_RESOURCES
from pymoji.resources.symbols import SYMBOLS_MOJI_RESOURCES


class PyMoji(object):

    __metaclass__ = Singleton

    def __init__(self):
        self.moji_resources = dict(
            NATURE_MOJI_RESOURCES.items() +
            OBJECTS_MOJI_RESOURCES.items() +
            PEOPLE_MOJI_RESOURCES.items() +
            PLACES_MOJI_RESOURCES.items() +
            SYMBOLS_MOJI_RESOURCES.items()
        )
        self.moji_resources_reversed = {message: code for code, message in self.moji_resources.items()}
        self.encode_r = re.compile(r'(%s)' % '|'.join(self.moji_resources.keys()))
        self.decode_r = re.compile(r'(%s)' % '|'.join([re.escape(message) for message in self.moji_resources_reversed.keys()]))

    def encode(self, text):
        return self.encode_r.sub(lambda m: self.moji_resources[m.group()], ensure_unicode(text))

    def decode(self, text):
        return self.decode_r.sub(lambda m: self.moji_resources_reversed[m.group()], ensure_unicode(text))
