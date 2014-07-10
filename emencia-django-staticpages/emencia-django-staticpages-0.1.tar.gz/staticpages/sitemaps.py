# -*- coding: utf-8 -*-
"""
Sitemaps for static pages
"""
import os, datetime

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.template.base import TemplateDoesNotExist
from django.template.loader import find_template_loader

class StaticPageEntryBase(object):
    """
    Dummy object to simulate a model entry because static pages does not have models
    """
    url_name = None # You static page MUST have an url name
    priority = None # Optional custom priority
    template_name = None # Optional template name used to generate the page
    pub_date = None # Optional custom datetime
    
    def __init__(self, **kwargs):
        self.url_name = kwargs.get('url_name', None) or self.url_name
        self.priority = kwargs.get('priority', None) or self.priority
        self.template_name = kwargs.get('template_name', None) or self.template_name
        
        # TODO: throw an error/warning if url_name is None because it's a requirement to have an url
    
    def get_pub_date(self):
        return self.pub_date

class StaticPageEntryTemplate(StaticPageEntryBase):
    """
    Inherit of StaticPageEntryBase to use the last modification datetime from the template
    """
    def get_pub_date(self):
        """
        Get the last modification time of the used template, this probably work only 
        with filesystem and apps template loaders
        """
        for item in settings.TEMPLATE_LOADERS:
            current_loader = find_template_loader(item)
            if current_loader.is_usable:
                try:
                    template, origin = current_loader.load_template_source(self.template_name)
                    if origin:
                        #print "Finded template:", origin
                        return datetime.datetime.fromtimestamp(os.path.getmtime(origin))
                except TemplateDoesNotExist:
                    pass
        
        return None

class StaticPageSitemapBase(Sitemap):
    """
    Simple sitemap for static pages
    """
    changefreq = "monthly"
    priority_base = 0.5
    page_entries = []

    def items(self):
        return self.page_entries
    
    def location(self, obj):
        return reverse(obj.url_name)
    
    def priority(self, obj):
        return obj.priority or self.priority_base
    
    def lastmod(self, obj):
        return obj.get_pub_date()
