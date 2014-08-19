import unittest
from unittest.mock import (
    patch,
    sentinel,
    )

from jsonmanager import exceptions
from jsonmanager import rules
from jsonmanager import validation_tools
from jsonmanager.schema_types import AnyType


class TestOverrideDefaults(unittest.TestCase):
    """ `rules.override_defaults` """

    def test_behavior(self):
        @rules.override_defaults
        def rule(data): # pylint: disable=unused-argument
            pass

        assert rule.override_defaults is True


class TestRequiredUnit(unittest.TestCase):
    """ `rules.Required` """

    def test_None_raises(self):
        with self.assertRaises(exceptions.RuleViolation):
            rules.Required(None)

    def test_empty_string_raises(self):
        data = ''
        with self.assertRaises(exceptions.RuleViolation):
            rules.Required(data)

    def test_other_passes(self):
        rules.Required(sentinel.data)


class TestNullableUnit(unittest.TestCase):
    """ `rules.Nullable` """

    def test_None_raises_stop_validation(self):
        with self.assertRaises(exceptions.StopValidation):
            rules.Nullable(None)

    def test_not_None_passes(self):
        rules.Nullable(sentinel.data)


class TestRequiredNullableIntegration(unittest.TestCase):
    """ `Required` and `Nullable` each override the other when the other is
        used in `default_rules`. """

    def test_Nullable_overrides_Required(self):
        defaults = validation_tools.ValidationDefaults(
            default_rules=(rules.Required,)
            )

        validation_tools.validate(
            schema=(AnyType, rules.Nullable),
            data=object(),
            defaults=defaults,
            )

    def test_Required_overrides_Nullable(self):
        defaults = validation_tools.ValidationDefaults(
            default_rules=(rules.Nullable,)
            )

        with self.assertRaises(exceptions.ValidationError) as exc_context:
            validation_tools.validate(
                schema=(AnyType, rules.Required),
                data=None,
                defaults=defaults,
                )
        exc = exc_context.exception
        assert len(exc.errors) == 1
        assert exc.errors[0]['code'] == 'required'


class TestLengthFunctional(unittest.TestCase):
    """ `rules.Length` """

    def test_correct_length_passes(self):
        rule = rules.Length(3)
        rule('xxx')

    def test_incorrect_length_raises(self):
        rule = rules.Length(3)
        with self.assertRaises(exceptions.RuleViolation):
            rule('xxxx')


class TestOneOfFunctional(unittest.TestCase):
    """ `rules.OneOf` """

    def test_yes_in_passes(self):
        """ `data` is in the collection. """
        rule = rules.OneOf(sentinel.a, sentinel.target, sentinel.b)
        rule(sentinel.target)

    def test_not_in_raises(self):
        """ `data` is not in the collection. """
        rule = rules.OneOf(sentinel.a, sentinel.b)
        with self.assertRaises(exceptions.RuleViolation):
            rule(sentinel.target)


class TestRangeFunctional(unittest.TestCase):
    """ `rules.Range` """

    def setUp(self):
        self.rule = rules.Range(1, 3)

    def test_in_range_passes(self):
        self.rule(2)

    def test_minimum_inclusive_passes(self):
        self.rule(1)

    def test_maximum_inclusive_passes(self):
        self.rule(3)

    def test_below_minimum_raises(self):
        with self.assertRaises(exceptions.RuleViolation):
            self.rule(0)

    def test_above_maximum_raises(self):
        with self.assertRaises(exceptions.RuleViolation):
            self.rule(4)


@patch('jsonmanager.rules.re.match')
class TestRegexUnit(unittest.TestCase):
    """ `rules.Regex` """

    def setUp(self):
        self.rule = rules.Regex(sentinel.pattern)

    def test_match_succeeds(self, mock_re_match):
        mock_re_match.return_value = True
        self.rule(sentinel.data)
        mock_re_match.assert_called_with(sentinel.pattern, sentinel.data)

    def test_match_fails(self, mock_re_match):
        mock_re_match.return_value = False
        with self.assertRaises(exceptions.RuleViolation):
            self.rule(sentinel.data)
        mock_re_match.assert_called_with(sentinel.pattern, sentinel.data)
