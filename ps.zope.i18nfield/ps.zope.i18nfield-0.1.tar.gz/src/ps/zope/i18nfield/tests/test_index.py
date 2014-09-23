# -*- coding: utf-8 -*-
"""Integration tests for the I18NFieldIndex."""

# python imports
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# zope imports
from zope.component import provideUtility
from zope.interface import implementer

# local imports
from ps.zope.i18nfield import index, interfaces, storage


@implementer(interfaces.ILanguageAvailability)
class LanguageAvailability(object):

    def getDefaultLanguage(self, combined=False):
        return u'en'

    def getAvailableLanguages(self, combined=False):
        return [u'de', u'en', u'es', u'fr', u'pt']

    def getLanguages(self, combined=False):
        pass

    def getLanguageListing(self, combined=False):
        pass


class TestI18NFieldIndex(unittest.TestCase):
    """Test case for the I18NFieldIndex."""

    def setUp(self):
        super(TestI18NFieldIndex, self).setUp()
        provideUtility(LanguageAvailability())

    def test_do_index(self):
        """Test that the I18NDict values are indexed properly."""
        idx = index.I18NFieldIndex()
        data = storage.I18NDict({u'en': u'English', u'de': u'Deutsch'})
        idx.doIndex(111, data)
        self.assertEqual(len(idx._indices), 2)

        # English
        sub_idx = idx._indices[u'en']
        self.assertEqual(sub_idx.documentCount(), 1)
        self.assertEqual(sub_idx.wordCount(), 1)

        data2 = storage.I18NDict({
            u'en': u'English with more words',
            u'es': u'Español con más palabras',
            u'de': u'Deutsch'
        })
        idx.doIndex(222, data2)
        self.assertEqual(len(idx._indices), 3)

        # English
        sub_idx = idx._indices[u'en']
        self.assertEqual(sub_idx.documentCount(), 2)
        self.assertEqual(sub_idx.wordCount(), 2)
        self.assertIn(u'English', list(sub_idx._rev_index.values()))
        self.assertIn(
            u'English with more words',
            list(sub_idx._rev_index.values()),
        )
        # Spanish
        sub_idx = idx._indices[u'es']
        self.assertEqual(sub_idx.documentCount(), 1)
        self.assertEqual(sub_idx.wordCount(), 1)
        self.assertIn(
            u'Español con más palabras',
            list(sub_idx._rev_index.values()),
        )
        # German
        sub_idx = idx._indices[u'de']
        self.assertEqual(sub_idx.documentCount(), 2)
        self.assertEqual(sub_idx.wordCount(), 1)
        self.assertIn(u'Deutsch', list(sub_idx._rev_index.values()))

    def test_do_index_required(self):
        """Test that the I18NDict values are indexed properly."""
        idx = index.I18NFieldIndex()
        data = storage.I18NDict({u'en': u'English', u'de': u'Deutsch'})
        data.required = True
        idx.doIndex(111, data)
        self.assertEqual(len(idx._indices), 5)

        # English
        sub_idx = idx._indices[u'en']
        self.assertEqual(sub_idx.documentCount(), 1)
        self.assertEqual(sub_idx.wordCount(), 1)
        self.assertIn(u'English', list(sub_idx._rev_index.values()))
        # Portuguese
        sub_idx = idx._indices[u'pt']
        self.assertEqual(sub_idx.documentCount(), 1)
        self.assertEqual(sub_idx.wordCount(), 1)
        self.assertIn(u'English', list(sub_idx._rev_index.values()))

        data2 = storage.I18NDict({
            u'en': u'English with more words',
            u'es': u'Español con más palabras',
            u'de': u'Deutsch'
        })
        data2.required = True
        idx.doIndex(222, data2)
        self.assertEqual(len(idx._indices), 5)

        # English
        sub_idx = idx._indices[u'en']
        self.assertEqual(sub_idx.documentCount(), 2)
        self.assertEqual(sub_idx.wordCount(), 2)
        self.assertIn(u'English', list(sub_idx._rev_index.values()))
        self.assertIn(
            u'English with more words',
            list(sub_idx._rev_index.values()),
        )
        # Spanish
        sub_idx = idx._indices[u'es']
        self.assertEqual(sub_idx.documentCount(), 2)
        self.assertEqual(sub_idx.wordCount(), 2)
        self.assertIn(u'English', list(sub_idx._rev_index.values()))
        self.assertIn(
            u'Español con más palabras',
            list(sub_idx._rev_index.values()),
        )
        # German
        sub_idx = idx._indices[u'de']
        self.assertEqual(sub_idx.documentCount(), 2)
        self.assertEqual(sub_idx.wordCount(), 1)
        self.assertIn(u'Deutsch', list(sub_idx._rev_index.values()))
        # Portuguese
        sub_idx = idx._indices[u'pt']
        self.assertEqual(sub_idx.documentCount(), 2)
        self.assertEqual(sub_idx.wordCount(), 2)
        self.assertIn(u'English', list(sub_idx._rev_index.values()))
        self.assertIn(
            u'English with more words',
            list(sub_idx._rev_index.values()),
        )

    def test_do_unindex(self):
        """Test that the I18NDict values are indexed properly."""
        idx = index.I18NFieldIndex()
        data = storage.I18NDict({u'en': u'English', u'de': u'Deutsch'})
        idx.doIndex(111, data)
        self.assertEqual(len(idx._indices), 2)

        data2 = storage.I18NDict({
            u'en': u'English with more words',
            u'es': u'Español con más palabras',
            u'de': u'Deutschland'
        })
        idx.doIndex(222, data2)
        self.assertEqual(len(idx._indices), 3)

        idx.doUnIndex(222)
        self.assertEqual(len(idx._indices), 3)

        # English
        sub_idx = idx._indices[u'en']
        self.assertEqual(sub_idx.documentCount(), 1)
        self.assertEqual(sub_idx.wordCount(), 1)
        self.assertIn(u'English', list(sub_idx._rev_index.values()))
        # Spanish
        sub_idx = idx._indices[u'es']
        self.assertEqual(sub_idx.documentCount(), 0)
        self.assertEqual(sub_idx.wordCount(), 0)
        # English
        sub_idx = idx._indices[u'de']
        self.assertEqual(sub_idx.documentCount(), 1)
        self.assertEqual(sub_idx.wordCount(), 1)
        self.assertIn(u'Deutsch', list(sub_idx._rev_index.values()))

        # clear all indices
        idx.clear()
        self.assertEqual(len(idx._indices), 0)
