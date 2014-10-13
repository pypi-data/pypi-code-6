from collections import MutableMapping, MutableSequence
from functools import partial
from operator import delitem

from jsonpath_rw import parse

from .utils import (
    build_converter, command, act_on_path, 
    root, set_on_path, root
    )

from . import shell as sh


@command
def write(json, *args):
    '''Calls the write method on the JSONConfigParser object.
    Implemented for interactive shell use.
    '''
    json.write()

@command
def shell(json, *args):
    '''Launches interactive shell prompt.'''
    sh.run(json)

@command
def view(json, path):
    '''A stored command for the view method of the JSONConfigParser
    object which pretty prints the endpoint's value.

    :param json JSONConfigParser: The JSON representation to act on
    :param path str: A string representation of a JSONpath endpoint
    :returns None:
    '''
    json.view(path)

@command
def add_file(json, other):
    '''Updates the JSONConfigParser object with another JSON file.

    :param json JSONConfigParser: The JSON representation to act on
    :param other str: A filepath to the JSON file to concatenate.
    :returns None:
    '''
    json.read(other)

@command
def add_field(json, path, value, convert=False):
    '''Adds another field to the JSONConfigParser object.

    :param json JSONConfigParser: The JSON representation to act on.
    :param path str: A string representation of a JSONpath endpoint,
        the end point should be the new field to add
    :param value: The value to place at the new endpoint
    :param convert str: A string representing the steps to convert the value to
        it's final form.
    :returns None:
    '''

    if convert:
        converter = build_converter(convert)
        value = converter(value)

    set_on_path(json, path, value)

@command
def append(json, path, value, multi=False, convert=False):
    '''Adds a value to a JSON collection at the endpoint.

    :param json JSONConfigParser: The JSON representation to act on.
    :param path str: A string representation of a JSONpath endpoint
        If the endpoint is not an array/list or object/dict, this function will
        raise a TypeError
    :param value: The place to place into the specified endpoint
    :param multi bool: If true, add the value to every matching endpoint.
        The default is False and if multiple endpoints are present this function
        will raise an AttributeError
    :param convert str: A string representing the steps to convert the value to
        it's final form.
    :returns None:
    '''
    expr = parse(path)
    matches = expr.find(json)

    if not all(isinstance(m.value, (MutableMapping, MutableSequence)) for m \
        in matches):
            raise TypeError("Expected mutable container at endpoint for {}."
                "".format(path))

    if len(matches) > 1 and not multi:
        raise AttributeError("Multiple paths found for {}. Please specify the "
        "multi flag if this is intended.".format(path))

    def guess_action(container):
        '''Guess if we're dealing with a dict/object endpoint
        or a list/array endpoint.

        Returns a callable that will either append or update depending on the
        container type.
        '''
        if isinstance(container, MutableMapping):
            return lambda j, f, v: j[f].update(v)
        return lambda j, f, v: j[f].append(v)

    if convert:
        converter = build_converter(convert)
        value = converter(value)

    for match in matches:
        action = guess_action(match.value)
        action = partial(action, v=value)
        act_on_path(json, str(match.full_path), action)

@command
def delete(json, path=False):
    '''Deletes a JSONPath endpoint from the JSONConfigParser object.

    :param json JSONConfigParser: The JSON representation to act on.
    :param path str: A string representation of a JSONpath endpoint. If False,
        it sets the JSON representation to a blank dictionary.
    '''
    if not path or path == root:
        json = {}
    else:
        act_on_path(json, path, delitem)

@command
def edit(json, path, value, convert=False):
    '''Updates the value at the JSONPath endpoint.

    :param json JSONConfigParser: The JSON representation to act on.
    :param path str: A string representation of a JSONpath endpoint
    :param value: The value to be placed at the endpoint
    :param convert str: A string representing the steps to convert the value to
        it's final form.
    '''

    if convert:
        converter = build_converter(convert)
        value = converter(value)

    set_on_path(json, path, value)
