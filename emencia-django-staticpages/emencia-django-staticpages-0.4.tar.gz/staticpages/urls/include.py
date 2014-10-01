"""
Urls for porticus
"""
from django.conf import settings
try:
    from django.conf.urls.defaults import url, patterns
except ImportError:
    from django.conf.urls import url, patterns
from staticpages.views import StaticPageView

make_url = lambda x,y,z: url(x, StaticPageView.as_view(template_name=y), name=z)

page_urls = [make_url(url_entry, template_name, url_name) for url_entry, template_name, url_name in getattr(settings, 'STATICPAGES', [])]

urlpatterns = patterns('', *page_urls)
