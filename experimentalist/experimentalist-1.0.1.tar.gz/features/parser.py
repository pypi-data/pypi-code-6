'''Config file parser'''

from features import config

def parse_config(conf, world):
    config = {}
    for name, stanza in conf:
        config[name] = config.Feature(name, world, stanza)
    return config
