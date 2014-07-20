from __future__ import absolute_import
import yaml
import os
import endpoints

_apis = {}
_default_api_name = None

base_directory = os.getcwd()


def add(config_file, default=False):
    global _apis, _default_api_name

    config = load_config_file(config_file)
    api = endpoints.api(**config)
    _apis[config['name']] = api

    if default:
        _default_api_name = config['name']

    return api


def get(name=None):
    if not name:
        name = _default_api_name
    return _apis.get(name)


def default():
    return get()


def get_all():
    return _apis.values()


def load_config_file(config_file):
    with open(os.path.join(base_directory, config_file)) as f:
        config = yaml.load(f)

    # Replace constants
    recursive_replace(config, 'API_EXPLORER_CLIENT_ID', endpoints.API_EXPLORER_CLIENT_ID)
    recursive_replace(config, 'USERINFO', 'https://www.googleapis.com/auth/userinfo.email')

    auth_level = config.get('auth_level', 'optional')
    config['auth_level'] = {
        'required': endpoints.AUTH_LEVEL.REQUIRED,
        'optional': endpoints.AUTH_LEVEL.OPTIONAL,
        'optional_continue': endpoints.AUTH_LEVEL.OPTIONAL_CONTINUE,
        'none': endpoints.AUTH_LEVEL.NONE
    }.get(auth_level)

    return config


def recursive_replace(container, old, new):
    if isinstance(container, dict):
        for key, value in container.iteritems():
            if value == old:
                container[key] = new
            if isinstance(value, (dict, list)):
                recursive_replace(value, old, new)
    else:
        for ix, value in enumerate(container):
            if value == old:
                container[ix] = new
