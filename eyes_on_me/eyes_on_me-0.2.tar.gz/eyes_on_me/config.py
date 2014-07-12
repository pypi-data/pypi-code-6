import os
import json


def load_config(path):
    with open(path) as fi:
        return json.load(fi)


config = load_config(os.environ['HOME'] + '/.eyes_on_me_rc')
