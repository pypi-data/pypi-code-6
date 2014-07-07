# -*- coding: utf-8 -*-
import json
from datetime import datetime

from Acquisition import aq_inner

from zope.component.hooks import getSite
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class ContentView(BrowserView):
    """Get Plone-Content with ajax
        ===> returns json 
    """
    
    def __call__(self):
        """Standard Json view
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        action  = request.get('action')

        if action == "query":
            return self.query()
        if action == "query_length":
            return self.query()
        elif action == "get_object":
            return self.get_object()
        elif action == "livesearch":
            return self.livesearch()
        else:
            return False

    def query(self):
        """query plone catalog
        """
        context  = aq_inner(self.context)
        request  = context.REQUEST

        portal_type = request.get('portal_type','')
        search_text = request.get('search_text','')
        sort_on     = request.get('sort_on','')
        sort_order  = request.get('sort_order','')
        year        = request.get('year',None)
        month       = request.get('month',None)
        max_items   = request.get('max_items',0)

        site_url = getSite().absolute_url()
        catalog  = getToolByName(context,'portal_catalog')

        q = {}
        if search_text:            
            q['SearchableText'] = search_text
        if portal_type:
            q['portal_type'] = portal_type
        if sort_on:    
            q['sort_on'] = sort_on
        if sort_order:    
            q['sort_order'] = sort_order

        if year and month:
            year = int(year)
            month = int(month)
            # all events of a given month 
            start  = datetime(year,month,01)
            if month < 12:
                end    = datetime(year,month+1,01)
            else:
                end    = datetime(year+1,1,1)
            
        elif year:
            year = int(year)
            start  = datetime(year,1,1)
            end    = datetime(year+1,1,1)
        
        if year:
            q['start'] = {"query" : [start,end],"range": "minmax"}
        
        items    = catalog.searchResults( **q )
        if max_items:
            items = items[0:int(max_items)]

        ju = JsonApiUtils()
        if request.get('action') == "query_length":
            return ju._json_response( context,  len(items)   )
        else:
            return ju._json_response( context,  self._convert_catalog_items(items)   )


    def get_object(self):
        """returns an plone object
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        uid     = request.get('uid','')

        if not uid:
            return None

        mt      = getToolByName(context,'portal_membership')
        catalog = getToolByName(context,'portal_catalog')

        items   = catalog.searchResults( {'UID':uid} )

        if items:
            ju = JsonApiUtils()
            return  ju._json_response( context,  self._convert_catalog_items(items, fields='obj')[0] )


    def _convert_catalog_items(self, items, fields=None):
        """Converts Catalogitems into a dict
        """
        context  = aq_inner(self.context)
        mt        = getToolByName(context,'portal_membership')
        item_list = []
        for i in items:

            creator = mt.getMemberById(i.Creator)
            if creator:
                fullname = creator.getProperty('fullname')
            else:
                fullname = i.Creator
            
            new_item = {
                'uid': i.UID,
                'id': i.id,
                'title': i.Title,
                'description': i.Description or '',
                'subjects': i.Subject or '',
                'creator': fullname,
                'listCreators': i.listCreators or '',
                'effective_date': context.toLocalizedTime(i.EffectiveDate, long_format=1) or '',
                'expiration_date': context.toLocalizedTime(i.ExpirationDate, long_format=1) or '',
                'modification_date': context.toLocalizedTime(i.ModificationDate, long_format=1) or '',
            'start_date': context.toLocalizedTime(i.start, long_format=1) or '',
            'end_date': context.toLocalizedTime(i.end, long_format=1) or '',
                'path': i.getPath(),
                'url': i.getURL(),
                'icon': i.getIcon or '',
                'type': i.portal_type or '',
                'review_state': i.review_state or '',
                'location': i.location or ''
            }
            if fields == 'obj':
                #ToDo
                new_item['text'] = i.getObject().getText()

            item_list.append(new_item)
        return item_list
    
    def livesearch(self):
        """query plone catalog
        """
        context  = aq_inner(self.context)
        request  = context.REQUEST
        q = request.get('search_text','')
        multispace = u'\u3000'.encode('utf-8')
        for char in ('?', '-', '+', '*', multispace):
            q = q.replace(char, ' ')
        r = q.split()
        r = " AND ".join(r)
        request.set('search_text', self._quote_bad_chars(r)+'*')
        return self.query()

    def _quote_bad_chars(self, s):
        bad_chars = ["(", ")"]
        for char in bad_chars:
            s = s.replace(char, self._quotestring(char))
        return s

    def _quotestring(self, s):
        return '"%s"' % s        

class JsonApiUtils():
    """small utilities
    """
    def _json_response(self, context, data):
        """ Returns Json Data in Callback function
        """
        request  = context.REQUEST
        callback = request.get('callback','')        
        request.response.setHeader("Content-type","application/json")
        if callback:
            cb = callback + "(%s);"
            return cb % json.dumps(data)
        else:
            return json.dumps(data)
