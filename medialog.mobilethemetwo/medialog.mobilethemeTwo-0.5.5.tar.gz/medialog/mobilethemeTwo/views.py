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
        selector = '#container' #default value
        #get settings from control panel / registry

        scrape_url_pair = api.portal.get_registry_record('medialog.mobilethemeTwo.interfaces.IMobilethemeTwoSettings.scrape_url_pair')
        scrape_javascript = api.portal.get_registry_record('medialog.mobilethemeTwo.interfaces.IMobilethemeTwoSettings.scrape_javascript')
        scrape_style = api.portal.get_registry_record('medialog.mobilethemeTwo.interfaces.IMobilethemeTwoSettings.scrape_style')
        url = api.portal.get_registry_record('medialog.mobilethemeTwo.interfaces.IMobilethemeTwoSettings.scrape_url')

        
        #get url if it was set in the request
        if hasattr(self.request, 'url'):
            url = str(urllib.unquote((self.request.url).decode('utf8')))
        
        #get base url, 
        #if the url is taken from request
        parts = url.split('//', 1)
        this_base_url = parts[0]+'//'+parts[1].split('/', 1)[0]
        
        #get html from the requested url
        r = requests.get(url)
        tree = lxml.html.fromstring(r.text)
             
        #clean evil stuff
        cleaner = Cleaner(javascript = scrape_javascript , style = scrape_style )
        cleaner(tree)
        
        #the parsed DOM Tree
        lxml.html.tostring(tree)

        #relink
        tree.make_links_absolute(this_base_url, resolve_base_href=True)
        tree.rewrite_links(self.repl)
        
        # construct a CSS Selector
        #it the request defines one, use that
        if hasattr(self.request, 'selector'):
            selector = str(urllib.unquote((self.request.selector).decode('utf8')))
        
        #if not, use settings from control panel
        else:
            for pair in scrape_url_pair:
                if pair['scrape_base_url'] in url:
                    selector = pair['scrape_selector']
                    break
                   
        sel = CSSSelector(selector)
                
        # Apply the selector to the DOM tree.
        results = sel(tree)

        # the HTML for the first result.
        if results:
            match = results[0]
            return lxml.html.tostring(match)

        #"Content can not be filtered, returning whole page"
        return lxml.html.tostring(tree)
        
    
    def repl(html, link):
        scrape_url_pair = api.portal.get_registry_record('medialog.mobilethemeTwo.interfaces.IMobilethemeTwoSettings.scrape_url_pair')
        root_url = api.portal.get().absolute_url()
        embed_urls = []
        
        for pair in scrape_url_pair:
            embed_urls.append(pair.'scrape_base_url')

        #dont modyfy image links
        if link.endswith('.jpg') or link.endswith('.png') or link.endswith('.gif') or link.endswith('.js') or link.endswith('.jpeg') or link.endswith('.pdf'):
            return link
        
        #point pages for sites from control panel to embedded view
        if site_url in embed_urls:
            return root_url + '/scrape?url=' + link
        
        #for all other links
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
