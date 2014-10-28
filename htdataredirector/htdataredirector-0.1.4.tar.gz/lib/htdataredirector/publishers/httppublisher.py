from urllib.parse import urlencode

import httplib2

class HttpPublisher:

    def __init__(self, url):
        self.url = url
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded' }

    def publish(self, data):
        h = httplib2.Http()
        resp, content = h.request(self.url, 'POST', urlencode(data), self.headers)

        return content.decode('utf-8')
