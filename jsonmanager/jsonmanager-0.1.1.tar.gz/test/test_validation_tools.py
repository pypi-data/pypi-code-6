""" Tests for `validation_tools` module. """
import collections
from contextlib import contextmanager

import unittest
from unittest.mock import (
    call,
    MagicMock,
    patch,
    sentinel,
    )

from test.util import (
    ConfiguredDecoratorTest,
    patch_builtin,
    )

from jsonmanager.exceptions import (
    RuleViolation,
    RulesValidationError,
    StopValidation,
    StructureValidationError,
    ValidationError,
    )
from jsonmanager.rules import override_defaults
from jsonmanager.schema_types import (
    AnyType,
    Dict,
    DictOf,
    ListOf
    )
from jsonmanager import exceptions
from jsonmanager import validation_tools


_NotSet = object()


class IntegrationTest(unittest.TestCase):

    def setUp(self):
        class ExpectedType:
            pass
        self.ExpectedType = ExpectedType


class ValidationErrorTest(IntegrationTest):

    @contextmanager
    def assertRaisesSingleValidationError(
        self,
        location,
        code,
        message=_NotSet,
        data=_NotSet,
        error_class=ValidationError
        ):
        """ An operation raises a `ValidationError` with a single error dict.
            Confirm that error dict values are correct. """
        with self.assertRaises(error_class) as exc_context:
            yield

        exc = exc_context.exception

        assert len(exc.errors) == 1

        error_dict = exc.errors[0]

        assert error_dict['location'] == location
        assert error_dict['code'] == code

        for key, expected in [('message', message), ('data', data)]:
            if expected is _NotSet:
                continue
            assert error_dict[key] == expected

    @contextmanager
    def assertRaisesMultipleValidationErrors(
        self, error_codes, error_class=ValidationError
        ):
        with self.assertRaises(error_class) as exc_context:
            yield

        exc = exc_context.exception

        assert len(exc.errors) == len(error_codes)

        errors = {error['location']: error for error in exc.errors}

        for location, code in error_codes:
            assert errors[location]['code'] == code


class TestValidateInputUnit(unittest.TestCase):
    """ `validation_tools.validate_input` """

    @patch('jsonmanager.validation_tools._validate_and_transform_errors')
    def test_behavior(self, mock_validate_and_transform_errors):
        mock_validate_and_transform_errors.return_value = sentinel.expected

        result = validation_tools.validate_input(
            schema=sentinel.schema,
            data=sentinel.data,
            default_rules=sentinel.default_rules,
            )

        mock_validate_and_transform_errors.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            default_rules=sentinel.default_rules,
            structure_error=exceptions.InputStructureValidationError,
            rules_error=exceptions.InputRulesValidationError,
            )

        assert result is sentinel.expected


class TestValidateInputIntegration(ValidationErrorTest):
    """ `validation_tools.validate_input` """

    def test_validation_passes(self):
        data = self.ExpectedType()

        result = validation_tools.validate_input(
            schema=self.ExpectedType,
            data=data,
            default_rules=tuple(),
            )

        assert result is data

    def test_validation_raises_structure_error(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(),
            code='TYPE',
            error_class=exceptions.InputStructureValidationError,
            ):
            validation_tools.validate_input(
                schema=self.ExpectedType,
                data=object(),
                default_rules=tuple(),
                )

    def test_validation_raises_rules_error(self):
        def rule(data): # pylint: disable=unused-argument
            raise RuleViolation(code='rule')

        with self.assertRaisesSingleValidationError(
            location=tuple(),
            code='rule',
            error_class=exceptions.InputRulesValidationError,
            ):
            validation_tools.validate_input(
                schema=(AnyType, rule),
                data=object(),
                default_rules=tuple(),
                )


class TestValidateOutputUnit(unittest.TestCase):
    """ `validation_tools.validate_output` """

    @patch('jsonmanager.validation_tools._validate_and_transform_errors')
    def test_behavior(self, mock_validate_and_transform_errors):
        mock_validate_and_transform_errors.return_value = sentinel.expected

        result = validation_tools.validate_output(
            schema=sentinel.schema,
            data=sentinel.data,
            default_rules=sentinel.default_rules,
            )

        mock_validate_and_transform_errors.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            default_rules=sentinel.default_rules,
            structure_error=exceptions.OutputStructureValidationError,
            rules_error=exceptions.OutputRulesValidationError,
            )

        assert result is sentinel.expected


class TestValidateOutputIntegration(ValidationErrorTest):
    """ `validation_tools.validate_output` """

    def test_validation_passes(self):
        data = self.ExpectedType()

        result = validation_tools.validate_output(
            schema=self.ExpectedType,
            data=data,
            default_rules=tuple(),
            )

        assert result is data

    def test_validation_raises_structure_error(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(),
            code='TYPE',
            error_class=exceptions.OutputStructureValidationError,
            ):
            validation_tools.validate_output(
                schema=self.ExpectedType,
                data=object(),
                default_rules=tuple(),
                )

    def test_validation_raises_rules_error(self):
        def rule(data): # pylint: disable=unused-argument
            raise RuleViolation(code='rule')

        with self.assertRaisesSingleValidationError(
            location=tuple(),
            code='rule',
            error_class=exceptions.OutputRulesValidationError,
            ):
            validation_tools.validate_output(
                schema=(AnyType, rule),
                data=object(),
                default_rules=tuple(),
                )


class TestValidateAndTransformErrorsUnit(unittest.TestCase):
    """ `validation_tools._validate_and_transform_errors` """

    @patch('jsonmanager.validation_tools.validate')
    def test_validate(self, mock_validate):
        mock_validate.return_value = sentinel.expected

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._validate_and_transform_errors(
            structure_error=sentinel.structure_error,
            rules_error=sentinel.rules_error,
            **kwargs
            )

        mock_validate.assert_called_with(**kwargs)

        assert result is sentinel.expected


    @patch('jsonmanager.validation_tools.validate')
    def test_structure_error(self, mock_validate):
        error_sequence = [sentinel.error]
        errors = MagicMock()
        errors.__iter__.return_value = error_sequence

        mock_validate.side_effect = exceptions.StructureValidationError(*errors)

        class ExpectedError(Exception):
            pass

        structure_error = MagicMock(side_effect=ExpectedError)

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        with self.assertRaises(ExpectedError):
            validation_tools._validate_and_transform_errors(
                structure_error=structure_error,
                rules_error=sentinel.rules_error,
                **kwargs
                )

        mock_validate.assert_called_with(**kwargs)

        structure_error.assert_called_with(*error_sequence)


    @patch('jsonmanager.validation_tools.validate')
    def test_rules_error(self, mock_validate):
        error_sequence = [sentinel.error]
        errors = MagicMock()
        errors.__iter__.return_value = error_sequence

        mock_validate.side_effect = exceptions.RulesValidationError(*errors)

        class ExpectedError(Exception):
            pass

        rules_error = MagicMock(side_effect=ExpectedError)

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        with self.assertRaises(ExpectedError):
            validation_tools._validate_and_transform_errors(
                structure_error=sentinel.structure_error,
                rules_error=rules_error,
                **kwargs
                )

        mock_validate.assert_called_with(**kwargs)

        rules_error.assert_called_with(*error_sequence)


@patch('jsonmanager.validation_tools._validate_rules')
@patch('jsonmanager.validation_tools._validate_structure')
class TestValidateUnit(unittest.TestCase):
    """ `validation_tools.validate` """

    def test_validation_behavior(
        self, mock_validate_structure, mock_validate_rules
        ):
        mock_validate_structure.return_value = sentinel.validated_data

        result = validation_tools.validate(
            schema=sentinel.schema,
            data=sentinel.data,
            default_rules=sentinel.default_rules,
            )

        mock_validate_structure.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            )
        mock_validate_rules.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.validated_data,
            default_rules=sentinel.default_rules,
            )

        assert result is sentinel.validated_data

    def test_schema_is_None_skips_validation(
        self, mock_validate_structure, mock_validate_rules
        ):
        result = validation_tools.validate(
            schema=None,
            data=sentinel.data,
            default_rules=sentinel.default_rules,
            )

        assert not mock_validate_structure.called
        assert not mock_validate_rules.called
        assert result is sentinel.data

    def test_default_rules(
        self, mock_validate_structure, mock_validate_rules
        ):
        mock_validate_structure.return_value = sentinel.validated_data

        result = validation_tools.validate(
            schema=sentinel.schema,
            data=sentinel.data,
            default_rules=None,
            )

        mock_validate_structure.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            )
        mock_validate_rules.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.validated_data,
            default_rules=tuple(),
            )

        assert result is sentinel.validated_data

    def test_default_rules_is_None(
        self, mock_validate_structure, mock_validate_rules
        ):
        mock_validate_structure.return_value = sentinel.validated_data

        result = validation_tools.validate(
            schema=sentinel.schema,
            data=sentinel.data,
            )

        mock_validate_structure.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            )
        mock_validate_rules.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.validated_data,
            default_rules=validation_tools.DEFAULT_RULES,
            )

        assert result is sentinel.validated_data


class TestValidateIntegration(ValidationErrorTest):
    """ `validation_tools.validate` """

    def setUp(self):
        super().setUp()

        def rule_fails(data): # pylint: disable=unused-argument
            raise RuleViolation(code='rule')

        self.rule_fails = rule_fails

    def test_validation_passes(self):
        """ `data` is returned unchanged. """
        data = object()

        result = validation_tools.validate(
            schema=AnyType, data=data, default_rules=None
            )

        assert result is data

    def test_structure_raises(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='TYPE'
            ):
            validation_tools.validate(
                schema=self.ExpectedType, data=object()
                )

    def test_rules_raises(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='rule'
            ):
            validation_tools.validate(
                schema=(AnyType, self.rule_fails),
                data=object(),
                default_rules=None
                )

    def test_structure_raises_before_rules(self):
        """ If `data` fails `structure` validation, rules are not evaluated. """
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='TYPE'
            ):
            validation_tools.validate(
                schema=(self.ExpectedType, self.rule_fails),
                data=object(),
                default_rules=None
                )


class TestValidateStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_structure` """

    @patch('jsonmanager.validation_tools._validate_data')
    def test_no_error(self, mock_validate_data):
        mock_validate_data.return_value = sentinel.expected

        result = validation_tools._validate_structure(
            schema=sentinel.schema, data=sentinel.data
            )

        mock_validate_data.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            location=tuple(),
            validation_map=validation_tools.STRUCTURE_MAP,
            )

        assert result is sentinel.expected

    @patch('jsonmanager.validation_tools.StructureValidationError')
    @patch('jsonmanager.validation_tools._validate_data')
    def test_yes_error(self, mock_validate_data, mock_StructureValidationError):
        """ If a `ValidationError` is raised, it is caught and
            `StructureValidationError` is raised. """
        errors = tuple([sentinel.error])
        mock_validate_data.side_effect = exceptions.ValidationError(*errors)

        class ExpectedError(Exception):
            pass

        mock_StructureValidationError.return_value = ExpectedError

        with self.assertRaises(ExpectedError):
            validation_tools._validate_structure(
                schema=sentinel.schema, data=sentinel.data
                )

        mock_validate_data.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            location=tuple(),
            validation_map=validation_tools.STRUCTURE_MAP,
            )
        mock_StructureValidationError.assert_called_with(*errors)


class TestValidateStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_structure` """

    def setUp(self):
        super().setUp()

        self.complex_schema = {
            'a': self.ExpectedType,
            'b': (self.ExpectedType,),
            'c': {'x': self.ExpectedType, 'y': AnyType},
            'd': Dict(
                {'m': self.ExpectedType, 'n': AnyType, 'o': AnyType},
                optional_keys=['n', 'o'],
                strip_extras=True,
                ),
            'e': DictOf(self.ExpectedType),
            'f': [self.ExpectedType, AnyType],
            'g': ListOf(self.ExpectedType),
            'h': {
                'q': Dict({
                    'r': DictOf(
                        [
                            ListOf(
                                self.ExpectedType
                                )
                            ]
                        )
                    })
                }
            }

    def test_validation_passes(self):
        data = self.ExpectedType()
        result = validation_tools._validate_structure(
            schema=self.ExpectedType, data=data
            )
        assert result is data

    def test_validation_passes_complex(self):
        data = {
            'a': self.ExpectedType(),
            'b': self.ExpectedType(),
            'c': {'x': self.ExpectedType(), 'y': object()},
            'd': {'m': self.ExpectedType(), 'n': object(), 'p': object()},
            'e': {'j': self.ExpectedType()},
            'f': [self.ExpectedType(), object()],
            'g': [self.ExpectedType()],
            'h': {
                'q': {
                    'r': {
                        's': [
                            [
                                self.ExpectedType()
                                ]
                            ]
                        }
                    }
                }
            }

        # data['d']['p'] is stripped.
        expected = data.copy()
        expected['d'] = {'m': data['d']['m'], 'n': data['d']['n']}

        result = validation_tools._validate_structure(
            schema=self.complex_schema, data=data
            )

        assert result == expected

    def test_validation_raises(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='TYPE', error_class=StructureValidationError
            ):
            validation_tools._validate_structure(
                schema=self.ExpectedType, data=object()
                )

    def test_validation_raises_complex(self):
        data = {
            'a': object(),
            'b': object(),
            'c': {'x': object(), 'y': object()},
            'd': {'m': object(), 'n': object(), 'p': object()},
            'e': {'j': object(), 'k': self.ExpectedType()},
            'f': [object(), object()],
            'g': [object(), self.ExpectedType()],
            'h': {
                'q': {
                    'r': {
                        's': [
                            [
                                object()
                                ]
                            ]
                        }
                    }
                }
            }

        error_codes = [
            [('a',), 'TYPE'],
            [('b',), 'TYPE'],
            [('c', 'x'), 'TYPE'],
            [('d', 'm'), 'TYPE'],
            [('e', 'j'), 'TYPE'],
            [('f', 0), 'TYPE'],
            [('g', 0), 'TYPE'],
            [('h', 'q', 'r', 's', 0, 0), 'TYPE'],
            ]

        with self.assertRaisesMultipleValidationErrors(
            error_codes=error_codes, error_class=StructureValidationError
            ):
            validation_tools._validate_structure(
                schema=self.complex_schema, data=data
                )


class TestValidateRulesUnit(unittest.TestCase):
    """ `validation_tools._validate_rules` """

    @patch('jsonmanager.validation_tools._validate_data')
    def test_no_error(self, mock_validate_data):
        validation_tools._validate_rules(
            schema=sentinel.schema,
            data=sentinel.data,
            default_rules=sentinel.default_rules,
            )

        mock_validate_data.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            location=tuple(),
            default_rules=sentinel.default_rules,
            validation_map=validation_tools.RULES_MAP,
            )

    @patch('jsonmanager.validation_tools.RulesValidationError')
    @patch('jsonmanager.validation_tools._validate_data')
    def test_yes_error(self, mock_validate_data, mock_RulesValidationError):
        """ If a `ValidationError` is raised, it is caught and
            `RulesValidationError` is raised. """
        errors = tuple([sentinel.error])
        mock_validate_data.side_effect = exceptions.ValidationError(*errors)

        class ExpectedError(Exception):
            pass

        mock_RulesValidationError.return_value = ExpectedError

        with self.assertRaises(ExpectedError):
            validation_tools._validate_rules(
                schema=sentinel.schema,
                data=sentinel.data,
                default_rules=sentinel.default_rules,
                )

        mock_validate_data.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            location=tuple(),
            default_rules=sentinel.default_rules,
            validation_map=validation_tools.RULES_MAP,
            )
        mock_RulesValidationError.assert_called_with(*errors)


class TestValidateRulesIntegration(ValidationErrorTest):
    """ `validation_tools._validate_rules` """

    def setUp(self):
        super().setUp()

        self.bad_default = object()
        self.bad_special = object()
        self.bad_overriding = object()

        def default_rule(data):
            if data is self.bad_default:
                raise RuleViolation(code='default')

        self.default_rules = (default_rule,)

        def special_rule(data):
            if data is self.bad_special:
                raise RuleViolation(code='special')

        self.special_rule = special_rule

        @override_defaults
        def overriding_rule(data):
            if data is self.bad_overriding:
                raise RuleViolation(code='overriding')

        self.complex_schema = {
            'a': AnyType,
            'b': (AnyType, special_rule),
            'c': {'x': AnyType, 'y': AnyType, 'z': (AnyType, special_rule)},
            'd': Dict({'j': (AnyType, special_rule)}),
            'e': DictOf(
                (AnyType, special_rule)
                ),
            'f': [AnyType, AnyType, (AnyType, special_rule)],
            'g': ListOf(
                (AnyType, special_rule)
                ),
            'h': {
                'q': Dict({
                    'r': DictOf(
                        [
                            ListOf(
                                (AnyType, special_rule)
                                )
                            ]
                        )
                    })
                },
            'i': ListOf(
                (AnyType, overriding_rule)
                )
            }

    def test_validation_passes_no_default_rules(self):
        validation_tools._validate_rules(
            schema=AnyType, data=object(), default_rules=tuple()
            )

    def test_validation_passes_yes_default_rules(self):
        validation_tools._validate_rules(
            schema=AnyType, data=object(), default_rules=self.default_rules
            )

    def test_validation_passes_complex(self):
        data = {
            'a': object(),
            'b': object(),
            'c': {'x': object(), 'y': object(), 'z': object()},
            'd': {'j': object()},
            'e': {'m': object()},
            'f': [object(), object(), object()],
            'g': [object()],
            'h': {
                'q': {
                    'r': {
                        's': [
                            [
                                object()
                                ]
                            ]
                        }
                    }
                },
            'i': [object()]
            }

        validation_tools._validate_rules(
            schema=self.complex_schema,
            data=data,
            default_rules=self.default_rules,
            )

    def test_validation_raises_no_default_rules(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='special', error_class=RulesValidationError,
            ):
            validation_tools._validate_rules(
                schema=(AnyType, self.special_rule),
                data=self.bad_special,
                default_rules=tuple()
                )

    def test_validation_raises_yes_default_rules(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='default', error_class=RulesValidationError,
            ):
            validation_tools._validate_rules(
                schema=AnyType,
                data=self.bad_default,
                default_rules=self.default_rules,
                )

    def test_validation_raises_complex(self):
        data = {
            'a': self.bad_default,
            'b': self.bad_special,
            'c': {'x': object(), 'y': self.bad_default, 'z': self.bad_special},
            'd': {'j': self.bad_special},
            'e': {'m': object(), 'n': self.bad_default, 'o': self.bad_special},
            'f': [object(), self.bad_default, self.bad_special],
            'g': [object(), self.bad_default, self.bad_special],
            'h': {
                'q': {
                    'r': {
                        's': [
                            [
                                self.bad_special,
                                ]
                            ]
                        }
                    }
                },
            'i': [self.bad_default, self.bad_overriding]
            }

        error_codes = [
            [('a',), 'default'],
            [('b',), 'special'],
            [('c', 'y'), 'default'],
            [('c', 'z'), 'special'],
            [('d', 'j'), 'special'],
            [('e', 'n'), 'default'],
            [('e', 'o'), 'special'],
            [('f', 1), 'default'],
            [('f', 2), 'special'],
            [('g', 1), 'default'],
            [('g', 2), 'special'],
            [('h', 'q', 'r', 's', 0, 0), 'special'],
            [('i', 1), 'overriding'],
            ]

        with self.assertRaisesMultipleValidationErrors(
            error_codes=error_codes, error_class=RulesValidationError
            ):
            validation_tools._validate_rules(
                schema=self.complex_schema,
                data=data,
                default_rules=self.default_rules
                )


class TestValidateDataUnit(unittest.TestCase):
    """ `validation_tools._validate_data` """

    @patch('jsonmanager.validation_tools.select_processor')
    def test_behavior(self, mock_select_processor):
        validation_function = MagicMock()
        validation_function.return_value = sentinel.expected

        mock_select_processor.return_value = validation_function
        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._validate_data(
            schema=sentinel.schema,
            data=sentinel.data,
            validation_map=sentinel.validation_map,
            **kwargs
            )

        mock_select_processor.assert_called_with(
            sentinel.schema, sentinel.validation_map
            )
        validation_function.assert_called_with(
            schema=sentinel.schema, data=sentinel.data, **kwargs
            )

        assert result is sentinel.expected


class TestValidateScalarStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_scalar_structure` """

    @patch_builtin('jsonmanager.validation_tools.isinstance')
    def test_correct_type_passes(self, mock_isinstance):
        mock_isinstance.return_value = True

        result = validation_tools._validate_scalar_structure(
            sentinel.schema, sentinel.data, sentinel.location
            )

        mock_isinstance.assert_called_with(sentinel.data, sentinel.schema)

        assert result is sentinel.data

    @patch_builtin('jsonmanager.validation_tools.isinstance')
    def test_none_passes(self, mock_isinstance):
        mock_isinstance.return_value = False

        result = validation_tools._validate_scalar_structure(
            sentinel.schema, None, sentinel.location
            )

        mock_isinstance.assert_called_with(None, sentinel.schema)

        assert result is None

    @patch('jsonmanager.validation_tools.raise_type_validation_error')
    @patch_builtin('jsonmanager.validation_tools.isinstance')
    def test_wrong_type_raises(
        self, mock_isinstance, mock_raise_type_validation_error
        ):
        schema = MagicMock()
        schema.__name__ = 'SCHEMA_TYPE'

        class ExpectedError(Exception):
            pass

        mock_isinstance.return_value = False
        mock_raise_type_validation_error.side_effect = ExpectedError

        with self.assertRaises(ExpectedError):
            validation_tools._validate_scalar_structure(
                schema, sentinel.data, sentinel.location
                )

        mock_isinstance.assert_called_with(sentinel.data, schema)
        mock_raise_type_validation_error.assert_called_with(
            '`SCHEMA_TYPE`', sentinel.data, sentinel.location
            )


class TestValidateScalarStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_scalar_structure` """

    def test_correct_type_passes(self):
        data = self.ExpectedType()

        result = validation_tools._validate_scalar_structure(
            schema=self.ExpectedType,
            data=data,
            location=tuple()
            )

        assert result is data

    def test_None_passes(self):
        result = validation_tools._validate_scalar_structure(
            schema=self.ExpectedType,
            data=None,
            location=tuple()
            )

        assert result is None

    def test_wrong_type_raises(self):
        with self.assertRaisesSingleValidationError(
            location=('x',), code='TYPE'
            ):
            validation_tools._validate_scalar_structure(
                schema=self.ExpectedType,
                data=object(),
                location=('x',)
                )


class TestValidateScalarRulesUnit(unittest.TestCase):
    """ `validation_tools._validate_scalar_rules` """

    @patch('jsonmanager.validation_tools._validate_tuple_rules')
    def test_behavior(self, mock_validate_tuple_rules):
        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        validation_tools._validate_scalar_rules(
            schema=sentinel.schema,
            **kwargs
            )

        mock_validate_tuple_rules.assert_called_with(
            schema=tuple([sentinel.schema]),
            **kwargs
            )


class TestValidateScalarRulesIntegration(ValidationErrorTest):
    """ `validation_tools._validate_scalar_rules` """

    def test_validation_passes(self):
        validation_tools._validate_scalar_rules(
            schema=AnyType,
            data=object(),
            location=tuple(),
            default_rules=tuple(),
            )

    def test_default_rules_applied(self):
        def rule(data): # pylint: disable=unused-argument
            raise RuleViolation(code='rule')

        with self.assertRaisesSingleValidationError(
            location=tuple(), code='rule'
            ):
            validation_tools._validate_scalar_rules(
                schema=AnyType,
                data=object(),
                location=tuple(),
                default_rules=(rule,)
                )


class TestValidateTupleStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_tuple_structure` """

    @patch('jsonmanager.validation_tools._validate_data')
    def test_behavior(self, mock_validate_data):
        schema_tuple = MagicMock()
        schema_tuple.__getitem__.return_value = sentinel.schema
        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        mock_validate_data.return_value = sentinel.expected

        result = validation_tools._validate_tuple_structure(
            schema=schema_tuple, **kwargs
            )

        schema_tuple.__getitem__.assert_called_with(0)
        mock_validate_data.assert_called_with(
            schema=sentinel.schema,
            validation_map=validation_tools.STRUCTURE_MAP,
            **kwargs
            )

        assert result is sentinel.expected


class TestValidateTupleStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_tuple_structure` """

    def test_passes(self):
        data = self.ExpectedType()
        result = validation_tools._validate_tuple_structure(
            schema=(self.ExpectedType, sentinel.rule),
            data=data,
            location=tuple()
            )
        assert result is data

    def test_raises(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='TYPE'
            ):
            validation_tools._validate_tuple_structure(
                schema=(self.ExpectedType, sentinel.rule),
                data=object(),
                location=tuple()
                )


class TestValidateTupleRulesUnit(unittest.TestCase):
    """ `validation_tools._validate_tuple_rules` """

    @patch('jsonmanager.validation_tools._validate_data')
    @patch('jsonmanager.validation_tools.apply_rules')
    @patch('jsonmanager.validation_tools.get_rules')
    def test_behavior(
        self, mock_get_rules, mock_apply_rules, mock_validate_data
        ):
        schema_tuple = MagicMock()
        schema_tuple.__getitem__.return_value = sentinel.schema

        mock_get_rules.return_value = sentinel.rules

        validation_tools._validate_tuple_rules(
            schema=schema_tuple,
            data=sentinel.data,
            location=sentinel.location,
            default_rules=sentinel.default_rules,
            )

        mock_get_rules.assert_called_with(
            schema_tuple, sentinel.default_rules
            )
        mock_apply_rules.assert_called_with(
            sentinel.rules, sentinel.data, sentinel.location
            )
        schema_tuple.__getitem__.assert_called_with(0)
        mock_validate_data.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            validation_map=validation_tools.RULES_TUPLE_MAP,
            location=sentinel.location,
            default_rules=sentinel.default_rules,
            )


class TestValidateTupleRulesIntegration(ValidationErrorTest):
    """ `validation_tools._validate_tuple_rules` """

    def setUp(self):
        super().setUp()

        def rule_passes(data): # pylint: disable=unused-argument
            pass

        def rule_fails(data): # pylint: disable=unused-argument
            raise RuleViolation(
                code=sentinel.code,
                message=sentinel.message,
                data=sentinel.data,
                key='b',
                )

        def rule_not_called(data): # pylint: disable=unused-argument
            raise Exception

        self.rule_passes = rule_passes
        self.rule_fails = rule_fails
        self.rule_not_called = rule_not_called

    def validation_passes_test(self, schema):
        validation_tools._validate_tuple_rules(
            schema=schema,
            data=object(),
            location=tuple(),
            default_rules=tuple(),
            )

    def test_passes(self):
        """ When rules raise no errors, validation passes. """
        schema = (AnyType, self.rule_passes)

        self.validation_passes_test(schema)

    def test_StopValidation_stops_validation(self):
        """ When a rule raises `StopValidation`, further rules are not called.
            """
        def rule_stops(data): # pylint: disable=unused-argument
            raise StopValidation

        schema = (
            AnyType, self.rule_passes, rule_stops, self.rule_not_called
            )

        self.validation_passes_test(schema)

    def validation_raises_test(self, schema, default_rules):
        with self.assertRaisesSingleValidationError(
            location=('a', 'b'),
            code=sentinel.code,
            message=sentinel.message,
            data=sentinel.data,
            ):
            validation_tools._validate_tuple_rules(
                schema=schema,
                data=object(),
                location=('a',),
                default_rules=default_rules,
                )

    def test_RuleViolation_raises_ValidationError(self):
        """ When a rule raises `RuleViolation`, the exception is caught and a
            `ValidationError` is raised. Further rules are not called. """
        schema = (
            AnyType, self.rule_passes, self.rule_fails, self.rule_not_called
            )
        default_rules = tuple()

        self.validation_raises_test(schema, default_rules)

    def test_default_rules(self):
        """ `default_rules` are prepended to given rules. """
        schema = (AnyType, self.rule_not_called)
        default_rules = (self.rule_passes, self.rule_fails)

        self.validation_raises_test(schema, default_rules)

    def test_override_defaults(self):
        """ When the first given rule is decorated with `override_defaults`,
            `default_rules` are not prepended. """

        @override_defaults
        def rule_overrides_defaults(data): # pylint: disable=unused-argument
            pass

        schema = (AnyType, rule_overrides_defaults, self.rule_fails)
        default_rules = (self.rule_not_called,)

        self.validation_raises_test(schema, default_rules)


class TestValidateTupleRulesTupleMapIntegration(ValidationErrorTest):
    """ `validation_tools._validate_tuple`, `validation_tools.RULES_TUPLE_MAP`

        Confirm that `RULES_TUPLE_MAP` is configured correctly for schema types
        other than `type` and `tuple`. """

    def validation_passes_test(self, schema, data):
        validation_tools._validate_tuple_rules(
            schema=tuple([schema]),
            data=data,
            location=tuple(),
            default_rules=tuple(),
            )

    def test_dict_passes(self):
        self.validation_passes_test(
            schema={'a': AnyType},
            data={'a': object()},
            )

    def test_Dict_passes(self):
        self.validation_passes_test(
            schema=Dict({'a': AnyType}),
            data={'a': object()},
            )

    def test_DictOf_passes(self):
        self.validation_passes_test(
            schema=DictOf(AnyType),
            data={'a': object()},
            )

    def test_list_passes(self):
        self.validation_passes_test(
            schema=[AnyType],
            data=[object()],
            )

    def test_ListOf_passes(self):
        self.validation_passes_test(
            schema=ListOf(AnyType),
            data=[object()],
            )


class TestApplyRulesUnit(unittest.TestCase):
    """ `validation_tools.apply_rules` """

    def test_rule_passes(self):
        """ Rule function raises no errors. """
        rules_sequence = [MagicMock() for i in range(3)]

        rules = MagicMock()
        rules.__iter__.return_value = rules_sequence

        validation_tools.apply_rules(
            rules=rules, data=sentinel.input_data, location=sentinel.location
            )

        for rule in rules_sequence:
            rule.assert_called_with(sentinel.input_data)

    @patch('jsonmanager.validation_tools.ValidationError')
    @patch('jsonmanager.validation_tools.make_error_dict')
    def test_rule_raises_RuleViolation(
        self, mock_make_error_dict, mock_ValidationError
        ):
        """ Rule function raises `RuleViolation`. """
        exc = RuleViolation(
            code=sentinel.code,
            message=sentinel.message,
            data=sentinel.error_data,
            key=sentinel.key,
            )

        rules_sequence = [MagicMock() for i in range(3)]
        rules_sequence[1].side_effect = exc

        rules = MagicMock()
        rules.__iter__.return_value = rules_sequence

        location = MagicMock()
        location.__add__.return_value = sentinel.full_location

        mock_make_error_dict.return_value = sentinel.error_dict

        class ExpectedError(Exception):
            pass

        mock_ValidationError.return_value = ExpectedError

        with self.assertRaises(ExpectedError):
            validation_tools.apply_rules(
                rules=rules, data=sentinel.input_data, location=location
                )

        rules_sequence[0].assert_called_with(sentinel.input_data)
        rules_sequence[1].assert_called_with(sentinel.input_data)
        assert not rules_sequence[2].called

        location.__add__.assert_called_with(
            tuple([sentinel.key])
            )

        mock_make_error_dict.assert_called_with(
            location=sentinel.full_location,
            code=sentinel.code,
            message=sentinel.message,
            data=sentinel.error_data,
            )

        mock_ValidationError.assert_called_with(sentinel.error_dict)

    def test_rule_raises_StopValidation(self):
        """ Rule function raises `StopValidation`. """
        rules_sequence = [MagicMock() for i in range(3)]
        rules_sequence[1].side_effect = StopValidation

        rules = MagicMock()
        rules.__iter__.return_value = rules_sequence

        validation_tools.apply_rules(
            rules=rules, data=sentinel.data, location=sentinel.location
            )

        rules_sequence[0].assert_called_with(sentinel.data)
        rules_sequence[1].assert_called_with(sentinel.data)
        assert not rules_sequence[2].called


class TestGetRulesUnit(unittest.TestCase):
    """ `validation_tools.get_rules` """

    def setUp(self):
        self.schema_tuple = (sentinel.schema, sentinel.rule_0, sentinel.rule_1)
        self.schema_rules = (sentinel.rule_0, sentinel.rule_1)
        self.default_rules = (sentinel.default_0, sentinel.default_1)

    @patch('jsonmanager.validation_tools.get_override_defaults')
    def test_yes_override_defaults(self, mock_override_defaults):
        """ Just schema rules returned. """
        mock_override_defaults.return_value = True

        result = validation_tools.get_rules(
            schema=self.schema_tuple,
            default_rules=self.default_rules
            )

        assert result == self.schema_rules

    @patch('jsonmanager.validation_tools.get_override_defaults')
    def test_no_override_defaults(self, mock_override_defaults):
        """ Default rules prepended to schema rules. """
        mock_override_defaults.return_value = False

        result = validation_tools.get_rules(
            schema=self.schema_tuple,
            default_rules=self.default_rules
            )

        assert result == self.default_rules + self.schema_rules


class TestGetOverrideDefaultsFunctional(unittest.TestCase):
    """ `validation_tools.get_override_defaults` """

    def test_no_rules(self):
        rules = tuple()
        result = validation_tools.get_override_defaults(rules)
        assert result is False

    def test_yes_override_defaults(self):
        rule = MagicMock()
        rule.override_defaults = sentinel.expected
        rules = (rule,)

        result = validation_tools.get_override_defaults(rules)

        assert result is sentinel.expected

    def test_no_override_defaults(self):
        rule = MagicMock()
        del rule.override_defaults
        rules = (rule,)

        result = validation_tools.get_override_defaults(rules)

        assert result is False


class TestValidateDictStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_dict_structure` """

    def test_validation_passes(self):
        schema = {'a': self.ExpectedType}
        data = {'a': self.ExpectedType()}

        result = validation_tools._validate_dict_structure(
            schema=schema, data=data, location=tuple()
            )

        assert result == data

    def test_empty_data_passes(self):
        result = validation_tools._validate_dict_structure(
            schema={}, data={}, location=tuple()
            )

        assert result == {}

    def test_missing_optional_passes(self):
        result = validation_tools._validate_dict_structure(
            schema={'a': AnyType},
            data={},
            location=tuple(),
            optional_keys=set(['a'])
            )

        assert result == {}

    def test_strip_extras_passes(self):
        schema = {'a': AnyType}
        data = {'a': sentinel.a, 'b': sentinel.b}
        expected = {'a': sentinel.a}

        result = validation_tools._validate_dict_structure(
            schema=schema, data=data, location=tuple(), strip_extras=True
            )

        assert result == expected

    def single_error_test(self, schema, data, location, code):
        with self.assertRaisesSingleValidationError(location, code):
            validation_tools._validate_dict_structure(
                schema=schema, data=data, location=('x',)
                )

    def test_not_a_dict_raises(self):
        self.single_error_test(
            schema={},
            data=object(),
            location=('x',),
            code='TYPE',
            )

    def test_wrong_type_raises(self):
        self.single_error_test(
            schema={'a': self.ExpectedType},
            data={'a': object()},
            location=('x', 'a'),
            code='TYPE',
            )

    def test_missing_raises(self):
        self.single_error_test(
            schema={'a': AnyType},
            data={},
            location=('x', 'a'),
            code='MISSING',
            )

    def test_not_allowed_raises(self):
        self.single_error_test(
            schema={},
            data={'a': object()},
            location=('x', 'a'),
            code='NOT_ALLOWED',
            )

    def multiple_errors_test(self, schema, data, error_codes):
        with self.assertRaisesMultipleValidationErrors(error_codes):
            validation_tools._validate_dict_structure(
                schema=schema, data=data, location=('x',)
                )

    def test_multiple_errors_raises(self):
        schema = {
            'a': self.ExpectedType,
            'b': self.ExpectedType,
            'c': AnyType,
            }
        data = {
            'a': self.ExpectedType(),
            'b': object(),
            'd': object(),
            }
        error_codes = [
            [('x', 'b'), 'TYPE'],
            [('x', 'c'), 'MISSING'],
            [('x', 'd'), 'NOT_ALLOWED'],
            ]

        self.multiple_errors_test(schema, data, error_codes)

    def test_nested_error_raises(self):
        """ Nested errors are correctly detected and merged with top-level
            errors. """
        schema = {
            'a': self.ExpectedType,
            'b': {'c': self.ExpectedType}
            }
        data = {
            'a': object(),
            'b': {'c': object()}
            }
        error_codes = [
            [('x', 'a'), 'TYPE'],
            [('x', 'b', 'c'), 'TYPE'],
            ]

        self.multiple_errors_test(schema, data, error_codes)


class TestGetValidatedItemAndCaptureErrorsUnit(unittest.TestCase):
    """ `validation_tools.get_validated_item_and_capture_errors` """

    @patch('jsonmanager.validation_tools._validate_data')
    def test_no_errors(self, mock_validate_data):
        mock_validate_data.return_value = sentinel.validated_data

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools.get_validated_item_and_capture_errors(
            key=sentinel.key, **kwargs
            )

        mock_validate_data.assert_called_with(
            validation_map=validation_tools.STRUCTURE_MAP, **kwargs
            )

        assert result == ((sentinel.key, sentinel.validated_data), tuple())

    @patch('jsonmanager.validation_tools._validate_data')
    def test_yes_errors(self, mock_validate_data):
        validation_error = exceptions.ValidationError(sentinel.error_dict)
        mock_validate_data.side_effect = validation_error

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools.get_validated_item_and_capture_errors(
            key=sentinel.key, **kwargs
            )

        mock_validate_data.assert_called_with(
            validation_map=validation_tools.STRUCTURE_MAP, **kwargs
            )

        assert result == ((sentinel.key, None), validation_error.errors)


class TestValidateDictRulesIntegration(ValidationErrorTest):
    """ `validation_tools._validate_dict_rules` """

    def test_validation_passes(self):
        validation_tools._validate_dict_rules(
            schema={'a': AnyType},
            data={'a': object()},
            location=tuple(),
            default_rules=tuple()
            )

    def test_rules_fail(self):
        def rule(data): # pylint: disable=unused-argument
            raise RuleViolation(code='rule')

        schema = {
            'a': (AnyType, rule),
            'b': (AnyType, rule),
            'c': AnyType,
            'd': {'x': (AnyType, rule)},
            }
        data = {
            'a': object(),
            'b': object(),
            'c': object(),
            'd': {'x': object()},
            }
        error_codes = [
            [('a',), 'rule'],
            [('b',), 'rule'],
            [('d', 'x'), 'rule'],
            ]

        with self.assertRaisesMultipleValidationErrors(error_codes):
            validation_tools._validate_dict_rules(
                schema=schema,
                data=data,
                location=tuple(),
                default_rules=tuple(),
                )


class TestRaiseIfErrorsUnit(unittest.TestCase):
    """ `validation_tools.raise_if_errors` """

    @patch('jsonmanager.validation_tools.ValidationError')
    def test_yes_errors_raises(self, mock_ValidationError):
        errors_list = [sentinel.error_dict_a, sentinel.error_dict_b]

        errors = MagicMock()
        errors.__bool__.return_value = True
        errors.__iter__.return_value = errors_list

        class ExpectedError(Exception):
            pass

        mock_ValidationError.return_value = ExpectedError()

        with self.assertRaises(ExpectedError):
            validation_tools.raise_if_errors(errors)

        mock_ValidationError.assert_called_with(*errors_list)

    def test_no_errors_passes(self):
        errors = MagicMock()
        errors.__bool__.return_value = False

        validation_tools.raise_if_errors(errors)


class TestCaptureErrorsUnit(unittest.TestCase):
    """ `validation_tools.capture_errors` """

    @patch('jsonmanager.validation_tools._validate_data')
    def test_yes_error(self, mock_validate_data):
        """ If a `ValidationError` is raised, the `.errors` attribute value is
            returned. """
        expected_error = ValidationError()
        expected_error.errors = sentinel.errors

        mock_validate_data.side_effect = expected_error

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools.capture_errors(**kwargs)

        mock_validate_data.assert_called_with(**kwargs)

        assert result is sentinel.errors

    @patch('jsonmanager.validation_tools._validate_data')
    def test_no_error(self, mock_validate_data):
        """ If no `ValidationError` is raised, an empty tuple is returned. """
        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools.capture_errors(**kwargs)

        mock_validate_data.assert_called_with(**kwargs)

        assert result == tuple()


class TestValidateDictSchemaTypeStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_Dict_structure` """

    @patch('jsonmanager.validation_tools._validate_dict_structure')
    def test_behavior(self, mock_validate_dict_structure):
        schema = MagicMock()
        schema.schema = sentinel.schema_dict
        schema.validate_structure_kwargs = dict(
            validation_kwarg_name=sentinel.validation_kwarg_value
            )

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        complete_kwargs = dict(
            kwarg_name=sentinel.kwarg_value,
            validation_kwarg_name=sentinel.validation_kwarg_value,
            )

        mock_validate_dict_structure.return_value = sentinel.expected

        result = validation_tools._validate_Dict_structure(
            schema=schema, **kwargs
            )

        mock_validate_dict_structure.assert_called_with(
            schema=sentinel.schema_dict, **complete_kwargs
            )

        assert result is sentinel.expected


class TestValidateDictSchemaTypeStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_Dict_structure` """

    def test_validation_passes(self):
        """ No special arguments provided. """
        data = {'a': self.ExpectedType()}

        result = validation_tools._validate_Dict_structure(
            schema=Dict({'a': self.ExpectedType}),
            data=data,
            location=tuple()
            )

        assert result == data

    def test_optional_keys_passes(self):
        """ With `optional_keys` argument, missing key does not raise error. """
        data = {'a': self.ExpectedType()}

        result = validation_tools._validate_Dict_structure(
            schema=Dict(
                {'a': self.ExpectedType, 'b': self.ExpectedType},
                optional_keys=['b']
                ),
            data=data,
            location=tuple()
            )

        assert result == data

    def test_strip_extras_passes(self):
        """ With `strip_extras` argument, extra keys are stripped, and no error
            is raised. """
        data = {'a': self.ExpectedType(), 'b': object()}
        expected = {'a': data['a']}

        result = validation_tools._validate_Dict_structure(
            schema=Dict(
                {'a': self.ExpectedType},
                strip_extras=True
                ),
            data=data,
            location=tuple()
            )

        assert result == expected

    def test_missing_raises(self):
        """ Without `optional_keys` argument, missing key raises error. """
        with self.assertRaisesSingleValidationError(
            location=('a',), code='MISSING'
            ):
            validation_tools._validate_Dict_structure(
                schema=Dict({'a': self.ExpectedType}),
                data={},
                location=tuple(),
                )

    def test_not_allowed_raises(self):
        """ Without `strip_extras` argument, extra key raises error. """
        with self.assertRaisesSingleValidationError(
            location=('a',), code='NOT_ALLOWED'
            ):
            validation_tools._validate_Dict_structure(
                schema=Dict({}),
                data={'a': self.ExpectedType()},
                location=tuple(),
                )


class TestValidateDictSchemaTypeRulesUnit(unittest.TestCase):
    """ `validation_tools._validate_Dict_rules` """

    @patch('jsonmanager.validation_tools._validate_dict_rules')
    def test_behavior(self, mock_validate_dict_rules):
        schema = MagicMock()

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        validation_tools._validate_Dict_rules(schema=schema, **kwargs)

        mock_validate_dict_rules.assert_called_with(
            schema=schema.schema, **kwargs
            )


class TestValidateDictSchemaTypeRulesIntegration(ValidationErrorTest):
    """ `validation_tools._validate_Dict_rules` """

    def test_validation_passes(self):
        validation_tools._validate_Dict_rules(
            schema=Dict({'a': AnyType}),
            data={'a': object()},
            location=tuple(),
            default_rules=tuple()
            )

    def test_rule_fails(self):
        def rule(data):
            if data is not None:
                raise RuleViolation(code='rule')

        with self.assertRaisesSingleValidationError(
            location=('a',), code='rule'
            ):
            validation_tools._validate_Dict_rules(
                schema=Dict({'a': (AnyType, rule)}),
                data={'a': object()},
                location=tuple(),
                default_rules=tuple(),
                )


class TestValidateDictOfStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_DictOf_structure` """

    @patch('jsonmanager.validation_tools._validate_DictOf')
    @patch('jsonmanager.validation_tools.confirm_mapping')
    def test_behavior(self, mock_confirm_mapping, mock_validate_DictOf):
        mock_validate_DictOf.return_value = sentinel.expected

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._validate_DictOf_structure(
            data=sentinel.data, location=sentinel.location, **kwargs
            )

        mock_confirm_mapping.assert_called_with(
            sentinel.data, sentinel.location
            )
        mock_validate_DictOf.assert_called_with(
            data=sentinel.data,
            location=sentinel.location,
            validation_map=validation_tools.STRUCTURE_MAP,
            **kwargs
            )

        assert result is sentinel.expected


class TestValidateDictOfStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_DictOf_structure` """

    def test_validation_passes(self):
        data = {'a': self.ExpectedType()}

        result = validation_tools._validate_DictOf_structure(
            schema=DictOf(self.ExpectedType), data=data, location=tuple()
            )

        assert result == data

    def test_empty_dict_passes(self):
        result = validation_tools._validate_DictOf_structure(
            schema=DictOf(self.ExpectedType), data={}, location=tuple()
            )
        assert result == {}

    def single_error_test(self, schema, data, location):
        with self.assertRaisesSingleValidationError(location, code='TYPE'):
            validation_tools._validate_DictOf_structure(
                schema=schema, data=data, location=('x',)
                )

    def test_arbitrary_keys(self):
        """ Validation works with arbitrary keys. """
        schema = DictOf(self.ExpectedType)
        data = {
            'a': self.ExpectedType(),
            'b': object(),
            }
        location = ('x', 'b')

        self.single_error_test(schema, data, location)

    def test_nested(self):
        """ Validation works with nested structures. """
        schema = DictOf(
            {'q': self.ExpectedType}
            )
        data = {
            'a': {'q': self.ExpectedType()},
            'b': {'q': object()},
            }
        location = ('x', 'b', 'q')

        self.single_error_test(schema, data, location)


class TestValidateDictOfRulesUnit(unittest.TestCase):
    """ `validation_tools._validate_DictOf_rules` """

    @patch('jsonmanager.validation_tools._validate_DictOf')
    def test_behavior(self, mock_validate_DictOf):
        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        validation_tools._validate_DictOf_rules(**kwargs)

        mock_validate_DictOf.assert_called_with(
            validation_map=validation_tools.RULES_MAP, **kwargs
            )


class TestValidateDictOfRulesIntegration(ValidationErrorTest):
    """ `validation_tools._validate_DictOf_rules` """

    def test_validation_passes(self):
        validation_tools._validate_DictOf_rules(
            schema=DictOf(AnyType),
            data={'a': object()},
            location=tuple(),
            default_rules=tuple()
            )

    def test_rules_fail(self):
        def rule(data):
            if data is not None:
                raise RuleViolation(code='rule')

        schema = DictOf(
            (AnyType, rule)
            )
        data = {
            'a': object(),
            'b': object(),
            'c': None,
            }
        error_codes = [
            [('a',), 'rule'],
            [('b',), 'rule'],
            ]

        with self.assertRaisesMultipleValidationErrors(error_codes):
            validation_tools._validate_DictOf_rules(
                schema=schema,
                data=data,
                location=tuple(),
                default_rules=tuple(),
                )


class TestValidateDictOfUnit(unittest.TestCase):
    """ `validation_tools._validate_DictOf` """

    @patch('jsonmanager.validation_tools._validate_data')
    def test_behavior(self, mock_validate_data):
        mock_validate_data.return_value = sentinel.expected

        schema = MagicMock()

        data = MagicMock()
        data.keys.return_value.__iter__.return_value = [sentinel.key]

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._validate_DictOf(
            schema=schema, data=data, **kwargs
            )

        mock_validate_data.assert_called_with(
            schema={sentinel.key: schema.schema}, data=data, **kwargs
            )

        assert result is sentinel.expected


class TestValidateListStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_list_structure` """

    @patch('jsonmanager.validation_tools._validate_list')
    @patch('jsonmanager.validation_tools.confirm_sequence')
    def test_behavior(self, mock_confirm_sequence, mock_validate_list):
        mock_validate_list.return_value = sentinel.expected

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._validate_list_structure(
            data=sentinel.data, location=sentinel.location, **kwargs
            )

        mock_confirm_sequence.assert_called_with(
            sentinel.data, sentinel.location
            )
        mock_validate_list.assert_called_with(
            data=sentinel.data,
            location=sentinel.location,
            validation_map=validation_tools.STRUCTURE_MAP,
            **kwargs
            )

        assert result is sentinel.expected


class TestValidateListStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_list_structure` """

    def test_no_errors_passes(self):
        data = [self.ExpectedType()]
        result = validation_tools._validate_list_structure(
            schema=[self.ExpectedType],
            data=data,
            location=('x',)
            )
        assert result == data

    def single_error_test(self, schema, data, location, code):
        with self.assertRaisesSingleValidationError(location, code):
            validation_tools._validate_list_structure(
                schema=schema, data=data, location=('x',)
                )

    def test_wrong_type_raises(self):
        self.single_error_test(
            schema=[self.ExpectedType],
            data=[object()],
            location=('x', 0),
            code='TYPE',
            )

    def test_missing_raises(self):
        self.single_error_test(
            schema=[AnyType],
            data=[],
            location=('x', 0),
            code='MISSING'
            )

    def test_not_allowed_raises(self):
        self.single_error_test(
            schema=[],
            data=[object()],
            location=('x', 0),
            code='NOT_ALLOWED',
            )

    def multiple_errors_test(self, schema, data, error_codes):
        with self.assertRaisesMultipleValidationErrors(error_codes):
            validation_tools._validate_list_structure(
                schema=schema, data=data, location=('x',)
                )

    def test_multiple_errors_raises(self):
        schema = [
            self.ExpectedType,
            self.ExpectedType,
            AnyType,
            ]
        data = [
            self.ExpectedType(),
            object(),
            ]
        error_codes = [
            [('x', 1), 'TYPE'],
            [('x', 2), 'MISSING'],
            ]

        self.multiple_errors_test(schema, data, error_codes)

    def test_nested_error_raises(self):
        """ Nested errors are correctly detected and merged with top-level
            errors. """
        schema = [
            self.ExpectedType,
            {'a': self.ExpectedType}
            ]
        data = [
            object(),
            {'a': object()}
            ]
        error_codes = [
            [('x', 0), 'TYPE'],
            [('x', 1, 'a'), 'TYPE']
            ]

        self.multiple_errors_test(schema, data, error_codes)


class TestValidateListRulesUnit(unittest.TestCase):
    """ `validation_tools._validate_list_rules` """

    @patch('jsonmanager.validation_tools._validate_list')
    def test_behavior(self, mock_validate_list):
        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        validation_tools._validate_list_rules(**kwargs)

        mock_validate_list.assert_called_with(
            validation_map=validation_tools.RULES_MAP, **kwargs
            )


class TestValidateListRulesIntegration(ValidationErrorTest):
    """ `validation_tools._validate_list_rules` """

    def test_validation_passes(self):
        validation_tools._validate_list_rules(
            schema=[AnyType],
            data=[object()],
            location=tuple(),
            default_rules=tuple()
            )

    def test_rules_fail(self):
        def rule(data): # pylint: disable=unused-argument
            raise RuleViolation(code='rule')

        schema = [
            (AnyType, rule),
            (AnyType, rule),
            AnyType
            ]
        data = [
            object(),
            object(),
            object(),
            ]
        error_codes = [
            [(0,), 'rule'],
            [(1,), 'rule'],
            ]

        with self.assertRaisesMultipleValidationErrors(error_codes):
            validation_tools._validate_list_rules(
                schema=schema,
                data=data,
                location=tuple(),
                default_rules=tuple(),
                )


class TestValidateListUnit(unittest.TestCase):
    """ `validation_tools._validate_list` """

    @patch('jsonmanager.validation_tools._validate_data')
    @patch_builtin('jsonmanager.validation_tools.dict')
    @patch_builtin('jsonmanager.validation_tools.enumerate')
    def test_behavior(
        self,
        mock_enumerate,
        mock_dict,
        mock_validate_data
        ):
        mock_enumerate.side_effect = [
            sentinel.enumerated_schema, sentinel.enumerated_data
            ]
        mock_dict.side_effect = [sentinel.dict_schema, sentinel.dict_data]

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._validate_list(
            schema=sentinel.schema, data=sentinel.data, **kwargs
            )

        mock_enumerate.assert_has_calls([
            call(sentinel.schema), call(sentinel.data)
            ])
        mock_dict.assert_has_calls([
            call(sentinel.enumerated_schema), call(sentinel.enumerated_data)
            ])
        mock_validate_data.assert_called_with(
            schema=sentinel.dict_schema,
            data=sentinel.dict_data,
            **kwargs
            )

        assert result is sentinel.data


class TestValidateListOfStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_ListOf_structure` """

    @patch('jsonmanager.validation_tools._validate_ListOf')
    @patch('jsonmanager.validation_tools.confirm_sequence')
    def test_behavior(self, mock_confirm_sequence, mock_validate_ListOf):
        mock_validate_ListOf.return_value = sentinel.expected

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._validate_ListOf_structure(
            data=sentinel.data,
            location=sentinel.location,
            **kwargs
            )

        mock_confirm_sequence.assert_called_with(
            sentinel.data, sentinel.location
            )
        mock_validate_ListOf.assert_called_with(
            data=sentinel.data,
            location=sentinel.location,
            validation_map=validation_tools.STRUCTURE_MAP,
            **kwargs
            )

        assert result is sentinel.expected


class TestValidateListOfStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_ListOf_structure` """

    def test_validation_passes(self):
        data = [self.ExpectedType()]
        result = validation_tools._validate_ListOf_structure(
            schema=ListOf(self.ExpectedType), data=data, location=tuple()
            )
        assert result == data

    def test_empty_list_passes(self):
        result = validation_tools._validate_ListOf_structure(
            schema=ListOf(self.ExpectedType), data=[], location=tuple()
            )
        assert result == []

    def single_error_test(self, schema, data, location):
        with self.assertRaisesSingleValidationError(location, code='TYPE'):
            validation_tools._validate_ListOf_structure(
                schema=schema, data=data, location=('x',)
                )

    def test_arbitrary_length(self):
        """ Validation passes with arbitrary length. """
        schema = ListOf(self.ExpectedType)
        data = [
            self.ExpectedType(),
            object()
            ]
        location = ('x', 1)

        self.single_error_test(schema, data, location)

    def test_nested(self):
        """ Validation works with nested structures. """
        schema = ListOf(
            {'q': self.ExpectedType}
            )
        data = [
            {'q': self.ExpectedType()},
            {'q': object()},
            ]
        location = ('x', 1, 'q')

        self.single_error_test(schema, data, location)


class TestValidateListOfRulesUnit(unittest.TestCase):
    """ `validation_tools._validate_ListOf_rules` """

    @patch('jsonmanager.validation_tools._validate_ListOf')
    def test_behavior(self, mock_validate_ListOf):
        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        validation_tools._validate_ListOf_rules(**kwargs)

        mock_validate_ListOf.assert_called_with(
            validation_map=validation_tools.RULES_MAP, **kwargs
            )


class TestValidateListOfRulesIntegration(ValidationErrorTest):
    """ `validation_tools._validate_ListOf_rules` """

    def test_validation_passes(self):
        validation_tools._validate_ListOf_rules(
            schema=ListOf(AnyType),
            data=[object()],
            location=tuple(),
            default_rules=tuple()
            )

    def test_rules_fail(self):
        def rule(data):
            if data is not None:
                raise RuleViolation(code='rule')

        schema = ListOf(
            (AnyType, rule)
            )
        data = [
            object(),
            object(),
            None
            ]
        error_codes = [
            [(0,), 'rule'],
            [(1,), 'rule'],
            ]

        with self.assertRaisesMultipleValidationErrors(error_codes):
            validation_tools._validate_ListOf_rules(
                schema=schema,
                data=data,
                location=tuple(),
                default_rules=tuple(),
                )


class TestValidateListOfUnit(unittest.TestCase):
    """ `validation_tools._validate_ListOf` """

    @patch('jsonmanager.validation_tools._validate_list')
    def test_behavior(self, mock_validate_list):
        mock_validate_list.return_value = sentinel.expected

        schema = MagicMock()

        data = MagicMock()
        data.__iter__.return_value = [sentinel.item]

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._validate_ListOf(
            schema=schema, data=data, **kwargs
            )

        mock_validate_list.assert_called_with(
            schema=[schema.schema], data=data, **kwargs
            )

        assert result is sentinel.expected


class TestValidatePassUnit(unittest.TestCase):
    """ `validation_tools._validate_pass` """

    def test_behavior(self):
        """ This function just passes. """
        validation_tools._validate_pass(kwarg_name=sentinel.kwarg_value)


class TestConfirmMappingUnit(unittest.TestCase):
    """ `validation_tools.confirm_mapping` """

    @patch('jsonmanager.validation_tools.is_mapping')
    def test_yes_mapping_passes(self, mock_is_mapping):
        mock_is_mapping.return_value = True

        validation_tools.confirm_mapping(
            data=sentinel.data, location=sentinel.location
            )

    @patch('jsonmanager.validation_tools.raise_type_validation_error')
    @patch('jsonmanager.validation_tools.is_mapping')
    def test_not_mapping_raises(
        self, mock_is_mapping, mock_raise_type_validation_error
        ):
        class ExpectedError(Exception):
            pass

        mock_is_mapping.return_value = False
        mock_raise_type_validation_error.side_effect = ExpectedError

        with self.assertRaises(ExpectedError):
            validation_tools.confirm_mapping(
                data=sentinel.data, location=sentinel.location
                )

        mock_is_mapping.assert_called_with(sentinel.data)
        mock_raise_type_validation_error.assert_called_with(
            schema_name='mapping',
            data=sentinel.data,
            location=sentinel.location
            )


class TestConfirmMappingIntegration(ValidationErrorTest):
    """ `validation_tools.confirm_mapping` """

    def test_dict_passes(self):
        validation_tools.confirm_mapping(data=dict(), location=tuple())

    def test_non_dict_mapping_passes(self):
        validation_tools.confirm_mapping(
            data=collections.UserDict(), location=tuple()
            )

    def test_not_a_mapping_raises(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='TYPE'
            ):
            validation_tools.confirm_mapping(data=object(), location=tuple())


class TestConfirmSequenceUnit(unittest.TestCase):
    """ `validation_tools.confirm_sequence` """

    @patch('jsonmanager.validation_tools.is_sequence')
    def test_yes_sequence_passes(self, mock_is_sequence):
        mock_is_sequence.return_value = True

        validation_tools.confirm_sequence(
            data=sentinel.data, location=sentinel.location
            )

    @patch('jsonmanager.validation_tools.raise_type_validation_error')
    @patch('jsonmanager.validation_tools.is_sequence')
    def test_not_sequence_raises(
        self, mock_is_sequence, mock_raise_type_validation_error
        ):
        class ExpectedError(Exception):
            pass

        mock_is_sequence.return_value = False
        mock_raise_type_validation_error.side_effect = ExpectedError

        with self.assertRaises(ExpectedError):
            validation_tools.confirm_sequence(
                data=sentinel.data, location=sentinel.location
                )

        mock_is_sequence.assert_called_with(sentinel.data)
        mock_raise_type_validation_error.assert_called_with(
            schema_name='sequence',
            data=sentinel.data,
            location=sentinel.location
            )


class TestConfirmSequenceIntegration(ValidationErrorTest):
    """ `validation_tools.confirm_sequence` """

    def test_list_passes(self):
        validation_tools.confirm_sequence(data=[], location=tuple())

    def test_non_list_sequence_data_passes(self):
        """ `data` which is a sequence, but not a `list`, passes. """
        validation_tools.confirm_sequence(data=tuple(), location=tuple())

    def single_error_test(self, data):
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='TYPE'
            ):
            validation_tools.confirm_sequence(data, location=tuple())

    def test_not_a_list_raises(self):
        self.single_error_test(data=object())

    def test_string_data_raises(self):
        self.single_error_test(data=str())


class TestRaiseTypeValidationErrorUnit(unittest.TestCase):
    """ `validation_tools.raise_type_validation_error` """

    @patch('jsonmanager.validation_tools.ValidationError')
    @patch('jsonmanager.validation_tools.make_error_dict')
    @patch_builtin('jsonmanager.validation_tools.type')
    def test_behavior(
        self, mock_type, mock_make_error_dict, mock_ValidationError
        ):
        data_type = MagicMock()
        data_type.__name__ = 'DATA_TYPE'

        class ExpectedError(Exception):
            pass

        mock_type.return_value = data_type
        mock_make_error_dict.return_value = sentinel.error_dict
        mock_ValidationError.return_value = ExpectedError()

        with self.assertRaises(ExpectedError):
            validation_tools.raise_type_validation_error(
                schema_name='SCHEMA_NAME',
                data=sentinel.data,
                location=sentinel.location
                )

        mock_type.assert_called_with(sentinel.data)
        mock_make_error_dict.assert_called_with(
            location=sentinel.location,
            code='TYPE',
            message='Expected SCHEMA_NAME; got `DATA_TYPE`.',
            data=None
            )
        mock_ValidationError.assert_called_with(sentinel.error_dict)


class TestMakeErrorDictUnit(unittest.TestCase):
    """ `validation_tools.make_error_dict` """

    def test_behavior(self):
        result = validation_tools.make_error_dict(
            location=sentinel.location,
            code=sentinel.code,
            message=sentinel.message,
            data=sentinel.data,
            )

        assert result == {
            'location': sentinel.location,
            'code': sentinel.code,
            'message': sentinel.message,
            'data': sentinel.data,
            }


class TestValidationIntegration(IntegrationTest, ConfiguredDecoratorTest):
    """ Confirm that `validation` works with no unexpected errors. """

    def setUp(self):
        super().setUp()
        self.configured_decorator = validation_tools.validation
