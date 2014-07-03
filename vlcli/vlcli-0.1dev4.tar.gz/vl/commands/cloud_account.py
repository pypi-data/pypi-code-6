import json
import logging
import requests
from vl.config.auth import get_auth


def add(cloud_provider, name, api_key, api_secret):
    logger = logging.getLogger(__name__)
    logger.debug('Adding cloud account...')
    logger.debug('Cloud Provider: %s, Name: %s', cloud_provider, name)

    auth_token = get_auth()
    if auth_token:
        url = 'http://api.veraxlabs.com/cloud-accounts'
        data = {'cloud_provider': cloud_provider, 'name': name, 'api_key': api_key, 'api_secret': api_secret}
        response = requests.post(url, auth=(auth_token, ''), data=json.dumps(data))

        logger.debug(response.status_code)
        logger.debug(response.text)
        return response.json()
    else:
        return {'error': 'user not logged in'}


def list_cloud_accounts(name):
    logger = logging.getLogger(__name__)
    logger.debug('List cloud accounts...')

    auth_token = get_auth()
    if auth_token:
        if name:
            url = 'http://api.veraxlabs.com/cloud-accounts/%s' % name
        else:
            url = 'http://api.veraxlabs.com/cloud-accounts'

        response = requests.get(url, auth=(auth_token, ''))
        logger.debug(response.status_code)
        logger.debug(response.text)
        return response.json()
    else:
        return {'error': 'user not logged in'}


def update(name, new_name, new_api_key, new_api_secret):
    logger = logging.getLogger(__name__)
    logger.debug('Updating cloud account...')
    logger.debug('Name: %s', name)

    auth_token = get_auth()
    if auth_token:
        url = 'http://api.veraxlabs.com/cloud-accounts/%s' % name
        data = {'name': name, 'new_name': new_name,
                'new_api_key': new_api_key, 'new_api_secret': new_api_secret}
        response = requests.patch(url, auth=(auth_token, ''), data=json.dumps(data))

        logger.debug(response.status_code)
        logger.debug(response.text)
        return response.json()
    else:
        return {'error': 'user not logged in'}


def delete(name):
    logger = logging.getLogger(__name__)
    logger.debug('Deleting cloud account...')
    logger.debug('Name: %s', name)

    auth_token = get_auth()
    if auth_token:
        url = 'http://api.veraxlabs.com/cloud-accounts/%s' % name
        response = requests.delete(url, auth=(auth_token, ''))

        logger.debug(response.status_code)
        logger.debug(response.text)
        return response.json()
    else:
        return {'error': 'user not logged in'}
