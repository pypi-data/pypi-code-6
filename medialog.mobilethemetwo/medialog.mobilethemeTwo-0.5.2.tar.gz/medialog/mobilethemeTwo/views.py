# -*- coding: utf-8 -*-

#import logging
from Acquisition import aq_inner
from zope.i18nmessageid import MessageFactory
from Products.Five import BrowserView

from plone import api
from medialog.mobilethemeTwo.interfaces import IMobilethemeTwoSettings

import lxml.html
import urllib 
from lxml.cssselect import CSSSelector
from lxml.html.clean import Cleaner

import requests

class Scrape(BrowserView):
    """   A View that uses lxml to embed external content    """
    
    def scraped(self):
        #get settings from control panel
        scrape_base_url = api.portal.get_registry_record('medialog.mobilethemeTwo.interfaces.IMobilethemeTwoSettings.scrape_base_url')
        scrape_javascript = api.portal.get_registry_record('medialog.mobilethemeTwo.interfaces.IMobilethemeTwoSettings.scrape_javascript')
        scrape_style = api.portal.get_registry_record('medialog.mobilethemeTwo.interfaces.IMobilethemeTwoSettings.scrape_style')
        
        #get settings from scrape_view if it was redirected
        selector = api.portal.get_registry_record('medialog.mobilethemeTwo.interfaces.IMobilethemeTwoSettings.scrape_selector')
        url = api.portal.get_registry_record('medialog.mobilethemeTwo.interfaces.IMobilethemeTwoSettings.scrape_url')
            
        if hasattr(self.request, 'selector'):
            selector = str(urllib.unquote((self.request.selector).decode('utf8')))

        if hasattr(self.request, 'url'):
            url = str(urllib.unquote((self.request.url).decode('utf8')))
        
        #get base url, we will use this to decide if the url should opened as a redirect view
        parts = url.split('//', 1)
        scrape_base_url = parts[0]+'//'+parts[1].split('/', 1)[0]

        #get html from the requested url
        r = requests.get(url)
        tree = lxml.html.fromstring(r.text)
             
        #clean evil stuff
        cleaner = Cleaner(javascript = scrape_javascript , style = scrape_style )
        cleaner(tree)
        
        #the parsed DOM Tree
        lxml.html.tostring(tree)

        #relink
        tree.make_links_absolute(scrape_base_url, resolve_base_href=True)
        tree.rewrite_links(self.repl)
        
        # construct a CSS Selector
        sel = CSSSelector(selector)
        
        # Apply the selector to the DOM tree.
        results = sel(tree)
        
        # the HTML for the first result.
        if results:
            match = results[0]
            return lxml.html.tostring(match)

        #return "Content can not be filtered, returning whole page"
        return lxml.html.tostring(tree)
        
    
    def repl(html, link):
        scrape_base_url = api.portal.get_registry_record('medialog.mobilethemeTwo.interfaces.IMobilethemeTwoSettings.scrape_base_url')
        root_url = api.portal.get().absolute_url()
        
        #open pages from other sites in its own window.
        if (not (link.startswith(scrape_base_url))):
            return link
        #dont modyfy image links
        if link.endswith('.jpg') or link.endswith('.png') or link.endswith('.gif') or link.endswith('.js') or link.endswith('.jpeg') or link.endswith('.pdf'):
            return link
        #point other pages from same site to embedded view
        link =   root_url + '/scrape?url=' + link
        return link


class ScrapeView(BrowserView):
    """   A Dexterity Content View that redirects to the scrape view """
    
    def __call__(self):
    	root_url = api.portal.get().absolute_url()
    	selector  = str(self.context.scrape_selector)
    	url = str(self.context.scrape_url)
    	
    	selector = urllib.quote(selector).decode('utf8') 
    	url =      urllib.quote(url).decode('utf8')
    	 
    	self.request.response.redirect(root_url + "/scrape?selector=" + selector + "&url=" + url )
    	