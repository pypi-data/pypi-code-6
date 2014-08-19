""" Tests for `coercion_tools` module. """

import unittest
from unittest.mock import (
    call,
    MagicMock,
    patch,
    sentinel
    )

from jsonmanager import coercion_tools
from jsonmanager.coercion_tools import (
    _coerce_data,
    _coerce_scalar,
    _coerce_dict,
    _coerce_DictOf,
    _coerce_list,
    _coerce_ListOf,
    _coerce_tuple,
    CoercionManagerBase,
    )
from jsonmanager.schema_types import (
    Dict,
    DictOf,
    ListOf
    )

from test.util import ConfiguredDecoratorTest


class TestCoerceInputOutput(unittest.TestCase):
    """ `coerce_input` and `coerce_output` methods. """

    def setUp(self):
        self.manager = CoercionManagerBase()

    @patch('jsonmanager.coercion_tools.process_data')
    def calls_coerce_test(self, mock_process_data, routine):
        """ `coerce_...` method calls `coerce` method. """
        mock_process_data.return_value = sentinel.expected

        coercion_method = getattr(self.manager, 'coerce_{}'.format(routine))

        result = coercion_method(sentinel.schema, sentinel.data)

        mock_process_data.assert_called_with(
            _coerce_data, sentinel.schema, sentinel.data, self.manager, routine
            )
        assert result is sentinel.expected

    def test_coerce_input(self):
        """ Calls `coerce` with 'input' routine. """
        self.calls_coerce_test(routine='input')

    def test_coerce_output(self):
        """ Calls `coerce` with 'output' routine. """
        self.calls_coerce_test(routine='output')


class TestCoerceData(unittest.TestCase):
    """ `_coerce_data` calls the appropriate coercion function depending on
        `schema` type. """

    @patch('jsonmanager.coercion_tools.select_function')
    def test_calls_coercion_function(self, mock_select_function):
        """ `select_function` called to get coercion function.
            `process_data` called with coercion function, schema, data.

            `process_data` return value returned. """
        coercion_function = MagicMock()
        mock_select_function.return_value = coercion_function
        coercion_function.return_value = sentinel.expected

        result = _coerce_data(
            sentinel.schema, sentinel.data, sentinel.manager, sentinel.routine
            )

        coercion_function.assert_called_with(
            sentinel.schema, sentinel.data, sentinel.manager, sentinel.routine
            )
        assert result is sentinel.expected

    def coercion_function_test(self, mock_coercion_function, schema_type):
        """ `.coerce` calls the appropriate function.

            These tests are necessary to ensure that `coercion_map` is
            defined correctly. """
        mock_coercion_function.return_value = sentinel.expected
        schema = MagicMock(schema_type)

        result = _coerce_data(
            schema, sentinel.data, sentinel.manager, sentinel.routine
            )

        mock_coercion_function.assert_called_with(
            schema, sentinel.data, sentinel.manager, sentinel.routine
            )
        assert result is sentinel.expected

    @patch('jsonmanager.coercion_tools._coerce_scalar')
    def test_scalar(self, mock_coerce_scalar):
        """ `_coerce_scalar` is called. """
        self.coercion_function_test(mock_coerce_scalar, type)

    @patch('jsonmanager.coercion_tools._coerce_dict')
    def test_dict(self, mock_coerce_dict):
        """ `_coerce_dict` is called. """
        self.coercion_function_test(mock_coerce_dict, dict)

    @patch('jsonmanager.coercion_tools._coerce_DictOf')
    def test_dict_of(self, mock_coerce_DictOf):
        """ `_coerce_DictOf` is called. """
        self.coercion_function_test(mock_coerce_DictOf, DictOf)

    @patch('jsonmanager.coercion_tools._coerce_list')
    def test_list(self, mock_coerce_list):
        """ `_coerce_list` is called. """
        self.coercion_function_test(mock_coerce_list, list)

    @patch('jsonmanager.coercion_tools._coerce_ListOf')
    def test_list_of(self, mock_coerce_ListOf):
        """ `_coerce_ListOf` is called. """
        self.coercion_function_test(mock_coerce_ListOf, ListOf)

    @patch('jsonmanager.coercion_tools._coerce_tuple')
    def test_tuple(self, mock_coerce_tuple):
        """ `_coerce_tuple` is called. """
        self.coercion_function_test(mock_coerce_tuple, tuple)


class TestCoerceScalar(unittest.TestCase):
    """ `_coerce_scalar` calls the appropriate coercion method. """

    def yes_coercion_test(self, routine):
        coercion_method_name = 'coerce_{}_SomeType'.format(routine)

        class SomeType:
            pass

        manager = MagicMock(spec=[coercion_method_name])
        coercion_method = getattr(manager, coercion_method_name)
        coercion_method.return_value = sentinel.expected

        result = _coerce_scalar(SomeType, sentinel.data, manager, routine)

        coercion_method.assert_called_with(sentinel.data)
        assert result is sentinel.expected

    def test_input_yes_coercion(self):
        """ When a method named `coerce_input_SomeType` is present, it is
            called. """
        self.yes_coercion_test('input')

    def test_output_yes_coercion(self):
        """ When a method named `coerce_output_SomeType` is present, it is
            called. """
        self.yes_coercion_test('output')

    def no_coercion_test(self, routine):
        """ When `coerce_...` method is not present, no coercion. """
        class SomeType:
            pass

        manager = MagicMock(spec=[])
        result = _coerce_scalar(SomeType, sentinel.data, manager, routine)
        assert result is sentinel.data

    def test_input_no_coercion(self):
        """ When method is not present, no coercion. """
        self.no_coercion_test('input')

    def test_output_no_coercion(self):
        """ When `coerce_output_SomeType` method is not present, no coercion.
            """
        self.no_coercion_test('output')


class TestCoerceDict(unittest.TestCase):
    """ `_coerce_dict` function. """

    @patch('jsonmanager.coercion_tools._coerce_data')
    def test_calls_coerce_data(self, mock_coerce_data):
        """ `coerce` called for each item in `data`. Dictionary of results
            returned. """
        schema = {
            'a': sentinel.a,
            'b': sentinel.b,
            'c': sentinel.c
            }
        data = {
            'a': sentinel.x,
            'b': sentinel.y,
            'c': sentinel.z
            }

        expected_calls = [
            call(schema[key], data[key], sentinel.manager, sentinel.routine)
            for key in 'abc'
            ]

        mock_coerce_data.return_value = sentinel.coerced_value
        expected_result = {key: sentinel.coerced_value for key in 'abc'}

        result = _coerce_dict(schema, data, sentinel.manager, sentinel.routine)

        mock_coerce_data.assert_has_calls(expected_calls, any_order=True)
        assert result == expected_result

    @patch('jsonmanager.coercion_tools.is_mapping')
    def test_non_mapping_data_no_coercion(self, mock_is_mapping):
        """ If `data` is not a mapping, no coercion. """
        mock_is_mapping.return_value = False
        result = _coerce_dict(
            sentinel.schema, sentinel.data, sentinel.manager, sentinel.routine
            )
        mock_is_mapping.assert_called_with(sentinel.data)
        assert result is sentinel.data

    @patch('jsonmanager.coercion_tools._coerce_data')
    def test_missing_item_no_error(self, mock_coerce_data):
        """ If some items from `schema` are missing, then the remaining items
            are coerced normally, and no exception is raised. """
        mock_coerce_data.return_value = sentinel.expected

        schema = {'a': sentinel.a, 'b': sentinel.b}
        data = {'a': sentinel.x}

        result = _coerce_dict(schema, data, sentinel.manager, sentinel.routine)

        mock_coerce_data.assert_called_with(
            sentinel.a, sentinel.x, sentinel.manager, sentinel.routine
            )
        assert result == {'a': sentinel.expected}

    @patch('jsonmanager.coercion_tools._coerce_data')
    def test_extra_item_no_coercion(self, mock_coerce_data):
        """ Items not present in `schema` are not coerced. """
        mock_coerce_data.return_value = sentinel.expected

        schema = {'a': sentinel.a}
        data = {'a': sentinel.x, 'b': sentinel.no_coercion}

        result = _coerce_dict(schema, data, sentinel.manager, sentinel.routine)

        mock_coerce_data.assert_called_with(
            sentinel.a, sentinel.x, sentinel.manager, sentinel.routine
            )
        assert result == {'a': sentinel.expected, 'b': sentinel.no_coercion}


class TestCoerceDictSchemaTypeUnit(unittest.TestCase):
    """ `coercion_tools._coerce_Dict` """

    @patch('jsonmanager.coercion_tools._coerce_dict')
    def test_behavior(self, mock_coerce_dict):
        schema = MagicMock()

        pargs = [sentinel.parg_value]

        mock_coerce_dict.return_value = sentinel.expected

        result = coercion_tools._coerce_Dict(schema, *pargs)

        mock_coerce_dict.assert_called_with(schema.schema, *pargs)

        assert result is sentinel.expected


class TestCoerceDictOf(unittest.TestCase):
    """ `_coerce_DictOf` method. """

    @patch('jsonmanager.coercion_tools._coerce_dict')
    def test_coerce_dict_called(self, mock_coerce_dict):
        """ A dictionary schema is constructed with keys from `data`. `data` is
            coerced with the constructed dictionary schema. """
        schema = DictOf(sentinel.schema)
        data = {'a': sentinel.a, 'b': sentinel.b, 'c': sentinel.c}

        schema_dict = {
            'a': sentinel.schema,
            'b': sentinel.schema,
            'c': sentinel.schema
            }

        mock_coerce_dict.return_value = sentinel.expected

        result = _coerce_DictOf(
            schema, data, sentinel.manager, sentinel.routine
            )

        mock_coerce_dict.assert_called_with(
            schema_dict, data, sentinel.manager, sentinel.routine
            )

        assert result is sentinel.expected

    @patch('jsonmanager.coercion_tools.is_mapping')
    def test_non_mapping_data_no_coercion(self, mock_is_mapping):
        """ If `data` is not a mapping, no coercion. """
        mock_is_mapping.return_value = False
        result = _coerce_DictOf(
            sentinel.schema, sentinel.data, sentinel.manager, sentinel.routine
            )
        mock_is_mapping.assert_called_with(sentinel.data)
        assert result is sentinel.data


class TestCoerceList(unittest.TestCase):
    """ `_coerce_list` method. """

    @patch('jsonmanager.coercion_tools._coerce_dict')
    def test_calls_coerce_dict(self, mock_coerce_dict):
        """ `data` and `schema` are converted to dictionaries and passed to
            `_coerce_dict`. The result is converted back to a list and returned.
            """
        schema = [sentinel.a, sentinel.b, sentinel.c]
        data = [sentinel.x, sentinel.y, sentinel.z]

        schema_dict = {0: sentinel.a, 1: sentinel.b, 2: sentinel.c}
        data_dict = {0: sentinel.x, 1: sentinel.y, 2: sentinel.z}

        mock_coerce_dict.return_value = {
            0: sentinel.coerced_x,
            1: sentinel.coerced_y,
            2: sentinel.coerced_z
            }

        result = _coerce_list(schema, data, sentinel.manager, sentinel.routine)

        mock_coerce_dict.assert_called_with(
            schema_dict, data_dict, sentinel.manager, sentinel.routine
            )

        assert result == [
            sentinel.coerced_x, sentinel.coerced_y, sentinel.coerced_z
            ]

    @patch('jsonmanager.coercion_tools.is_sequence')
    def test_non_sequence_data_no_coercion(self, mock_is_sequence):
        """ If `data` is not a sequence, no coercion. """
        mock_is_sequence.return_value = False
        result = _coerce_list(
            sentinel.schema, sentinel.data, sentinel.manager, sentinel.routine
            )
        mock_is_sequence.assert_called_with(sentinel.data)
        assert result is sentinel.data

    @patch('jsonmanager.coercion_tools._coerce_data')
    def test_missing_item_no_error(self, mock_coerce_data):
        """ If some items from `schema` are missing, then the remaining elements
            are coerced normally, and no exception is raised. """
        mock_coerce_data.return_value = sentinel.expected

        schema = [sentinel.a, sentinel.b]
        data = [sentinel.x]

        result = _coerce_list(schema, data, sentinel.manager, sentinel.routine)

        mock_coerce_data.assert_called_with(
            sentinel.a, sentinel.x, sentinel.manager, sentinel.routine
            )
        assert result == [sentinel.expected]

    @patch('jsonmanager.coercion_tools._coerce_data')
    def test_extra_item_no_coercion(self, mock_coerce_data):
        """ Items not present in `schema` are not coerced. """
        mock_coerce_data.return_value = sentinel.expected

        schema = [sentinel.a]
        data = [sentinel.x, sentinel.no_coercion]

        result = _coerce_list(schema, data, sentinel.manager, sentinel.routine)

        mock_coerce_data.assert_called_with(
            sentinel.a, sentinel.x, sentinel.manager, sentinel.routine
            )
        assert result == [sentinel.expected, sentinel.no_coercion]


class TestCoerceListOf(unittest.TestCase):
    """ `_coerce_ListOf` method. """

    @patch('jsonmanager.coercion_tools._coerce_list')
    def test_calls_coerce_list(self, mock_coerce_list):
        schema = ListOf(sentinel.schema)
        data = [sentinel.a, sentinel.b, sentinel.c]

        mock_coerce_list.return_value = sentinel.expected

        schema_list = [
            sentinel.schema, sentinel.schema, sentinel.schema
            ]

        result = _coerce_ListOf(
            schema, data, sentinel.manager, sentinel.routine
            )

        mock_coerce_list.assert_called_with(
            schema_list, data, sentinel.manager, sentinel.routine
            )

        assert result is sentinel.expected

    @patch('jsonmanager.coercion_tools.is_sequence')
    def test_non_sequence_data_no_coercion(self, mock_is_sequence):
        """ If `data` is not a sequence, no coercion. """
        mock_is_sequence.return_value = False
        result = _coerce_ListOf(
            sentinel.schema, sentinel.data, sentinel.manager, sentinel.routine
            )
        mock_is_sequence.assert_called_with(sentinel.data)
        assert result is sentinel.data


class TestCoerceTuple(unittest.TestCase):
    """ `_coerce_tuple` method. """

    @patch('jsonmanager.coercion_tools._coerce_data')
    def test_calls_coerce_data(self, mock_coerce_data):
        """ The first tuple element is passed to `coerce`. """
        mock_coerce_data.return_value = sentinel.expected
        schema_tuple = (sentinel.schema_element, sentinel.validator)

        result = _coerce_tuple(
            schema_tuple, sentinel.data, sentinel.manager, sentinel.routine
            )

        mock_coerce_data.assert_called_with(
            sentinel.schema_element,
            sentinel.data,
            sentinel.manager,
            sentinel.routine
            )
        assert result is sentinel.expected


class IntegrationTest(unittest.TestCase):

    def setUp(self):
        class ExpectedType:
            pass
        self.ExpectedType = ExpectedType

        class Manager(CoercionManagerBase):
            # pylint: disable=unused-argument
            def coerce_input_ExpectedType(self, data):
                return data
        self.manager = Manager()


class TestIntegrationCoerceMethod(IntegrationTest):
    """ Confirm that `coerce_input` passes without any unexpected errors. """

    def integration_test(self, schema, data):
        """ No unexpected errors raised. Result is coerced input.

            Note that, in this case, coercion just returns the data unchanged.
            """
        result = self.manager.coerce_input(schema, data)
        assert result == data

    def test_scalar(self):
        """ Scalar value passes. """
        self.integration_test(
            schema=self.ExpectedType,
            data=self.ExpectedType()
            )

    def test_dictionary(self):
        """ Dictionary passes. """
        self.integration_test(
            schema={'a': self.ExpectedType},
            data={'a': self.ExpectedType()}
            )

    def test_dict_of(self):
        """ `DictOf` passes. """
        self.integration_test(
            schema=DictOf(self.ExpectedType),
            data={'a': self.ExpectedType()}
            )

    def test_Dict(self):
        self.integration_test(
            schema=Dict({'a': self.ExpectedType}),
            data={'a': self.ExpectedType()}
            )

    def test_list(self):
        """ List passes. """
        self.integration_test(
            schema=[self.ExpectedType],
            data=[self.ExpectedType()]
            )

    def test_list_of(self):
        """ `ListOf` passes. """
        self.integration_test(
            schema=ListOf(self.ExpectedType),
            data=[self.ExpectedType()]
            )

    def test_tuple(self):
        """ Tuple schema with validators passes. """
        def validator(schema, data): # pylint: disable=unused-argument
            pass

        self.integration_test(
            schema=(self.ExpectedType, validator),
            data=self.ExpectedType()
            )

    def test_none(self):
        """ `None` schema passes. """
        self.integration_test(
            schema=None,
            data=self.ExpectedType()
            )


class TestIntegrationCoercion(IntegrationTest, ConfiguredDecoratorTest):
    """ Confirm that `coercion` works with no unexpected errors. """

    def setUp(self):
        super().setUp()
        self.configured_decorator = self.manager.coercion
