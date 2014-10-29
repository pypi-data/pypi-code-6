import fastkml
import lxml
import requests

from seantis.placemap import _
from seantis.plonetools import tools


def translate_kml_document(request, document):
    # collective.geo.kml doesn't correctly translate strings in KML, so we
    # do it here to work around this issue.

    translate = tools.translator(request, 'seantis.placemap')
    translation = translate(_(u"See the original resource"))

    return document.replace(u"See the original resource", translation)


def fetch_kml_document(url):

    candidates = (url, url + '/@@kml-document')

    for url in candidates:
        response = requests.get(url)

        if response.status_code != 200:
            continue

        try:
            fastkml.kml.KML().from_string(response.content)
        except (lxml.etree.XMLSyntaxError, TypeError):
            continue
        else:
            return response.content.decode('utf-8')

    return None
