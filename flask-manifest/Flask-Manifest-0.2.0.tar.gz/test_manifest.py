from cStringIO import StringIO
from contextlib import contextmanager
import mock
import pytest

from flask import Flask, current_app
from flask.ext.manifest import (Manifest, get_state, url_for, FOREVER,
                                EXTENSION_KEY)


TEST_MANIFEST = """{
  "image1.jpg": "image1-xyz.jpg",
  "image2.jpg": "image2-def.jpg"
}
"""


def create_test_app(debug=False, config=None):
    app = Flask(__name__)
    app.debug = debug

    if config:
        app.config.update(**config)

    Manifest(app)
    return app


@contextmanager
def open_manifest(*args):
    yield StringIO(TEST_MANIFEST)


@pytest.yield_fixture(autouse=True)
def app(monkeypatch):
    with mock.patch.object(Flask, 'open_resource', open_manifest):
        test_app = create_test_app()

    with test_app.test_request_context():
        yield test_app


def uses_app(func):
    return pytest.mark.usefixtures('app')


def test_manifest_contents_loaded():
    contents = get_state().manifest_contents
    assert 2 == len(contents)
    assert 'image1-xyz.jpg' == contents['image1.jpg']


def test_url_for():
    values = {'filename': 'image1.jpg'}
    assert '/dist/image1-xyz.jpg' == url_for('static', **values)


def test_url_for_fallback_to_flask_url_for():
    """
    If the ``filename`` isn't present in the manifest contents,
    the normal static URL should be returned.
    """
    assert '/static/image3.jpg' == url_for('static', filename='image3.jpg')


def test_manifest_endpoint_view_func():
    target = 'flask_manifest.send_from_directory'

    with current_app.test_client() as client:
        with mock.patch(target) as mock_send_file:
            mock_send_file.return_value = 'contents'
            response = client.get(url_for('static', filename='image1.jpg'))

    state = get_state()
    mock_send_file.assert_called_once_with(state.root, 'image1-xyz.jpg',
                                           cache_timeout=FOREVER)
    assert 'contents' == response.data


def test_extension_does_nothing_in_debug_mode(app):
    assert EXTENSION_KEY in app.extensions
    assert EXTENSION_KEY not in create_test_app(debug=True).extensions

    with mock.patch.object(Flask, 'open_resource', open_manifest):
        app = create_test_app(debug=True, config={'MANIFEST_DEBUG': True})

    assert EXTENSION_KEY in app.extensions


@pytest.mark.xfail
def test_url_for_without_serving_dist_root():
    """
    Some other server might be serving the files in the manifest.
    TODO: Figure out the best way to construct URLs with the
    ``MANIFEST_DOMAIN``.
    """
    state = get_state()
    state.serve_root = False
    state.domain = 'example.com'
    expected_url = 'http://example.com/dist/image1-xyz.jpg'
    assert expected_url == url_for('static', filename='image1.jpg')
