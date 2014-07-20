# http://stackoverflow.com/questions/1875052/using-paired-certificates-with-urllib2

# We need to login to vCenter server as an extension and this means that
# vCenter needs to be able to see our certificate.
# If we just connect to the vCenter server HTTPS
# reverse proxy at https://<vcenter>/sdk, the certificate is not forwarded to
# the vCenter server endpoint. We will get an HTTPS connection to the reverse
# proxy, but the connection from the reverse proxy to vCenter will be HTTP.
#
# To handle this we need to tunnel all our traffic through the proxy server
# when talking to vCenter.

import urllib2
import suds.client

from logging import getLogger
logger = getLogger(__name__)


try:
    from gevent import sleep
except ImportError:
    from time import sleep


def retry_on_exception(func, seconds_between_retries=1, max_retries=None, exception_predicate=None):
    """ Retries the call if an exception occurrs.
    seconds_between_retries indicates the number of seconds to sleep after the operation fails, before the next retry.
    max_retries specifies the number of times to retry the execution, not including the first call.
    i.e. if max_retries is 1, then the command will be called once, and retried once more. If the command still fails
    after max_retries, the last exception will be raised. If max_retries is None, the command will be retried
    indefinitely.
    exception_predicate is a function that is called with the raised exception, to test the exception if only
    specific exceptions are valid for retry. If the function returns True, the command will be retried, otherwise the
    exception will be raised without a retry. If exception_predicate is None, the command will be retried for all
    exceptions. """
    from infi.pyutils.decorators import wraps

    @wraps(func)
    def retry(*args, **kwargs):
        from time import sleep
        retries = 0
        while True:
            try:
                return func(*args, **kwargs)
            except Exception, error:
                if exception_predicate is not None and not exception_predicate(error):
                    raise
                retries += 1
                if max_retries is not None and retries > max_retries:
                    raise
                logger.warn("function {!r} failed with {!r}, retrying".format(func, error))
                sleep(seconds_between_retries)
    return retry


def retry_on_URLError(func):
    from urllib2 import URLError
    # INFINILAB-82: sometimes FC commands fail on the switch, retry works
    def predicate(error):
        return isinstance(error, URLError)
    # we retry twice, with 2 seconds in between. The predicate filters only the relevant exceptions
    return retry_on_exception(func, 1, 30, predicate)


class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
    def __init__(self, key, cert):
        urllib2.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert

    def https_open(self, req):
        # Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=300):
        from httplib import HTTPSConnection
        return HTTPSConnection(host, key_file=self.key, cert_file=self.cert)


class HttpAuthenticated(suds.client.HttpAuthenticated):
    def __init__(self, certfile=None, keyfile=None, proxy=None, **kwargs):
        suds.client.HttpAuthenticated.__init__(self, **kwargs)
        self._certfile = certfile
        self._keyfile = keyfile
        self._proxy = proxy

    def u2handlers(self):
        handlers = suds.client.HttpAuthenticated.u2handlers(self)
        if self._certfile and self._keyfile:
            handlers.append(urllib2.ProxyHandler({'https':self._proxy}))
            handlers.append(HTTPSClientAuthHandler(self._keyfile,
                                                   self._certfile))
        return handlers
