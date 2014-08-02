"""Mirador API client

.. moduleauthor:: Nick Jacob <nick@mirador.im>

"""
from __future__ import absolute_import

import base64
import requests
import logging
from functools import wraps
from .errors import http_exceptions, MiradorException
from .result import MiradorResult, MiradorResultList


def classification_method(name=None):
    """decorator that provides a consistent interface"""

    def classification_wrap(fn):

        @wraps(fn)
        def classification_wrapper(self, *args, **mapped_items):
            """Accepts arguments to classify in 3 forms:
                items<dict> - mapped items as dict
                items<list> - unmapped (int-keys)
                **mapped_items - mapped items
            """

            # items will always end up as a dict
            items = MiradorClient._classification_input(
                fn, args, mapped_items
            )

            # get the payload, using the provided fn
            payloads = self._prepare_payload(fn, items, name)

            if not payloads:
                self._log.error(
                    "invalid request: {}".format(items)
                )
                raise MiradorException(
                    "invalid request data: {}".format(items)
                )

            output = MiradorResultList()
            for load in payloads:
                output.concat(self._request(load))
            return output

        return classification_wrapper
    return classification_wrap


class MiradorClient(object):
    """Interface for the Mirador API

    Simple interface for retrieving results from the
    Mirador API. Returns [MiradorResult] on all method
    """

    API_BASE = "http://api.mirador.im"
    CLASSIFY_ENDPOINT = "/v1/classify"
    HEADERS = {
        'User-Agent': 'MiradorClient/1.0 Python'
    }

    # 30 seconds; long but w/e
    TIMEOUT = 30.0
    MAX_LEN = 2

    def __init__(self, api_key, timeout=10):
        """Instaniate a MiradorClient
        Args:
            api_key: the mirador api key (string)
            timeout: timeout for API access (default: 10 seconds)

        Returns:
            A MiradorClient instance
        """
        self._log = logging.getLogger(__name__)
        self._api_key = api_key

        self._log.info(
            "instantiating MiradorClient with key: {}"
            .format(self._api_key)
        )

    def _request(self, payload):
        """Send a request to the API and parse output"""

        # put the api_key into the request
        payload['api_key'] = self._api_key

        try:

            self._log.info(
                "making content moderation request"
            )

            self._log.debug(
                "mirador api request: {}".format(payload)
            )

            r = requests.post(
                self.API_BASE + self.CLASSIFY_ENDPOINT,
                data=payload,
                headers=self.HEADERS,
                timeout=self.TIMEOUT,
            )

            if r.status_code != 200:

                self._log.error(
                    "error from mirador server: {}, {}"
                    .format(r.text, r)
                )

                raise http_exceptions[200](r.text)

            result = r.json()

            if not result or 'results' not in result:

                self._log.error(
                    "bad output form API: {}"
                    .format(r.text)
                )

                raise http_exceptions[500](
                    (result.get('errors', 'Error')
                     if result else 'Unexpected Error')
                )

            # parse the results
            self._log.info("parsing response from Mirador API")
            return self._parse_response(result['results'])

        except Exception as e:
            self._log.error(
                "unexpected error in Mirador API: {}"
                .format(e)
            )
            raise http_exceptions[500]("{}".format(e))

    def _parse_response(self, output):
        return MiradorResult.parse_results(output)

    #
    # image processing helper functions
    #

    def _read_image(self, image):
        """read an image if it's a file and return the name"""

        if isinstance(image, basestring):
            with open(image, 'rb') as imf:
                return image, imf.read()
        else:
            return image.name, image.read()

    def _prepare_image(self, im_f):
        """convert an image name or file into base64 encoded string"""

        name, data = self._read_image(im_f)

        if not data:
            raise http_exceptions[400]("no image data for: {}".format(name))

        return base64.b64encode(data)

    def _param_key(self, name, idx):
        base_key = "{name}[{idx}]".format(**locals())
        return base_key + '[id]', base_key + '[data]'

    #
    # public interface for classifying files, urls, etc
    #

    @staticmethod
    def _classification_input(fn, args, mapped_items):
        """take different input possibilities and return a dict"""

        if args:

            if isinstance(args[0], dict):
                return args[0]
            elif isinstance(args[0], (list, tuple)):
                return dict(
                    [(idx, el) for idx, el in enumerate(args[0])]
                )
            elif isinstance(args[0], basestring) or hasattr(args[0], 'read'):

                # may be either a filename or a file-object
                items = {}
                for ex in args:

                    if isinstance(ex, basestring):
                        items[ex] = ex
                    elif hasattr(ex, 'read') and hasattr(ex, 'name'):
                        items[ex.name] = ex
                    else:
                        raise MiradorException(
                            "{} execpts dict, list, string, or fh: {} provided"
                            .format(fn.__name__, type(ex))
                        )
                return items
            else:
                raise MiradorException(
                    "{} takes only dict, fh, list, or string(s); {} provided"
                    .format(fn.__name__, type(args[0]))
                )

        elif mapped_items:
            return mapped_items

        else:
            raise MiradorException(
                "bad input to {}: {}"
                .format(fn.__name__, mapped_items)
            )

    def _prepare_payload(self, fn, items, name):

        idx = 0

        payloads = []
        curr = {}

        for id, data in items.items():

            if ((idx + 1) % self.MAX_LEN) == 0 and len(curr) > 1:
                payloads.append(curr)
                curr = {}
                idx = 0

            pk, pvk = self._param_key(name, idx)

            curr[pk] = id
            curr[pvk] = fn(self, data)

            idx += 1

        # finish; append last one
        if len(curr) > 1:
            payloads.append(curr)

        return payloads

    #
    # public @classification_method methods
    #

    @classification_method(name='image')
    def classify_files(self, file):
        return self._prepare_image(file)

    @classification_method(name='url')
    def classify_urls(self, url):
        return url

    @classification_method(name='image')
    def classify_buffers(self, image_buffer):
        return base64.b64encode(image_buffer).replace("\n", '')

    @classification_method(name='image')
    def classify_raw(self, image_buffer):
        return base64.b64encode(image_buffer).replace("\n", '')
