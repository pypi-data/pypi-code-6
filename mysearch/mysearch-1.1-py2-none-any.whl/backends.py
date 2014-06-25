#!/usr/bin/env python

"""
MySearch
Copyright (C) 2013   Tuxicoman

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from twisted.internet import reactor, protocol, defer
from twisted.web.http_headers import Headers
from HTMLParser import HTMLParser
import urllib, time, json, base64, re
from utils import outputlog
import onion

locales = ("en", "fr", "be", "br", "de", "es")

class WikipediaResult:
  def __init__(self, link_name, link_url):
    self.link_name = sanitize(HTML_reserved_chars_decode(link_name))
    self.link_url = sanitize(link_url)
    self.redirect_link_url = create_redirect_link(self.link_url)
    
class TxtResult:
  def __init__(self, link_name, link_url, link_resume):
    self.link_name = sanitize(HTML_reserved_chars_decode(link_name))
    self.link_url = sanitize(link_url)
    self.link_resume = sanitize(HTML_reserved_chars_decode(link_resume))
    self.redirect_link_url = create_redirect_link(self.link_url)
    
class VideoResult:
  def __init__(self, link_name, link_url, image_url):
    self.link_name = sanitize(HTML_reserved_chars_decode(link_name))
    self.link_url = sanitize(link_url)
    self.image_url = sanitize(image_url)
    self.image_data = None
    self.redirect_link_url = create_redirect_link(self.link_url)

class ImageResult:
  def __init__(self, link_url, image_url, height, width):
    self.image_url = sanitize(image_url)
    self.image_data = None
    self.link_url = sanitize(link_url)
    self.redirect_link_url = create_redirect_link(self.link_url)
    self.height = int(height)
    self.width= int(width)
    
class LocationResult:
  def __init__(self, link_name, link_url, latitude, longitude):
    self.link_name = sanitize(HTML_reserved_chars_decode(link_name))
    self.link_url = link_url
    self.latitude = float(latitude)
    self.longitude = float(longitude)
    self.redirect_link_url = create_redirect_link(self.link_url)
    
class Body:
  def __init__(self, data, content_type=None):
    self.data = data
    self.content_type = content_type
    
class SimpleReceiver(protocol.Protocol):
  def __init__(self, d, content_type):
    self.buf = ''
    self.content_type = content_type
    self.d = d
    
  def dataReceived(self, data):
    self.buf += data
    
  def connectionLost(self, reason):
    self.d.callback(Body(self.buf, self.content_type))

def download_body(response):
  content_type =  response.headers.getRawHeaders('content-type')[0]
  d = defer.Deferred()
  response.deliverBody(SimpleReceiver(d, content_type))
  return d


class MLStripper(HTMLParser):
  def __init__(self):
      self.reset()
      self.fed = []
  def handle_data(self, d):
      self.fed.append(d)
  def get_data(self):
      return ''.join(self.fed)

def sanitize(data):
    s = MLStripper()
    s.feed(data)
    return s.get_data()
    
def HTML_reserved_chars_decode(data):
  data = data.replace("&#34;", '"')
  data = data.replace("&#39;", "'")
  data = data.replace("&#38;", "&")
  data = data.replace("&#60;", "<")
  data = data.replace("&#62;", ">")
  return data
    
def create_redirect_link(url):
  url = "/redirect?url=%s" % url.replace("&", "%26")
  return url
  
class MatchNotFound(BaseException):
  pass
  
def match(data, pattern, mode="end"):
  pos = data.find(pattern)
  if pos == -1 :
    raise MatchNotFound
    
  if mode=="end":
    pos += len(pattern)
  return pos
  

  
class ImageCacheBackend: 
  def build(self, img_results):
    self.timer = time.time()
    self.img_results = img_results
    user_agent = 'Mozilla/5.0 (Linux U; en-US)  AppleWebKit/528.5  (KHTML, like Gecko, Safari/528.5 ) Version/4.0 Kindle/3.0 (screen 600x800; rotate)'
    deferred_list = []
    #Download all images data
    for img in self.img_results :
      agent = onion.OnionAgent(reactor)
      d = agent.request('GET', str(img.image_url), Headers({'User-Agent': [user_agent]}), None)
      d.addCallback(download_body)
      d.addCallback(self.pack_data, img)
      deferred_list.append(d)
    dl = defer.DeferredList(deferred_list)
    dl.addCallback(self.return_results)
    return dl

  def pack_data(self, body, img):
    #pack data in base64
    if body.content_type in ("image/jpeg", "image/jpg", "image/png", "image/gif") :
      img.image_data = "data:%s;base64,%s" %(body.content_type, base64.b64encode(body.data))
    
  def return_results(self, d):
    #Only return images packed / discard those needing request to external url
    results = [img for img in self.img_results if img.image_data != None]
    outputlog("Timer %s : %.2f" % (self.__class__, time.time()-self.timer), 'info')
    return results

class WebBackend: 
   
  def __init__(self, use_relay=True):
    self.use_relay=use_relay
    
  def search(self, query, locale, more_results = 0):
    self.locale = locale
    self.query = query
    self.more_results = more_results
    self.timer = time.time()

    agent = onion.OnionAgent(reactor, use_relay = self.use_relay )
    d = agent.request('GET',self.get_query_url(), Headers({'User-Agent': [self.get_user_agent()]}), None)
    d.addCallback(download_body)
    d.addCallback(self.parser)
    return d
  
  def parser(self, body):
    results = self.page_parser(body.data)
    outputlog("Timer %s : %.2f" % (self.__class__, time.time()-self.timer), 'info')
    return results
    
class SearchGoogleTxt(WebBackend):
  name = "Google"
  type = "Web"
  results_by_page = 10
  def get_destination_domains(self):
    domains = []
    for locale in locales:
      if locale == "en":
        ext = "com"
      elif locale == "br":
        ext = "com.br"
      else :
        ext = locale
      domains.append("www.google.%s" % ext)
    return domains
  
  def get_query_url(self):
    if self.locale == "en":
      ext = "com"
    elif self.locale == "br":
      ext = "com.br"
    else :
      ext = self.locale
    start_result_id = self.results_by_page*self.more_results
    return "https://www.google.%s/search?q=%s&start=%s" % (ext, urllib.quote(self.query.encode('utf-8')), start_result_id)
  def get_user_agent(self):
    return 'Mozilla/5.0 (Linux U; en-US)  AppleWebKit/528.5  (KHTML, like Gecko, Safari/528.5 ) Version/4.0 Kindle/3.0 (screen 600x800; rotate)'  
  def page_parser(self,data): 
    """   
    with open('debug.html', 'w') as f:
      f.write(data)
    """
    
    results = []
    pos = 0
    for i in range(self.results_by_page):
      try :
        pos += match(data[pos:], 'class="web_result">')
        pos += match(data[pos:], '<a href="')
        pos += match(data[pos:], 'url?q=')
        start = pos
        pos += match(data[pos:], '&', mode="begin")
        stop = pos
        link_url = data[start:stop].decode("utf-8")
        
        pos += match(data[pos:], '>')
        start = pos
        pos += match(data[pos:], '</a>', mode="begin")
        stop = pos
        link_name = data[start:stop].decode("utf-8")
        
        pos += match(data[pos:], '<div>')
        start = pos
        pos += match(data[pos:], '<div>', mode="begin")
        stop = pos
        link_resume = data[start:stop].decode("utf-8")
      except MatchNotFound:
        break
      results.append(TxtResult(link_name, link_url, link_resume))
        
    return results
  
class SearchGoogleImage(WebBackend):
  name = "Google Image"
  type = "Image"
  results_by_page = 30
  def get_destination_domains(self):
    domains = []
    for locale in locales:
      if locale == "en":
        ext = "com"
      elif locale == "br":
        ext = "com.br"
      else :
        ext = locale
      domains.append("www.google.%s" % ext)
    for i in xrange(10):
      domains.append("encrypted-tbn%i.gstatic.com" % i)
    return domains
  
  def get_query_url(self):
    if self.locale == "en":
      site = "com"
    elif self.locale == "br":
      site = "com.br"
    else :
      site = self.locale
    start_result_id = self.results_by_page*self.more_results
    return "https://www.google.%s/search?q=%s&tbm=isch&start=%s" % (site, urllib.quote(self.query.encode('utf-8')), start_result_id)
  def get_user_agent(self):
    return 'Mozilla/5.0 (PLAYSTATION 3; 2.00)'  
  
  def page_parser(self,data):
    def replace_google_static(m):
      i = int(m.group()[1])
      return 'encrypted-tbn%i.gstatic.com' % i
          
    data = data.decode('utf-8')
    """
    with open('debug.html', 'w') as f:
      f.write(data.encode('utf-8'))
    """
    pos = 0
    results = []
    for i in range(self.results_by_page):
      try :
        pos += match(data[pos:], '/imgres?imgurl=')
        start = pos
        pos += match(data[pos:], '&', mode="begin")
        stop = pos
        link_url = data[start:stop]
        
        pos += match(data[pos:], 'tbnh=')
        start = pos
        pos += match(data[pos:], '&', mode="begin")
        stop = pos
        height = data[start:stop]
        
        pos += match(data[pos:], 'tbnw=')
        start = pos
        pos += match(data[pos:], '&', mode="begin")
        stop = pos
        width = data[start:stop]
        
        pos += match(data[pos:], 'src="')
        start = pos
        pos += match(data[pos:], '"', mode="begin")
        stop = pos
        image_url = data[start:stop]

        #Use encrypted Gstatic
        if image_url[:5] == "http:":
          image_url = "https:" + image_url[5:]
        image_url = re.sub("t.\.gstatic\.com", replace_google_static, image_url)

          
      except MatchNotFound:
        break
      results.append(ImageResult(link_url, image_url, height, width))
      
    return results
  
class SearchGoogleVideo(WebBackend):
  name = "Google Video"
  type = "Video"
  results_by_page = 10
  def get_destination_domains(self):
    domains = []
    for locale in locales:
      if locale == "en":
        ext = "com"
      elif locale == "br":
        ext = "com.br"
      else :
        ext = locale
      domains.append("www.google.%s" % ext)
    domains.append("img.youtube.com")
    for i in xrange(10):
      domains.append("encrypted-tbn%i.gstatic.com" % i)
    return domains
    
  def get_query_url(self):
    if self.locale == "en":
      site = "com"
    elif self.locale == "br":
      site = "com.br"
    else :
      site = self.locale
    start_result_id = self.results_by_page*self.more_results
    return "https://www.google.%s/search?q=%s&tbm=vid&start=%s" % (site, urllib.quote(self.query.encode('utf-8')), start_result_id)
  def get_user_agent(self):
    return 'Mozilla/5.0 (Linux U; en-US)  AppleWebKit/528.5  (KHTML, like Gecko, Safari/528.5 ) Version/4.0 Kindle/3.0 (screen 600x800; rotate)'  
  def page_parser(self,data):
    data = data.decode('utf-8')
    """
    with open('debug.html', 'w') as f:
      f.write(data.encode('utf-8'))
    """
    pos = 0# match(data, '<div id="universal">')
    results = []
    for i in range(self.results_by_page):
      try:
        pos += match(data[pos:], 'class="video_result"><div><a href="/url?q=')
        start = pos
        pos += match(data[pos:], '&', mode="begin")
        stop = pos
        link_url = urllib.unquote(data[start:stop])
        
        pos += match(data[pos:], '>')
        start = pos
        pos += match(data[pos:], '</a>', mode="begin")
        stop = pos
        link_name = data[start:stop]
        
        pos += match(data[pos:], '<img src="')
        start = pos
        pos += match(data[pos:], '"', mode="begin")
        stop = pos
        image_url = data[start:stop]
      except MatchNotFound:
        break
      results.append(VideoResult(link_name, link_url, image_url))

    return results
    
    
    
class SearchWikipediaTxt(WebBackend):
  name = "Wikipedia"
  type = "Wiki"
  def get_destination_domains(self):
    domains = ["%s.wikipedia.org" % locale for locale in locales]
    return domains
  def get_query_url(self):
    return "https://%s.wikipedia.org/w/api.php?action=opensearch&format=json&search=%s&limit=10&namespace=0&suggest=" % (self.locale, urllib.quote(self.query.encode('utf-8')))
  def get_user_agent(self):
    return ''  
  def page_parser(self,data):
    data = data.decode('utf-8')
    
    """
    with open('debug.html', 'w') as f:
      f.write(data.encode('utf-8'))
    """
    
    results = []
    data = json.loads(data)
    for result in data[1]:
      link_name = result
      link_url = "https://%s.wikipedia.org/wiki/" % (self.locale) + result.replace(' ', '_')
      results.append(WikipediaResult(link_name, link_url))
    
    return results
    
    
class SearchOpenStreetMap(WebBackend):
  name = "OpenStreetmap"
  type = "Location"
  def get_destination_domains(self):
    domains = ["nominatim.openstreetmap.org"]
    return domains
  def get_query_url(self):
    return "https://nominatim.openstreetmap.org/search?q=%s&format=json" % self.query.encode('utf-8')
  def get_user_agent(self):
    return ''  
  def page_parser(self,data):
    data = data.decode('utf-8')
    
    """
    with open('debug.html', 'w') as f:
      f.write(data.encode('utf-8'))
    """
    
    results = []
    data = json.loads(data)    
    for result in data:
      link_name = result["display_name"]
      latitude = float(result["lat"])
      longitude = float(result["lon"])
      link_url = "https://www.openstreetmap.org/?mlat=%.4f&mlon=%.4f" % (latitude, longitude)
      results.append(LocationResult(link_name, link_url, latitude, longitude))
    
    return results
    
class SearchYacyTxt(WebBackend):
  name = "Yacy"
  type = "Web"
  results_by_page = 10
  def get_destination_domains(self):
    domains = ["search.yacy.net"]
    return domains
  def get_query_url(self):
    start_result_id = self.results_by_page*self.more_results
    return "http://search.yacy.net/yacysearch.json?query=%s&maximumRecords=%s&startRecord=%s" % (urllib.quote(self.query.encode('utf-8')), self.results_by_page, start_result_id)
  def get_user_agent(self):
    return ''  
  def page_parser(self,data): 
    data = data.decode('utf-8')
    """
    with open('debug.html', 'w') as f:
      f.write(data.encode('utf-8'))
    """
    
    results = []
    data = json.loads(data)
    for result in data["channels"][0]["items"]:
      link_name = result["title"]
      link_resume = result["description"]
      link_url = result["link"]
      results.append(TxtResult(link_name, link_url, link_resume))
        
    return results
    
available_backends = [SearchGoogleTxt, SearchGoogleImage, SearchGoogleVideo, SearchWikipediaTxt, SearchOpenStreetMap, SearchYacyTxt]
