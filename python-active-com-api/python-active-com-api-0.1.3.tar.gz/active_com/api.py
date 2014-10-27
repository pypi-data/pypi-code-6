import json
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from urllib.request import urlopen


class SearchApiV2(object):

    def __init__(self, api_key):
        self.query_url = \
            'http://api.amp.active.com/v2/search?api_key=%s' % api_key

    def _append_query(self, **request):
        """
        Appends query.

        :param request: HTTP GET request to append
        :rtype: str
        :return: self.query_url with appended HTTP GET keys and vals
        """
        url_parts = list(urlparse(self.query_url))
        query = dict(parse_qsl(url_parts[4]))
        query.update(request)
        url_parts[4] = urlencode(query)

        query = urlunparse(url_parts)
        self.query_url = query.replace('%2C', ',')  # fix commas
        return self.query_url

    def get(self):
        """
        Make query and get data.

        :rtype: dict
        :return: data from API
        """
        response = urlopen(self.query_url)
        encoding = response.headers.get_content_charset()
        data = json.loads(response.read().decode(encoding))
        return data

    def near(self, near):
        """
        Place that can be geocoded. If the near string is not
        geocodable, returns a failed geocoded error.

        Example: San%20Diego,CA,US

        :type near: str
        :param near: Geocodable place name
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(near=near)
        return self

    def lat_lon(self, lat, lon):
        """
        A location specified as a latitude and longitude.

        :type lat: float|int
        :param lat: Latitude. Example: 43.2
        :type lon: float|int
        :param lon: Longitude. Example: -118
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(lat_lon="%s,%s" % (lat, lon))
        return self

    def bbox(self):
        """
        Not Implemented. I'm lazy.
        """
        raise NotImplementedError

    def geo_points(self):
        """
        Not Implemented. I'm lazy.
        """
        raise NotImplementedError

    def radius(self, miles=None, kilometers=None):
        """
        The search radius as specified in miles or kilometers.

        :type miles: int|float
        :param miles: The search radius as specified in miles
        :type kilometers: int|float
        :param kilometers: The search radius as specified in kilometers
        :rtype: SearchApiV2
        :return: self object
        """
        assert miles or kilometers
        assert not(miles and kilometers)

        miles = miles or kilometers * 0.621371

        self._append_query(radius=miles)
        return self

    def city(self, city):
        """
        Matches assets by city name.

        :type city: str
        :param city: city name
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(city=city)
        return self

    def state(self, state):
        """
        Matches assets by state or province code.

        :type state: str
        :param state: state or province code
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(state=state)
        return self

    def zip(self, zip_code):
        """
        Matches assets by zip or postal code.

        :type zip_code: str
        :param zip_code: zip or postal code
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(zip=zip_code)
        return self

    def country(self, country):
        """
        Matches assets by country name.

        :type country: str
        :param country: country name
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(country=country)
        return self

    def query(self, query):
        """
        Search by keywords. The free-form query to search.
        Equivalent to what a user types in the search box.

        :type query: str
        :param query: query string
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(query=query)
        return self

    def current_page(self, current_page):
        """
        The current page of results. Defaults to 1.

        :type current_page: int
        :param current_page: current page number
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(current_page=current_page)
        return self

    def per_page(self, per_page):
        """
        The number of results to return. Defaults to 10.

        :type per_page: int
        :param per_page: number of results to return
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(per_page=per_page)
        return self

    def sort(self, sort):
        """
        The sort order of the results.
        The possible values are date_asc, date_desc, and distance.
        If sort is not specified, results are sort by relevance to the
        query param. Distance can only be used when either the near or
        lat_lon parameters are specified and sorts the results
        according to distance from the specified location smallest to
        largest.

        :type sort: str
        :param sort: sort by (date_asc | date_desc | distance)
        :rtype: SearchApiV2
        :return: self object
        """
        assert sort in ['date_asc', 'date_desc', 'distance']

        self._append_query(sort=sort)
        return self

    def facets(self, facets):
        """
        List containing the facet counts to return. It will bring all
        values for a particular field that show up in your result set.
        In the example below, you will get a break down of all the
        category names present in your search for tinker bell half
        marathon.

        Example:
        query=tinker%20bell%20half%20marathon&facets=categoryName

        :type facets: list|tuple
        :param facets: facet counts to return
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(facets=','.join(facets))
        return self

    def category(self, category):
        """
        Matches assets by category name.

        :type: str
        :param category: category string
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(category=category)
        return self

    def topic(self, topic):
        """
        Matches assets by topic name.

        :type: str
        :param topic: topic string
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(topic=topic)
        return self

    def start_date(self, from_date=None, to_date=None):
        """
        Limits results to assets with a start date in the given range.

        :type from_date: date
        :param from_date: beginning of range
        :type to_date: date
        :param to_date: end of range
        :rtype: SearchApiV2
        :return: self object
        """
        assert from_date or to_date

        from_date_str = from_date.isoformat() if from_date else ''
        to_date_str = to_date.isoformat() if to_date else ''

        range_str = '%s..%s' % (from_date_str, to_date_str)
        self._append_query(start_date=range_str)
        return self

    def end_date(self, from_date=None, to_date=None):
        """
        Limits results to assets with an end date in the given range.

        :type from_date: date
        :param from_date: beginning of range
        :type to_date: date
        :param to_date: end of range
        :rtype: SearchApiV2
        :return: self object
        """
        assert from_date or to_date

        from_date_str = from_date.isoformat() if from_date else ''
        to_date_str = to_date.isoformat() if to_date else ''

        range_str = '%s..%s' % (from_date_str, to_date_str)
        self._append_query(end_date=range_str)
        return self

    def exclude_children(self, exclude_children):
        """
        Removes children assets from the results list. If the parameter
        is not present, all assets will be returned in the results list.

        :type exclude_children: bool
        :param exclude_children: are children should be excluded?
        :rtype: SearchApiV2
        :return: self object
        """
        bool_str = 'true' if exclude_children else 'false'
        self._append_query(exclude_children=bool_str)
        return self

    def exists(self, exists):
        """
        Filters results to assets that have a value for the specified
        field(s).

        :type: list|tuple
        :param exists: fields, which must have values
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(exists=','.join(exists))
        return self

    def not_exists(self, not_exists):
        """
        Filters results to assets that do not have a value for the
        specified field(s)

        :type: list|tuple
        :param not_exists: fields, which must have values
        :rtype: SearchApiV2
        :return: self object
        """
        self._append_query(not_exists=','.join(not_exists))
        return self
