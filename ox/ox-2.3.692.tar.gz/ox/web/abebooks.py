from ox.cache import read_url
import re
import lxml.html

def get_data(id):
    info = {}
    base = 'http://www.abebooks.com'
    url = '%s/servlet/SearchResults?isbn=%s&sts=t' % (base, id)
    data = read_url(url)
    urls = re.compile('href="(/servlet/BookDetailsPL[^"]+)"').findall(data)
    if urls:
        details = '%s%s' % (base, urls[0])
        data = read_url(details)
        doc = lxml.html.document_fromstring(data)
        for e in doc.xpath("//*[contains(@id, 'biblio')]"):
            key = e.attrib['id'].replace('biblio-', '')
            value = e.text_content()
            if value and key not in ('bookcondition', 'binding'):
                info[key] = value
    return info
