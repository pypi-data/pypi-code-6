import logging
import json
import os
import pprint

log = logging.getLogger(__name__)


class Settings(object):
    """
    Parses a JSON file for user defined settings.
    """
    defaults  = {
        # Path to your CSS file relative to the settings file (or CWD if no settings file).
        'preview_cssfile': None,

        # The output directory relative to the settings file (or CWD if no settings file).
        'outdir': 'vitalstyles_styleguide',

        # A list of files or directories to parse.
        # Directories is searched recursively for ``.scss``,
        # ``.sass``, ``.css`` and ``.less`` files.
        'inpaths': [os.getcwd()],

        # User defined templates directory.
        'template_dir': None,

        # The title of the guide
        'title': 'Vitalstyles style guide',

        # A list of filesystem directories. The contents of these directories
        # are copied into the assets sub-directory of the ``outdir``.
        # The directory itself is not copied, so if you specify two directories
        # containing the same file, the file from the last directory in the
        # list will overwrite the first.
        'asset_directories': [],

        # Include stock assets? This will add a directory named
        # stock to your assets/ directory, and fill it with assets
        # that you can use in your styleguide.
        'include_stock_assets': False
    }

    def __init__(self, filename=None):
        self.settings = self.defaults.copy()
        self.basedir = os.getcwd()
        if filename:
            if os.path.exists(filename):
                self.setup_with_settingsfile(filename)
            else:
                self.handle_settingsfile_missing()
        else:
            self.setup_without_settingsfile()

    def handle_settingsfile_missing(self):
        log.info('No settings file found. Using default settings:\n%s', pprint.pformat(self.settings))

    def setup_with_settingsfile(self, filename):
        log.debug('Loading settings from %s', filename)
        self.filename = filename
        self.basedir = os.path.dirname(filename)
        with open(self.filename, 'rb') as f:
            self.rawdata = f.read()
        usersettings = json.loads(self.rawdata)
        for key, value in usersettings.iteritems():
            if not key in self.defaults:
                raise KeyError('Invalid settings key: {}.'.format(key))
            else:
                self.settings[key] = value

    def setup_without_settingsfile(self):
        log.info('No settings file specified. Using default settings:\n%s', pprint.pformat(self.settings))

    def __getitem__(self, key):
        return self.settings[key]

    def __contains__(self, key):
        return key in self.settings

    def get_outdir_path(self):
        return os.path.abspath(os.path.join(self.basedir, self.settings['outdir']))

    def get_assets_outdir_path(self):
        return os.path.join(self.get_outdir_path(), 'assets')

    def get_stock_assets_directory(self):
        return os.path.join(os.path.dirname(__file__), 'stock_assets')

    def iter_asset_directories(self):
        if self.settings['include_stock_assets']:
            yield self.get_stock_assets_directory()
        for path in self.settings['asset_directories']:
            yield os.path.abspath(os.path.join(self.basedir, path))

    def get_preview_cssfilepath_relative_to_outdir(self):
        path = os.path.abspath(os.path.join(self.basedir, self.settings['preview_cssfile']))
        return os.path.relpath(path, self.get_outdir_path())

    def get_template_dir_path(self):
        if self.settings['template_dir']:
            return os.path.abspath(os.path.join(self.basedir, self.settings['template_dir']))
        else:
            return None
