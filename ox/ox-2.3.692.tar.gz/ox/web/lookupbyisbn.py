from ox.cache import read_url
from ox import find_re, strip_tags
import re

base = 'http://www.lookupbyisbn.com'

def get_data(isbn):
    r = {}
    url = '%s/Search/Book/%s/1' % (base, isbn)

    data = read_url(url).decode('utf-8')
    m = re.compile('href="(/Lookup/Book/[^"]+?)"').findall(data)
    if m:
        ids = m[0].split('/')
        r['isbn'] = ids[-2]
        r['asin'] = ids[-3]
        url = '%s%s' % (base, m[0])
        data = read_url(url).decode('utf-8')
        r["title"] = find_re(data, "<h2>(.*?)</h2>")
        keys = {
            'author': 'Author(s)',
            'publisher': 'Publisher',
            'date': 'Publication date',
            'edition': 'Edition',
            'binding': 'Binding',
            'volume': 'Volume(s)',
            'pages': 'Pages',
        }
        for key in keys:
            r[key] = find_re(data, '<span class="title">%s:</span>(.*?)</li>'% re.escape(keys[key]))
            if r[key] == '--':
                r[key] = ''
            if key == 'pages' and r[key]:
                r[key] = int(r[key])
        desc = find_re(data, '<h2>Description:<\/h2>(.*?)<div ')
        desc = desc.replace('<br /><br />', ' ').replace('<br /> ', ' ').replace('<br />', ' ')
        r['description'] = strip_tags(desc).strip()
        if r['description'] == u'Description of this item is not available at this time.':
            r['description'] = ''
        r['cover'] = find_re(data, '<img src="(.*?)" alt="Book cover').replace('._SL160_', '')
    return r

