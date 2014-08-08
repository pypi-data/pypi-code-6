import os

from flask import (json, send_from_directory, current_app,
                   url_for as flask_url_for)

CONFIG_PREFIX = 'MANIFEST_'
DEFAULT_CONFIG = {
    'MANIFEST_DEBUG': False,
    'MANIFEST_ROOT': 'dist',
    'MANIFEST_SERVE_ROOT': True,
    'MANIFEST_FILENAME': 'rev-manifest.json',
    'MANIFEST_ENDPOINT': 'manifest-dist',
    'MANIFEST_URL_PATH': '/dist',
    'MANIFEST_CND_NAME': None,
}
FOREVER = 10 * 365 * 24 * 60 * 60
EXTENSION_KEY = 'manifest'


def get_state():
    return current_app.extensions[EXTENSION_KEY]


def send_static_file(filename):
    return send_from_directory(get_state().root, filename,
                               cache_timeout=FOREVER)


def url_for(endpoint, **values):
    if endpoint == 'static':
        state = get_state()

        try:
            rev_file = state.manifest_contents[values['filename']]
        except KeyError:
            pass
        else:
            values['filename'] = rev_file

            if state.serve_root:
                endpoint = state.endpoint
            else:
                # TODO: Handle external domains like CDNs or integrate
                # with Flask-CDN
                values['_external'] = True

    return flask_url_for(endpoint, **values)


class ManifestState(object):
    def __init__(self, app):
        for key, value in DEFAULT_CONFIG.items():
            attr_name = key.replace(CONFIG_PREFIX, '').lower()
            setattr(self, attr_name, app.config.get(key, value))

        self.manifest = {}


class Manifest(object):
    def __init__(self, app=None):
        self.app = app

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app):
        state = ManifestState(app)

        if app.debug and not state.debug:
            return

        app.extensions[EXTENSION_KEY] = state

        path = os.path.join(state.root, state.filename)

        with app.open_resource(path) as manifest:
            state.manifest_contents = json.load(manifest)

        if state.serve_root:
            app.add_url_rule(state.url_path + '/<path:filename>',
                             endpoint=state.endpoint,
                             view_func=send_static_file)

        app.jinja_env.globals['url_for'] = url_for
