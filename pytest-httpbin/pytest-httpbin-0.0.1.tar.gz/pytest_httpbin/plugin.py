from __future__ import absolute_import
import pytest
from httpbin import app as httpbin_app
from . import serve


@pytest.fixture(scope='session')
def httpbin(request):
    server = serve.Server(application=httpbin_app)
    server.start()
    request.addfinalizer(server.stop)
    return server


@pytest.fixture(scope='session')
def httpbin_secure(request):
    server = serve.SecureServer(application=httpbin_app)
    server.start()
    request.addfinalizer(server.stop)
    return server


@pytest.fixture(scope='session', params=['http','https'])
def httpbin_both(request, httpbin, httpbin_secure):
    if request.param == 'http':
        return httpbin
    elif request.param == 'https':
        return httpbin_secure


