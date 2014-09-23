#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2014 Rajat Agarwal
import logging; log = logging.getLogger(__name__)

# Try to load JSON libraries in this order:
# ujson -> simplejson -> json
try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

import cStringIO as StringIO
import inspect
import math
import time
import urllib
import sys

# 3rd party libraries that might not be present during initial install
#  but we need to import for the version #
try:
    import requests

    # Monkey patch to requests' json using ujson when available;
    # Otherwise it wouldn't affect anything
    requests.models.json = json
except ImportError:
    pass


# Helpful for debugging what goes in and out
NETWORK_DEBUG = False
if NETWORK_DEBUG:
    # These two lines enable debugging at httplib level (requests->urllib3->httplib)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    import httplib
    httplib.HTTPConnection.debuglevel = 1
    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


API_ENDPOINT = 'http://api.sqoot.com/v2' # Should not be used

# Number of times to retry http requests
NUM_REQUEST_RETRIES = 3

# Max number of sub-requests per multi request
MAX_MULTI_REQUESTS = 5

# Change this if your Python distribution has issues with SSL Cert
VERIFY_SSL = True


# Generic sqoot exception
class SqootException(Exception): pass
# Specific exceptions
# TODO::: Update this list per tests
class InvalidAuth(SqootException): pass
class ParamError(SqootException): pass
class EndpointError(SqootException): pass
class NotAuthorized(SqootException): pass
class RateLimitExceeded(SqootException): pass
class Deprecated(SqootException): pass
class ServerError(SqootException): pass
class FailedGeocode(SqootException): pass
class Other(SqootException): pass

error_types = {
    'invalid_auth': InvalidAuth,
    'param_error': ParamError,
    'endpoint_error': EndpointError,
    'not_authorized': NotAuthorized,
    'rate_limit_exceeded': RateLimitExceeded,
    'deprecated': Deprecated,
    'server_error': ServerError,
    'failed_geocode': FailedGeocode,
    'other': Other,
}

class responseType:
    json, image, html = range(3)

class Sqoot(object):
    """Sqoot API v2 wrapper"""

    def __init__(self, publicApiKey=None, privateApiKey=None):
        """Sets up the api object"""
        # Set up endpoints
        self.base_requester = self.Requester(publicApiKey, privateApiKey)
        # Dynamically enable endpoints
        self._attach_endpoints()

    def _attach_endpoints(self):
        """Dynamically attach endpoint callables to this client"""
        for name, endpoint in inspect.getmembers(self):
            if inspect.isclass(endpoint) and issubclass(endpoint, self._Endpoint) and (endpoint is not self._Endpoint):
                endpoint_instance = endpoint(self.base_requester)
                setattr(self, endpoint_instance.endpoint, endpoint_instance)

    def set_api_key(self, publicApiKey, privateApiKey):
        """Update the access token to use"""
        self.base_requester.set_key(publicApiKey, privateApiKey)

    @property
    def rate_limit(self):
        """Returns the maximum rate limit for the last API call i.e. X-RateLimit-Limit"""
        return self.base_requester.rate_limit

    @property
    def rate_remaining(self):
        """Returns the remaining rate limit for the last API call i.e. X-RateLimit-Remaining"""
        return self.base_requester.rate_remaining


    class Requester(object):
        """Api requesting object"""
        def __init__(self, publicApiKey=None, privateApiKey=None):
            """Sets up the api object"""
            self.set_key(publicApiKey, privateApiKey)
            self.multi_requests = list()
            self.rate_limit = None
            self.rate_remaining = None
            self.isPublicApi = False
            self.responseType = responseType.json

        def set_key(self, publicApiKey, privateApiKey):
            """Set the api_key for this requester"""
            self.publicApiKey = publicApiKey
            self.privateApiKey = privateApiKey

        def GET(self, path, params={}, **kwargs):
            """GET request that returns processed data"""
            params = params.copy()
            # Short-circuit multi requests
            if kwargs.get('multi') is True:
                return self.add_multi_request(path, params)
            # Continue processing normal requests
            headers = self._create_headers()
            params = self._enrich_params(params)
            url = '{API_ENDPOINT}{path}'.format(
                API_ENDPOINT=API_ENDPOINT,
                path=path
            )
            print url
            print params
            result = _get(url, headers=headers, params=params, responseTypeVal=self.responseType)
            #self.rate_limit = result['headers']['X-RateLimit-Limit']
            #self.rate_remaining = result['headers']['X-RateLimit-Remaining']
            #return result['data']['response']
            return result

        def add_multi_request(self, path, params={}):
            """Add multi request to list and return the number of requests added"""
            url = path
            if params:
                # First convert the params into a query string then quote the whole string
                # so it will fit into the multi request query -as a value for the requests= query param-
                url += '?{0}'.format(urllib.quote_plus(urllib.urlencode(params)))
            self.multi_requests.append(url)
            return len(self.multi_requests)

        def _enrich_params(self, params):
            """Enrich the params dict"""
            if self.isPublicApi:
                params['api_key'] = self.publicApiKey
            else:
                params['api_key'] = self.privateApiKey
            return params

        def _create_headers(self):
            """Get the headers we need"""
            headers = {}
            return headers


    class _Endpoint(object):
        """Generic endpoint class"""
        def __init__(self, requester):
            """Stores the request function for retrieving data"""
            self.requester = requester

        def _expanded_path(self, path=None):
            """Gets the expanded path, given this endpoint"""
            return '/{expanded_path}'.format(
                expanded_path='/'.join(p for p in (self.endpoint, path) if p)
            )

        def GET(self, path=None, *args, **kwargs):
            """Use the requester to get the data"""
            return self.requester.GET(self._expanded_path(path), *args, **kwargs)



    class Categories(_Endpoint):
        """Categories specific endpoint"""
        endpoint = 'categories'

        def __call__(self, multi=False):
            """http://docs.sqoot.com/v2/categories.html"""
            self.isPublicApi = True
            return self.GET('', multi=multi)

        def categories(self, multi=False):
            """http://docs.sqoot.com/v2/categories.html"""
            self.isPublicApi = True
            return self.GET('', multi=multi)


    class Clicks(_Endpoint):
        """Clicks specific endpoint"""
        endpoint = 'clicks'

        def __call__(self, params={}, multi=False):
            """http://docs.sqoot.com/v2/clicks.html"""
            self.isPublicApi = False
            return self.GET('', params, multi=multi)

        def clicks(self, params, multi=False):
            """http://docs.sqoot.com/v2/clicks.html"""
            self.isPublicApi = False
            return self.GET('', params, multi=multi)


    class Commissions(_Endpoint):
        """Commissions specific endpoint"""
        endpoint = 'commissions'

        def __call__(self, params, multi=False):
            """http://docs.sqoot.com/v2/commissions.html"""
            self.isPublicApi = False
            return self.GET('', params, multi=multi)

        def commissions(self, params, multi=False):
            """http://docs.sqoot.com/v2/commissions.html"""
            self.isPublicApi = False
            return self.GET('', params, multi=multi)


    class Coupons(_Endpoint):
        """Coupons specific endpoint"""
        endpoint = 'coupons'

        def __call__(self, params={}, multi=False):
            """http://docs.sqoot.com/v2/coupons.html"""
            self.isPublicApi = True
            return self.GET('', params, multi=multi)

        def coupons(self, multi=False):
            """http://docs.sqoot.com/v2/coupons.html"""
            self.isPublicApi = True
            return self.GET('', multi=multi)

        """
        This "coupon" API could also be used to track metadata with the purchase. Pasting snippet below"

        It can be helpful to track additional metadata to a click and subsequently to a purchase.
        Traditionally, this is known as "sub-ID" tracking. We call it metadata. You can use metadata to:

        * Give your users credit for purchasing coupons.
        * Track the performance of different advertising campaigns.
        * Subdivide your analytics by advertiser.
        * Simply pass metadata in as query string parameters on the click URL.

        For example:
        http://api.sqoot.com/v2/coupons/:coupon_id?api_key=:public_key&user_id=123&page=coupons

        We save that data as key-value pairs along with the click and the purchase.

        Later, when you hit our Commissions API, we hand the data back to you.

        Note that keys and values for metadata should be URL-escaped strings and that we don’t include the
        api_key parameter in the metadata.
        """
        def coupon(self, COUPON_ID, params, multi=False):
            """http://docs.sqoot.com/v2/deals.html#find_a_deal"""
            self.isPublicApi = True
            return self.GET('{COUPON_ID}'.format(COUPON_ID=COUPON_ID), params, multi=multi)

        def clickTrack(self, COUPON_ID, multi=False):
            """http://docs.sqoot.com/v2/deals.html#track_a_click"""
            self.isPublicApi = True
            self.requester.responseType = responseType.html
            return self.GET('{COUPON_ID}/click'.format(COUPON_ID=COUPON_ID), multi=multi)

        def image(self, COUPON_ID, params, multi=False):
            """http://docs.sqoot.com/v2/deals.html#track_an_impression"""
            self.isPublicApi = True
            self.requester.responseType = responseType.image
            return self.GET('{COUPON_ID}/image'.format(COUPON_ID=COUPON_ID), params, multi=multi)


    class Deals(_Endpoint):
        """Deals specific endpoint"""
        endpoint = 'deals'

        def __call__(self, params={}, multi=False):
            """http://docs.sqoot.com/v2/deals.html"""
            self.isPublicApi = True
            return self.GET('', params, multi=multi)

        def deals(self, multi=False):
            """http://docs.sqoot.com/v2/deals.html"""
            self.isPublicApi = True
            return self.GET('', multi=multi)

        """
        This "deal" API could also be used to track metadata with the purchase. Pasting snippet below"

        It can be helpful to track additional metadata to a click and subsequently to a purchase.
        Traditionally, this is known as "sub-ID" tracking. We call it metadata. You can use metadata to:

        * Give your users credit for purchasing coupons.
        * Track the performance of different advertising campaigns.
        * Subdivide your analytics by advertiser.
        * Simply pass metadata in as query string parameters on the click URL.

        For example:
        http://api.sqoot.com/v2/deals/:deal_id?api_key=:public_key&user_id=123&page=deals

        We save that data as key-value pairs along with the click and the purchase.

        Later, when you hit our Commissions API, we hand the data back to you.

        Note that keys and values for metadata should be URL-escaped strings and that we don’t include the
        api_key parameter in the metadata.
        """
        def deal(self, DEAL_ID, params, multi=False):
            """http://docs.sqoot.com/v2/deals.html#find_a_deal"""
            self.isPublicApi = True
            return self.GET('{DEAL_ID}'.format(DEAL_ID=DEAL_ID), params, multi=multi)

        def clickTrack(self, DEAL_ID, multi=False):
            """http://docs.sqoot.com/v2/deals.html#track_a_click"""
            self.isPublicApi = True
            self.requester.responseType = responseType.html
            return self.GET('{DEAL_ID}/click'.format(DEAL_ID=DEAL_ID), multi=multi)

        def image(self, DEAL_ID, params, multi=False):
            """http://docs.sqoot.com/v2/deals.html#track_an_impression"""
            self.isPublicApi = True
            self.requester.responseType = responseType.image
            return self.GET('{DEAL_ID}/image'.format(DEAL_ID=DEAL_ID), params, multi=multi)



    class Merchants(_Endpoint):
        """Merchants specific endpoint"""
        endpoint = 'merchants'

        def __call__(self, MERCHANT_ID, params, multi=False):
            """http://docs.sqoot.com/v2/merchants.html"""
            return self.GET('{MERCHANT_ID}'.format(MERCHANT_ID=MERCHANT_ID), params, multi=multi)

        def merchants(self, MERCHANT_ID, params, multi=False):
            """http://docs.sqoot.com/v2/merchants.html"""
            return self.GET('{MERCHANT_ID}'.format(MERCHANT_ID=MERCHANT_ID), params, multi=multi)



    class Providers(_Endpoint):
        """Providers specific endpoint"""
        endpoint = 'providers'

        def __call__(self, multi=False):
            """http://docs.sqoot.com/v2/providers.html"""
            return self.GET('', multi=multi)

        def providers(self, multi=False):
            """http://docs.sqoot.com/v2/providers.html"""
            return self.GET('', multi=multi)


    class Multi(_Endpoint):
        """Multi request endpoint handler"""
        endpoint = 'multi'

        def __len__(self):
          return len(self.requester.multi_requests)

        def __call__(self):
            """
            Generator to process the current queue of multi's

            note: This generator will yield both data and SqootException's
            The code processing this sequence must check the yields for their type.
            The exceptions should be handled by the calling code, or raised.
            """
            while self.requester.multi_requests:
                # Pull n requests from the multi-request queue
                requests = self.requester.multi_requests[:MAX_MULTI_REQUESTS]
                del(self.requester.multi_requests[:MAX_MULTI_REQUESTS])
                # Process the 4sq multi request
                params = {
                    'requests': ','.join(requests),
                }
                responses = self.GET(params=params)['responses']
                # ... and yield out each individual response
                for response in responses:
                    # Make sure the response was valid
                    try:
                        _raise_error_from_response(response)
                        yield response['response']
                    except FoursquareException, e:
                        yield e

        @property
        def num_required_api_calls(self):
            """Returns the expected number of API calls to process"""
            return int(math.ceil(len(self.requester.multi_requests) / float(MAX_MULTI_REQUESTS)))

def _log_and_raise_exception(msg, data, cls=SqootException):
  """Calls log.error() then raises an exception of class cls"""
  data = u'{0}'.format(data)
  # We put data as a argument for log.error() so error tracking systems such
  # as Sentry will properly group errors together by msg only
  log.error(u'{0}: %s'.format(msg), data)
  raise cls(u'{0}: {1}'.format(msg, data))

"""
Network helper functions
"""
#def _request_with_retry(url, headers={}, data=None):
def _get(url, headers={}, params=None, responseTypeVal=responseType.json):
    """Tries to GET data from an endpoint using retries"""
    param_string = _sqoot_urlencode(params)
    for i in xrange(NUM_REQUEST_RETRIES):
        try:
            try:
                response = requests.get(url, headers=headers, params=param_string, verify=VERIFY_SSL)
                return _process_response(response, responseTypeVal)
            except requests.exceptions.RequestException, e:
                _log_and_raise_exception('Error connecting with Sqoot API', e)
        except SqootException, e:
            # Some errors don't bear repeating
            if e.__class__ in [InvalidAuth, ParamError, EndpointError, NotAuthorized, Deprecated]: raise
            # If we've reached our last try, re-raise
            if ((i + 1) == NUM_REQUEST_RETRIES): raise
        time.sleep(1)


def _process_response(response, responseTypeVal):
    """Make the request and handle exception processing"""
    # Read the response as JSON if the expected value is in JSON format
    if responseTypeVal == responseType.json:
        try:
            data = response.json()
        except ValueError:
            _log_and_raise_exception('Invalid response', response.text)
    else:
        # For HTML and image responses, just return the content as data
        data = response.content

    # Default case, Got proper response
    if response.status_code == 200:
        return { 'headers': response.headers, 'data': data }
    else:
        if response.status_code == 404 and responseTypeVal == responseType.html:
            return { 'headers': response.headers, 'data': data }
        else:
            print "Reponse Status Code and headers:"
            print response.status_code, response.headers
            return { 'headers': response.headers, 'data': data }


    if responseTypeVal == responseType.json:
        return _raise_error_from_response(data)

def _raise_error_from_response(data):
    """Processes the response data"""
    # Check the meta-data for why this request failed
    meta = data.get('meta')
    if meta:
        # Account for sqoot conflicts (HTTP reponse status 409)
        if meta.get('code') in (200, 409): return data
        exc = error_types.get(meta.get('errorType'))
        if exc:
            raise exc(meta.get('errorDetail'))
        else:
            _log_and_raise_exception('Unknown error. meta', meta)
    else:
        _log_and_raise_exception('Response format invalid, missing meta property. data', data)

def _as_utf8(s):
    try:
        return str(s)
    except UnicodeEncodeError:
        return unicode(s).encode('utf-8')

def _sqoot_urlencode(query, doseq=0, safe_chars="&/,+"):
    """Gnarly hack because Sqoot doesn't properly handle standard url encoding"""
    # Original doc: http://docs.python.org/2/library/urllib.html#urllib.urlencode
    # Works the same way as urllib.urlencode except two differences -
    # 1. it uses `quote()` instead of `quote_plus()`
    # 2. it takes an extra parameter called `safe_chars` which is a string
    #    having the characters which should not be encoded.
    #
    # Courtesy of github.com/iambibhas
    if hasattr(query,"items"):
        # mapping objects
        query = query.items()
    else:
        # it's a bother at times that strings and string-like objects are
        # sequences...
        try:
            # non-sequence items should not work with len()
            # non-empty strings will fail this
            if len(query) and not isinstance(query[0], tuple):
                raise TypeError
            # zero-length sequences of all types will get here and succeed,
            # but that's a minor nit - since the original implementation
            # allowed empty dicts that type of behavior probably should be
            # preserved for consistency
        except TypeError:
            ty,va,tb = sys.exc_info()
            raise TypeError, "not a valid non-string sequence or mapping object", tb

    l = []
    if not doseq:
        # preserve old behavior
        for k, v in query:
            k = urllib.quote(_as_utf8(k), safe=safe_chars)
            v = urllib.quote(_as_utf8(v), safe=safe_chars)
            l.append(k + '=' + v)
    else:
        for k, v in query:
            k = urllib.quote(_as_utf8(k), safe=safe_chars)
            if isinstance(v, (str, unicode)):
                v = urllib.quote(_as_utf8(v), safe=safe_chars)
                l.append(k + '=' + v)
            else:
                try:
                    # is this a sufficient test for sequence-ness?
                    len(v)
                except TypeError:
                    # not a sequence
                    v = urllib.quote(_as_utf8(v), safe=safe_chars)
                    l.append(k + '=' + v)
                else:
                    # loop over the sequence
                    for elt in v:
                        l.append(k + '=' + urllib.quote(_as_utf8(elt)))
    return '&'.join(l)
