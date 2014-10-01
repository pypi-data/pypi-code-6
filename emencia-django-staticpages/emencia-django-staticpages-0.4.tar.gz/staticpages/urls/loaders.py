"""
URLs loaders
"""
#from django.conf import settings
try:
    from django.conf.urls.defaults import url
except ImportError:
    from django.conf.urls import url
from staticpages.views import StaticPageView

def mount_staticpages(*args):
    """
    Mount pages from the given list
    """
    urls = []
    for url_pattern, template_name, url_name in args:
        urls.append( url(url_pattern, StaticPageView.as_view(template_name=template_name, page_map=args), name=url_name))
        
    return urls
