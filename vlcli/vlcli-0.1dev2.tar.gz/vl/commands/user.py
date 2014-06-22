import json
import logging
import requests
from vl.config.auth import set_auth, delete_auth


def register(name, email, password):
    logger = logging.getLogger(__name__)
    logger.debug('Registering user...')
    logger.debug('Name: %s, Email: %s', name, email)

    data = json.dumps({'email': email, 'name': name, 'password': password})
    response = requests.post('http://api.veraxlabs.com/user', data=data)

    logger.debug(response.status_code)
    logger.debug(response.text)
    return response.json()


def activate(email, password, code):
    logger = logging.getLogger(__name__)
    logger.debug('User activation ...')
    logger.debug('Email: %s', email)

    data = json.dumps({'code': code})
    response = requests.put('http://api.veraxlabs.com/user/%s/activation' % email, auth=(email, password), data=data)

    logger.debug(response.status_code)
    logger.debug(response.text)
    return response.json()


def resend_activation(email, password):
    logger = logging.getLogger(__name__)
    logger.debug('Resending activation code...')
    logger.debug('Email: %s', email)

    response = requests.post('http://api.veraxlabs.com/user/%s/activation' % email, auth=(email, password))

    logger.debug(response.status_code)
    logger.debug(response.text)
    return response.json()


def login(email, password):
    logger = logging.getLogger(__name__)
    logger.debug('Logging in...')
    logger.debug('Email: %s', email)

    response = requests.post('http://api.veraxlabs.com/user/%s/token' % email, auth=(email, password))

    logger.debug(response.status_code)
    set_auth(response.json())

    return {'success': 'logged in'}


def logout():
    logger = logging.getLogger(__name__)
    logger.debug('Logging out...')

    delete_auth()

    return {'success': 'logged out'}


def forgot_password(email):
    logger = logging.getLogger(__name__)
    logger.debug('Forgot password...')
    logger.debug('Email: %s', email)

    response = requests.post('http://api.veraxlabs.com/user/%s/password' % email)

    logger.debug(response.status_code)
    logger.debug(response.text)
    return response.json()


def reset_password(email, new_password, code):
    logger = logging.getLogger(__name__)
    logger.debug('Resetting password...')
    logger.debug('Email: %s', email)

    data = json.dumps({'new_password': new_password, 'code': code})
    response = requests.put('http://api.veraxlabs.com/user/%s/password' % email, data=data)

    logger.debug(response.status_code)
    logger.debug(response.text)
    return response.json()


def change_password(email, old_password, new_password):
    logger = logging.getLogger(__name__)
    logger.debug('Changing password...')
    logger.debug('Email: %s', email)

    data = json.dumps({'new_password': new_password, 'old_password': old_password})
    response = requests.put('http://api.veraxlabs.com/user/%s/password' % email, data=data)

    logger.debug(response.status_code)
    logger.debug(response.text)
    return response.json()


def update(email, password, new_name, new_email):
    logger = logging.getLogger(__name__)
    logger.debug('Updating user...')
    logger.debug('Email: %s, New Name: %s, New Email: %s', email, new_name, new_email)

    data = json.dumps({'new_email': new_email, 'new_name': new_name})
    response = requests.put('http://api.veraxlabs.com/user/%s' % email, auth=(email, password), data=data)

    logger.debug(response.status_code)
    logger.debug(response.text)
    return response.json()
