""" Tests for `exceptions` module. """
import unittest
from unittest.mock import (
    patch,
    sentinel,
    )

from jsonmanager import exceptions

class TestValidationErrorUnit(unittest.TestCase):
    """ `exceptions.ValidationError` """

    def test_errors(self):
        """ Arguments are stashed in the `errors` attribute. """
        exc = exceptions.ValidationError(sentinel.a, sentinel.b, sentinel.c)
        assert exc.errors == (sentinel.a, sentinel.b, sentinel.c)


class TestRuleViolationUnit(unittest.TestCase):
    """ `exceptions.RuleViolation` """

    @patch('jsonmanager.exceptions._key_location')
    def test_behavior(self, mock_key_location):
        mock_key_location.return_value = sentinel.location

        result = exceptions.RuleViolation(
            code=sentinel.code,
            message=sentinel.message,
            data=sentinel.data,
            key=sentinel.key,
            )

        mock_key_location.assert_called_with(sentinel.key)

        assert result.code is sentinel.code
        assert result.message is sentinel.message
        assert result.data is sentinel.data
        assert result.location is sentinel.location


class TestKeyLocationUnit(unittest.TestCase):
    """ `exceptions._key_location` """

    def test_key_is_none(self):
        result = exceptions._key_location(None)
        assert result == tuple()

    def test_key_is_not_none(self):
        result = exceptions._key_location(sentinel.key)
        assert result == tuple([sentinel.key])
