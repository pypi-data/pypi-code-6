# -*- coding: utf-8 -*-


class ContentModifier(object):
    """WSGI middleware that changes the content on the fly. Is implemented on a
    non-buffering way, and handles the gory details to it for you.

    Usage:
    - overwrite ``response_modifier()`` to transform the chunks from your app
    and pass on.
    - overwrite ``header_modifier()`` to handle header changes,
    like ``Content-Length``, or adding/replacing new headers.

    Examples:

    A WSGI middleware that changes the response to upper, in a non-buffered way:

        class ContentUpper(ContentModifier):
            "MAKES THE VISITOR CRY"
            def response_modifier(self, app_iter):
                for line in app_iter:
                    yield line.upper()

    Note that you need not to call ``app_iter.close()``. It gets called for you.

    This one adds or changes ``X-Powered-By`` header to the response:

        class ProudlyYeller(ContentModifier):
            "Leaks information about your backend"
            def header_modifier(self, status, headers, exc_info=None):
                headers = filter(lambda h: h[0].lower() != 'x-powered-by', headers)
                headers.append(('X-Powered-By', 'AmazingTech/1.0'))
                return status, headers, exc_info

    Now for something barely util, this one adds Google Analytics snippet to the header
    of all pages, right after ``<head>`` tag:

        class GAInjector(ContentModifier):
            "Inject Google Analytics snippet to your pages at <head/>"
            def __init__(self, app, tracking_code):
                self.snippet = '''<script type="text/javascript">
                    var _gaq = _gaq || [];
                    _gaq.push(['_setAccount', 'TRACKING_CODE']);
                    _gaq.push(['_trackPageview']);
                    (function() {
                      var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
                      ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
                      var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
                    })();
                </script>'''.replace('TRACKING_CODE', tracking_code)
                super(GAInjector, self).__init__(app)

            def response_modifier(self, app_iter):
                snippet_injected = False
                for line in app_iter:
                    if not snippet_injected and '<head>' in line.lower():
                        line = line.replace('<head>', '<head>' + self.snippet)
                        snippet_injected = True
                    yield line

            def header_modifier(self, status, headers, exc_info=None):
                # Remove ``content-length``, as the size of the body changed
                headers = filter(lambda h: h[0].lower() != 'content-length', headers)
                return status, headers, exc_info
    """

    ## Intended to be reimplemented by child classes:

    def response_modifier(self, app_iter):
        """Overwrite this to change app_iter chunks on the fly.

        Clients might not bother calling .close() as it is handled by the
        middleware.
        """
        for line in app_iter:
            yield line

    def header_modifier(self, status, headers, exc_info=None):
        """Overwrite on children classes to change headers on the fly

        It SHOULD return status, headers and exc_info, (modified or not)
        """
        ## Usage example:
        # headers.append(('X-Content-Modified', 'Yes'))
        #
        # Question: Should we care about 'Content-Length' as most servers
        # already chop it if response_modifier() is an iterator?

        return status, headers, exc_info

    ## No problem if reimplemented:

    def __init__(self, app):
        self.app = app
        super(ContentModifier, self).__init__()

    ## Not intended to be modified:

    def __call__(self, environ, start_response):
        app_iter = self.app(environ, self._start_response(start_response))
        modified_iter = self.response_modifier(app_iter)

        if hasattr(app_iter, 'close'):
            def closing_iter():
                for line in modified_iter:
                    yield line
                if hasattr(app_iter, 'close'):
                    app_iter.close()

            return closing_iter()
        else:
            return modified_iter

    def _start_response(self, original_start_response):
        def new_start_response(status, headers, exc_info=None):
            status, headers, exc_info = self.header_modifier(status, headers, exc_info)
            original_start_response(status, headers, exc_info)
        return new_start_response
