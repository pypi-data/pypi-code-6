""" Tools for validation. """

import itertools

from .exceptions import (
    InputRulesValidationError,
    InputStructureValidationError,
    OutputRulesValidationError,
    OutputStructureValidationError,
    RuleViolation,
    RulesValidationError,
    StopValidation,
    StructureValidationError,
    ValidationError,
    )
from .rules import (
    Required,
    )
from .schema_types import (
    Dict,
    DictOf,
    ListOf,
    )
from .util import (
    is_mapping,
    is_sequence,
    key_set,
    processing_decorator,
    select_processor,
    )


DEFAULT_RULES = (Required,)


def validate_input(*, schema, data, default_rules=DEFAULT_RULES):
    return _validate_and_transform_errors(
        schema=schema,
        data=data,
        default_rules=default_rules,
        structure_error=InputStructureValidationError,
        rules_error=InputRulesValidationError,
        )


def validate_output(*, schema, data, default_rules=DEFAULT_RULES):
    return _validate_and_transform_errors(
        schema=schema,
        data=data,
        default_rules=default_rules,
        structure_error=OutputStructureValidationError,
        rules_error=OutputRulesValidationError,
        )


validation = processing_decorator(validate_input, validate_output)


def _validate_and_transform_errors(structure_error, rules_error, **kwargs):
    try:
        return validate(**kwargs)
    except StructureValidationError as exc:
        raise structure_error(*exc.errors)
    except RulesValidationError as exc:
        raise rules_error(*exc.errors)


def validate(*, schema, data, default_rules=DEFAULT_RULES):
    if schema is None:
        return data

    if default_rules is None:
        default_rules = tuple()

    validated_data = _validate_structure(schema=schema, data=data)
    _validate_rules(
        schema=schema, data=validated_data, default_rules=default_rules
        )

    return validated_data


def _validate_structure(schema, data):
    try:
        return _validate_data(
            schema=schema,
            data=data,
            location=tuple(),
            validation_map=STRUCTURE_MAP,
            )
    except ValidationError as exc:
        raise StructureValidationError(*exc.errors)


def _validate_rules(schema, data, default_rules):
    try:
        _validate_data(
            schema=schema,
            data=data,
            location=tuple(),
            default_rules=default_rules,
            validation_map=RULES_MAP,
            )
    except ValidationError as exc:
        raise RulesValidationError(*exc.errors)


def _validate_data(schema, data, validation_map, **kwargs):
    """ Call the appropriate validation function, depending on `schema` type.
        If no exception is raised, return `data` unchanged. """

    validation_function = select_processor(schema, validation_map)
    return validation_function(schema=schema, data=data, **kwargs)


def _validate_scalar_structure(schema, data, location):
    """ `data` must be an instance of `schema` type. """
    if isinstance(data, schema) or data is None:
        return data

    schema_name = '`{}`'.format(schema.__name__)

    raise_type_validation_error(schema_name, data, location)


def _validate_scalar_rules(schema, **kwargs):
    schema_tuple = (schema,)
    _validate_tuple_rules(schema=schema_tuple, **kwargs)


def _validate_tuple_structure(schema, **kwargs):
    """ Validate a tuple. The first tuple element is the actual schema. """
    return _validate_data(
        schema=schema[0], validation_map=STRUCTURE_MAP, **kwargs
        )


def _validate_tuple_rules(schema, data, location, default_rules):
    rules = get_rules(schema, default_rules)

    apply_rules(rules, data, location)

    _validate_data(
        schema=schema[0],
        data=data,
        validation_map=RULES_TUPLE_MAP,
        location=location,
        default_rules=default_rules
        )


def get_rules(schema, default_rules):
    rules = schema[1:]

    override_defaults = get_override_defaults(rules)

    if override_defaults:
        return rules

    return default_rules + rules


def get_override_defaults(rules):
    if not rules:
        return False
    return getattr(rules[0], 'override_defaults', False)


def apply_rules(rules, data, location):
    for rule in rules:
        try:
            rule(data)
        except RuleViolation as exc:
            error_dict = make_error_dict(
                location=location + exc.location,
                code=exc.code,
                message=exc.message,
                data=exc.data,
                )
            raise ValidationError(error_dict)
        except StopValidation:
            break


def _validate_dict_structure(
    # pylint: disable=dangerous-default-value
    schema, data, location, optional_keys=set(), strip_extras=False
    ):
    confirm_mapping(data, location)

    missing_errors = get_missing_errors(schema, data, optional_keys, location)

    resolved_data = resolve_data_dict(schema, data, strip_extras)

    not_allowed_errors = get_not_allowed_errors(schema, resolved_data, location)

    validated_items, captured_errors_lists = (
        get_validated_items_and_capture_errors(schema, resolved_data, location)
        )

    errors_chain = itertools.chain(
        missing_errors, not_allowed_errors, *captured_errors_lists
        )
    errors = list(errors_chain)

    raise_if_errors(errors)

    return dict(validated_items)


def get_missing_errors(schema, data, optional_keys, location):
    schema_keys = key_set(schema)
    data_keys = key_set(data)

    required_keys = schema_keys - optional_keys
    missing_keys = required_keys - data_keys

    return [
        make_error_dict(
            location=location + (key,),
            code='MISSING',
            message='Key missing.',
            data=None
            )
        for key in missing_keys
        ]


def resolve_data_dict(schema, data, strip_extras):
    if not strip_extras:
        return data

    schema_keys = key_set(schema)
    data_keys = key_set(data)

    actual_keys = schema_keys & data_keys

    return {
        key: value
        for key, value in data.items()
        if key in actual_keys
        }


def get_not_allowed_errors(schema, resolved_data, location):
    schema_keys = key_set(schema)
    resolved_data_keys = key_set(resolved_data)

    not_allowed_keys = resolved_data_keys - schema_keys

    return [
        make_error_dict(
            location=location + (key,),
            code='NOT_ALLOWED',
            message='Key not allowed.',
            data=None
            )
        for key in not_allowed_keys
        ]


def get_validated_items_and_capture_errors(schema, resolved_data, location):
    schema_keys = key_set(schema)
    resolved_data_keys = key_set(resolved_data)

    result = tuple(zip(*[
        get_validated_item_and_capture_errors(
            schema=schema[key],
            data=resolved_data[key],
            location=location + (key,),
            key=key,
            )
        for key in schema_keys & resolved_data_keys
        ]))

    if not result:
        return tuple([tuple(), tuple()])

    return result


def get_validated_item_and_capture_errors(key, **kwargs):
    try:
        validated_data = _validate_data(validation_map=STRUCTURE_MAP, **kwargs)
    except ValidationError as exc:
        return (key, None), exc.errors

    return (key, validated_data), tuple()


def _validate_dict_rules(schema, data, location, **kwargs):
    schema_keys = key_set(schema)
    data_keys = key_set(data)

    captured_errors_lists = [
        capture_errors(
            schema=schema[key],
            data=data[key],
            location=location + (key,),
            validation_map=RULES_MAP,
            **kwargs
            )
        for key in schema_keys & data_keys
        ]

    errors_chain = itertools.chain(*captured_errors_lists)
    errors = list(errors_chain)

    raise_if_errors(errors)


def capture_errors(**kwargs):
    try:
        _validate_data(**kwargs)
    except ValidationError as exc:
        return exc.errors

    return tuple()


def raise_if_errors(errors):
    if errors:
        raise ValidationError(*errors)


def _validate_Dict_structure(schema, **kwargs):
    kwargs.update(schema.validate_structure_kwargs)
    return _validate_dict_structure(schema=schema.schema, **kwargs)


def _validate_Dict_rules(schema, **kwargs):
    return _validate_dict_rules(schema=schema.schema, **kwargs)


def _validate_DictOf_structure(data, location, **kwargs):
    confirm_mapping(data, location)
    return _validate_DictOf(
        data=data, location=location, validation_map=STRUCTURE_MAP, **kwargs
        )


def _validate_DictOf_rules(**kwargs):
    _validate_DictOf(validation_map=RULES_MAP, **kwargs)


def _validate_DictOf(schema, data, **kwargs):
    """ Validate a dictionary with arbitrary keys.
        Validate each value from `data` against `schema.schema`.
        `schema` is a `DictOf` instance. """

    schema_dict = {key: schema.schema for key in data.keys()}

    return _validate_data(schema=schema_dict, data=data, **kwargs)


def _validate_list_structure(data, location, **kwargs):
    confirm_sequence(data, location)
    return _validate_list(
        data=data, location=location, validation_map=STRUCTURE_MAP, **kwargs
        )


def _validate_list_rules(**kwargs):
    _validate_list(validation_map=RULES_MAP, **kwargs)


def _validate_list(schema, data, **kwargs):
    """ Validate a list.
        Validate each value from `data` against the corresponding `schema`
        value.
        `schema` and `data` must have the same length. """

    schema_dict = dict(enumerate(schema))
    data_dict = dict(enumerate(data))

    _validate_data(schema=schema_dict, data=data_dict, **kwargs)

    return data


def _validate_ListOf_rules(**kwargs):
    _validate_ListOf(validation_map=RULES_MAP, **kwargs)


def _validate_ListOf_structure(data, location, **kwargs):
    confirm_sequence(data, location)
    return _validate_ListOf(
        data=data, location=location, validation_map=STRUCTURE_MAP, **kwargs
        )


def _validate_ListOf(schema, data, **kwargs):
    """ Validate a list with arbitrary length.
        Validate each value from `data` against `schema.schema`.
        `schema` is a `ListOf` instance. """
    schema_list = [schema.schema for item in data]

    return _validate_list(schema=schema_list, data=data, **kwargs)


def _validate_pass(**kwargs): # pylint: disable=unused-argument
    """ This function is used to prevent an endless loop between
        `_validate_tuple_rules` and `_validate_scalar_rules`. """
    pass


def confirm_mapping(data, location):
    if is_mapping(data):
        return

    raise_type_validation_error(
        schema_name='mapping', data=data, location=location
        )


def confirm_sequence(data, location):
    if is_sequence(data):
        return

    raise_type_validation_error(
        schema_name='sequence', data=data, location=location
        )


def raise_type_validation_error(schema_name, data, location):
    message = 'Expected {expected}; got `{actual}`.'.format(
        expected=schema_name, actual=type(data).__name__
        )

    error_dict = make_error_dict(
        location=location, code='TYPE', message=message, data=None
        )

    raise ValidationError(error_dict)


def make_error_dict(location, code, message, data):
    return {
        'location': location,
        'code': code,
        'message': message,
        'data': data,
        }


STRUCTURE_MAP = (
    (type, _validate_scalar_structure),
    (tuple, _validate_tuple_structure),
    (dict, _validate_dict_structure),
    (Dict, _validate_Dict_structure),
    (DictOf, _validate_DictOf_structure),
    (list, _validate_list_structure),
    (ListOf, _validate_ListOf_structure),
    )


RULES_MAP = (
    (type, _validate_scalar_rules),
    (tuple, _validate_tuple_rules),
    (dict, _validate_dict_rules),
    (Dict, _validate_Dict_rules),
    (DictOf, _validate_DictOf_rules),
    (list, _validate_list_rules),
    (ListOf, _validate_ListOf_rules),
    )


RULES_TUPLE_MAP = (
    (type, _validate_pass),
    (tuple, _validate_tuple_rules),
    (dict, _validate_dict_rules),
    (Dict, _validate_Dict_rules),
    (DictOf, _validate_DictOf_rules),
    (list, _validate_list_rules),
    (ListOf, _validate_ListOf_rules),
    )
