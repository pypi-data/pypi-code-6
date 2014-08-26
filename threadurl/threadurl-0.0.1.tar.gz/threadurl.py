#!/usr/bin/env python
from urlparse import urlparse
from threading import Thread
from httplib import HTTPConnection
from Queue import Queue
from time import sleep



class ThreadUrl(object):

  __version__ = '0.0.1'
  __author__  = 'Renan Vicente <renanvice@gmail.com>'

  def __init__(self,concurrent=1):
    self.concurrent = concurrent
    self.q = Queue(concurrent)
    self.data_done = {}
    self.verbose = None
    self.method  = "GET"


  def doWork(self):
    while True:
      sleep(0.01)
      url=self.q.get()
      status,url=self.get_status(url)
      if self.verbose:
        self.print_status(status,url)
      self.data_done[url] = status
      self.q.task_done()

  def get_status(self,ourl):
    try:
      url = urlparse(ourl)
      conn = HTTPConnection(url.netloc)
      conn.request(self.method , url.path)
      res = conn.getresponse()
      return res.status, ourl
    except Exception as e:
      return e, ourl

  def print_status(self,status, url):
    print(status, url)

  def trigger(self,urls):
    for url in urls:
      self.q.put(url.strip())
    self.q.join()
    return self.q

  def load(self):
    for _ in range(self.concurrent):
      t=Thread(target=self.doWork)
      t.daemon=True
      t.start()
