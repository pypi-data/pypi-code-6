import os.path
import json


def get_config_file():
    vl_dir = os.path.join(os.path.expanduser('~'), '.vl/')
    if not os.path.exists(vl_dir):
        os.makedirs(vl_dir, mode=0700)
    config_file = os.path.join(vl_dir, 'config')
    return config_file


def read_config():
    try:
        with open(get_config_file()) as config_file:
            return json.load(config_file)
    except IOError:
        return {}


def write_config(config):
    with open(get_config_file(), 'w') as config_file:
        json.dump(config, config_file, indent=4)


def get_auth():
    config = read_config()
    auth = None
    if 'auth_token' in config:
        auth = config['auth_token']
    return auth


def set_auth(token):
    config = read_config()
    config.update(token)
    write_config(config)


def delete_auth():
    config = read_config()
    if 'auth_token' in config:
        del config['auth_token']
    write_config(config)
