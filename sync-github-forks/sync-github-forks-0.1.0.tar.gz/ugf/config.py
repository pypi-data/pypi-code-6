from os import environ as env
from os.path import join as path_join


import yaml


CONFIG_FILE_PATH = path_join(env['HOME'], '.github-api.yml')


class ConfigurationError(Exception):
    pass


class Configuration:
    config = None

    def __init__(self):
        with open(CONFIG_FILE_PATH, 'rb') as f:
            self.config = yaml.load(f)

        self.ensure_valid_config()

    def ensure_valid_config(self):
        if type(self.config) is not dict:
            raise TypeError('Invalid format configuration file, YAML must represent a dictionary')

        key_missing_format = 'Key missing in YAML file: %s'

        for key in ('username', 'password'):
            if key not in self.config:
                raise ConfigurationError(key_missing_format % key)

    def get_user(self):
        return self.config['username']

    def get_password(self):
        return self.config['password']
