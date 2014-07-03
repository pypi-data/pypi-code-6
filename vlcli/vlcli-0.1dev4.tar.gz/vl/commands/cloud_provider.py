import logging
import requests
from vl.config.auth import get_auth


def list_cloud_providers(name):
    logger = logging.getLogger(__name__)
    logger.debug('List cloud providers...')

    auth_token = get_auth()
    if auth_token:
        if name:
            url = 'http://api.veraxlabs.com/cloud-providers/%s' % name
        else:
            url = 'http://api.veraxlabs.com/cloud-providers'

        response = requests.get(url, auth=(auth_token, ''))
        logger.debug(response.status_code)
        logger.debug(response.text)
        return response.json()
    else:
        return {'error': 'user not logged in'}
