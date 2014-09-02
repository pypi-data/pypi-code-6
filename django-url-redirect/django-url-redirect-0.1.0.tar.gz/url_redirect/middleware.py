import re

from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponsePermanentRedirect
from django.conf import settings


class UrlRedirectMiddleware(object):
    def __init__(self):
        url_redirect_settings = getattr(settings, 'URL_REDIRECTS', None)
        if not url_redirect_settings:
            raise MiddlewareNotUsed
        else:
            self.URL_REDIRECTS = tuple([
                (re.compile(url_pattern), redirect_pattern)
                for url_pattern, redirect_pattern
                in url_redirect_settings
            ])

    def process_request(self, request):
        requested_path = request.get_full_path()
        for url_pattern_regex, redirect_pattern in self.URL_REDIRECTS:
            redirect_url = self._get_redirect_url(url_pattern_regex, redirect_pattern, requested_path)
            if redirect_url:
                return self._redirect(request, redirect_url)

    def _get_redirect_url(self, url_pattern_regex, redirect_pattern, requested_path):
        if url_pattern_regex.match(requested_path):
            if url_pattern_regex.match(requested_path).groups():
                return url_pattern_regex.sub(redirect_pattern, requested_path)
            else:
                return redirect_pattern

    def _redirect(self, request, new_path):
        if request.is_secure():
            protocol = 'https'
        else:
            protocol = 'http'

        newurl = "{}://{}{}".format(
            protocol,
            request.get_host(),
            new_path
        )
        return HttpResponsePermanentRedirect(newurl)
