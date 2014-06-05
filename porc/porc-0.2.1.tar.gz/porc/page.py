from .resource import Resource
from collections import Iterator
from requests_futures.sessions import FuturesSession


class Page(Iterator, Resource):

    """
    Class used for paging through search results.

    Can be used as an iterator, ex: `for page in Page`,
    or by using the methods `next` and `prev` explicitly
    to page through results.

    Used in searching collections and events.
    """

    def __init__(self, uri, querydict={}, **kwargs):
        opts = dict(kwargs, params=querydict)
        # if async, create a callback that stores current page state after each request
        if 'session' in kwargs and type(kwargs['session']) == FuturesSession:
            opts['background_callback'] = self._handle_res
        super(Page, self).__init__(uri, **opts)
        self._url_root = self.uri[:self.uri.find('/v0')]
        self.response = None

    def _handle_res(self, session, response):
        """
        Stores the response, which we use for determining
        next and prev pages.
        """
        self.response = response

    def reset(self):
        """
        Clear the page's current place.

            page_1 = page.next().result()
            page_2 = page.next().result()
            page.reset()
            page_x = page.next().result()
            assert page_x.url == page_1.url
        """
        self.response = None

    def _handle_page(self, querydict={}, val='next', **headers):
        """
        Executes the request getting the next (or previous) page,
        incrementing (or decrementing) the current page.
        """
        # if async, wait for previous page to load
        if hasattr(self.response, 'result'):
            self.response.result()
        # update uri based on next page
        if self.response:
            self.response.raise_for_status()
            _next = self.response.json().get(val, False)
            if _next:
                self.uri = self._url_root + _next
            else:
                raise StopIteration
        # execute request
        response = self.get(querydict, **headers)
        self._handle_res(None, response)
        return response

    def next(self, querydict={}, **headers):
        """
        Gets the next page of results.
        Raises `StopIteration` when there are no more results.
        """
        return self._handle_page(querydict, **headers)

    def __next__(self):
        return self.next()

    def prev(self, querydict={}, **headers):
        """
        Gets the previous page of results.
        Raises `StopIteration` when there are no more results.

        Note: Only collection searches provide a `prev` value.
        For all others, `prev` will always return `StopIteration`.
        """
        return self._handle_page(querydict, 'prev', **headers)        
