
__author__='''
Dawson Reid (dawson@streamlye.co)
'''
import logging
import requests
from requests.auth import HTTPBasicAuth
import json
import config

from bson.objectid import ObjectId
import re
oid_re = re.compile('([0-9a-fA-F]{24})')

class SplashClient(object):
  '''
  '''

  def __init__(self, username=None, password=None):
    self.log = logging.getLogger('{0}'.format(self))
    self.set_credentials(username, password)


  def set_credentials(self, username, password):
    self._username = username
    self._password = password


  def register(self, user):
    '''
    '''
    resp = requests.post('{0}/{1}'.format(config.SPLASH_URI, 'users'),
      headers=config.DEFAULT_HEADERS,
      data=json.dumps(user))

    ret_data = json.loads(resp.text)
    if ret_data['_status'] == 'OK':
      self._username = user['username']
      self._password = user['password']

    return ret_data


  def stream(self, _id):
    '''
    '''
    uri = '{0}/{1}/{2}'.format(config.SPLASH_URI, 'streams', _id)
    print(uri)
    resp = requests.get(uri, headers=config.DEFAULT_HEADERS)
    ret_data = json.loads(resp.text)

    print(ret_data)

    return SplashStream(self, ret_data)


  def _query(self, resource, where, sort):
    '''
    '''
    query = 'where={0}&sort={1}'.format(json.dumps(where), json.dumps(sort))
    uri = '{0}/{1}?{2}'.format(config.SPLASH_URI, resource, query)

    resp = requests.get(uri, headers=config.DEFAULT_HEADERS)
    ret_data = json.loads(resp.text)
    return ret_data


  def streams(self, where={}, sort=[]):
    '''
    '''
    ret_data = self._query('streams', where, sort)

    _streams = []
    for stream_data in ret_data['_items']:
      stream = SplashStream(self, stream_data)
      _streams.append(stream)

    return _streams


  def create_stream(self, name, description=''):
    '''
    '''
    resp = requests.post('{0}/{1}'.format(config.SPLASH_URI, 'streams'),
      headers=config.DEFAULT_HEADERS,
      data=json.dumps({
        'name': name,
        'description': description
      }),
      auth=HTTPBasicAuth(self._username, self._password))

    ret_data = json.loads(resp.text)
    if ret_data['_status'] == 'OK':
      stream = self.stream(ret_data['_id'])
      return stream
    else:
      raise Exception('Failed to create stream.')


  def stream_or_create(self, name):
    _streams = self.streams(where={'name': name})
    if len(_streams) == 1:
      return _streams[0]

    # create a stream
    elif len(_streams) == 0:
      _stream = self.create_stream(name)
      return _stream

    # multiple streams with the same name this is a major error.
    else:
      raise Exception('''
        Multiple streams with the same name. Please report at
        https://github.com/Splash-io/splash-python/issues?state=open
        ''')


  def _emit_event(self, stream, tipe, properties={}, context={}):
    '''
    '''
    resp = requests.post('{0}/{1}'.format(config.SPLASH_URI, 'events'),
      headers=config.DEFAULT_HEADERS,
      data=json.dumps({
        'stream': stream,
        'type': tipe,
        'properties': properties,
        'context': context
      }),
      auth=HTTPBasicAuth(self._username, self._password))

    ret_data = json.loads(resp.text)
    return ret_data


class SplashStream(object):

  def __init__(self, splash, stream_data):
    self._splash = splash
    self._id = stream_data['_id']
    self._created = stream_data['_created']
    self._updated = stream_data['_updated']

    self.name = stream_data['name']
    self.description = stream_data['description']
    self.creator = stream_data['creator']
    self.owner = stream_data['owner']


  def emit(self, tipe, properties={}, context={}):
    self._splash._emit_event(
      stream=self._id,
      tipe=tipe,
      properties=properties,
      context=context)


  def read(self, where={}, sort={}):
    where['stream'] = self._id
    ret_data = self._splash._query('events', where, sort)
    return ret_data['_items']
