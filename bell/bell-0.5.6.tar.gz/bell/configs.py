# coding=utf8

import os

import toml

from bell.utils import normjoin, update_nested_dict


class Configs(dict):

    current_directory = os.path.dirname(__file__)
    default_configs_path = normjoin(current_directory, 'res',
                                        'configs.toml')
    default_configs = toml.loads(open(default_configs_path).read())

    def __init__(self):
        super(Configs, self).__init__()
        self.update(Configs.default_configs)

    def update(self, other):
        return update_nested_dict(self, other)


configs = Configs()
