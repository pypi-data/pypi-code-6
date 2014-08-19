""" Tools for coercion. """

from .schema_types import (
    Dict,
    DictOf,
    ListOf
    )
from .util import (
    is_mapping,
    is_sequence,
    process_data,
    processing_decorator,
    select_function
    )


class CoercionManagerBase:
    """ Defines methods for input and output coercion.

        To define a coercion method, add an instance method named like this:
            `coerce_{routine}_{type_name}`
        - 'routine' is either 'input' or 'output'.
        - 'type_name' is the `__name__` attribute value of the target type.

        `@coercion_manager.coercion` decorator adds input/output coercion to a
        decorated function. """

    def coerce_input(self, schema, data):
        """ Coerce input data. """
        return process_data(_coerce_data, schema, data, self, 'input')

    def coerce_output(self, schema, data):
        """ Coerce output data. """
        return process_data(_coerce_data, schema, data, self, 'output')

    @property
    def coercion(self):
        """ Returns a decorator.
            Add input/output coercion to the wrapped function. """
        return processing_decorator(self.coerce_input, self.coerce_output)


def _coerce_data(schema, data, manager, routine):
    """ Call the appropriate coercion function, depending on `schema` type.
        Return coerced data.

        `routine` is either `input` or `output`. """
    coercion_map = [
        (type, _coerce_scalar),
        (dict, _coerce_dict),
        (Dict, _coerce_Dict),
        (DictOf, _coerce_DictOf),
        (list, _coerce_list),
        (ListOf, _coerce_ListOf),
        (tuple, _coerce_tuple)
        ]

    coercion_function = select_function(schema, coercion_map)
    return coercion_function(schema, data, manager, routine)


def _coerce_scalar(schema, data, manager, routine):
    """ Get the appropriate coercion method from `manager`, depending on
        `schema`.
        If no coercion method found, return `data` unchanged. """
    method_name = 'coerce_{routine}_{typename}'.format(
        routine=routine,
        typename=schema.__name__
        )

    try:
        coercion_method = getattr(manager, method_name)
    except AttributeError:
        return data

    return coercion_method(data)


def _coerce_dict(schema, data, manager, routine):
    """ Coerce a dictionary.
        Coerce each value from `data` with the corresponding `schema` value.
        Extra elements from `data` are returned unchanged. """
    if not is_mapping(data):
        return data

    schema_keys = set(schema.keys())
    data_keys = set(data.keys())

    result = {}

    for key in schema_keys & data_keys:
        result[key] = _coerce_data(schema[key], data[key], manager, routine)

    for key in data_keys - schema_keys:
        result[key] = data[key]

    return result


def _coerce_Dict(schema, *pargs):
    return _coerce_dict(schema.schema, *pargs)


def _coerce_DictOf(dict_of, data, manager, routine):
    """ Coerce a dictionary with arbitrary keys.
        Coerce each value from `data` with `dict_of.schema`. """
    if not is_mapping(data):
        return data

    schema_dict = {key: dict_of.schema for key in data.keys()}

    return _coerce_dict(schema_dict, data, manager, routine)


def _coerce_list(schema, data, manager, routine):
    """ Coerce a list.
        Coerce each value from `data` with the corresponding `schema` value.
        Extra elements from `data` are returned unchanged. """
    if not is_sequence(data):
        return data

    schema_dict = dict(enumerate(schema))
    data_dict = dict(enumerate(data))

    result_dict = _coerce_dict(schema_dict, data_dict, manager, routine)
    return [value for key, value in sorted(result_dict.items())]


def _coerce_ListOf(list_of, data, manager, routine):
    """ Coerce a list with arbitrary length.
        Coerce each value from `data` with `list_of.schema`. """
    if not is_sequence(data):
        return data

    schema_list = [list_of.schema for item in data]

    return _coerce_list(schema_list, data, manager, routine)


def _coerce_tuple(schema_tuple, data, manager, routine):
    """ Coerce a tuple.
        The first tuple element is `schema`.
        `data` is coerced with `schema`.
        The remaining tuple elements are validators; they are ignored during
        coercion. """
    schema = schema_tuple[0]

    return _coerce_data(schema, data, manager, routine)
