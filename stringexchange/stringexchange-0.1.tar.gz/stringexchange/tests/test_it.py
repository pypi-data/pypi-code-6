# -*- coding:utf-8 -*-
def _makeRequest(config, path="/"):
    from pyramid.request import Request
    from pyramid.interfaces import IRequestExtensions

    request = Request.blank(path)
    extensions = config.registry.getUtility(IRequestExtensions)
    request.registry = config.registry
    request._set_extensions(extensions)
    return request


def _makeRouter(config):
    from pyramid.router import Router
    router = Router(config.registry)
    return router


def test_reify_it():
    from pyramid.testing import testConfig

    with testConfig() as config:
        config.include("stringexchange")

        # request time
        request = _makeRequest(config, path="/")
        assert request.string_exchange == request.string_exchange


def test_it():
    from pyramid.testing import testConfig

    with testConfig() as config:
        config.include("stringexchange")
        config.add_route("hello", "/")

        def hello_view(context, request):
            from pyramid.response import Response
            js = request.string_exchange.publisher("js")
            response = Response("""
            <html><head>{}</head><body></body></html>
            """.format(request.string_exchange.subscribe("js")))

            js.publish('<script src="my.js></script>"')
            assert "my.js" not in response.text
            return response

        config.add_view(hello_view, route_name="hello")

        # request time
        router = _makeRouter(config)

        request = _makeRequest(config, path="/")
        response = router.handle_request(request)

        assert "my.js" in response.text
