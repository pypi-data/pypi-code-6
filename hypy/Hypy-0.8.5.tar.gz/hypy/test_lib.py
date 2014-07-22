"""
Test hypy.lib module
"""

from __future__ import with_statement

import unittest
import os
from contextlib import contextmanager

import hypy

from hypy import (HDocument, HDatabase, HHit, HResults, HCondition, OpenFailed,
        PutFailed, CloseFailed, FlushFailed, EditFailed)

class TestHDocument(unittest.TestCase):
    """
    Test the dictionary and text properties of HDocument
    """
    def setUp(self):
        """
        Create a document
        """
        self.doc = HDocument(uri=u'1')

    def test_dictlike(self):
        """
        HDocument mostly conforms to the dictionary protocol.  Make sure that
        works. 
        """
        doc = self.doc

        # byte strings, other types are not allowed.
        self.assertRaises(TypeError, doc.__setitem__, 'foobar', 'baz')
        self.assertRaises(TypeError, doc.__setitem__, 'foobar', 1)

        doc[u'foobar'] = u'baz'
        doc[u'foobar']
        self.assertEqual(doc[u'foobar'], u'baz')
        self.assertEqual(doc.get(u'foobar', 'default'), u'baz')
        self.assertEqual(doc.get(u'xyz', 'default'), 'default')
        self.assertEqual(doc.get(u'xyz'), None)

        newattrs = {u'new1': u'lala', u'foobar': u'bazz'}
        doc.update(newattrs)
        self.assertEqual(sorted(doc.items()), [(u'@uri', u'1'), (u'foobar', u'bazz'), (u'new1',
            u'lala')])

        doc[u'ninjas'] = u'11'
        self.assertEqual(sorted(doc.keys()), [u'@uri', u'foobar', u'new1', u'ninjas', ])
        self.assertEqual(sorted(doc.values()), [u'1', u'11', u'bazz', u'lala'])

        self.assertRaises(NotImplementedError, doc.__delitem__, u'ninjas')

    def test_text(self):
        """
        Mess with document text
        """
        doc = self.doc
        self.assertRaises(TypeError, doc.addText, 'xyz')
        doc.addText(u'xyz')
        self.assertEqual([u'xyz'], doc.getTexts())
        doc.addText(u'123')
        self.assertEqual([u'xyz', u'123'], doc.getTexts())
        self.assertRaises(TypeError, doc.addHiddenText, 'abc')
        doc.addHiddenText(u'abc')
        self.assertEqual([u'xyz', u'123'], doc.getTexts())

        self.assertEqual(u'xyz\n123', doc.text)

        doc.addText(u'\u062b')

        self.assertEqual('xyz123\xd8\xab', doc.encode('utf-8'))

    def test_unicodeType(self):
        """
        Almost everything in hypy must be unicode
        """
        self.assertRaises(TypeError, HDocument, uri='notunicode')


class TestDatabase(unittest.TestCase):
    """
    Tests HResults, HCondition and HHit.  And since you can't test these
    things without a database, test HDatabase.
    """
    @contextmanager
    def freshenDatabase(self, extras=0):
        """
        Use:
            with self.freshenDatabase() as db:
                ... stuff that should test using these three documents ...
        """
        db = HDatabase()
        db.open('_temp_db', 'w')

        doc = HDocument(uri=u'1')
        doc.addText(u'word this is my document. do you like documents? this one is hi-res.')
        db.putDoc(doc, clean=True)

        doc = HDocument(uri=u'2')
        doc.addText(u'word lorem ipsum dolor sit amet something whatever whatever i do not remember the rest')
        db.putDoc(doc)

        doc = HDocument(uri=u'3')
        doc.addText(u'word four score and 7 years ago our forefathers brought forth upon upon something')
        db.putDoc(doc)

        for x in range(4, extras+4):
            doc = HDocument(uri=unicode(x))
            doc.addText(u'filler filler filler carrot top')
            # set some attributes for attribute operator testing
            doc[u'specialId'] = unicode(x)
            doc[u'description'] = unicode(x) * x
            doc[u'date'] = u'2008-12-%s' % (x,)
            db.putDoc(doc)

        db.flush()

        try:
            yield db
        finally:
            try:
                db.close()
            except CloseFailed:
                """Some of the tests do this close on their own."""

    def test_dbOptimize(self):
        """
        Make sure the various optimize flags do not cause a heart attack.
        """
        with self.freshenDatabase() as db:
            db.optimize(purge=True)
        with self.freshenDatabase() as db:
            db.optimize(opt=True)
        with self.freshenDatabase() as db:
            db.optimize()
            self.assertRaises(NotImplementedError, db.sync)

    def test_removeUpdate(self):
        """
        Test for document id, update, document removal, len() of database.
        """
        docxx = HDocument(uri=u'xx')
        docxx.addText(u'xx')

        # id of a non-stored document
        self.assertEqual(docxx.id, -1)

        # updateAttributes on opened db?
        db = HDatabase()
        self.assertRaises(EditFailed, db.updateAttributes, docxx)

        # removes and updates
        with self.freshenDatabase() as db:
            # flags; just test that these do not nuke us. no idea what they
            # are supposed to do.
            db.putDoc(docxx, clean=True)
            del db[u'xx']
            # delete same doc twice?
            self.assertRaises(EditFailed, db.remove, uri=u'xx')

            db.putDoc(docxx)

            # __len__
            self.assertEqual(len(db), 4)

            # remove by uri, by id, by reference
            db.remove(uri=u'1')
            self.assertEqual(len(db), 3)
            doc2 = db[u'2']
            db.remove(doc2)
            self.assertEqual(len(db), 2)
            doc3id = db[u'3'].id
            db.remove(id=doc3id)
            self.assertEqual(len(db), 1)
            # no arg?
            self.assertRaises(TypeError, db.remove)
            # already removed?
            self.assertRaises(EditFailed, db.remove, id=doc3id)

            self.assertRaises(KeyError, db.__getitem__, '1')

            # fetch a document from the database, edit it, store it, compare
            # it with the original (unfetched) document.  Verify that they are
            # different after the edit. Then verify that the document can be
            # fetched (again) from the database with the edited text.
            dbdocxx = db[u'xx']
            # yes, these are different objects
            self.assertFalse(docxx is dbdocxx)
            self.assertTrue(dbdocxx.get(u'zz') is None)

            dbdocxx[u'zz'] = u'hello'
            db.updateAttributes(dbdocxx)
            dbdocxx2 = db[u'xx']
            # again, different objects
            self.assertFalse(dbdocxx is dbdocxx2)
            self.assertEqual(dbdocxx2.get(u'zz'), u'hello')

    def test_removeURINone(self):
        """
        #356253: should be able to explicitly say "uri=None" when calling remove
        """
        with self.freshenDatabase() as db:
            # this is odd, but it should work
            db.remove(id=1, uri=None)

    def test_removeNulls(self):
        """
        Bug 321579: nulls should not kill addText
        """
        docnulls = HDocument(uri=u'nulls\0')
        docnulls.addText(u'hello there\0 children')
        docnulls.addHiddenText(u'sweet\0sweet love')
        docnulls[u'character\0'] = u'chef\0'
        with self.freshenDatabase() as db:
            db.putDoc(docnulls)
            db.flush()
            cond = HCondition(u'there*')
            self.assertEqual(db.search(cond).pluck(u'@uri'), [u'nulls'])
            cond = HCondition(u'sweet*')
            self.assertEqual(db.search(cond).pluck(u'@uri'), [u'nulls'])

            cond = HCondition()
            cond.addAttr(u'character STREQ chef')
            self.assertEqual(db.search(cond).pluck(u'@uri'), [u'nulls'])

            docnulls[u'voi\0ce'] = u'Isaac Hayes'
            db.updateAttributes(docnulls)

            cond = HCondition()
            cond.addAttr(u'voice STRRX .saac.*')
            self.assertEqual(db.search(cond).pluck(u'@uri'), [u'nulls'])

    def test_putFlags(self):
        """
        Tests for put flags, other put-related corner cases.
        """
        docxx = HDocument(uri=u'xx')
        docxx.addText(u'xx')

        with self.freshenDatabase() as db:
            # flags; just test that these do not nuke us. no idea what they
            # are supposed to do.
            db.putDoc(docxx, clean=True)
            del db[u'xx']
            db.putDoc(docxx, weight=True)
            del db[u'xx']

            ## # put same doc twice?
            ## apparently this works. huh.
            ## db.putDoc(docxx); db.putDoc(docxx)

    def test_condExtras(self):
        """
        Tests for search skip, search options, cond on attributes
        """
        with self.freshenDatabase(extras=10) as db:
            self.assertEqual(len(db), 13)
            # skip and max
            cond4_8 = HCondition(u'filler', max=5)
            cond9_11 = HCondition(u'filler', max=3, skip=5)
            res1 = db.search(cond4_8)
            self.assertEqual(res1.pluck(u'@uri'), list(u'45678'))
            res2 = db.search(cond9_11)
            self.assertEqual(res2.pluck(u'@uri'), [u'9', u'10', u'11'])

            # union matching
            result = db.search(HCondition(u'ipsum score', matching='simple'))
            self.assertEqual(len(result), 0)
            result = db.search(HCondition(u'ipsum score', matching='union'))
            self.assertEqual(len(result), 2)

            # isect matching
            result = db.search(HCondition(u'lorem* ipsum*', matching='simple'))
            self.assertEqual(len(result), 1)
            result = db.search(HCondition(u'lorem* ipsum*', matching='isect'))
            self.assertEqual(len(result), 0)
            result = db.search(HCondition(u'lorem ipsum', matching='isect'))
            self.assertEqual(len(result), 1)

            # rough matching
            result = db.search(HCondition(u'lorem* ipsum*', matching='simple'))
            self.assertEqual(len(result), 1)
            result = db.search(HCondition(u'lorem* ipsum*', matching='rough'))
            self.assertEqual(len(result), 0)
            result = db.search(HCondition(u'lorem ipsum', matching='rough'))
            self.assertEqual(len(result), 1)

            # fewer-than-max hits
            result = db.search(HCondition(u'7*', matching='simple', max=2))
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][u'@uri'], u'3')

            # attribute conditions
            cc = HCondition(u'*.**')
            self.assertRaises(TypeError, cc.addAttr, 'xxx')

            # None as a kwarg should work (bug #356253)
            c2 = HCondition(phrase=None)

            def attrSearch(expr, order=None, phrase=None):
                if phrase:
                    cond = HCondition(phrase)
                else:
                    cond = HCondition()
                cond.addAttr(expr)
                if order:
                    self.assertRaises(TypeError, cond.setOrder, '*.**')
                    cond.setOrder(order)
                return db.search(cond)
            result = attrSearch(u'description STREQ 4444')
            self.assertEqual(result.pluck(u'@uri'), [u'4'])
            result = attrSearch(u'specialId NUMGE 10')
            self.assertEqual(result.pluck(u'@uri'), [u'10', u'11', u'12', u'13'])
            result = attrSearch(u'date NUMGE 2008-12-09')
            self.assertEqual(sorted(map(int, result.pluck(u'@uri'))), [9, 10, 11, 12, 13])
            result = attrSearch(u'description STRRX .{10,14}')
            self.assertEqual(result.pluck(u'@uri'), [u'10', u'11', u'12', u'13'])
            # ordering and !not
            result = attrSearch(u'description !STRRX .{10,14}', u'@uri NUMA')
            self.assertEqual(result.pluck(u'@uri'), list(u'123456789'))
            result = attrSearch(u'description STRRX .{10,14}', u'@uri NUMD')
            self.assertEqual(result.pluck(u'@uri'), [u'13', u'12', u'11', u'10'])

            # one attribute search combined with a text search - regular
            # expression match, all characters
            result = attrSearch(u'description STRRX .{10,14}', u'@uri NUMD', u'*.**')
            self.assertEqual(result.pluck(u'@uri'), [u'13', u'12', u'11', u'10'])

    def test_dbOpenClosed(self):
        """
        Tests for all the db open/close modes
        """
        docyy = HDocument(uri=u'yy')
        docyy.addText(u'yy')
        docxx = HDocument(uri=u'xx')
        docxx.addText(u'xx')
        condxx = HCondition(u'xx')
        condyy = HCondition(u'yy')

        db = HDatabase()
        # open of unreachable directory
        self.assertRaises(OpenFailed, db.open, 'does/not/exist', 'a')
        # close before successful open
        self.assertRaises(CloseFailed, db.close)

        # w mode
        db.open('_temp_db', 'w')
        self.assert_(os.path.exists('_temp_db/_idx'))
        db.putDoc(docyy)
        db.close()

        # r mode
        db.open('_temp_db', 'r')
        # write to read-only db
        self.assertRaises(PutFailed, db.putDoc, docxx)
        self.assertEqual(len(db.search(condyy)), 1)
        db.close()

        # a mode
        db.open('_temp_db', 'a')
        db.putDoc(docxx)
        db.flush()
        self.assertEqual(len(db.search(condxx)), 1)
        self.assertEqual(len(db.search(condyy)), 1)
        db.close()

        # w mode again - check that the db is clobbered
        db.open('_temp_db', 'w')
        self.assertEqual(len(db.search(condxx)), 0)
        db.close()

        # close after successful close
        self.assertRaises(CloseFailed, db.close)
        self.assertRaises(FlushFailed, db.flush)

    def test_queries(self):
        """
        Test various conditions against an index to make sure search works.
        """
        with self.freshenDatabase() as db:
            # plain search, 8-bit str
            result = db.search(HCondition(u'wor*', matching='simple'))
            self.assertEqual(len(result), 3)

            # unicode searches
            result = db.search(HCondition(u'wor*', matching='simple'))
            self.assertEqual(len(result), 3)

            # test simple query with multiple hits
            result = db.search(HCondition(u'res*', matching='simple'))
            self.assertEqual(result.pluck(u'@uri'), [u'1', u'2'])

            # vary query terms to check result scoring
            result = db.search(HCondition(u'someth* | whatever*', matching='simple', max=2))
            self.assertEqual(result.pluck(u'@uri'), [u'2', u'3'])
            result = db.search(HCondition(u'someth* | upon*', matching='simple', max=2))
            self.assertEqual(result.pluck(u'@uri'), [u'3', u'2']) # FIXME

            self.assertEqual(result.hintWords(), [u'someth', u'upon'])

    def test_hits(self):
        """
        Poke at the hits returned by a search and see if document data and
        teaser text come out right.
        """
        with self.freshenDatabase() as db:
            cc = HCondition(u'hi-res')
            for hit in db.search(cc):
                self.assertEqual(str(hit), 
'@digest=17de33c57e358f0fc5d57cd26a08b48e\n@id=1\n@uri=1\n\nword this is my document. do you like documents? this one is hi-res.\n')
                self.assertEqual(hit.teaser([u'document']), u'word this is my <strong>document</strong>. do you li ... ke <strong>document</strong>s? this one is hi-re ... ')
                self.assertEqual(hit.teaser([u'document'], 'rst'), u'word this is my **document**. do you li ... ke **document**s? this one is hi-re ... ')
                self.assertRaises(TypeError, hit.teaser, ['document'])
                self.assertRaises(NotImplementedError, hit.teaser, 
                        [u'document'], 'pdf')

    def test_autoflush(self):
        """
        Verify that autoflush is not on when it's not turned on, and that
        words are autoindexed when it is turned on
        """
        cond = HCondition(u'doc*')

        @contextmanager
        def setup(**kw):
            db1 = HDatabase(**kw)
            db1.open('_temp_db', 'w')

            doc = HDocument(uri=u'1')
            doc.addText(u'word this is my document. do you like documents? this one is hi-res.')
            db1.putDoc(doc, clean=True)

            try:
                yield db1
            finally:
                db1.close()

        # non-autoflush: can't search for doc*
        with setup() as db:
            self.assertEqual(len(db.search(cond)), 0)

        # autoflush: now you can.
        with setup(autoflush=True) as db:
            self.assertEqual(len(db.search(cond)), 1)


class TestMisc(unittest.TestCase):
    """
    Test misc. features of the package such as version string
    """
    def test_version(self):
        """
        __version__ and other release info can be found in copyright.py and
        __init__.py

        This doesn't really verify that copyright.py is generated correctly,
        just that it exists and has the right contents.
        """
        from hypy import __version__ as version1
        from hypy.copyright import __version__ as version2
        self.assertEqual(version1, version2)


if __name__ == '__main__':
    unittest.main()
