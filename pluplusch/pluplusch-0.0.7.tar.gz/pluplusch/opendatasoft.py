# -*- encoding: utf-8 -*-
import datetime
import json
from logging import getLogger
logger = getLogger(__name__)

catalogs = [
    (('http',), 'data.iledefrance.fr'),
    (('http',), 'opendata.paris.fr.opendatasoft.com'),
    (('http',), 'tourisme04.opendatasoft.com'),
    (('http',), 'tourisme62.opendatasoft.com'),
    (('http',), 'grandnancy.opendatasoft.com'),
    (('http',), 'bistrotdepays.opendatasoft.com'),
    (('http',), 'scisf.opendatasoft.com'),
    (('http',), 'pod.opendatasoft.com'),
    (('http',), 'dataratp.opendatasoft.com'),
    (('http',), 'public.opendatasoft.com'),
    (('http',), 'ressources.data.sncf.com'),
    (('http',), 'data.enseignementsup-recherche.gouv.fr'),
]

def metadata(get, catalog):
    '''
    Download everything from an OpenDataSoft catalog.
    '''

    # Search an OpenDataSoft portal, and add things.
    # I chose OpenDataSoft because they care a lot about metadata.
    response = get(catalog + '/api/datasets/1.0/search?rows=1000000')
    result = json.loads(response.text)['datasets']
    for dataset in result:
        dataset['catalog'] = catalog
        yield dataset

def standardize(original):
    '''
    Nonstandard metadata to standard metadata
    dict -> dict
    '''
    data = {
        'url': '%(catalog)s/explore/dataset/%(datasetid)s' % original,
        'download_url': '%(catalog)s/explore/dataset/%(datasetid)s/download/?format=csv' % original,
        "title": original['metas']['title'],
        "creator_name" : original['metas'].get('publisher'),
        "creator_id": None,
        "date": datetime.datetime.strptime(original['metas']['modified'], '%Y-%m-%dT%H:%M:%S+00:00'),
        "tags" : original['metas'].get('keyword',[]),
    }
    return data

def colnames(get, original):
    '''
    Get the column names for a dataset
    function, dict -> list
    '''
    # Ignore the get function; this is so that different modules'
    # colnames functions have the same signature.
    return [field['name'] for field in original['fields']] if 'fields' in original else []
