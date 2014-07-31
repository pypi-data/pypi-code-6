import os
import json

from unittest import TestCase

from pmp_api.collectiondoc.navigabledoc import NavigableDoc
from pmp_api.core.exceptions import BadQuery


class TestNavigableDoc(TestCase):

    def setUp(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        fixture_dir = os.path.join(current_dir, 'fixtures')
        # Fixture locations
        home_doc = os.path.join(fixture_dir, 'homedoc.json')
        data_doc = os.path.join(fixture_dir, 'test_data.json')
        # Fixture Data
        with open(home_doc, 'r') as hfile:
            home_values = json.loads(hfile.read())
            self.home_doc = NavigableDoc(home_values)
        with open(data_doc, 'r') as dfile:
            data_values = json.loads(dfile.read())
            self.data_doc = NavigableDoc(data_values)

    def test_options_none_results(self):
        calls = [self.home_doc.options('urn:collectiondoc:query'),
                 self.home_doc.options('urn:collectiondoc'),
                 self.home_doc.options('urn:collecti'),
                 self.home_doc.options('urn:collectiondoc:query'),
                 self.home_doc.options('urn:collectiondoc:query:issuetoken')]
        self.assertFalse(any(calls))

    def test_options_one_result(self):
        result1 = self.home_doc.options('urn:collectiondoc:form:issuetoken')
        expected = {
            'href': 'http://127.0.0.1:8080/auth/access_token?json_response=fixtures/authdetails.json',
            'hints': {'docs':
                      'http://docs.pmp.io/wiki/Authentication-Model#token-management',
                      'allow': ['POST']},
            'title': 'Issue OAuth2 Token',
            'rels': ['urn:collectiondoc:form:issuetoken']}
        self.assertEqual(result1, expected)

        expected = {'guid': 'http://docs.pmp.io/wiki/Content-Retrieval',
                    'title': 'Query for documents'}
        result2 = self.home_doc.options('urn:collectiondoc:query:docs')
        self.assertEqual(expected['title'], result2['title'])
        self.assertEqual(expected['guid'], result2['href-vars']['guid'])

    def test_template_real_urn(self):
        result1 = self.data_doc.template('urn:collectiondoc:query:profiles')
        result2 = self.data_doc.template('urn:collectiondoc:query:docs')
        expected1 = 'http://127.0.0.1:8080/profiles{?limit,offset,tag,collection,text,searchsort,has}'
        expected2 = 'http://127.0.0.1:8080/docs{?guid,limit,offset,tag,collection,text,searchsort,has,author,distributor,distributorgroup,startdate,enddate,profile,language}'
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    def test_template_bad_urn(self):
        result1 = self.data_doc.template('urn:collectiondoc:form:issuetoken')
        result2 = self.data_doc.template('urn:collectiondoc:form:mediaupload')
        self.assertEqual(result1, None)
        self.assertEqual(result2, None)

    def test_query_no_params(self):
        expected_base = "http://127.0.0.1:8080/"
        result1 = self.home_doc.query('urn:collectiondoc:query:docs')
        result2 = self.home_doc.query('urn:collectiondoc:query:users')
        self.assertEqual(result1, expected_base + "docs")
        self.assertEqual(result2, expected_base + "users")

    def test_query_bad_results(self):
        result1 = self.home_doc.query('urn:collectiondoc:form:issuetoken')
        result2 = self.home_doc.query('urn:collectiondoc:form:mediaupload')
        self.assertEqual(result1, None)
        self.assertEqual(result2, None)

    def test_query_with_params(self):
        doc_params = {'guid': 'SOMEGUID',
                      'limit': 25,
                      'collection': 'somecollection',
                      'searchsort': True,
                      'language': 'LATIN'}
        prof_params = {'offset': 100,
                       'text': 'yes',
                       'has': 'thirst'}
        dq = 'urn:collectiondoc:query:docs'
        pq = 'urn:collectiondoc:query:profiles'
        expected_docq = 'http://127.0.0.1:8080/docs?guid=SOMEGUID&limit=25&collection=somecollection&searchsort=True&language=LATIN'
        expected_profq = 'http://127.0.0.1:8080/profiles?offset=100&text=yes&has=thirst'
        result1 = self.home_doc.query(dq, params=doc_params)
        result2 = self.data_doc.query(pq, params=prof_params)
        self.assertEqual(result1, expected_docq)
        self.assertEqual(result2, expected_profq)
        

    def test_query_bad_params(self):
        bad_params = {'guid': 'SOMEGUID',
                      'limit': 25,
                      'collection': 'somecollection',
                      'searchsort': True,
                      'language': 'LATIN',
                      'someJUNK': 'junk'}
        dq = 'urn:collectiondoc:query:docs'
        pq = 'urn:collectiondoc:query:profiles'
        with self.assertRaises(BadQuery):
            self.home_doc.query(dq, bad_params)
        with self.assertRaises(BadQuery):
            self.data_doc.query(pq, bad_params)

    def test_query_types(self):
        expected = [('Issue OAuth2 Token', ['urn:collectiondoc:form:issuetoken']),
                    ('Revoke OAuth2 Token', ['urn:collectiondoc:form:revoketoken']),
                    ('Query for users', ['urn:collectiondoc:query:users']),
                    ('Query for groups', ['urn:collectiondoc:query:groups']),
                    ('Access profiles', ['urn:collectiondoc:hreftpl:profiles']),
                    ('Query for profiles', ['urn:collectiondoc:query:profiles']),
                    ('Access schemas', ['urn:collectiondoc:hreftpl:schemas']),
                    ('Query for schemas', ['urn:collectiondoc:query:schemas']),
                    ('Access documents', ['urn:collectiondoc:hreftpl:docs']),
                    ('Query for documents', ['urn:collectiondoc:query:docs']),
                    ('Generate guids', ['urn:collectiondoc:query:guids']),
                    ('Document Save', ['urn:collectiondoc:form:documentsave']),
                    ('Profile Save', ['urn:collectiondoc:form:profilesave']),
                    ('Schema Save', ['urn:collectiondoc:form:schemasave'])]
        doc_types = list(self.home_doc.query_types())
        home_types = list(self.home_doc.query_types())
        self.assertTrue(all(map(lambda x: x in home_types, expected)))
        self.assertTrue(all(map(lambda x: x in doc_types, expected)))

    def test_attributes(self):
        self.assertNotEqual(self.home_doc.attributes, None)
        self.assertNotEqual(self.data_doc.attributes, None)

    def test_items(self):
        self.assertNotEqual(self.data_doc.items, None)
        self.assertEqual(self.home_doc.items, None)

    def test_links(self):
        self.assertNotEqual(self.home_doc.links, None)
        self.assertNotEqual(self.data_doc.links, None)

    def test_querylinks(self):
        self.assertNotEqual(self.home_doc.querylinks, None)
        self.assertNotEqual(self.data_doc.querylinks, None)
