#!/usr/bin/env python

import random
import json
import threading

from flask import request, url_for
from flask.ext import restful
from flask.ext.restful import fields, abort
from shelves import shelves, boxes

from ..common.utils import get_shelf

running_searches = {}

search_fields = {
    'search_id': fields.String,
    'uri': fields.Url('search_ep'),
    'state': fields.String,
    'results': fields.List(fields.Raw),
    'hits': fields.String
    }

def async_search(search, query):
    """
    This is the callback called by Search.do_search(), it will
    manage anythng about results.
    """
    results = search.shelf.search(query=query)

    # Let's find how many hits we have
    if results.has_exact_length():
        search.hits = len(results)
    else:
        search.hits = results.estimated_length()

    for hits in results:
        item = {}
        for key in hits:
            item[key] = hits[key]
        item['score'] = hits.score
        item['doc_url'] = u'/doc/%s' % hits['hash']
        search.results.append(item)

    # And end the job
    search.state = 'done'

class Search(object):
    """
    This class is used to manage the state of a search and
    to keep it's results.
    """
    def __init__(self, search_id):
        """
        We need to get a grasp on a shelf before launching the search.
        """
        self.shelf = get_shelf()
        self.state = 'init'
        self.results = []
        self.search_id = search_id
        self.hits = 0
        self.metadata = {}

    def do_request(self, metadata):
        """
        Let's initiate a request
        """
        if metadata is None:
            abort(400, message="We need metadata to search for")

        self.metadata = metadata
        self.state = 'search'
        t = threading.Thread(target=async_search, name='search_%s' % (self.search_id,), kwargs={'search': self, 'query': self.metadata})
        t.start()

class SearchResource(restful.Resource):
    """
    This resource is used to manage searches, and handle GET/POST and DELETE.
    """
    @restful.marshal_with(search_fields)
    def get(self, search_id=''):
        """
        Let's get a search state
        """
        # We will fail if no search_id is provided
        if search_id == '':
            abort(404, message="You must give a search_id") 

        # Let's find out if the search_id exist.
        if search_id not in running_searches.keys():
            abort(404, message="Search %s doesn't exist. %s" % (search_id, running_searches.keys(),))

        return running_searches[unicode(search_id)], 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'content-type'}

    @restful.marshal_with(search_fields)
    def put(self):
        """
        Let's create a new search. We will store it in this global list of search
        The query is provided as a json dictionnaries, to be sent as is.
        """
        # Let's create a search and assign it a number.
        s_id = unicode(random.randrange(1, 9999))

        while s_id in running_searches.keys():
            s_id = random.randrange(1, 9999)

        s = Search(s_id)

        # So, let's extract the body of the request as json and send it to the
        # search object
        s.do_request(request.get_json())
        running_searches[s_id] = s

        return s, 201, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'content-type'}

    @restful.marshal_with(search_fields)
    def post(self, search_id):
        """
        Let's update a search. We will only change the metadata fields which are
        provided, living the other as is. We will then rerun the search.
        """
        # Let's find out if the search_id exist.
        if search_id not in running_searches.keys():
            abort(404, message="Search %s doesn't exist. %s" % (search_id, running_searches.keys(),))

        # Lets' grab the search and check for it's thread.
        s = running_searches[search_id]

        # Let's update the metadata
        for key in request.get_json():
            s.metadata[key] = request.get_json()[key]

        # We now have a new metadata to search for
        s.do_request(s.metadata)

        return s, 201, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'content-type'}

    @restful.marshal_with(search_fields)
    def delete(self, search_id):
        """
        Let's delete a search
        """
        # Let's find out if the search_id exist.
        if search_id not in running_searches.keys():
            abort(404, message="Search %s doesn't exist. %s" % (search_id, running_searches.keys(),))

        # We need to find the thread associated to the search.
        search_thread = None
        threads = [ thread for thread in threading.enumerate() if thread.name == 'search_%s' % (search_id,) ]

        if len(threads) != 0:
            # The thread isn't terminated
            threads.wait()

        # Get it out of line
        del running_searches[search_id]
        return {}, 201, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'content-type'}

    def options(self):
        return {'Allow': 'PUT, POST, DELETE, GET'}, 200, {'Access-Control-Allow-Origin': '*', 
                        'Access-Control-Allow-Methods': 'PUT, POST, DELETE, GET',
                        'Access-Control-Allow-Headers': 'content-type'}
