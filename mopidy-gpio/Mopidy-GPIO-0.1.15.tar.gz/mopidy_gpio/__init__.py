from __future__ import unicode_literals

import os
import logging

from mopidy import config, ext

logger = logging.getLogger(__name__)
__version__ = '0.1.15'


class Extension(ext.Extension):

    dist_name = 'Mopidy-GPIO'
    ext_name = 'gpio'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['pin_button_radio_1'] = config.Integer()
        schema['pin_button_radio_2'] = config.Integer()
        schema['pin_button_radio_3'] = config.Integer()
        schema['pin_button_radio_4'] = config.Integer()
        schema['pin_button_radio_5'] = config.Integer()
        return schema

    def setup(self, registry):
        from .backend import GPIOBackend
        registry.add('backend', GPIOBackend)