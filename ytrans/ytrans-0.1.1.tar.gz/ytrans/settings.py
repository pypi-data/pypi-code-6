# coding: utf-8
import os
from ytrans.utils import to_unicode

from ytrans.exceptions import KeyNotFound


# Environment variable, that contains api key file
KEY_ENVIRON_VARIABLE = "YANDEX_TRANSLATOR_KEY"

# Translation service URL
URL = "https://translate.yandex.net/api/v1.5/tr.json/"

# encoding
ENCODING = 'utf-8'


def _get_environ_key_path():
    assert KEY_ENVIRON_VARIABLE in os.environ, (
        "Environment variable wasn't set "
        "{0}".format(to_unicode(KEY_ENVIRON_VARIABLE)))

    return os.environ[KEY_ENVIRON_VARIABLE]


def read_key(path_to_key=None):
    from ytrans.utils import check_existance_and_permissions
    if path_to_key is None:
        path_to_key = _get_environ_key_path()

    check_existance_and_permissions(path_to_key, permissions=os.R_OK)

    value = None
    with open(path_to_key, "rt") as f:
        for line in f.readlines():
            line = line.strip().replace(" ", "").rsplit("=", 1)
            if len(line) == 2:
                key, value = line
                if key.lower() == "key":
                    break
        else:
            raise KeyNotFound
    return value
