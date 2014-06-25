#!/usr/bin/env python

"""
MySearch
Copyright (C) 2013   Tuxicoman

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
current_path = os.path.dirname(__file__)
if current_path != "":
  os.chdir(current_path) #set current directory to script folder

#Import OS libs
from twisted.web import server, resource, _newclient
from twisted.internet import reactor, defer
import jinja2, time, json, datetime, ConfigParser

#Import project libs
import backends, onion
from utils import outputlog

#configuration
config = {}
config["bind_interface"] = "localhost"
config["bind_port"] = "60061"
config["relay"] = True


config_file_path = os.path.expanduser('~/.config/mysearch/mysearch.conf')
config_section = "mysearch"

def read_config(config_file_path, config_dict):
  configparser = ConfigParser.RawConfigParser()
  configparser.read(config_file_path)
  for key, previous_value in config_dict.items():
    if configparser.has_option(config_section, key):
      new_value = configparser.get(config_section, key).decode('utf-8')
      if type(previous_value) in (list, bool):
        new_value = json.loads(new_value)
      config_dict[key] = new_value

def save_config(config_file_path, config_dict):
  configparser = ConfigParser.RawConfigParser()
  configparser.add_section(config_section)
  for key, value in config_dict.items():
    if type(value) in (list, bool) :
      value = json.dumps(value)
    configparser.set(config_section, key, value.encode('utf-8'))
    
  config_file_folder = os.path.dirname(config_file_path)
  if not os.path.exists(config_file_folder) :
    os.makedirs(config_file_folder)
  with open(config_file_path, 'w') as configfile:
    configparser.write(configfile)

available_pages = "Available url are : \
\n/mysearch?q=keywords"



def cookie_expiration_time_string():
  expire_time = datetime.datetime.now() + datetime.timedelta(days=300)
  return expire_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
  
def get_jinja_template(template):
  from jinja2 import FileSystemLoader
  from jinja2.environment import Environment
  env = Environment()
  env.loader = FileSystemLoader('templates/')
  return env.get_template(template)

class SearchRequest:  
  
  #ensure the search request doesn't take too long to process
  def set_timeout(self, d, datatype, timeout = 3):
    def cancel():
      d.cancel()
      self.fail("Timeout : %i sec exceeded" % timeout, datatype)
      
    timeoutCall = reactor.callLater(timeout, cancel)
      
    def completed(passthrough):
      if timeoutCall.active():
        timeoutCall.cancel()
      return passthrough
    d.addBoth(completed)
    
  #ensure the search request finishes in case of error
  def fail(self, failure, datatype):
    if type(failure) != str:
      if failure.type == _newclient.ResponseNeverReceived :
        failure = "Response never received"
      else:
        failure = "Unknown error"
     
    outputlog(failure, "error") 
    print failure
    self.store_results([], datatype, failed = failure)      

  
  def __init__(self, request, query, locale, backend_name, more_results):
    self.request = request
    self.query = query
    self.locale = locale
    self.more_results = more_results
    self.backend_name = backend_name
    self.results = {}
    self.failures = {}
    self.timer = time.time()
    self.backends_to_wait = 0

    if self.query =="":
      self.display_page()
    elif self.backend_name in [backend.name for backend in backends.available_backends]:
      if backends.SearchGoogleTxt.name == self.backend_name:
        datatype = "txt"
        self.results[datatype] = None
        search_backend = backends.SearchGoogleTxt(use_relay=config["relay"])
        self.backends_to_wait += 1
        d = search_backend.search(self.query, self.locale, self.more_results)
        d.addCallback(self.store_results, datatype)
        d.addErrback(self.fail, datatype)
        self.set_timeout(d, datatype)
      elif backends.SearchYacyTxt.name == self.backend_name:
        datatype = "txt"
        self.results[datatype] = None
        search_backend = backends.SearchYacyTxt(use_relay=config["relay"])
        self.backends_to_wait += 1
        d = search_backend.search(self.query, self.locale, self.more_results)
        d.addCallback(self.store_results, datatype)
        d.addErrback(self.fail, datatype)
        self.set_timeout(d, datatype)
      elif  backends.SearchGoogleImage.name == self.backend_name :
        datatype = "img"
        self.results[datatype] = None
        search_backend = backends.SearchGoogleImage(use_relay=config["relay"])
        self.backends_to_wait += 1
        d = search_backend.search(self.query, self.locale, self.more_results)
        img_cache_backend = backends.ImageCacheBackend()
        d.addCallback(img_cache_backend.build)
        d.addCallback(self.store_results, datatype)
        d.addErrback(self.fail, datatype)
        self.set_timeout(d, datatype, 10)
      elif backends.SearchGoogleVideo.name == self.backend_name:
        datatype = "video"
        self.results[datatype] = None
        search_backend = backends.SearchGoogleVideo(use_relay=config["relay"])
        self.backends_to_wait += 1
        d = search_backend.search(self.query, self.locale, self.more_results)
        img_cache_backend = backends.ImageCacheBackend()
        d.addCallback(img_cache_backend.build)
        d.addCallback(self.store_results, datatype)
        d.addErrback(self.fail, datatype)
        self.set_timeout(d, datatype)
      elif backends.SearchWikipediaTxt.name == self.backend_name:
        datatype = "wiki"
        self.results[datatype] = None
        search_backend = backends.SearchWikipediaTxt(use_relay=config["relay"])
        self.backends_to_wait += 1
        d = search_backend.search(self.query, self.locale)
        d.addCallback(self.store_results, datatype)
        d.addErrback(self.fail, datatype)
        self.set_timeout(d, datatype)
      elif backends.SearchOpenStreetMap.name == self.backend_name:
        datatype = "location"
        self.results[datatype] = None
        search_backend = backends.SearchOpenStreetMap(use_relay=config["relay"])
        self.backends_to_wait += 1
        d = search_backend.search(self.query, self.locale)
        d.addCallback(self.store_results, datatype)
        d.addErrback(self.fail, datatype)
        self.set_timeout(d, datatype)
    else:
      outputlog("Bad SearchRequest input", "error")
      
  def store_results(self, data, datatype, failed = False):
    if self.backends_to_wait > 0:
      
      #Append results
      if self.results[datatype] == None:
        self.results[datatype] = data
      else:
        self.results[datatype].extend(data)
      
      #Notice failure
      
      if failed != False:
        self.failures[datatype] = failed
        
      self.backends_to_wait -=1
          
      if self.backends_to_wait == 0:
        #Filter empty results
        for datatype, data in  self.results.items():
          if len(data) == 0 :
            del self.results[datatype]
            
        self.display_page()
      
  def display_page(self):
    template = get_jinja_template('mysearch.html')
    timer = time.time()-self.timer
    outputlog("Timer %s : %.2f" % (self.__class__, timer), "info")
    
    #Flag if no results are available
    if len(self.results.keys()) == 0:
      no_results = True
    else:
      no_results = False
    
    data = template.render(query=self.query.replace("+"," "), current_locale = self.locale, locales=backends.locales, no_results=no_results, failures=self.failures, results=self.results, more_results = self.more_results, current_backend = self.backend_name, backends = backends.available_backends, timer=timer)
    self.request.setHeader("content-type", "text/html;charset=utf-8")
    self.request.addCookie("locale", self.locale, expires=cookie_expiration_time_string())
    self.request.addCookie("backend", self.backend_name, expires=cookie_expiration_time_string())
    self.request.write(data.encode('utf-8'))
    self.request.finish()
    
class HomePage:
  def __init__(self, request, locale, backend_name):
    self.request = request
    self.locale = locale
    self.timer = time.time()
    self.backend_name = backend_name
    
    self.display_page()
  
  def display_page(self):
    template = get_jinja_template("index.html")
    timer = time.time()-self.timer
    outputlog("Timer %s : %.2f" % (self.__class__, timer), "info")
    data = template.render(current_locale = self.locale, locales=backends.locales, current_backend = self.backend_name, backends = backends.available_backends, more_results = 0)
    self.request.setHeader("content-type", "text/html;charset=utf-8")
    self.request.addCookie("locale", self.locale, expires=cookie_expiration_time_string())
    self.request.addCookie("backend", self.backend_name, expires=cookie_expiration_time_string())
    self.request.write(data.encode('utf-8'))
    self.request.finish()

class Redirect:
  def __init__(self, request, url):
    self.request = request
    self.url = url
    self.timer = time.time()
    self.display_page()
    
  def display_page(self):
    template = get_jinja_template("redirect.html")
    timer = time.time()-self.timer
    outputlog("Timer %s : %.2f" % (self.__class__, timer), "info")
    data = template.render(url = self.url)
    self.request.setHeader("content-type", "text/html;charset=utf-8")
    self.request.write(data.encode('utf-8'))
    self.request.finish()
    
class OpenSearchDescription:
  def __init__(self, request, public_address):
    self.request = request
    self.public_address = public_address
    self.timer = time.time()
    self.display_page()
    
  def display_page(self):
    template = get_jinja_template("opensearchdescription.xml")
    timer = time.time()-self.timer
    outputlog("Timer %s : %.2f" % (self.__class__, timer), "info")
    data = template.render(public_address = self.public_address)
    self.request.setHeader("content-type", "text/xml")
    self.request.write(data.encode('utf-8'))
    self.request.finish()
  

class MainPage(resource.Resource):
  isLeaf = True
  requestID = 0
  
  def getChild(self, name, request):
    if name == '':
        return self
    return Resource.getChild(self, name, request)

  def render_GET(self, request):
    self.requestID += 1
    
    #User headers to know if the terminal is a mobile
    terminal_profile = ''
    user_agent = request.getHeader('user-agent')
    if user_agent != None:
      if "mobile" in "".join(user_agent).lower():
        terminal_profile = 'mobile'
    #print 'terminal_profile', terminal_profile
    
    #public_address // Useful for Apache proxy
    if request.getHeader('x-app-location') != None:
      public_address = request.getHeader('x-app-location')
    else:
      public_address = "%s:%s" % (request.getHost().host, request.getHost().port)

    if request.path == "/mysearch" and (request.args.has_key("q") and len(request.args["q"][0].replace(" ",""))>0):

      #Language
      if request.args.has_key("locale"):
        locale = request.args["locale"][0]
      else:
        locale =  request.getCookie("locale")
        if locale == None:
          locale = "en"
      
      #Ask for more results
      if request.args.has_key("more_results"):
        more_results = int(request.args["more_results"][0])
      else:
        more_results = 0
        
      #Backends
      if request.args.has_key("backend"):
        backend_name = request.args["backend"][0]
      else:
        backend_name = request.getCookie("backend")
        if backend_name == None :
          #Text backend
          backend_name = backends.available_backends[0].name

      query = "+".join(request.args["q"][0].split())
      query = query.decode('utf-8')

      search_request = SearchRequest(request, query, locale, backend_name, more_results)

      return server.NOT_DONE_YET
      
    elif request.path == "/" or (request.path == "/mysearch" and request.args.has_key("q") and len(request.args["q"][0].replace(" ","")) == 0):
      #Home page
      
      #Langage
      if request.args.has_key("locale"):
        locale = request.args["locale"][0]
      else:
        locale =  request.getCookie("locale")
        if locale == None:
          locale = "en"     
          
      #Backends
      if request.args.has_key("backend"):
        backend_name = request.args["backend"][0]
      else:
        backend_name = request.getCookie("backend")
        if backend_name == None:
          #Text backend
          backend_name = backends.available_backends[0].name
          
      HomePage(request, locale, backend_name)
      return server.NOT_DONE_YET
      
    elif request.path == "/redirect" and request.args.has_key("url"):
      url = request.args["url"][0]
      url = url.decode('utf-8')
      Redirect(request, url)
      return server.NOT_DONE_YET
      
    elif request.path == "/opensearchdescription.xml":
      OpenSearchDescription(request, public_address)
      return server.NOT_DONE_YET
      
    else:
      #Static files
      if request.path[0] == "/":
        request.path = request.path[1:]
      
      startdir = os.path.abspath(os.path.join(os.curdir, "static"))
      if not os.path.isdir(startdir):
        outputlog("the Static dir %s doesn't exist" % startdir, "error")
        return "Static dir issue"
      else :
        requested_path = os.path.join(startdir, request.path)
        
        
        ##### VERY IMPORTANT FOR SECURITY #####
        requested_path =  os.path.abspath(requested_path)
        startdir = os.path.abspath(startdir)
        if os.path.commonprefix([requested_path, startdir]) != startdir:
          outputlog("%s not served for security reason" % request.path, "error")
          return "Dir traversal forbidden"
        ##### VERY IMPORTANT FOR SECURITY #####
        
        
        else:
          if not os.path.isfile(requested_path):
            outputlog("%s doesn't exist" % requested_path, "error")
            return "URL doesn't exist" + "\n" + available_pages
          else:
            outputlog("serving %s" % requested_path, "info")
            with open(requested_path, 'rb') as f:
              file_data = f.read()
            if os.path.splitext(requested_path)[1] == ".css":
              request.setHeader("content-type", "text/css")
            elif os.path.splitext(requested_path)[1] == ".xml":
              request.setHeader("content-type", "text/xml")
            elif os.path.splitext(requested_path)[1] == ".png":
              request.setHeader("content-type", "image/png")
            elif os.path.splitext(requested_path)[1] == ".ico":
              request.setHeader("content-type", "image/x-icon")
            request.write(file_data)
            request.finish()
            return server.NOT_DONE_YET

if __name__ == "__main__" :
  print "### Welcome to MySearch ###"
  read_config(config_file_path, config)
  save_config(config_file_path, config)
  if config["relay"] == True:
    reactor.listenTCP(onion.relay_port, onion.RelayServerFactory())
  reactor.listenTCP(int(config["bind_port"]), server.Site(MainPage()), interface=config["bind_interface"])
  reactor.run()


