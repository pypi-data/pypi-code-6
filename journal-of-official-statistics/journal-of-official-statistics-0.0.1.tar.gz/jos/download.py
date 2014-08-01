import os

import requests
from picklecache import cache

@cache(os.path.join(os.path.expanduser('~'),'.jos'))
def get(url, **kwargs):
    return requests.get(url, **kwargs)
