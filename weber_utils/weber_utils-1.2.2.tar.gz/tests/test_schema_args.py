import flask

import pytest
import weber_utils

_OK = object()
_SENTINEL = object()

def test_missing_fields_default_uses_arg_default(app):

    @weber_utils.takes_schema_args(field=weber_utils.Optional(int))
    def func(field=_SENTINEL):
        assert field is _SENTINEL
        return _OK

    with app.test_request_context(method="POST", data={}):
        assert func() is _OK



@pytest.fixture
def app():
    return flask.Flask(__name__)
