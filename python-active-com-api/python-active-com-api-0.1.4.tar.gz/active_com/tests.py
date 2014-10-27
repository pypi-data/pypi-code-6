from datetime import date
from unittest import TestCase
from urllib.parse import urlparse

from active_com.api import SearchApiV2


class SearchApiV2Tests(TestCase):

    def setUp(self):
        self.search_api = SearchApiV2('abc')
        self.base_query = 'http://api.amp.active.com/v2/search?api_key=abc'

    def assertQueriesEqual(self, query1, query2):
        parsed_query1 = list(urlparse(query1))
        parsed_query2 = list(urlparse(query2))

        self.assertListEqual(
            sorted(parsed_query1[4].split('&')),
            sorted(parsed_query2[4].split('&')))

        # check uri without GET values
        self.assertListEqual(parsed_query1[:4], parsed_query2[:4])

        # check GET values
        self.assertListEqual(
            sorted(parsed_query1[4].split('&')),
            sorted(parsed_query2[4].split('&')))

    def test_append_query_returns_query(self):
        query = self.search_api._append_query(key='val', key2='val 2')
        expected_query = self.base_query + '&key=val&key2=val+2'

        self.assertQueriesEqual(query, expected_query)

    def test_near(self):
        query = self.search_api.near('dupa').query_url
        expected_query = self.base_query + '&near=dupa'

        self.assertQueriesEqual(query, expected_query)

    def test_lan_lot(self):
        query = self.search_api.lat_lon(52.2464391, 21.0334827).query_url
        expected_query = self.base_query + '&lat_lon=52.2464391,21.0334827'

        self.assertQueriesEqual(query, expected_query)

    def test_radius(self):
        query = self.search_api.radius(kilometers=123).query_url
        expected_query = self.base_query + '&radius=76.428633'
        self.assertQueriesEqual(query, expected_query)

        query = self.search_api.radius(miles=123).query_url
        expected_query = self.base_query + '&radius=123'
        self.assertQueriesEqual(query, expected_query)

    def test_city(self):
        query = self.search_api.city('dupa').query_url
        expected_query = self.base_query + '&city=dupa'
        self.assertQueriesEqual(query, expected_query)

    def test_state(self):
        query = self.search_api.state('CA').query_url
        expected_query = self.base_query + '&state=CA'
        self.assertQueriesEqual(query, expected_query)

    def test_zip(self):
        query = self.search_api.zip('12345').query_url
        expected_query = self.base_query + '&zip=12345'
        self.assertQueriesEqual(query, expected_query)

    def test_country(self):
        query = self.search_api.country('12345').query_url
        expected_query = self.base_query + '&country=12345'
        self.assertQueriesEqual(query, expected_query)

    def test_query_string(self):
        query = self.search_api.query('marathon').query_url
        expected_query = self.base_query + '&query=marathon'
        self.assertQueriesEqual(query, expected_query)

    def test_current_page(self):
        query = self.search_api.current_page(3).query_url
        expected_query = self.base_query + '&current_page=3'
        self.assertQueriesEqual(query, expected_query)

    def test_per_page(self):
        query = self.search_api.per_page(30).query_url
        expected_query = self.base_query + '&per_page=30'
        self.assertQueriesEqual(query, expected_query)

    def test_sort(self):
        query = self.search_api.sort('distance').query_url
        expected_query = self.base_query + '&sort=distance'
        self.assertQueriesEqual(query, expected_query)

    def test_facets(self):
        query = self.search_api.facets(
            ['countryName', 'categoryName']).query_url
        expected_query = self.base_query + '&facets=countryName,categoryName'
        self.assertQueriesEqual(query, expected_query)

    def test_category(self):
        query = self.search_api.category('Person').query_url
        expected_query = self.base_query + '&category=Person'
        self.assertQueriesEqual(query, expected_query)

    def test_topic(self):
        query = self.search_api.topic('Running').query_url
        expected_query = self.base_query + '&topic=Running'
        self.assertQueriesEqual(query, expected_query)

    def test_start_date(self):
        d1 = date(2014, 1, 2)
        d2 = date(2014, 3, 4)

        query = self.search_api.start_date(from_date=d1, to_date=d2).query_url
        expected_query = self.base_query + '&start_date=2014-01-02..2014-03-04'
        self.assertQueriesEqual(query, expected_query)

        query = self.search_api.start_date(from_date=d1).query_url
        expected_query = self.base_query + '&start_date=2014-01-02..'
        self.assertQueriesEqual(query, expected_query)

        query = self.search_api.start_date(to_date=d2).query_url
        expected_query = self.base_query + '&start_date=..2014-03-04'
        self.assertQueriesEqual(query, expected_query)

    def test_end_date(self):
        d1 = date(2014, 1, 2)
        d2 = date(2014, 3, 4)

        query = self.search_api.end_date(from_date=d1, to_date=d2).query_url
        expected_query = self.base_query + '&end_date=2014-01-02..2014-03-04'
        self.assertQueriesEqual(query, expected_query)

        query = self.search_api.end_date(from_date=d1).query_url
        expected_query = self.base_query + '&end_date=2014-01-02..'
        self.assertQueriesEqual(query, expected_query)

        query = self.search_api.end_date(to_date=d2).query_url
        expected_query = self.base_query + '&end_date=..2014-03-04'
        self.assertQueriesEqual(query, expected_query)

    def test_exclude_children(self):
        query = self.search_api.exclude_children(True).query_url
        expected_query = self.base_query + '&exclude_children=true'
        self.assertQueriesEqual(query, expected_query)

        query = self.search_api.exclude_children(False).query_url
        expected_query = self.base_query + '&exclude_children=false'
        self.assertQueriesEqual(query, expected_query)

    def test_exists(self):
        query = self.search_api.exists(['countryName', 'authorName']).query_url
        expected_query = self.base_query + '&exists=countryName,authorName'
        self.assertQueriesEqual(query, expected_query)

        query = self.search_api.exists(['asset.authorName']).query_url
        expected_query = self.base_query + '&exists=asset.authorName'
        self.assertQueriesEqual(query, expected_query)

    def test_not_exists(self):
        query = self.search_api.not_exists(
            ['countryName', 'authorName']).query_url
        expected_query = self.base_query + '&not_exists=countryName,authorName'
        self.assertQueriesEqual(query, expected_query)

        query = self.search_api.not_exists(['asset.authorName']).query_url
        expected_query = self.base_query + '&not_exists=asset.authorName'
        self.assertQueriesEqual(query, expected_query)

    def test_chaining_filters(self):
        query = self.search_api.country('Canada').city('Radom').query_url
        expected_query = self.base_query + '&country=Canada&city=Radom'
        self.assertQueriesEqual(query, expected_query)

    def test_chaining_filters_with_nones(self):
        query = self.search_api.country('Canada').city(None).query_url
        expected_query = self.base_query + '&country=Canada'
        self.assertQueriesEqual(query, expected_query)
