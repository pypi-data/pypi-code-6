"""Utilities for initializing the database."""

import os

from django.conf import settings

from csvkit import CSVKitReader, join


def get_data(path, encoding='utf-8'):
    """Load CSV formatted data from a a file.

    Args:
        directory (str): the directory to load the data from.
        filename (str): the name of the file in the directory

    Return:
        a table containing the data
    """
    with open(path, 'rb') as fp:
        return list(CSVKitReader(fp, encoding=encoding))


def get_languages():
    """Get the list of languages supported by the model.

    Returns:
        a list of the language suffixes from the LANGUAGES setting.
    """
    return [lang[0] for lang in settings.LANGUAGES]


def filter_dict(keys, dictionary, default=''):
    """Filter a dictionary so it only contains a given list of keys.

    If the dictionary does not contain a given key then it is added
    to the result with a value given by the argument default.

    Args:
        keys (list): the names of the keys to select.
        data (dict): dictionary to filter
        default (str): the value used for a missing key.

    Returns:
        a dict that only include keys from the list in fields
    """
    result = {}
    for key in keys:
        if key in dictionary:
            result[key] = dictionary[key]
        else:
            result[key] = default
    return result


def create_objects(model, fields, table):
    """Create model objects from a table of data.

    The names of the object attributes are defined in the first row of the
    table. The data in the table is filtered to only include values for the
    names in the fields argument.

    Args:
        model (class): the Model class.
        fields (list): the names of the columns to select.
        table (list): the table of data for the objects.

    Raises:
        IntegrityError if the object already exists.
    """
    keys = table[0]
    for values in table[1:]:
        model.objects.create(**filter_dict(fields, dict(zip(keys, values))))
