from __future__ import unicode_literals

import os

from mopidy import config, ext

__version__ = '0.1.6'

class Extension(ext.Extension):

    dist_name = 'Mopidy-GPIO'
    ext_name = 'gpio'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['pin_button_vol_up'] = config.Integer()
        schema['pin_button_vol_down'] = config.Integer()
        return schema

    def setup(self, registry):
        #from .frontend import GPIOFrontend
        #registry.add('frontend', GPIOFrontend)

		from .backend import GPIOBackend
        registry.add('backend', GPIOBackend)