"""
Urls for porticus
"""
from django.conf import settings
from django.conf.urls.defaults import url, patterns
from django.views.generic import TemplateView

make_url = lambda x,y,z: url(x, TemplateView.as_view(template_name=y), name=z)

page_urls = [make_url(url_entry, template_name, url_name) for url_entry, template_name, url_name in getattr(settings, 'STATICPAGES', [])]

urlpatterns = patterns('', *page_urls)
