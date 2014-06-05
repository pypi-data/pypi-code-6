from urllib.parse import urlsplit

import commasearch.db as db
from commasearch.util import traceback
import commasearch.dsv as dsv
import commasearch.rdbms as rdbms

RDBMS_SCHEMES = {'sqlite'}
DSV_SCHEMES = {'http','https','file'}

def _index(url:str):
    scheme = urlsplit(url).scheme
    if scheme in DSV_SCHEMES:
        result = dsv.index(db, url)
    elif scheme in RDBMS_SCHEMES:
        result = rdbms.index(db, url)
    else:
        raise ValueError('The scheme %s:// is not supported.')
    return result

def index(stderr, url:str):
    try:
        return _index(url)
    except:
        stderr.write('Error at %s:\n%s' % (url,traceback()))
