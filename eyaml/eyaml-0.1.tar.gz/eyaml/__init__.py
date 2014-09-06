import os
import yaml


class EnvLoader(yaml.SafeLoader):

    def construct_env(self, node):
        default = None
        if node.id == 'scalar':
            key = self.construct_scalar(node)
        elif node.id == 'mapping':
            mapping = self.construct_mapping(node)
            key = mapping['key']
            default = mapping['default']
        return os.getenv(key, default=default)


EnvLoader.add_constructor(
    u'tag:yaml.org,2002:env',
    EnvLoader.construct_env
)


def load(file_path):
    return _load(open(file_path, 'rb'))


def _load(stream, Loader=EnvLoader):
    return yaml.load(stream, Loader)
