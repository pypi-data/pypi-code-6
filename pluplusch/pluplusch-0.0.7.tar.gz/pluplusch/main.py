import os
from concurrent.futures import ThreadPoolExecutor
import logging
import functools
from traceback import print_exc
from io import StringIO
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from thready import threaded
from pickle_warehouse import Warehouse
from picklecache import cache
import requests

import pluplusch.index as i

cache_dir = os.path.join(os.path.expanduser('~'), '.pluplusch')

def getlogger():
    logger = logging.getLogger(__name__)
    fp_stream = logging.StreamHandler()
    fp_stream.setLevel(logging.ERROR)
    logger.addHandler(fp_stream)
    return logger
logger = getlogger()

def _pluplusch(get, catalogs = [], standardize = True, force_colnames = False):
    '''
    pluplusch downloads data from open data websites. Here are
    its inputs.

    catalogs
        List of catalogs to download, each item being either
        a full URL string, including the scheme, or a tuple
        of the full URL string and the software, in case pluplusch
        doesn't know about the catalog
    standardize
        Should the metadata schema be standardized across softwares?
    force_colnames
        Should the full data file be downloaded if needed?
        (This is only relevant if standardize is True.)

    It returns a generator of datasets.
    '''

    # Use all catalogs by default.
    if catalogs == []:
        catalogs = list(i.all_catalogs())

    # Detect catalog softwares if they're not specified.
    catalog_names = [(catalog[0] if len(catalog) == 2 else catalog) for catalog in catalogs]
    catalog_softwares = [(catalog[1] if len(catalog) == 2 else i.catalog_to_software(catalog)) for catalog in catalogs]
    catalog_names_softwares = list(zip(catalog_names, catalog_softwares))

    # Threading
    queue = []
    running = set(catalog_names)
    submodules = i.submodules()

    def enqueue_datasets(catalog_name_software):
        catalog_name, catalog_software = catalog_name_software
        generator = submodules[catalog_software].metadata(get, catalog_name)
        while True:
            try:
                dataset = next(generator)
            except StopIteration:
                break
            except:
                not_file = StringIO()
                print_exc(file = not_file)
                logger.error('Error at %s:\n%s\n' % (catalog_name, not_file.getvalue()))
            else:
                if standardize:
                    out = submodules[catalog_software].standardize(dataset)
                    if out['download_url'] != None:
                        out['download_url'] = urljoin(out['url'], out['download_url'])
                    if catalog_software == 'ckan' and not force_colnames:
                        # Getting column names from CKAN involves downloading all the data
                        out['colnames'] = set()
                    else:
                        out['colnames'] = submodules[catalog_software].colnames(get, dataset)
                else:
                    out = dataset
                    out['_catalog'] = catalog_name
                    out['_software'] = catalog_software
                queue.append(out)
        running.remove(catalog_name)

    threaded(catalog_names_softwares, enqueue_datasets, join = False)

    from time import sleep
    while len(running) > 0 or queue != []:
        sleep(0.0001)
        if queue != []:
            yield queue.pop(0)

def get(url, cache_dir = cache_dir):
    @cache(cache_dir, mutable = False)
    def _get(url):
        return requests.get(url, verify = False)

    try:
        response = _get(url)
    except Exception as e:
        logger.error('Could not download %s:\n%s' % (url, e))
        raise e
    if response.ok:
        return response
    else:
        raise ValueError('%d response at %s' % (response.status_code, url))

def pluplusch(catalogs = [], standardize = True, force_colnames = False,
              get = get):
    '''
    pluplusch downloads data from open data websites. Here are
    its inputs.

    get
        Function that takes a url and returns a response
    catalogs
        List of catalogs to download, each item being either
        a full URL string, including the scheme, or a tuple
        of the full URL string and the software, in case pluplusch
        doesn't know about the catalog
    standardize
        Should the metadata schema be standardized across softwares?
    force_colnames
        Should the full data file be downloaded if needed for colnames?
        (This is only relevant if standardize is True.)

    It returns a generator of datasets.
    '''

    # Ugh Python2
    for x in _pluplusch(get, catalogs = catalogs, standardize = standardize,
                        force_colnames = force_colnames):
        yield x
