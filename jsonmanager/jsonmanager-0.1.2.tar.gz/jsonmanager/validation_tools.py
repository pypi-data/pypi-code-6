""" Tools for validation. """

import collections
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
    Nullable,
    Required,
    )
from .schema_types import (
    Call,
    Dict,
    DictOf,
    ListOf,
    )
from .util import (
    is_mapping,
    is_sequence,
    key_set,
    processing_decorator,
    select_function,
    )


_NotSet = object()


DEFAULT_INPUT_RULES = (Required,)
DEFAULT_OUTPUT_RULES = (Nullable,)


class ValidationDefaults:
    def __init__(
        self,
        default_rules=tuple(),
        dict_optional_keys=tuple(),
        dict_strip_extras=False,
        list_strip_extras=False,
        ):
        if default_rules is None:
            default_rules = tuple()

        self.default_rules = default_rules

        dict_optional_keys_set = set(dict_optional_keys)

        self.validate_dict_structure_kwargs = dict(
            optional_keys=dict_optional_keys_set,
            strip_extras=dict_strip_extras
            )

        self.validate_list_structure_kwargs = dict(
            optional_keys=set(),
            strip_extras=list_strip_extras,
            )


INPUT_DEFAULTS = ValidationDefaults(default_rules=DEFAULT_INPUT_RULES)
OUTPUT_DEFAULTS = ValidationDefaults(default_rules=DEFAULT_OUTPUT_RULES)


def validate_input(*, schema, data, defaults=INPUT_DEFAULTS):
    return _validate_and_transform_errors(
        schema=schema,
        data=data,
        defaults=defaults,
        structure_error=InputStructureValidationError,
        rules_error=InputRulesValidationError,
        )


def validate_output(*, schema, data, defaults=OUTPUT_DEFAULTS):
    return _validate_and_transform_errors(
        schema=schema,
        data=data,
        defaults=defaults,
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


def validate(*, schema, data, defaults=None):
    if schema is None:
        return data

    if defaults is None:
        defaults = ValidationDefaults()

    validated_data = _validate_structure(
        schema=schema, data=data, defaults=defaults
        )
    _validate_rules(
        schema=schema, data=validated_data, defaults=defaults
        )

    return validated_data


def _validate_structure(schema, data, defaults):
    try:
        return _dispatch(
            schema=schema,
            data=data,
            location=tuple(),
            defaults=defaults,
            function_map=STRUCTURE_MAP,
            )
    except ValidationError as exc:
        raise StructureValidationError(*exc.errors)


def _validate_rules(schema, data, defaults):
    try:
        _dispatch(
            schema=schema,
            data=data,
            location=tuple(),
            defaults=defaults,
            function_map=RULES_MAP,
            )
    except ValidationError as exc:
        raise RulesValidationError(*exc.errors)


def process_input(*, schema, data, default_kwargs=None):
    return _process_and_transform_errors(
        schema=schema,
        data=data,
        default_kwargs=default_kwargs,
        rules_error=InputRulesValidationError,
        )


def process_output(*, schema, data, default_kwargs=None):
    return _process_and_transform_errors(
        schema=schema,
        data=data,
        default_kwargs=default_kwargs,
        rules_error=OutputRulesValidationError,
        )


def _process_and_transform_errors(rules_error, **kwargs):
    try:
        return process(**kwargs)
    except RulesValidationError as exc:
        raise rules_error(*exc.errors)


def process(*, schema, data, default_kwargs=None):
    if default_kwargs is None:
        default_kwargs = {}

    try:
        return _dispatch(
            schema=schema,
            data=data,
            location=tuple(),
            default_kwargs=default_kwargs,
            function_map=PROCESS_MAP,
            )
    except ValidationError as exc:
        raise RulesValidationError(*exc.errors)


def _dispatch(schema, function_map, **kwargs):
    """ Call the appropriate function, depending on `schema` type. """

    function = select_function(schema, function_map)
    return function(
        schema=schema, function_map=function_map, **kwargs
        )


def _validate_scalar_structure(
    # pylint: disable=unused-argument
    schema, data, location, **kwargs
    ):
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
    return _dispatch(schema=schema[0], **kwargs)


def _validate_tuple_rules(
    # pylint: disable=unused-argument
    schema, data, location, defaults, **kwargs
    ):
    rules = get_rules(schema, defaults)

    apply_rules(rules, data, location)

    inner_schema = schema[0]

    if isinstance(inner_schema, type):
        return

    _dispatch(
        schema=schema[0],
        data=data,
        location=location,
        defaults=defaults,
        **kwargs
        )


def get_rules(schema, defaults):
    rules = schema[1:]

    override_defaults = get_override_defaults(rules)

    if override_defaults:
        return rules

    return defaults.default_rules + rules


def get_override_defaults(rules):
    if not rules:
        return False
    return getattr(rules[0], 'override_defaults', False)


def apply_rules(rules, data, location):
    for rule in rules:
        try:
            rule(data)
        except RuleViolation as exc:
            raise_validation_error_from_rule_violation(exc, location)
        except StopValidation:
            break


def _validate_dict_structure(
    schema,
    data,
    location,
    defaults,
    optional_keys=_NotSet,
    strip_extras=_NotSet,
    **kwargs
    ):
    confirm_mapping(data, location)

    default_kwargs = defaults.validate_dict_structure_kwargs

    optional_keys = resolve_kwarg(
        optional_keys, default_kwargs, 'optional_keys'
        )
    strip_extras = resolve_kwarg(
        strip_extras, default_kwargs, 'strip_extras'
        )

    missing_errors = get_missing_errors(schema, data, optional_keys, location)

    resolved_data = resolve_data_dict(schema, data, strip_extras)

    not_allowed_errors = get_not_allowed_errors(schema, resolved_data, location)

    return _utilize_dict(
        schema=schema,
        data=resolved_data,
        location=location,
        other_error_lists=(missing_errors, not_allowed_errors),
        defaults=defaults,
        **kwargs
        )


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


def _utilize_dict(schema, data, location, other_error_lists=tuple(), **kwargs):
    result_items, captured_error_lists = (
        get_result_items_and_capture_errors(schema, data, location, **kwargs)
        )

    all_error_lists = other_error_lists + captured_error_lists

    errors_chain = itertools.chain(*all_error_lists)
    errors = list(errors_chain)

    raise_if_errors(errors)

    return dict(result_items)


def get_result_items_and_capture_errors(schema, data, location, **kwargs):
    schema_keys = key_set(schema)
    data_keys = key_set(data)

    result = tuple(zip(*[
        get_result_item_and_capture_errors(
            schema=schema[key],
            data=data[key],
            location=location + (key,),
            key=key,
            **kwargs
            )
        for key in schema_keys & data_keys
        ]))

    if not result:
        return tuple([tuple(), tuple()])

    return result


def get_result_item_and_capture_errors(key, **kwargs):
    try:
        validated_data = _dispatch(**kwargs)
    except ValidationError as exc:
        return (key, None), exc.errors

    return (key, validated_data), tuple()


def raise_if_errors(errors):
    if errors:
        raise ValidationError(*errors)


def _validate_Dict_structure(schema, **kwargs):
    kwargs.update(schema.validate_structure_kwargs)
    return _utilize_Dict(schema=schema, **kwargs)


def _utilize_Dict(schema, **kwargs):
    return _dispatch(schema=schema.schema, **kwargs)


def _validate_DictOf_structure(data, location, **kwargs):
    confirm_mapping(data, location)
    return _utilize_DictOf(data=data, location=location, **kwargs)


def _utilize_DictOf(schema, data, **kwargs):
    """ Validate a dictionary with arbitrary keys.
        Validate each value from `data` against `schema.schema`.
        `schema` is a `DictOf` instance. """

    schema_dict = {key: schema.schema for key in data.keys()}

    return _dispatch(schema=schema_dict, data=data, **kwargs)


def _validate_list_structure(data, location, defaults, **kwargs):
    confirm_sequence(data, location)

    kwargs.update(defaults.validate_list_structure_kwargs)

    return _utilize_list(
        data=data, location=location, defaults=defaults, **kwargs
        )


def _utilize_list(schema, data, **kwargs):
    """ Validate a list.
        Validate each value from `data` against the corresponding `schema`
        value.
        `schema` and `data` must have the same length. """

    schema_dict = dict(enumerate(schema))
    data_dict = dict(enumerate(data))

    result_dict = _dispatch(schema=schema_dict, data=data_dict, **kwargs)

    return reassemble_list(result_dict)


def reassemble_list(result_dict):
    return [value for key, value in sorted(result_dict.items())]


def _validate_ListOf_structure(data, location, **kwargs):
    confirm_sequence(data, location)
    return _utilize_ListOf(
        data=data, location=location, **kwargs
        )


def _utilize_ListOf(schema, data, **kwargs):
    """ Validate a list with arbitrary length.
        Validate each value from `data` against `schema.schema`.
        `schema` is a `ListOf` instance. """
    schema_list = [schema.schema for item in data]

    return _utilize_list(schema=schema_list, data=data, **kwargs)


def _process_Call(
    # pylint: disable=unused-argument
    schema, data, location, default_kwargs, **kwargs
    ):
    function_kwargs = default_kwargs.copy()
    function_kwargs.update(data)
    function_kwargs.update(schema.kwargs)

    try:
        return schema.function(**function_kwargs)
    except RuleViolation as exc:
        raise_validation_error_from_rule_violation(exc, location)


def _process_Callable(schema, **kwargs):
    return _process_Call(schema=Call(schema), **kwargs)


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


def raise_validation_error_from_rule_violation(exc, location):
    error_dict = make_error_dict(
        location=location + exc.location,
        code=exc.code,
        message=exc.message,
        data=exc.data,
        )
    raise ValidationError(error_dict)


def resolve_kwarg(value, default_kwargs, key):
    if value is not _NotSet:
        return value

    return default_kwargs[key]


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
    (dict, _utilize_dict),
    (Dict, _utilize_Dict),
    (DictOf, _utilize_DictOf),
    (list, _utilize_list),
    (ListOf, _utilize_ListOf),
    )


PROCESS_MAP = (
    (Call, _process_Call),
    (collections.abc.Callable, _process_Callable),
    (dict, _utilize_dict),
    (DictOf, _utilize_DictOf),
    (list, _utilize_list),
    (ListOf, _utilize_ListOf),
    )
