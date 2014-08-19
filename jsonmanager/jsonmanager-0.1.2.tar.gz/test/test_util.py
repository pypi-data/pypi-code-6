""" Tests for `jsonmanager.util`. """

from collections import abc

import unittest
from unittest.mock import (
    call,
    MagicMock,
    patch,
    sentinel
    )

from jsonmanager import util
from jsonmanager.exceptions import SchemaError
from jsonmanager.util import(
    check_input_schema,
    is_mapping,
    is_sequence,
    process_data,
    processing_decorator,
    resolve_decorator_schemas,
    select_function
    )


class TestSelectFunctionFunctional(unittest.TestCase):
    """ `util.select_function` """

    def setUp(self):
        class TargetType:
            pass

        class OtherType:
            pass

        self.TargetType = TargetType
        self.OtherType = OtherType

    def success_test(self, function_map):
        """ `target_function` is returned. """
        schema = self.TargetType()
        result = select_function(schema, function_map)
        assert result is sentinel.target_function

    def test_target_before_other(self):
        """ `TargetType` before `OtherType` in `function_map`. """
        function_map = [
            (self.TargetType, sentinel.target_function),
            (self.OtherType, sentinel.other_function),
            ]
        self.success_test(function_map)

    def test_target_after_other(self):
        """ `TargetType` after `OtherType` in `function_map`. """
        function_map = [
            (self.OtherType, sentinel.other_function),
            (self.TargetType, sentinel.target_function),
            ]
        self.success_test(function_map)

    def test_target_type_not_in_map_raises(self):
        """ `TargetType` not in `function_map`. """
        function_map = [
            (self.OtherType, sentinel.other_function)
            ]
        schema = MagicMock(self.TargetType)
        with self.assertRaises(SchemaError):
            select_function(schema, function_map)


class TestIsMapping(unittest.TestCase):
    """ 'is_mapping` function. """

    def test_mapping_returns_true(self):
        """ A `Mapping`-type instance returns True. """
        value = MagicMock(abc.Mapping)
        result = is_mapping(value)
        assert result is True

    def test_other_type_returns_false(self):
        """ An instance of a non-mapping type returns False. """
        value = object()
        result = is_mapping(value)
        assert result is False


class TestIsSequence(unittest.TestCase):
    """ `is_sequence` function. """

    def test_sequence_returns_true(self):
        """ A `Sequence`-type instance returns True. """
        value = MagicMock(abc.Sequence)
        result = is_sequence(value)
        assert result is True

    def test_non_sequence_returns_false(self):
        """ An instance of a non-sequence type returns False. """
        value = MagicMock()
        result = is_sequence(value)
        assert result is False

    def test_string_returns_false(self):
        """ A `str` instance returns false. """
        value = 'abc'
        result = is_sequence(value)
        assert result is False


class TestKeySetFunctional(unittest.TestCase):
    """ `util.key_set` """

    def test_result(self):
        d = {'a': 0, 'b': 1, 'c': 2}
        expected = set(['a', 'b', 'c'])
        assert util.key_set(d) == expected


class TestProcessData(unittest.TestCase):
    """ If `schema` is provided, calls `processor` and returns the processed
        value. If `schema` not provided, returns `data` unchanged.
        Additional positional arguments are passed through to `processor`. """

    def test_yes_schema(self):
        """ `processor` is called. return value is returned. """
        processor = MagicMock(return_value=sentinel.expected)
        result = process_data(processor, sentinel.schema, sentinel.data)
        processor.assert_called_with(sentinel.schema, sentinel.data)
        assert result is sentinel.expected

    def test_empty_schema(self):
        """ If `schema` is anything except None (even an empty container!), then
            `processor` is called. Return value is returned. """
        processor = MagicMock(return_value=sentinel.expected)
        result = process_data(processor, {}, sentinel.data)
        processor.assert_called_with({}, sentinel.data)
        assert result is sentinel.expected

    def test_no_schema(self):
        """ `processor` not called. `data` returned unchanged. """
        processor = MagicMock()
        result = process_data(processor, None, sentinel.data)
        assert not processor.called
        assert result is sentinel.data

    def test_extra_positional_arguments(self):
        """ Extra positional arguments are passed to `processor`. """
        processor = MagicMock(return_value=sentinel.expected)
        result = process_data(
            processor, sentinel.schema, sentinel.data, sentinel.extra_parg
            )

        processor.assert_called_with(
            sentinel.schema, sentinel.data, sentinel.extra_parg
            )

        assert result is sentinel.expected


class TestResolveDecoratorSchemas(unittest.TestCase):
    """ Select schema from either provided argument or wrapped callable. """

    def test_schema_from_argument(self):
        """ Schema provided as an argument takes precedence. """
        result = resolve_decorator_schemas(
            sentinel.schema_from_argument,
            sentinel.wrapped,
            sentinel.schema_name
            )
        assert result is sentinel.schema_from_argument

    def test_schema_from_attribute(self):
        """ Schema from wrapped callable attribute used if no schema provided as
            an argument. """
        wrapped = MagicMock()
        wrapped.schema_attribute = sentinel.schema_from_attribute

        result = resolve_decorator_schemas(
            None, wrapped, 'schema_attribute'
            )

        assert result is sentinel.schema_from_attribute

    def test_no_argument_no_attribute(self):
        """ When no schema provided as argument, and wrapped has no schema
            attribute, None is returned. """
        wrapped = MagicMock(spec=[])

        result = resolve_decorator_schemas(
            None, wrapped, 'schema_attribute'
            )

        assert result is None


class TestCheckInputSchema(unittest.TestCase):
    """ If an input schema is not a dictionary, raise an exception. """

    def test_dict_passes(self):
        schema = MagicMock(dict)
        check_input_schema(schema)

    def test_none_passes(self):
        check_input_schema(None)

    def test_raises(self):
        schema = MagicMock()
        with self.assertRaises(SchemaError):
            check_input_schema(schema)


class TestProcessingDecorator(unittest.TestCase):
    """ `processing_decorator` function. Returns a decorator used for both the
        `validation` and `coercion` decorators. """

    @patch('jsonmanager.util.check_input_schema')
    @patch('jsonmanager.util.resolve_decorator_schemas')
    def test_decorator(
        self,
        mock_resolve_decorator_schemas,
        mock_check_input_schema
        ):
        """ Keyword arguments are packed up into `input_schema`.
            Input and output schemas are resolved from schemas passed in as
            arguments and from schemas stored as attributes on the wrapped
            callable.
            `input_data` and `output_data` are processed with the resolved
            input and output schemas.
            The wrapped callable is called with the processed input data.
            The processed output data is returned. """

        wrapped_callable = MagicMock(return_value=sentinel.output_data)

        input_data = dict(arg_name=sentinel.arg_value)
        processed_input_data = dict(arg_name=sentinel.processed_arg_value)

        mock_resolve_decorator_schemas.side_effect = [
            sentinel.resolved_input_schema,
            sentinel.resolved_output_schema
            ]

        input_processor = MagicMock()
        output_processor = MagicMock()

        input_processor.return_value = processed_input_data
        output_processor.return_value = sentinel.processed_output_data

        # Create the decorator.
        decorator = processing_decorator(
            input_processor=input_processor,
            output_processor=output_processor
            )

        # Decorate a wrapped callable.
        decorated = decorator(
            input_schema=sentinel.input_schema,
            output_schema=sentinel.output_schema
            )(wrapped_callable)

        # When the callable is decorated:
        # - `input_schema` and `output_schema` are resolved.
        # - `input_schema` is checked.
        # - `resolved_input_schema` and `resolved_output_schema` are stored as
        #   attributes of the decorated callable.

        mock_resolve_decorator_schemas.assert_has_calls([
            call(sentinel.input_schema, wrapped_callable, 'input_schema'),
            call(sentinel.output_schema, wrapped_callable, 'output_schema')
            ])

        mock_check_input_schema.assert_called_with(
            sentinel.resolved_input_schema
            )

        assert decorated.input_schema is sentinel.resolved_input_schema
        assert decorated.output_schema is sentinel.resolved_output_schema

        # Call the decorated function.
        result = decorated(**input_data)

        # When the decorated function is called:
        # - `input_data` is processed and passed to the wrapped callable as
        #   keyword arguments.
        # - The wrapped callable returns `output_data`.
        # - `output_data` is processed and returned.

        input_processor.assert_called_with(
            schema=sentinel.resolved_input_schema, data=input_data
            )

        output_processor.assert_called_with(
            schema=sentinel.resolved_output_schema, data=sentinel.output_data
            )

        wrapped_callable.assert_called_with(**processed_input_data)

        assert result is sentinel.processed_output_data


class TestProcessingDecoratorSyntax(unittest.TestCase):
    """ Test the various usage syntax of `processing_decorator`. """

    def setUp(self):
        self.input_processor = MagicMock()
        self.output_processor = MagicMock()
        self.decorator = processing_decorator(
            self.input_processor,
            self.output_processor
            )

    def test_no_schemas(self):
        """ Decorator raises no errors when no schemas provided. """
        self.decorator()(sentinel.wrapped)

    def test_pargs_not_allowed(self):
        """ Calling decorated function with positional arguments raises an
            exception. """
        wrapped = MagicMock(spec=[])
        decorated = self.decorator()(wrapped)

        with self.assertRaises(TypeError):
            # pylint: disable=too-many-function-args
            decorated(sentinel.positional_argument)

    def decorator_syntax_test(self, decorator):
        """ Confirm that a decorator syntax works correctly.

            `self.input_processor` produces the input for the decorated
            function.
            `self.output_processor` produces the output from the decorated
            function. """
        self.output_processor.return_value = sentinel.expected

        @decorator
        def function():
            pass

        result = function() # pylint: disable=assignment-from-no-return

        assert self.input_processor.called
        assert self.output_processor.called

        assert result is sentinel.expected

    def test_no_call_before_decorating(self):
        """ Decorator can be used without calling; syntactic sugar. """
        decorator = self.decorator
        self.decorator_syntax_test(decorator)

    def test_yes_call_yes_schema_args_before_decorating(self):
        """ Decorator can be used by calling with arguments before decorating.
            """
        decorator = self.decorator(
            input_schema=MagicMock(dict),
            output_schema=sentinel.output_schema
            )
        self.decorator_syntax_test(decorator)

    def test_yes_call_no_schema_args_before_decorating(self):
        """ Decorator can be used by calling with no arguments before
            decorating. """
        decorator = self.decorator()
        self.decorator_syntax_test(decorator)
