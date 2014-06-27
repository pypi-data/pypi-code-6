"""This package is the helper module for the python wrapper for the ordr.in API.
The main developer documentation for this API is located at 
http://ordr.in/developers"""
from hashlib import sha256
from google.appengine.api import urlfetch
# import urllib3
import pdb
import json
import re
import urllib
import mutate
import jsonschema
import os

_dir = os.path.dirname(__file__)

ENDPOINT_INFO = json.load(open(os.path.join(_dir, 'schemas.json')))

PRODUCTION = 0
TEST = 1

class APIHelper(object):
  urls = {}
  _methods = {}
  def __init__(self, api_key, servers):
    """Sets up this module to make API calls. The first argument is the developer's
    API key and the second specifies which servers should be used.

    Arguments:
    api_key -- The developer's API key
    servers -- How the server URLs should be set. Must be PRODUCTION or TEST.
    """
    self.api_key = api_key
    if servers==PRODUCTION:
      self.urls['restaurant'] = "https://r.ordr.in"
      self.urls['user'] = "https://u.ordr.in"
      self.urls['order'] = "https://o.ordr.in"
    elif servers==TEST:
      self.urls['restaurant'] = "https://r-test.ordr.in"
      self.urls['user'] = "https://u-test.ordr.in"
      self.urls['order'] = "https://o-test.ordr.in"

    # pool = urllib3.PoolManager()

    def make_method(method_name):
        def method(url, data=None, headers=None):
            if data:
                data = urllib.urlencode(data)
            # return pool.request(method_name, url, fields=data, headers=headers)
            if method_name == 'GET':
                meth = urlfetch.GET
            if method_name == 'POST':
                meth = urlfetch.POST
            if method_name == 'PUT':
                meth = urlfetch.PUT
            if method_name == 'DELETE':
                meth = urlfetch.DELETE

            return urlfetch.fetch(url=url, payload=data, method=meth, headers=headers, validate_certificate=False, deadline=60)
            # res = urlfetch.fetch(url=url, payload=data, method=meth, headers=headers)
            # if res.status_code == 200:
            #     return json.loads(res.content, 'utf-8')
            # else:
            #     pdb.set_trace()
        return method

    for method_name in 'GET POST PUT DELETE'.split(): 
        self._methods[method_name] = make_method(method_name)


  def _call_api(self, base_url, method, uri, data=None, login=None):
    """Calls the api at the saved url and returns the return value as Python data structures.
    Rethrows any api error as a Python exception"""
    full_url = base_url+uri
    headers = {}
    if self.api_key:
      headers['X-NAAMA-CLIENT-AUTHENTICATION'] = 'id="{}", version="1"'.format(self.api_key)
    if login:
      hash_code = sha256(''.join((login['password'], login['email'], uri))).hexdigest()
      headers['X-NAAMA-AUTHENTICATION'] = 'username="{}", response="{}", version="1"'.format(login['email'], hash_code)
    try:
      r = self._methods[method](full_url, data=data, headers=headers)
    except KeyError:
      raise error.request_method(method)
    # r.raise_for_status()
    try:
      result = json.loads(r.content)
    except ValueError:
      raise ApiInvalidResponseError(r.data)
    if '_error' in result and result['_error']:
      if 'text' in result:
        raise Exception(result['msg']+';'+result['text'])
      else:
        raise Exception(result['msg'])
    return result

  def _call_endpoint(self, endpoint_group, endpoint_name, url_params, **kwargs):
    kwargs = dict((k,v) for k,v in kwargs.iteritems() if v is not None)
    endpoint_data = ENDPOINT_INFO[endpoint_group][endpoint_name]
    value_mutators = {}
    for name in endpoint_data['properties']:
      if 'mutator' in endpoint_data['properties'][name]:
        value_mutators[name] = mutate.mutators[endpoint_data['properties'][name]['mutator']]
      else:
        value_mutators[name] = mutate.identity
    if "allOf" in endpoint_data:
      for subschema in endpoint_data['allOf']:
        for option in subschema['oneOf']:
          for name in option['properties']:
            if 'mutator' in option['properties'][name]:
              value_mutators[name] = mutate.mutators[option['properties'][name]['mutator']]
            else:
              value_mutators[name] = mutate.identity
    if 'email' not in value_mutators:
      value_mutators['email'] = mutate.identity
    jsonschema.validate(kwargs, endpoint_data)
    arg_dict = {name:urllib.quote_plus(value_mutators[name](kwargs[name])) for name in url_params}
    data = {name:value_mutators[name](value) for name,value in kwargs.items() if name not in url_params+['current_password']}
    uri = endpoint_data['meta']['uri'].format(**arg_dict)
    if not data:
      data = None
    if endpoint_data['meta']['userAuth']:
      return self._call_api(self.urls[endpoint_group], endpoint_data['meta']['method'], uri, data, 
                            {'email' : kwargs['email'], 
                             'password' : mutate.sha256(kwargs['current_password'])})
    else:
      return self._call_api(self.urls[endpoint_group], endpoint_data['meta']['method'], uri, data)
