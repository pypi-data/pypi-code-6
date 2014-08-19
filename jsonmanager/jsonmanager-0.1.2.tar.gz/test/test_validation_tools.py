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
    Call,
    Dict,
    DictOf,
    ListOf
    )
from jsonmanager import exceptions
from jsonmanager import validation_tools
from jsonmanager.validation_tools import ValidationDefaults


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
            defaults=sentinel.defaults,
            )

        mock_validate_and_transform_errors.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            defaults=sentinel.defaults,
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
            defaults=ValidationDefaults(default_rules=None),
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
                defaults=ValidationDefaults(default_rules=None),
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
                defaults=ValidationDefaults(default_rules=None),
                )


class TestValidateOutputUnit(unittest.TestCase):
    """ `validation_tools.validate_output` """

    @patch('jsonmanager.validation_tools._validate_and_transform_errors')
    def test_behavior(self, mock_validate_and_transform_errors):
        mock_validate_and_transform_errors.return_value = sentinel.expected

        result = validation_tools.validate_output(
            schema=sentinel.schema,
            data=sentinel.data,
            defaults=sentinel.defaults,
            )

        mock_validate_and_transform_errors.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            defaults=sentinel.defaults,
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
            defaults=ValidationDefaults(default_rules=None),
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
                defaults=ValidationDefaults(default_rules=None),
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
                defaults=ValidationDefaults(default_rules=None),
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


class TestValidateUnit(unittest.TestCase):
    """ `validation_tools.validate` """

    @patch('jsonmanager.validation_tools._validate_rules')
    @patch('jsonmanager.validation_tools._validate_structure')
    def test_validation_behavior(
        self, mock_validate_structure, mock_validate_rules
        ):
        mock_validate_structure.return_value = sentinel.validated_data

        result = validation_tools.validate(
            schema=sentinel.schema,
            data=sentinel.data,
            defaults=sentinel.defaults,
            )

        mock_validate_structure.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            defaults=sentinel.defaults,
            )
        mock_validate_rules.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.validated_data,
            defaults=sentinel.defaults,
            )

        assert result is sentinel.validated_data

    @patch('jsonmanager.validation_tools._validate_rules')
    @patch('jsonmanager.validation_tools._validate_structure')
    def test_schema_is_None_skips_validation(
        self, mock_validate_structure, mock_validate_rules
        ):
        result = validation_tools.validate(
            schema=None,
            data=sentinel.data,
            defaults=sentinel.defaults,
            )

        assert not mock_validate_structure.called
        assert not mock_validate_rules.called
        assert result is sentinel.data

    @patch('jsonmanager.validation_tools._validate_rules')
    @patch('jsonmanager.validation_tools._validate_structure')
    @patch('jsonmanager.validation_tools.ValidationDefaults')
    def test_default_defaults(
        self,
        mock_ValidationDefaults,
        mock_validate_structure,
        mock_validate_rules,
        ):
        mock_ValidationDefaults.return_value = sentinel.validation_defaults

        mock_validate_structure.return_value = sentinel.validated_data

        result = validation_tools.validate(
            schema=sentinel.schema,
            data=sentinel.data,
            )

        mock_ValidationDefaults.assert_called_with()
        mock_validate_structure.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            defaults=sentinel.validation_defaults,
            )
        mock_validate_rules.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.validated_data,
            defaults=sentinel.validation_defaults,
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
            schema=AnyType,
            data=data,
            defaults=ValidationDefaults(default_rules=None),
            )

        assert result is data

    def test_structure_raises(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='TYPE'
            ):
            validation_tools.validate(
                schema=self.ExpectedType,
                data=object(),
                defaults=ValidationDefaults(default_rules=None),
                )

    def test_rules_raises(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='rule'
            ):
            validation_tools.validate(
                schema=(AnyType, self.rule_fails),
                data=object(),
                defaults=ValidationDefaults(default_rules=None),
                )

    def test_structure_raises_before_rules(self):
        """ If `data` fails `structure` validation, rules are not evaluated. """
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='TYPE'
            ):
            validation_tools.validate(
                schema=(self.ExpectedType, self.rule_fails),
                data=object(),
                defaults=ValidationDefaults(default_rules=None),
                )


class TestValidateStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_structure` """

    @patch('jsonmanager.validation_tools._dispatch')
    def test_no_error(self, mock_dispatch):
        mock_dispatch.return_value = sentinel.expected

        result = validation_tools._validate_structure(
            schema=sentinel.schema,
            data=sentinel.data,
            defaults=sentinel.defaults,
            )

        mock_dispatch.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            location=tuple(),
            defaults=sentinel.defaults,
            function_map=validation_tools.STRUCTURE_MAP,
            )

        assert result is sentinel.expected

    @patch('jsonmanager.validation_tools.StructureValidationError')
    @patch('jsonmanager.validation_tools._dispatch')
    def test_yes_error(self, mock_dispatch, mock_StructureValidationError):
        """ If a `ValidationError` is raised, it is caught and
            `StructureValidationError` is raised. """
        errors = tuple([sentinel.error])
        mock_dispatch.side_effect = exceptions.ValidationError(*errors)

        class ExpectedError(Exception):
            pass

        mock_StructureValidationError.return_value = ExpectedError

        with self.assertRaises(ExpectedError):
            validation_tools._validate_structure(
                schema=sentinel.schema,
                data=sentinel.data,
                defaults=sentinel.defaults,
                )

        mock_dispatch.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            location=tuple(),
            defaults=sentinel.defaults,
            function_map=validation_tools.STRUCTURE_MAP,
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
            schema=self.complex_schema, data=data, defaults=ValidationDefaults()
            )

        assert result == expected

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
                schema=self.complex_schema,
                data=data,
                defaults=ValidationDefaults(),
                )


class TestValidateRulesUnit(unittest.TestCase):
    """ `validation_tools._validate_rules` """

    @patch('jsonmanager.validation_tools._dispatch')
    def test_no_error(self, mock_dispatch):
        validation_tools._validate_rules(
            schema=sentinel.schema,
            data=sentinel.data,
            defaults=sentinel.defaults,
            )

        mock_dispatch.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            location=tuple(),
            defaults=sentinel.defaults,
            function_map=validation_tools.RULES_MAP,
            )

    @patch('jsonmanager.validation_tools.RulesValidationError')
    @patch('jsonmanager.validation_tools._dispatch')
    def test_yes_error(self, mock_dispatch, mock_RulesValidationError):
        """ If a `ValidationError` is raised, it is caught and
            `RulesValidationError` is raised. """
        errors = tuple([sentinel.error])
        mock_dispatch.side_effect = exceptions.ValidationError(*errors)

        class ExpectedError(Exception):
            pass

        mock_RulesValidationError.return_value = ExpectedError

        with self.assertRaises(ExpectedError):
            validation_tools._validate_rules(
                schema=sentinel.schema,
                data=sentinel.data,
                defaults=sentinel.defaults,
                )

        mock_dispatch.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            location=tuple(),
            defaults=sentinel.defaults,
            function_map=validation_tools.RULES_MAP,
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

        self.defaults = ValidationDefaults(
            default_rules=(default_rule,)
            )

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
            defaults=self.defaults,
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
                defaults=self.defaults,
                )

    def test_key_added_to_location(self):
        """ When `RuleViolation` is raised, `key` is added to `location`. """

        def key_rule(data): # pylint: disable=unused-argument
            raise RuleViolation(code='rule', key='b')

        schema = {
            'a': (AnyType, key_rule),
            }
        data = {'a': object()}

        with self.assertRaisesSingleValidationError(
            location=('a', 'b'), code='rule', error_class=RulesValidationError
            ):
            validation_tools._validate_rules(
                schema=schema,
                data=data,
                defaults=ValidationDefaults(default_rules=None),
                )


class TestValidateRulesMapIntegration(ValidationErrorTest):
    """ `validation_tools._validate_rules`, `validation_tools.RULES_MAP`

        Confirm that `RULES_MAP` is correctly configured for types other than
        `type` and `tuple`. """

    def validation_passes_test(self, schema, data):
        validation_tools._validate_rules(
            schema=schema,
            data=data,
            defaults=ValidationDefaults(default_rules=None),
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

    def validation_raises_test(self, schema, data, error_codes):
        with self.assertRaisesMultipleValidationErrors(
            error_codes=error_codes, error_class=RulesValidationError
            ):
            validation_tools._validate_rules(
                schema=schema,
                data=data,
                defaults=ValidationDefaults(default_rules=None),
                )

    def test_dict_raises(self):
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

        self.validation_raises_test(schema, data, error_codes)

    def test_Dict_raises(self):
        def rule(data):
            if data is not None:
                raise RuleViolation(code='rule')

        schema = Dict({'a': (AnyType, rule)})
        data = {'a': object()}
        error_codes = [
            [('a',), 'rule'],
            ]

        self.validation_raises_test(schema, data, error_codes)

    def test_DictOf_raises(self):
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

        self.validation_raises_test(schema, data, error_codes)

    def test_list_raises(self):
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

        self.validation_raises_test(schema, data, error_codes)

    def test_ListOf_raises(self):
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

        self.validation_raises_test(schema, data, error_codes)


class TestProcessInputUnit(unittest.TestCase):
    """ `validation_tools.process_input` """

    @patch('jsonmanager.validation_tools._process_and_transform_errors')
    def test_behavior(self, mock_process_and_transform_errors):
        mock_process_and_transform_errors.return_value = sentinel.expected

        result = validation_tools.process_input(
            schema=sentinel.schema,
            data=sentinel.data,
            default_kwargs=sentinel.default_kwargs,
            )

        mock_process_and_transform_errors.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            default_kwargs=sentinel.default_kwargs,
            rules_error=exceptions.InputRulesValidationError,
            )

        assert result is sentinel.expected


class TestProcessInputIntegration(ValidationErrorTest):
    """ `validation_tools.process_input` """

    def test_process_passes(self):
        def function(a): # pylint: disable=unused-argument
            return sentinel.expected

        result = validation_tools.process_input(
            schema=function,
            data={'a': object()},
            default_kwargs=None,
            )

        assert result is sentinel.expected

    def test_process_raises_rules_error(self):
        def function(a): # pylint: disable=unused-argument
            raise RuleViolation(code='rule')

        with self.assertRaisesSingleValidationError(
            location=tuple(),
            code='rule',
            error_class=exceptions.InputRulesValidationError,
            ):
            validation_tools.process_input(
                schema=function,
                data={'a': object()},
                default_kwargs=None,
                )


class TestProcessOutputUnit(unittest.TestCase):
    """ `validation_tools.process_output` """

    @patch('jsonmanager.validation_tools._process_and_transform_errors')
    def test_behavior(self, mock_process_and_transform_errors):
        mock_process_and_transform_errors.return_value = sentinel.expected

        result = validation_tools.process_output(
            schema=sentinel.schema,
            data=sentinel.data,
            default_kwargs=sentinel.default_kwargs,
            )

        mock_process_and_transform_errors.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            default_kwargs=sentinel.default_kwargs,
            rules_error=exceptions.OutputRulesValidationError,
            )

        assert result is sentinel.expected


class TestProcessOutputIntegration(ValidationErrorTest):
    """ `validation_tools.process_output` """

    def test_process_passes(self):
        def function(a): # pylint: disable=unused-argument
            return sentinel.expected

        result = validation_tools.process_output(
            schema=function,
            data={'a': object()},
            default_kwargs=None,
            )

        assert result is sentinel.expected

    def test_process_raises_rules_error(self):
        def function(a): # pylint: disable=unused-argument
            raise RuleViolation(code='rule')

        with self.assertRaisesSingleValidationError(
            location=tuple(),
            code='rule',
            error_class=exceptions.OutputRulesValidationError,
            ):
            validation_tools.process_output(
                schema=function,
                data={'a': object()},
                default_kwargs=None,
                )


class TestProcessAndTransformErrorsUnit(unittest.TestCase):
    """ `validation_tools._process_and_transform_errors` """

    @patch('jsonmanager.validation_tools.process')
    def test_validate(self, mock_process):
        mock_process.return_value = sentinel.expected

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._process_and_transform_errors(
            rules_error=sentinel.rules_error,
            **kwargs
            )

        mock_process.assert_called_with(**kwargs)

        assert result is sentinel.expected


    @patch('jsonmanager.validation_tools.process')
    def test_rules_error(self, mock_process):
        error_sequence = [sentinel.error]
        errors = MagicMock()
        errors.__iter__.return_value = error_sequence

        mock_process.side_effect = exceptions.RulesValidationError(*errors)

        class ExpectedError(Exception):
            pass

        rules_error = MagicMock(side_effect=ExpectedError)

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        with self.assertRaises(ExpectedError):
            validation_tools._process_and_transform_errors(
                rules_error=rules_error,
                **kwargs
                )

        mock_process.assert_called_with(**kwargs)

        rules_error.assert_called_with(*error_sequence)


class TestProcessUnit(unittest.TestCase):
    """ `validation_tools.process` """

    @patch('jsonmanager.validation_tools._dispatch')
    def test_no_error(self, mock_dispatch):
        mock_dispatch.return_value = sentinel.expected

        result = validation_tools.process(
            schema=sentinel.schema,
            data=sentinel.data,
            default_kwargs=sentinel.default_kwargs,
            )

        mock_dispatch.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            location=tuple(),
            default_kwargs=sentinel.default_kwargs,
            function_map=validation_tools.PROCESS_MAP,
            )

        assert result is sentinel.expected

    @patch('jsonmanager.validation_tools.RulesValidationError')
    @patch('jsonmanager.validation_tools._dispatch')
    def test_yes_error(self, mock_dispatch, mock_RulesValidationError):
        """ If a `ValidationError` is raised, it is caught and
            `RulesValidationError` is raised. """
        errors = tuple([sentinel.error])
        mock_dispatch.side_effect = exceptions.ValidationError(*errors)

        class ExpectedError(Exception):
            pass

        mock_RulesValidationError.return_value = ExpectedError

        with self.assertRaises(ExpectedError):
            validation_tools.process(
                schema=sentinel.schema,
                data=sentinel.data,
                default_kwargs=sentinel.default_kwargs,
                )

        mock_dispatch.assert_called_with(
            schema=sentinel.schema,
            data=sentinel.data,
            location=tuple(),
            default_kwargs=sentinel.default_kwargs,
            function_map=validation_tools.PROCESS_MAP,
            )
        mock_RulesValidationError.assert_called_with(*errors)


class TestProcessIntegration(ValidationErrorTest):
    """ `validation_tools.process` """

    def make_schema(self, function, call_z):
        return {
            'a': Call(function, z=call_z),
            'b': function,
            'c': {'m': function},
            'd': DictOf(function),
            'e': [function],
            'f': ListOf(function),
            'g': {
                'h': DictOf(
                    [
                        ListOf(
                            Call(function, z=call_z)
                            )
                        ]
                    )
                },
            }

    def test_process_passes_complex(self):
        def function(x, y, z):
            return x, y, z

        default_x = object()
        data_y = object()
        data_z = object()
        call_z = object()

        schema = self.make_schema(function, call_z)

        data = {
            'a': {'y': data_y},
            'b': {'y': data_y, 'z': data_z},
            'c': {
                'm': {'y': data_y, 'z': data_z},
                },
            'd': {
                'j': {'y': data_y, 'z': data_z},
                },
            'e': [
                {'y': data_y, 'z': data_z},
                ],
            'f': [
                {'y': data_y, 'z': data_z},
                ],
            'g': {
                'h': {
                    'i': [
                        [
                            {'y': data_y},
                            ]
                        ]
                    }
                }
            }

        expected = {
            'a': (default_x, data_y, call_z),
            'b': (default_x, data_y, data_z),
            'c': {
                'm': (default_x, data_y, data_z),
                },
            'd': {
                'j': (default_x, data_y, data_z),
                },
            'e': [
                (default_x, data_y, data_z),
                ],
            'f': [
                (default_x, data_y, data_z),
                ],
            'g': {
                'h': {
                    'i': [
                        [
                            (default_x, data_y, call_z),
                            ]
                        ]
                    }
                }
            }

        result = validation_tools.process(
            schema=schema,
            data=data,
            default_kwargs=dict(x=default_x),
            )

        assert result == expected

    def test_process_raises_complex(self):
        def function(**kwargs): # pylint: disable=unused-argument
            raise RuleViolation(code='rule')

        schema = self.make_schema(function, sentinel.call_z)

        data = {
            'a': {},
            'b': {},
            'c': {'m': {}},
            'd': {'j': {}},
            'e': [{}],
            'f': [{}],
            'g': {
                'h': {
                    'i': [
                        [
                            {}
                            ]
                        ]
                    }
                }
            }

        error_codes = [
            [('a',), 'rule'],
            [('b',), 'rule'],
            [('c', 'm'), 'rule'],
            [('d', 'j'), 'rule'],
            [('e', 0), 'rule'],
            [('f', 0), 'rule'],
            [('g', 'h', 'i', 0, 0), 'rule'],
            ]

        with self.assertRaisesMultipleValidationErrors(
            error_codes=error_codes, error_class=RulesValidationError
            ):
            validation_tools.process(
                schema=schema,
                data=data,
                default_kwargs=None,
                )


class TestProcessMapIntegration(ValidationErrorTest):
    """ `validation_tools.process`, `validation_tools.PROCESS_MAP`

        Confirm that `PROCESS_MAP` is correctly configured for types other than
        `Call`, `collections.abc.Callable`. """

    def setUp(self):
        def function(x):
            if x is sentinel.good:
                return sentinel.return_value
            if x is sentinel.bad:
                raise RuleViolation(code='rule')

        self.function = function

    def process_passes_test(self, schema, data, expected):
        result = validation_tools.process(
            schema=schema,
            data=data,
            default_kwargs=None,
            )
        assert result == expected

    def test_dict_passes(self):
        schema = {'a': self.function}
        data = {
            'a': {'x': sentinel.good},
            }
        expected = {'a': sentinel.return_value}

        self.process_passes_test(schema, data, expected)

    def test_DictOf_passes(self):
        schema = DictOf(self.function)
        data = {
            'a': {'x': sentinel.good},
            'b': {'x': sentinel.good},
            }
        expected = {'a': sentinel.return_value, 'b': sentinel.return_value}

        self.process_passes_test(schema, data, expected)

    def test_list_passes(self):
        schema = [self.function]
        data = [
            {'x': sentinel.good},
            ]
        expected = [sentinel.return_value]

        self.process_passes_test(schema, data, expected)

    def test_ListOf_passes(self):
        schema = ListOf(self.function)
        data = [
            {'x': sentinel.good},
            {'x': sentinel.good},
            ]
        expected = [sentinel.return_value, sentinel.return_value]

        self.process_passes_test(schema, data, expected)

    def process_raises_test(self, schema, data, error_codes):
        with self.assertRaisesMultipleValidationErrors(error_codes):
            validation_tools.process(
                schema=schema,
                data=data,
                default_kwargs=None,
                )

    def test_dict_raises(self):
        schema = {
            'a': self.function,
            'b': self.function,
            }
        data = {
            'a': {'x': sentinel.good},
            'b': {'x': sentinel.bad},
            }
        error_codes = [
            [('b',), 'rule'],
            ]

        self.process_raises_test(schema, data, error_codes)

    def test_DictOf_raises(self):
        schema = DictOf(self.function)
        data = {
            'a': {'x': sentinel.good},
            'b': {'x': sentinel.bad},
            }
        error_codes = [
            [('b',), 'rule'],
            ]

        self.process_raises_test(schema, data, error_codes)

    def test_list_raises(self):
        schema = [self.function, self.function]
        data = [
            {'x': sentinel.good},
            {'x': sentinel.bad},
            ]
        error_codes = [
            [(1,), 'rule'],
            ]

        self.process_raises_test(schema, data, error_codes)

    def test_ListOf_raises(self):
        schema = ListOf(self.function)
        data = [
            {'x': sentinel.good},
            {'x': sentinel.bad},
            ]
        error_codes = [
            [(1,), 'rule'],
            ]

        self.process_raises_test(schema, data, error_codes)


class TestDispatchUnit(unittest.TestCase):
    """ `validation_tools._dispatch` """

    @patch('jsonmanager.validation_tools.select_function')
    def test_behavior(self, mock_select_function):
        function = MagicMock()
        function.return_value = sentinel.expected

        mock_select_function.return_value = function
        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._dispatch(
            schema=sentinel.schema,
            function_map=sentinel.function_map,
            **kwargs
            )

        mock_select_function.assert_called_with(
            sentinel.schema, sentinel.function_map
            )
        function.assert_called_with(
            schema=sentinel.schema, function_map=sentinel.function_map, **kwargs
            )

        assert result is sentinel.expected


class TestValidateScalarStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_scalar_structure`

        Extra keyword arguments are ignored. """

    @patch_builtin('jsonmanager.validation_tools.isinstance')
    def test_correct_type_passes(self, mock_isinstance):
        mock_isinstance.return_value = True

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._validate_scalar_structure(
            sentinel.schema, sentinel.data, sentinel.location, **kwargs
            )

        mock_isinstance.assert_called_with(sentinel.data, sentinel.schema)

        assert result is sentinel.data

    @patch_builtin('jsonmanager.validation_tools.isinstance')
    def test_none_passes(self, mock_isinstance):
        mock_isinstance.return_value = False

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._validate_scalar_structure(
            sentinel.schema, None, sentinel.location, **kwargs
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

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        with self.assertRaises(ExpectedError):
            validation_tools._validate_scalar_structure(
                schema, sentinel.data, sentinel.location, **kwargs
                )

        mock_isinstance.assert_called_with(sentinel.data, schema)
        mock_raise_type_validation_error.assert_called_with(
            '`SCHEMA_TYPE`', sentinel.data, sentinel.location
            )


class TestValidateScalarStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_scalar_structure` """

    def test_correct_type_passes(self):
        data = self.ExpectedType()

        result = validation_tools._validate_structure(
            schema=self.ExpectedType,
            data=data,
            defaults=ValidationDefaults(),
            )

        assert result is data

    def test_None_passes(self):
        result = validation_tools._validate_structure(
            schema=self.ExpectedType,
            data=None,
            defaults=ValidationDefaults(),
            )

        assert result is None

    def test_wrong_type_raises(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='TYPE', error_class=StructureValidationError
            ):
            validation_tools._validate_structure(
                schema=self.ExpectedType,
                data=object(),
                defaults=ValidationDefaults(),
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
        validation_tools._validate_rules(
            schema=AnyType,
            data=object(),
            defaults=ValidationDefaults(default_rules=None),
            )

    def test_default_rules_passes(self):
        def rule_passes(data): # pylint: disable=unused-argument
            pass

        default_rules = (rule_passes,)

        validation_tools._validate_rules(
            schema=AnyType,
            data=object(),
            defaults=ValidationDefaults(default_rules=default_rules)
            )

    def test_default_rules_raises(self):
        def rule(data): # pylint: disable=unused-argument
            raise RuleViolation(code='rule')

        defaults = ValidationDefaults(
            default_rules=(rule,)
            )

        with self.assertRaisesSingleValidationError(
            location=tuple(), code='rule', error_class=RulesValidationError
            ):
            validation_tools._validate_rules(
                schema=AnyType,
                data=object(),
                defaults=defaults,
                )


class TestValidateTupleStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_tuple_structure` """

    @patch('jsonmanager.validation_tools._dispatch')
    def test_behavior(self, mock_dispatch):
        schema_tuple = MagicMock()
        schema_tuple.__getitem__.return_value = sentinel.schema
        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        mock_dispatch.return_value = sentinel.expected

        result = validation_tools._validate_tuple_structure(
            schema=schema_tuple, **kwargs
            )

        schema_tuple.__getitem__.assert_called_with(0)
        mock_dispatch.assert_called_with(
            schema=sentinel.schema, **kwargs
            )

        assert result is sentinel.expected


class TestValidateTupleStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_tuple_rules` """

    def test_validation_passes(self):
        data = self.ExpectedType()
        result = validation_tools._validate_structure(
            schema=(self.ExpectedType, sentinel.rule),
            data=data,
            defaults=ValidationDefaults(),
            )
        assert result is data

    def test_validation_raises(self):
        with self.assertRaisesSingleValidationError(
            location=tuple(), code='TYPE', error_class=StructureValidationError
            ):
            validation_tools._validate_structure(
                schema=(self.ExpectedType, sentinel.rule),
                data=object(),
                defaults=ValidationDefaults(),
                )


class TestValidateTupleRulesUnit(unittest.TestCase):
    """ `validation_tools._validate_tuple_rules` """

    @patch('jsonmanager.validation_tools._dispatch')
    @patch_builtin('jsonmanager.validation_tools.isinstance')
    @patch('jsonmanager.validation_tools.apply_rules')
    @patch('jsonmanager.validation_tools.get_rules')
    def test_behavior(
        self, mock_get_rules, mock_apply_rules, mock_isinstance, mock_dispatch
        ):
        schema_tuple = MagicMock()
        schema_tuple.__getitem__.return_value = sentinel.inner_schema

        mock_get_rules.return_value = sentinel.rules

        mock_isinstance.return_value = False

        # Extra keyword arguments are discarded.
        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        validation_tools._validate_tuple_rules(
            schema=schema_tuple,
            data=sentinel.data,
            location=sentinel.location,
            defaults=sentinel.defaults,
            **kwargs
            )

        mock_get_rules.assert_called_with(
            schema_tuple, sentinel.defaults
            )
        mock_apply_rules.assert_called_with(
            sentinel.rules, sentinel.data, sentinel.location
            )
        schema_tuple.__getitem__.assert_called_with(0)
        mock_isinstance.assert_called_with(sentinel.inner_schema, type)
        mock_dispatch.assert_called_with(
            schema=sentinel.inner_schema,
            data=sentinel.data,
            location=sentinel.location,
            defaults=sentinel.defaults,
            **kwargs
            )


class TestValidateTupleRulesIntegration(ValidationErrorTest):
    """ `validation_tools._validate_tuple_rules` """

    def setUp(self):
        super().setUp()

        def rule_passes(data): # pylint: disable=unused-argument
            pass

        def rule_fails(data): # pylint: disable=unused-argument
            raise RuleViolation(
                code='code',
                message='message',
                data='data',
                key='a',
                )

        def rule_not_called(data): # pylint: disable=unused-argument
            raise Exception

        self.rule_passes = rule_passes
        self.rule_fails = rule_fails
        self.rule_not_called = rule_not_called

    def validation_passes_test(self, schema):
        validation_tools._validate_rules(
            schema=schema,
            data=object(),
            defaults=ValidationDefaults(default_rules=tuple()),
            )

    def test_no_rules_passes(self):
        schema = (AnyType,)
        self.validation_passes_test(schema)

    def test_yes_rules_passes(self):
        """ When rules raise no errors, validation passes. """
        schema = (AnyType, self.rule_passes)
        self.validation_passes_test(schema)

    def test_StopValidation_stops_validation_passes(self):
        """ When a rule raises `StopValidation`, further rules are not called.
            """
        def rule_stops(data): # pylint: disable=unused-argument
            raise StopValidation

        schema = (
            AnyType, self.rule_passes, rule_stops, self.rule_not_called
            )

        self.validation_passes_test(schema)

    def validation_raises_test(self, schema, default_rules):
        defaults = ValidationDefaults(default_rules=default_rules)

        with self.assertRaisesSingleValidationError(
            location=('a',),
            code='code',
            message='message',
            data='data',
            error_class=RulesValidationError,
            ):
            validation_tools._validate_rules(
                schema=schema,
                data=object(),
                defaults=defaults,
                )

    def test_rule_raises(self):
        """ When a rule raises `RuleViolation`, the exception is caught and a
            `ValidationError` is raised. Further rules are not called. """
        schema = (
            AnyType, self.rule_passes, self.rule_fails, self.rule_not_called
            )
        default_rules = tuple()

        self.validation_raises_test(schema, default_rules)

    def test_default_rules_raises(self):
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

    @patch(
        'jsonmanager.validation_tools.'
        'raise_validation_error_from_rule_violation'
        )
    def test_rule_raises_RuleViolation(
        self, mock_raise_validation_error_from_rule_violation
        ):
        """ Rule function raises `RuleViolation`. """
        exc = RuleViolation()

        rules_sequence = [MagicMock() for i in range(3)]
        rules_sequence[1].side_effect = exc

        rules = MagicMock()
        rules.__iter__.return_value = rules_sequence

        class ExpectedError(Exception):
            pass

        mock_raise_validation_error_from_rule_violation.side_effect = \
            ExpectedError

        with self.assertRaises(ExpectedError):
            validation_tools.apply_rules(
                rules=rules,
                data=sentinel.data,
                location=sentinel.location
                )

        rules_sequence[0].assert_called_with(sentinel.data)
        rules_sequence[1].assert_called_with(sentinel.data)
        assert not rules_sequence[2].called

        mock_raise_validation_error_from_rule_violation.assert_called_with(
            exc, sentinel.location
            )

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
        self.defaults = MagicMock()
        self.defaults.default_rules = (sentinel.default_0, sentinel.default_1)

    @patch('jsonmanager.validation_tools.get_override_defaults')
    def test_yes_override_defaults(self, mock_override_defaults):
        """ Just schema rules returned. """
        mock_override_defaults.return_value = True

        result = validation_tools.get_rules(
            schema=self.schema_tuple,
            defaults=self.defaults,
            )

        assert result == self.schema_rules

    @patch('jsonmanager.validation_tools.get_override_defaults')
    def test_no_override_defaults(self, mock_override_defaults):
        """ Default rules prepended to schema rules. """
        mock_override_defaults.return_value = False

        result = validation_tools.get_rules(
            schema=self.schema_tuple,
            defaults=self.defaults,
            )

        assert result == self.defaults.default_rules + self.schema_rules


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
        result = validation_tools._validate_structure(
            schema=schema, data=data, defaults=ValidationDefaults()
            )

        assert result == data

    def test_empty_data_passes(self):
        result = validation_tools._validate_structure(
            schema={}, data={}, defaults=ValidationDefaults()
            )

        assert result == {}

    def test_missing_optional_passes(self):
        schema = {'a': self.ExpectedType, 'b': self.ExpectedType}
        data = {'a': self.ExpectedType()}
        defaults = ValidationDefaults(dict_optional_keys=['b'])

        result = validation_tools._validate_structure(
            schema=schema, data=data, defaults=defaults
            )

        assert result == data

    def test_strip_extras_passes(self):
        schema = {'a': self.ExpectedType}
        data = {'a': self.ExpectedType(), 'b': object()}
        defaults = ValidationDefaults(dict_strip_extras=True)

        expected = {'a': data['a']}

        result = validation_tools._validate_structure(
            schema=schema, data=data, defaults=defaults
            )

        assert result == expected

    def single_error_test(self, schema, data, defaults, location, code):
        with self.assertRaisesSingleValidationError(
            location=location, code=code, error_class=StructureValidationError
            ):
            validation_tools._validate_structure(
                schema=schema, data=data, defaults=defaults
                )

    def test_not_a_dict_raises(self):
        self.single_error_test(
            schema={},
            data=object(),
            defaults=ValidationDefaults(),
            location=tuple(),
            code='TYPE',
            )

    def test_wrong_type_raises(self):
        self.single_error_test(
            schema={'a': self.ExpectedType},
            data={'a': object()},
            defaults=ValidationDefaults(),
            location=('a',),
            code='TYPE',
            )

    def test_missing_raises(self):
        self.single_error_test(
            schema={'a': AnyType},
            data={},
            defaults=ValidationDefaults(),
            location=('a',),
            code='MISSING',
            )

    def test_not_allowed_raises(self):
        self.single_error_test(
            schema={},
            data={'a': object()},
            defaults=ValidationDefaults(),
            location=('a',),
            code='NOT_ALLOWED',
            )

    def multiple_errors_test(self, schema, data, defaults, error_codes):
        with self.assertRaisesMultipleValidationErrors(
            error_codes=error_codes, error_class=StructureValidationError
            ):
            validation_tools._validate_structure(
                schema=schema, data=data, defaults=defaults,
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
            [('b',), 'TYPE'],
            [('c',), 'MISSING'],
            [('d',), 'NOT_ALLOWED'],
            ]
        defaults = ValidationDefaults()

        self.multiple_errors_test(schema, data, defaults, error_codes)

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
            [('a',), 'TYPE'],
            [('b', 'c'), 'TYPE'],
            ]
        defaults = ValidationDefaults()

        self.multiple_errors_test(schema, data, defaults, error_codes)


class TestGetResultItemAndCaptureErrorsUnit(unittest.TestCase):
    """ `validation_tools.get_result_item_and_capture_errors` """

    @patch('jsonmanager.validation_tools._dispatch')
    def test_no_errors(self, mock_dispatch):
        mock_dispatch.return_value = sentinel.validated_data

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools.get_result_item_and_capture_errors(
            key=sentinel.key, **kwargs
            )

        mock_dispatch.assert_called_with(**kwargs)

        assert result == ((sentinel.key, sentinel.validated_data), tuple())

    @patch('jsonmanager.validation_tools._dispatch')
    def test_yes_errors(self, mock_dispatch):
        validation_error = exceptions.ValidationError(sentinel.error_dict)
        mock_dispatch.side_effect = validation_error

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools.get_result_item_and_capture_errors(
            key=sentinel.key, **kwargs
            )

        mock_dispatch.assert_called_with(**kwargs)

        assert result == ((sentinel.key, None), validation_error.errors)


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


class TestValidateDictSchemaTypeStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_Dict_structure` """

    @patch('jsonmanager.validation_tools._utilize_Dict')
    def test_behavior(self, mock_utilize_Dict):
        schema = MagicMock()
        schema.validate_structure_kwargs = dict(
            validation_kwarg_name=sentinel.validation_kwarg_value
            )

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        complete_kwargs = dict(
            kwarg_name=sentinel.kwarg_value,
            validation_kwarg_name=sentinel.validation_kwarg_value,
            )

        mock_utilize_Dict.return_value = sentinel.expected

        result = validation_tools._validate_Dict_structure(
            schema=schema, **kwargs
            )

        mock_utilize_Dict.assert_called_with(
            schema=schema, **complete_kwargs
            )

        assert result is sentinel.expected


class TestValidateDictSchemaTypeStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_Dict_structure` """

    def test_validation_passes(self):
        """ No special arguments provided. """
        data = {'a': self.ExpectedType()}

        result = validation_tools._validate_structure(
            schema=Dict({'a': self.ExpectedType}),
            data=data,
            defaults=ValidationDefaults(),
            )

        assert result == data

    def test_missing_optional_passes(self):
        """ With `optional_keys` argument, missing key does not raise error. """
        data = {'a': self.ExpectedType()}

        result = validation_tools._validate_structure(
            schema=Dict(
                {'a': self.ExpectedType, 'b': self.ExpectedType},
                optional_keys=['b']
                ),
            data=data,
            defaults=ValidationDefaults(),
            )

        assert result == data

    def test_strip_extras_passes(self):
        """ With `strip_extras` argument, extra keys are stripped, and no error
            is raised. """
        schema = Dict(
            {'a': self.ExpectedType},
            strip_extras=True
            )
        data = {'a': self.ExpectedType(), 'b': object()}
        expected = {'a': data['a']}

        result = validation_tools._validate_structure(
            schema=schema, data=data, defaults=ValidationDefaults()
            )

        assert result == expected

    def test_missing_raises(self):
        """ Without `optional_keys` argument, missing key raises error. """
        with self.assertRaisesSingleValidationError(
            location=('a',),
            code='MISSING',
            error_class=StructureValidationError,
            ):
            validation_tools._validate_structure(
                schema=Dict({'a': self.ExpectedType}),
                data={},
                defaults=ValidationDefaults(),
                )

    def test_not_allowed_raises(self):
        """ Without `strip_extras` argument, extra key raises error. """
        with self.assertRaisesSingleValidationError(
            location=('a',),
            code='NOT_ALLOWED',
            error_class=StructureValidationError,
            ):
            validation_tools._validate_structure(
                schema=Dict({}),
                data={'a': self.ExpectedType()},
                defaults=ValidationDefaults(),
                )

    def test_arguments_do_not_propagate(self):
        """ Special arguments do not propagate to nested dictionaries. """
        schema = Dict(
            {
                'a': {'b': AnyType},
                'b': AnyType,
                },
            optional_keys=['b'],
            strip_extras=True,
            )

        data = {
            'a': {'c': object()},
            'c': object(),
            }

        error_codes = [
            [('a', 'b'), 'MISSING'],
            [('a', 'c'), 'NOT_ALLOWED'],
            ]

        with self.assertRaisesMultipleValidationErrors(
            error_codes=error_codes, error_class=StructureValidationError
            ):
            validation_tools._validate_structure(
                schema=schema, data=data, defaults=ValidationDefaults()
                )


class TestUtilizeDictSchemaTypeUnit(unittest.TestCase):
    """ `validation_tools._utilize_Dict` """

    @patch('jsonmanager.validation_tools._dispatch')
    def test_behavior(self, mock_dispatch):
        schema = MagicMock()

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        validation_tools._utilize_Dict(schema=schema, **kwargs)

        mock_dispatch.assert_called_with(
            schema=schema.schema, **kwargs
            )


class TestValidateDictOfStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_DictOf_structure` """

    @patch('jsonmanager.validation_tools._utilize_DictOf')
    @patch('jsonmanager.validation_tools.confirm_mapping')
    def test_behavior(self, mock_confirm_mapping, mock_utilize_DictOf):
        mock_utilize_DictOf.return_value = sentinel.expected

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._validate_DictOf_structure(
            data=sentinel.data, location=sentinel.location, **kwargs
            )

        mock_confirm_mapping.assert_called_with(
            sentinel.data, sentinel.location
            )
        mock_utilize_DictOf.assert_called_with(
            data=sentinel.data,
            location=sentinel.location,
            **kwargs
            )

        assert result is sentinel.expected


class TestValidateDictOfStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_DictOf_structure` """

    def test_validation_passes(self):
        data = {'a': self.ExpectedType()}

        result = validation_tools._validate_structure(
            schema=DictOf(self.ExpectedType),
            data=data,
            defaults=ValidationDefaults(),
            )

        assert result == data

    def test_empty_dict_passes(self):
        result = validation_tools._validate_structure(
            schema=DictOf(self.ExpectedType),
            data={},
            defaults=ValidationDefaults(),
            )
        assert result == {}

    def single_error_test(self, schema, data, location):
        with self.assertRaisesSingleValidationError(
            location=location, code='TYPE', error_class=StructureValidationError
            ):
            validation_tools._validate_structure(
                schema=schema, data=data, defaults=ValidationDefaults()
                )

    def test_not_a_dict_raises(self):
        self.single_error_test(
            schema=DictOf(AnyType),
            data=object(),
            location=tuple(),
            )

    def test_arbitrary_keys(self):
        """ Validation works with arbitrary keys. """
        schema = DictOf(self.ExpectedType)
        data = {
            'a': self.ExpectedType(),
            'b': object(),
            }
        location = ('b',)

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
        location = ('b', 'q')

        self.single_error_test(schema, data, location)


class TestUtilizeDictOfUnit(unittest.TestCase):
    """ `validation_tools._utilize_DictOf` """

    @patch('jsonmanager.validation_tools._dispatch')
    def test_behavior(self, mock_dispatch):
        mock_dispatch.return_value = sentinel.expected

        schema = MagicMock()

        data = MagicMock()
        data.keys.return_value.__iter__.return_value = [sentinel.key]

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._utilize_DictOf(
            schema=schema, data=data, **kwargs
            )

        mock_dispatch.assert_called_with(
            schema={sentinel.key: schema.schema}, data=data, **kwargs
            )

        assert result is sentinel.expected


class TestValidateListStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_list_structure` """

    @patch('jsonmanager.validation_tools._utilize_list')
    @patch('jsonmanager.validation_tools.confirm_sequence')
    def test_behavior(self, mock_confirm_sequence, mock_utilize_list):
        defaults = MagicMock()
        defaults.validate_list_structure_kwargs = dict(
            default_kwarg_name=sentinel.default_kwarg_value
            )

        mock_utilize_list.return_value = sentinel.expected

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        complete_kwargs = dict(
            kwarg_name=sentinel.kwarg_value,
            default_kwarg_name=sentinel.default_kwarg_value,
            )

        result = validation_tools._validate_list_structure(
            data=sentinel.data,
            location=sentinel.location,
            defaults=defaults,
            **kwargs
            )

        mock_confirm_sequence.assert_called_with(
            sentinel.data, sentinel.location
            )
        mock_utilize_list.assert_called_with(
            data=sentinel.data,
            location=sentinel.location,
            defaults=defaults,
            **complete_kwargs
            )

        assert result is sentinel.expected


class TestValidateListStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_list_structure` """

    def test_validation_passes(self):
        data = [self.ExpectedType()]
        result = validation_tools._validate_structure(
            schema=[self.ExpectedType],
            data=data,
            defaults=ValidationDefaults(),
            )
        assert result == data

    def test_strip_extras_passes(self):
        schema = [self.ExpectedType],
        data = [self.ExpectedType(), object()]
        defaults = ValidationDefaults(list_strip_extras=True)

        result = validation_tools._validate_structure(
            schema=schema, data=data, defaults=defaults
            )

        assert result == data[:1]

    def single_error_test(self, schema, data, location, code):
        with self.assertRaisesSingleValidationError(
            location=location, code=code, error_class=StructureValidationError
            ):
            validation_tools._validate_structure(
                schema=schema, data=data, defaults=ValidationDefaults(),
                )

    def test_not_a_list_raises(self):
        self.single_error_test(
            schema=[AnyType],
            data=object(),
            location=tuple(),
            code='TYPE',
            )

    def test_wrong_type_raises(self):
        self.single_error_test(
            schema=[self.ExpectedType],
            data=[object()],
            location=(0,),
            code='TYPE',
            )

    def test_missing_raises(self):
        self.single_error_test(
            schema=[AnyType],
            data=[],
            location=(0,),
            code='MISSING'
            )

    def test_not_allowed_raises(self):
        self.single_error_test(
            schema=[],
            data=[object()],
            location=(0,),
            code='NOT_ALLOWED',
            )

    def test_error_location_concatenation(self):
        """ Confirm that list index error location concatenates correctly. """
        self.single_error_test(
            schema={'a': [self.ExpectedType]},
            data={'a': [object()]},
            location=('a', 0),
            code='TYPE'
            )

    def multiple_errors_test(self, schema, data, error_codes):
        with self.assertRaisesMultipleValidationErrors(error_codes):
            validation_tools._validate_structure(
                schema=schema, data=data, defaults=ValidationDefaults()
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
            [(1,), 'TYPE'],
            [(2,), 'MISSING'],
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
            [(0,), 'TYPE'],
            [(1, 'a'), 'TYPE']
            ]

        self.multiple_errors_test(schema, data, error_codes)


class TestValidationDefaultsDefaultsIntegration(ValidationErrorTest):
    """ Default arguments for `_validate_dict_structure` provided by the
        `ValidationDefaults` instance should be limited to their intended schema
        type. So, default arguments for `dict` schemas should not be applied to
        `list` schemas, and vice-versa. """

    def test_dict_defaults_not_applied_to_list(self):
        schema = [
            AnyType,
            {
                'a': [AnyType],
                },
            ]
        data = [
            object(),
            {
                'a': [object(), object()],
                },
            object(),
            ]
        defaults = ValidationDefaults(dict_strip_extras=True)

        error_codes = [
            [(1, 'a', 1), 'NOT_ALLOWED'],
            [(2,), 'NOT_ALLOWED'],
            ]

        with self.assertRaisesMultipleValidationErrors(
            error_codes=error_codes, error_class=StructureValidationError
            ):
            validation_tools._validate_structure(
                schema=schema, data=data, defaults=defaults
                )

    def test_list_defaults_not_applied_to_dict(self):
        schema = {
            'a': AnyType,
            'b': [
                {'a': AnyType},
                ],
            }
        data = {
            'a': object(),
            'b': [
                {'a': object(), 'b': object()},
                ],
            'c': object(),
            }
        defaults = ValidationDefaults(list_strip_extras=True)

        error_codes = [
            [('b', 0, 'b'), 'NOT_ALLOWED'],
            [('c',), 'NOT_ALLOWED'],
            ]

        with self.assertRaisesMultipleValidationErrors(
            error_codes=error_codes, error_class=StructureValidationError
            ):
            validation_tools._validate_structure(
                schema=schema, data=data, defaults=defaults
                )


class TestUtilizeListUnit(unittest.TestCase):
    """ `validation_tools._utilize_list` """

    @patch('jsonmanager.validation_tools.reassemble_list')
    @patch('jsonmanager.validation_tools._dispatch')
    @patch_builtin('jsonmanager.validation_tools.dict')
    @patch_builtin('jsonmanager.validation_tools.enumerate')
    def test_behavior(
        self, mock_enumerate, mock_dict, mock_dispatch, mock_reassemble_list
        ):
        mock_enumerate.side_effect = [
            sentinel.enumerated_schema, sentinel.enumerated_data
            ]
        mock_dict.side_effect = [sentinel.dict_schema, sentinel.dict_data]

        mock_dispatch.return_value = sentinel.result_dict

        mock_reassemble_list.return_value = sentinel.expected

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._utilize_list(
            schema=sentinel.schema, data=sentinel.data, **kwargs
            )

        mock_enumerate.assert_has_calls([
            call(sentinel.schema), call(sentinel.data)
            ])
        mock_dict.assert_has_calls([
            call(sentinel.enumerated_schema), call(sentinel.enumerated_data)
            ])
        mock_dispatch.assert_called_with(
            schema=sentinel.dict_schema,
            data=sentinel.dict_data,
            **kwargs
            )
        mock_reassemble_list.assert_called_with(sentinel.result_dict)

        assert result is sentinel.expected


class TestReassembleListFunctional(unittest.TestCase):
    """ `validation_tools.reassemble_list` """

    def test_result(self):
        result_dict = {
            0: 'x',
            1: 'a',
            2: 'm',
            3: 'j',
            4: 'z',
            5: 'c',
            }
        expected = ['x', 'a', 'm', 'j', 'z', 'c']

        result = validation_tools.reassemble_list(result_dict)

        assert result == expected


class TestValidateListOfStructureUnit(unittest.TestCase):
    """ `validation_tools._validate_ListOf_structure` """

    @patch('jsonmanager.validation_tools._utilize_ListOf')
    @patch('jsonmanager.validation_tools.confirm_sequence')
    def test_behavior(self, mock_confirm_sequence, mock_utilize_ListOf):
        mock_utilize_ListOf.return_value = sentinel.expected

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._validate_ListOf_structure(
            data=sentinel.data,
            location=sentinel.location,
            **kwargs
            )

        mock_confirm_sequence.assert_called_with(
            sentinel.data, sentinel.location
            )
        mock_utilize_ListOf.assert_called_with(
            data=sentinel.data,
            location=sentinel.location,
            **kwargs
            )

        assert result is sentinel.expected


class TestValidateListOfStructureIntegration(ValidationErrorTest):
    """ `validation_tools._validate_ListOf_structure` """

    def test_validation_passes(self):
        data = [self.ExpectedType()]
        result = validation_tools._validate_structure(
            schema=ListOf(self.ExpectedType),
            data=data,
            defaults=ValidationDefaults(),
            )
        assert result == data

    def test_empty_list_passes(self):
        result = validation_tools._validate_structure(
            schema=ListOf(self.ExpectedType),
            data=[],
            defaults=ValidationDefaults(),
            )
        assert result == []

    def single_error_test(self, schema, data, location):
        with self.assertRaisesSingleValidationError(
            location=location, code='TYPE', error_class=StructureValidationError
            ):
            validation_tools._validate_structure(
                schema=schema, data=data, defaults=ValidationDefaults(),
                )

    def test_not_a_list_raises(self):
        self.single_error_test(
            schema=ListOf(AnyType),
            data=object(),
            location=tuple(),
            )

    def test_arbitrary_length(self):
        """ Validation passes with arbitrary length. """
        schema = ListOf(self.ExpectedType)
        data = [
            self.ExpectedType(),
            object()
            ]
        location = (1,)

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
        location = (1, 'q')

        self.single_error_test(schema, data, location)


class TestUtilizeListOfUnit(unittest.TestCase):
    """ `validation_tools._utilize_ListOf` """

    @patch('jsonmanager.validation_tools._utilize_list')
    def test_behavior(self, mock_utilize_list):
        mock_utilize_list.return_value = sentinel.expected

        schema = MagicMock()

        data = MagicMock()
        data.__iter__.return_value = [sentinel.item]

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._utilize_ListOf(
            schema=schema, data=data, **kwargs
            )

        mock_utilize_list.assert_called_with(
            schema=[schema.schema], data=data, **kwargs
            )

        assert result is sentinel.expected


class TestProcessCallFunctional(unittest.TestCase):
    """ `validation_tools._process_Call` """

    def kwargs_test(
        self, default_kwargs, data_kwargs, call_kwargs, expected_kwargs
        ):
        function = MagicMock()
        function.return_value = sentinel.expected

        result = validation_tools._process_Call(
            schema=Call(function, **call_kwargs),
            data=data_kwargs,
            location=sentinel.location,
            default_kwargs=default_kwargs,
            )

        function.assert_called_with(**expected_kwargs)
        assert result is sentinel.expected

    def test_default_kwargs(self):
        """ Function is called with `default_kwargs` as keyword arguments. """
        default_kwargs = dict(a=sentinel.default_a)
        data_kwargs = dict()
        call_kwargs = dict()
        expected_kwargs = dict(a=sentinel.default_a)

        self.kwargs_test(
            default_kwargs, data_kwargs, call_kwargs, expected_kwargs
            )

    def test_data_kwargs(self):
        """ Function is called. `data` arguments override `default_kwargs`. """
        default_kwargs = dict(a=sentinel.default_a, b=sentinel.default_b)
        data_kwargs = dict(b=sentinel.data_b)
        call_kwargs = dict()
        expected_kwargs = dict(a=sentinel.default_a, b=sentinel.data_b)

        self.kwargs_test(
            default_kwargs, data_kwargs, call_kwargs, expected_kwargs
            )

    def test_Call_kwargs(self):
        """ Function is called. `Call` arguments override both `data` and
            `default_kwargs` arguments. """
        default_kwargs = dict(
            a=sentinel.default_a,
            b=sentinel.default_b,
            c=sentinel.default_c,
            )
        data_kwargs = dict(
            b=sentinel.data_b,
            c=sentinel.data_c,
            )
        call_kwargs = dict(
            c=sentinel.call_c,
            )
        expected_kwargs = dict(
            a=sentinel.default_a,
            b=sentinel.data_b,
            c=sentinel.call_c,
            )

        self.kwargs_test(
            default_kwargs, data_kwargs, call_kwargs, expected_kwargs
            )


class TestProcessCallIntegration(ValidationErrorTest):
    """ `validation_tools.process_Call` """

    def test_process_passes(self):
        def function(a, b, c):
            return (a, b, c)

        default_kwargs = dict(
            a=sentinel.default_a,
            b=sentinel.default_b,
            c=sentinel.default_c,
            )
        data = dict(
            b=sentinel.data_b,
            c=sentinel.data_c,
            )
        call_kwargs = dict(
            c=sentinel.call_c,
            )

        result = validation_tools.process(
            schema=Call(function, **call_kwargs),
            data=data,
            default_kwargs=default_kwargs,
            )

        assert result == (sentinel.default_a, sentinel.data_b, sentinel.call_c)

    def test_process_raises(self):
        """ Function raises `RuleViolation`. Error is caught and transformed to
            `RulesValidationError`. """
        def function():
            raise RuleViolation(code='rule')

        with self.assertRaisesSingleValidationError(
            location=tuple(), code='rule', error_class=RulesValidationError
            ):
            validation_tools.process(
                schema=Call(function),
                data={},
                default_kwargs=None,
                )


class TestProcessCallableUnit(unittest.TestCase):
    """ `validation_tools._process_Callable` """

    @patch('jsonmanager.validation_tools._process_Call')
    @patch('jsonmanager.validation_tools.Call')
    def test_behavior(self, mock_Call, mock_process_Call):
        mock_Call.return_value = sentinel.call_schema

        mock_process_Call.return_value = sentinel.expected

        kwargs = dict(kwarg_name=sentinel.kwarg_value)

        result = validation_tools._process_Callable(
            schema=sentinel.schema,
            **kwargs
            )

        mock_Call.assert_called_with(sentinel.schema)
        mock_process_Call.assert_called_with(
            schema=sentinel.call_schema,
            **kwargs
            )

        assert result is sentinel.expected


class TestProcessCallableIntegration(ValidationErrorTest):
    """ `validation_tools._process_Callable` """

    def test_process_passes(self):
        def function(a, b):
            return (a, b)

        default_kwargs = dict(
            a=sentinel.default_a,
            b=sentinel.default_b,
            )
        data = dict(
            b=sentinel.data_b,
            )

        result = validation_tools.process(
            schema=function,
            data=data,
            default_kwargs=default_kwargs,
            )

        assert result == (sentinel.default_a, sentinel.data_b)

    def test_process_raises(self):
        """ Function raises `RuleViolation`. Error is caught and transformed to
            `RulesValidationError`. """
        def function():
            raise RuleViolation(code='rule')

        with self.assertRaisesSingleValidationError(
            location=tuple(), code='rule', error_class=RulesValidationError
            ):
            validation_tools.process(
                schema=function,
                data={},
                default_kwargs=None,
                )


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


class TestRaiseValidationErrorFromRuleViolationUnit(unittest.TestCase):
    """ `validation_tools.raise_validation_error_from_rule_violation` """

    @patch('jsonmanager.validation_tools.ValidationError')
    @patch('jsonmanager.validation_tools.make_error_dict')
    def test_behavior(self, mock_make_error_dict, mock_ValidationError):
        exc = MagicMock()

        location = MagicMock()
        location.__add__.return_value = sentinel.complete_location

        mock_make_error_dict.return_value = sentinel.error_dict

        class ExpectedError(Exception):
            pass

        mock_ValidationError.return_value = ExpectedError()

        with self.assertRaises(ExpectedError):
            validation_tools.raise_validation_error_from_rule_violation(
                exc, location
                )

        mock_make_error_dict.assert_called_with(
            location=sentinel.complete_location,
            code=exc.code,
            message=exc.message,
            data=exc.data,
            )
        mock_ValidationError.assert_called_with(sentinel.error_dict)


class TestResolveKwargFunctional(unittest.TestCase):
    """ `validation_tools.resolve_kwarg` """

    def test_yes_set_value(self):
        """ When an argument value is provided, it is returned. """
        result = validation_tools.resolve_kwarg(
            value=sentinel.value,
            default_kwargs=sentinel.defaults,
            key=sentinel.key
            )
        assert result is sentinel.value

    def test_not_set_value(self):
        """ When an argument value is not provided, the default value is
            returned. """
        result = validation_tools.resolve_kwarg(
            value=validation_tools._NotSet,
            default_kwargs={'a': sentinel.expected},
            key='a'
            )
        assert result is sentinel.expected


class TestValidationIntegration(IntegrationTest, ConfiguredDecoratorTest):
    """ Confirm that `validation` works with no unexpected errors. """

    def setUp(self):
        super().setUp()
        self.configured_decorator = validation_tools.validation
