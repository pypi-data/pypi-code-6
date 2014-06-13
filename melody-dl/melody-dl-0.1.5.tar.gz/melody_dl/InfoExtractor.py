import re
from urlparse import urlparse

import requests
from bs4 import BeautifulSoup

import melody_dl.utils as utils



class InfoExtractor(object):

    def __init__(self):
        self.BeautifulSoup = BeautifulSoup
        self.webpage_response = None


    def request_webpage(self, url):
        """ Set the response handle """

        self.webpage_response = requests.get(url)


    def cleanup(self, text):
        text = unicode(text)

        text = text.replace('&nbsp;', ' ')
        text = text.replace(u'\xa0', ' ')
        text = text.strip()

        return text


    def verify_url(self, url):
        return re.search(self.VALID_URL, url) is not None


    def build_url(self, path):
        """ Build a full url based on the path (if nessicary) """

        if utils.is_path(path):
            parsed_url = urlparse(self.webpage_response.url)
            return "{0}://{1}{2}".format(parsed_url.scheme, parsed_url.netloc, path)

        else:
            return path
