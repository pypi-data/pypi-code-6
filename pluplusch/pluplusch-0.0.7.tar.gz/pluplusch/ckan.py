from io import StringIO
import datetime
import json
import functools, itertools
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
from logging import getLogger

from pluplusch.util import colnames as _colnames

logger = getLogger(__name__)

catalogs = [
#   (('http',), 'datahub.io'),
    (('http',), 'opendata.comune.bari.it'),
    (('http',), 'africaopendata.org'),
#   (('http',), 'opendata.aragon.es'),
#   (('http',), 'daten.berlin.de'),
    (('http',), 'data.buenosaires.gob.ar'),
    (('http',), 'ie.ckan.net'),
    (('http',), 'it.ckan.net'),
    (('http',), 'rs.ckan.net'),
    (('http',), 'br.ckan.net'),
    (('http',), 'datos.codeandomexico.org'),
    (('http',), 'cz.ckan.net'),
    (('http',), 'dados.gov.br'),
    (('http',), 'dadosabertos.senado.gov.br'),
    (('http',), 'dados.novohamburgo.rs.gov.br'),
#   (('http',), 'data.gv.at'),
#   (('http',), 'data.linz.gv.at'),
#   (('http',), 'fi.thedatahub.org'),
    (('http',), 'data.sa.gov.au'),
#   (('http',), 'www.data.gc.ca'),
    (('http',), 'data.gov.sk'),
    (('http',), 'data.gov.uk'),
    (('http',), 'data.qld.gov.au'),
    (('http',), 'data.openpolice.ru'),
    (('http',), 'datacatalogs.org'),
    (('http',), 'www.datagm.org.uk'),
    (('http',), 'datakilder.no'),
#   (('http',), 'datospublicos.org'),
#   (('http',), 'data.denvergov.org'),
#   (('http',), 'ckan.emap.fgv.br'),
#   (('http',), 'open-data.europa.eu'),
#   (('http',), 'www.healthdata.gov'),
#   (('http',), 'www.hri.fi'),
#   (('http',), 'data.graz.gv.at'),
#   (('http',), 'daten.hamburg.de'),
    (('http',), 'data.codeforhouston.com'),
    (('http',), 'iatiregistry.org'),
    (('http',), 'data.klp.org.in'),
#   (('http',), 'thedatahub.kr'),
    (('http',), 'www.nosdonnees.fr'),
    (('http',), 'offenedaten.de'),
    (('http',), 'data.opencolorado.org'),
#   (('http',), 'catalog.opendata.in.th'),
    (('http',), 'www.opendatahub.it'),
    (('http',), 'dati.trentino.it'),
    (('http',), 'data.openva.com'),
    (('http',), 'www.opendata-hro.de'),
    (('http',), 'opengov.es'),
    (('http',), 'data.ottawa.ca'),
#   (('http',), 'data.overheid.nl'),
    (('http',), 'www.opendata.provincia.roma.it'),
    (('http',), 'publicdata.eu'),
    (('http',), 'www.daten.rlp.de'),
    (('http',), 'www.rotterdamopendata.nl'),
    (('http',), 'data.cityofsantacruz.com'),
#   (('http',), 'thedatahub.org'),
    (('http',), 'dati.toscana.it'),
]
# catalogs = []

def search(get, catalog, page):
    url = urljoin(catalog, '/api/search/dataset?q=&start=%d' % page)
    response = get(url)
    data = json.loads(response.text)
    return data['results']

def rest(get, catalog, datasetid):
    url = urljoin(catalog, '/api/rest/dataset/%s' % datasetid)
    try:
        response = get(url)
    except Exception as e:
        logger.error('Error downloading %s:\n%s' % (url, e))
    else:
        if response.ok:
            dataset = json.loads(response.text)
            dataset['catalog'] = catalog
            return dataset

def metadata(get, catalog):
    search_page = functools.partial(search, get, catalog)
    for page in itertools.count(1):
        try:
            result = search_page(page)
            if result == []:
                break
            else:
                for dataset_id in result:
                    try:
                        dataset = rest(get, catalog, dataset_id)
                    except Exception as e:
                        logger.error('Error at %s on page %d of %s:\n%s' % (dataset_id, page, catalog, e))
                    else:
                        if dataset != None:
                            yield dataset
        except Exception as e:
            logger.error('Error at page %d of %s:\n%s' % (page, catalog, e))

def download_url(dataset):
    for resource in dataset['resources']:
        if resource['format'] in {'tsv','csv'}:
            return resource['url']

def standardize(original):
    dl = download_url(original)
    standardized_dataset = {
        "url": '%(catalog)s/dataset/%(name)s' % original,
        "download_url": dl,
        "title": original["title"],
        "creator_name": original.get("maintainer", original["author"]),
        "creator_id": original.get("maintainer_email", original["author_email"]), 
        "date": datetime.datetime.strptime(original.get('metadata_modified', original['metadata_created']).split('.')[0], '%Y-%m-%dT%H:%M:%S'),
        "tags": original['tags'],
    }
    return standardized_dataset

def colnames(get, original):
    'function, dict -> list'
    dl = download_url(original)
    return [] if dl == None else _colnames(StringIO(get(dl).text))
