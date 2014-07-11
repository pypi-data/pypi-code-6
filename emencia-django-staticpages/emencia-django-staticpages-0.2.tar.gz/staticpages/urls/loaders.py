"""
URLs loaders
"""
#from django.conf import settings
from django.conf.urls.defaults import url
from django.views.generic import TemplateView

def mount_staticpages(*args):
    """
    Mount pages from the given list
    """
    urls = []
    for url_pattern, template_name, url_name in args:
        urls.append( url(url_pattern, TemplateView.as_view(template_name=template_name), name=url_name))
        
    return urls
