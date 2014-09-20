import urllib
import base64

def b64kwargs(**kwargs):
    return base64.b64encode(urllib.urlencode(kwargs))
