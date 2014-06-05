from urllib.parse import urlsplit

from commasearch.util import traceback
import commasearch.db as db
import commasearch.dsv as dsv
import commasearch.rdbms as rdbms

RDBMS_SCHEMES = {'sqlite'}
DSV_SCHEMES = {'http','https','file'}

def _search(db, url:str):
    scheme = urlsplit(url).scheme
    if scheme in DSV_SCHEMES:
        result = dsv.search(db, url)
    elif scheme in RDBMS_SCHEMES:
        result = rdbms.search(db, url)
    else:
        raise ValueError('The scheme %s:// is not supported.')
    return result

def search(stderr, url:str):
    try:
        result = dsv.search(db, url)
    except:
        stderr.write('Error at %s:\n%s' % (url,traceback()))
    else:
        scheme, _, rest = result['path'].partition('/')
        result['url'] = '%s://%s' % (scheme, rest)
        del(result['path'])
        return result
