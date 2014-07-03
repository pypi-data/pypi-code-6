# coding: utf-8
'''
File: corpus.py
Author: Oliver Zscheyge
Description:
    Confopy corpus superclass.
'''

from nltk.corpus.reader.api import CorpusReader
from localizable import Localizable
from confopy.model import Document

NO_WORDS = [
      u"."
    , u","
    , u";"
    , u":"
    , u"+"
    , u"/"
    , u"!"
    , u"?"
    , u"("
    , u")"
    , u"["
    , u"]"
    , u"{"
    , u"}"
    , u"-"
    , u"//"
    , u"%"
    , u"\u2013"
    , u"\uf0f1"
]

class Corpus(Localizable, CorpusReader, Document):
    def __init__(self, ID, language, brief=u"", description=u""):
        self.ID = ID
        self.language = language
        self.brief = brief
        self.description = description

    def tagger(self):
        return None

    def parser(self):
        return None

    def sent_tokenizer(self):
        return None

    def fillers(self):
        return list()

