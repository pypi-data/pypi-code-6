import os
import json


_config = {}


def config():
    global _config
    return _config


def _load_config(path):
    with open(path) as fi:
        return json.load(fi)


def load_config():
    global _config
    _config = _load_config(os.environ['HOME'] + '/.eyes_on_me_rc')


def mock_config(mocked_config):
    global _config
    _config = mocked_config
