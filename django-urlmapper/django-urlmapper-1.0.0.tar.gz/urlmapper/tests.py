from django.conf.urls import include, url
from django.test import TestCase

from .utils import get_urls


def view(request, **kwargs):
    pass


extra = [
    url("^world/$", view),
]

nested = [
    url(r"^(?P<slug>\w+)/", include([
        url(r"^$", view),
        url(r"^history/$", view),
        url(r"^edit/$", view),
    ])),
]

urlpatterns = [
    url("^$", view),
    url("^product/(?P<slug>[^/]+)/$", view, name="product-detail"),
    url("^about/$", view, name="about"),
    url("^hello/", include(extra)),
    url("^page/", include(nested)),
]


class GetUrlsTest(TestCase):

    def test_get(self):
        urls = get_urls(urlpatterns)

        self.assertEqual(urls[0]["path"], "/")
        self.assertEqual(urls[0]["name"], "")
        self.assertEqual(urls[0]["view"], "urlmapper.tests.view")

        self.assertEqual(urls[1]["path"], "/product/<slug>/")
        self.assertEqual(urls[1]["name"], "product-detail")

        self.assertEqual(urls[2]["path"], "/about/")
        self.assertEqual(urls[2]["name"], "about")

        self.assertEqual(urls[3]["path"], "/hello/world/")
        self.assertEqual(urls[4]["path"], "/page/<slug>/")
        self.assertEqual(urls[5]["path"], "/page/<slug>/history/")
        self.assertEqual(urls[6]["path"], "/page/<slug>/edit/")

    def test_sort(self):
        urls = get_urls(urlpatterns, sort=True)

        self.assertEqual(urls[0]["path"], "/")
        self.assertEqual(urls[1]["path"], "/about/")
        self.assertEqual(urls[2]["path"], "/hello/world/")
