from os import path

import requests
from picklecache import cache

@cache(path.join(path.expanduser('~'), '.wbcontractawards'))
def get(url):
    return requests.get(url)

def search(os:int):
    url = 'http://search.worldbank.org/wcontractawards'
    params = {'os': os}
    return get('%s?os=%d' % (url, os))
