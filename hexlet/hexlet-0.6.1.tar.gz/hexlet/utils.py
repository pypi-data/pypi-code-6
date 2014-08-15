import yaml
import os
import pip
import time
import sys
import os
import click
from hexlet import exceptions

if sys.version_info > (3,0):
    from xmlrpc import client as xmlrpclib
else:
    import xmlrpclib


def get_app_path():
    if os.environ.get('APP_PATH', ''):
        app_path = os.environ['APP_PATH']
    else:
        app_path = click.get_app_dir('Hexlet', force_posix=True)
    return app_path


def get_credentials_file_name():
    return "credentials"


def get_config_path():
    return os.path.join(get_app_path(),
                        get_credentials_file_name())


def value_for(key):
    try:
        with open(get_config_path(), 'r') as stream:
            return yaml.load(stream)[key]
    except IOError:
        raise exceptions.ConfigError()


def write_config(data):
    app_path = get_app_path()
    config_path = get_config_path()

    if not os.path.isdir(app_path):
        os.mkdir(app_path)

    write_config_path(data, config_path)


def write_config_path(data, path):
    with open(path, 'w+') as outfile:
        outfile.write(yaml.dump(data, default_flow_style=False))

def build_key_value(params):
    def iter(params, path, base):
        if isinstance(params, dict):
            for k, v in params.items():
                path_copy = list(path)
                path_copy.append("[%s]" % k)
                if isinstance(v, dict) or isinstance(v, list):
                    iter(v, path_copy, base)
                else:
                    base["".join(path_copy)] = v
        elif isinstance(params, list):
            for idx, v in enumerate(params):
                path_copy = list(path)
                path_copy.append("[%s]" % idx)
                if isinstance(v, dict) or isinstance(v, list):
                    iter(v, path_copy, base)
                else:
                    base["".join(path_copy)] = v

    base = {}
    for k, v in params.items():
        path = []
        path.append(k)
        iter(v, path, base)

    return base

def get_api_key_header(api_key=""):
    if not api_key:
        api_key = value_for('hexlet_api_key')
    return {'X-Hexlet-Api-Key': api_key}
