# -*- coding: utf-8 -*-
import base64
import hmac
import requests

from requests.auth import AuthBase
from hashlib import sha1
from urlparse import urlparse
from email.utils import formatdate

from fds.auth.Common import Common
from fds.model.SubResource import SubResource


class Signer(AuthBase):


  def __init__(self, app_key, app_secret, service_url=None):
    if service_url:
      self.service_base_url = service_url
    self.app_key = str(app_key)
    self.app_secret = str(app_secret)

  def __call__(self, r):
    r.headers[Common.DATE] = formatdate(timeval=None, localtime=False, usegmt=True)
    signature = self.get_signature(r.method, r.headers, r.url, self.app_secret)
    r.headers[Common.AUTHORIZATION] = 'Galaxy-V2 %s:%s' % (self.app_key, signature)
    return r

  @staticmethod
  def get_signature(method, headers, url, app_secret):
    string_to_sign = Signer.construct_string_to_sign(method, headers, url)
    h = hmac.new(app_secret, string_to_sign, digestmod=sha1)
    return base64.encodestring(h.digest()).strip()

  @staticmethod
  def construct_string_to_sign(http_method, http_headers, uri):
    result = ''
    result += '%s\n' % http_method
    result += '%s\n' % Signer.get_header_value(http_headers, Common.CONTENT_MD5)
    result += '%s\n' % Signer.get_header_value(http_headers, Common.CONTENT_TYPE)
    expires = Signer.get_expires(uri)
    if expires > 0:
      result += '%s\n' % expires
    else:
      xiaomi_date = Signer.get_header_value(http_headers, Common.XIAOMI_HEADER_DATE)
      date = ''
      if xiaomi_date is '':
        date = Signer.get_header_value(http_headers, Common.DATE)
      result += '%s\n' % date
    result += '%s' % Signer.canonicalize_xiaomi_headers(http_headers)
    result += '%s' % Signer.canonicalize_resource(uri)
    return result

  @staticmethod
  def get_header_value(http_headers, name):
    if http_headers is not None and name in http_headers:
      value = http_headers[name]
      if type(value) is list:
        return http_headers[name][0]
      else:
        return value
    return ""

  @staticmethod
  def canonicalize_xiaomi_headers(http_headers):
    if http_headers is None or http_headers == {}:
      return ''
    canonicalized_headers = {}
    for key in http_headers:
      lk = key.lower()
      try:
        lk = lk.decode('utf-8')
      except:
        pass
      if http_headers[key] and lk.startswith(Common.XIAOMI_HEADER_PREFIX):
        if type(http_headers[key]) != str:
          canonicalized_headers[lk] = ''
          i=0
          for k in http_headers[key]:
            canonicalized_headers[lk] += '%s' % (k.strip())
            i=i+1
            if i < len(http_headers[key]):
              canonicalized_headers[lk] += ','
        else:
          canonicalized_headers[lk] = http_headers[key].strip()
    result = ""
    for key in sorted(canonicalized_headers.keys()):
      values = canonicalized_headers[key]
      result += '%s:%s\n' % (key, values)
    return result

  @staticmethod
  def canonicalize_resource(uri):
    result = ""
    parsedurl = urlparse(uri)
    result += '%s' % parsedurl.path
    query_args = parsedurl.query.split('&')
    i = 0
    for q in sorted(query_args):
      k = q.split('=')
      if k[0] in SubResource.get_all_subresource():
        if i == 0:
          result += '?'
        else:
          result += '&'
        if len(k) == 1:
          result += '%s' % k[0]
        else:
          result += '%s=%s' % (k[0], k[1])
        i = i+1
    return result

  @staticmethod
  def get_expires(uri):
    parsedurl = urlparse(uri)
    query_args = sorted(parsedurl.query.split('&'))
    for q in query_args:
      k = q.split('=')[0]
      if k==Common.EXPIRES:
        return q.split('=')[1]
    return 0





'''
access_key = "5341725076926"
access_secret = "vhlqXBAsWMbRIKZx+UBfPQ=="

r = requests.get(('http://files.fds.api.xiaomi.com/%s/%s' % ("python-test-15652193901", "test333")), auth=Signer(access_key, access_secret), headers={'xiaomi-haha': 'aa'})


#r = requests.put(('http://files.fds.api.xiaomi.com/%s/%s' % ("python-test-15652193901", "test444")), data="hahhaha", auth=Signer(access_key, access_secret))
print r.content
print r.status_code
print r.headers
'''
