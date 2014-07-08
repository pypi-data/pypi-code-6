
from django.http import HttpResponse

from rated import settings

class RateLimitBackend(object):

    def source_for_request(self, request):
        '''Return a source identifier for a request'''
        try:
            return request.META['X-Forwarded-For']
        except KeyError:
            pass
        return request.META['REMOTE_ADDR']

    def make_limit_response(self, realm):
        conf = settings.REALMS.get(realm, {})

        return HttpResponse(conf.get('message', settings.RESPONSE_MESSAGE),
            status=conf.get('code', settings.RESPONSE_CODE)
        )

    def check_realm(self, source, realm):
        '''
        Check if `source` has reached their limit in `realm`.

        Returns True if limit is reached.
        '''
        conf = settings.REALMS.get(realm, {})

        # Check against Realm whitelist
        if source in conf.get('whitelist', settings.DEFAULT_WHITELIST):
            return None

        return self.do_check_realm(source, realm, conf)

    def do_check_realm(self, source, realm, conf):
        raise NotImplementedError
