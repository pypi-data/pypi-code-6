import os

import requests
from picklecache import cache

@cache(os.path.join(os.path.expanduser('~'), '.company'))
def get(country_code, query):
    '''
    country_code :: Open Corporates country code | None
    query :: str
    '''
    baseurl = 'https://opencorporates.com/reconcile'
    url = baseurl if country_code == None else base_url + '/' + country_code
    params = {'query': query}
    return requests.get(url, params = params)


def reconcile(country_code, name):
    query = name.replace('/','%2F') # %2F so that pickle_warehouse doesn't make directories
    response = get(country_code, query)
    if response.ok:
        return response.json().get('result')
    else:
        raise ValueError(response)
