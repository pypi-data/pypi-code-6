#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
# implicit test ??
from flask.ext.iniconfig import INIConfig

import nose.tools as nt

class TestINIConfig(object):

    @classmethod
    def setupClass(cls):
        cls.app = Flask('foo')
        INIConfig(cls.app)

    def setup(self):
        with self.app.app_context():
            self.app.config.from_inifile('test.ini')

    @staticmethod
    def check_type(value, type_):
        nt.assert_is_instance(value, type_)

    @staticmethod
    def check_membership(config, name):
        nt.assert_in(name, config)

    @staticmethod
    def check_no_membership(config, name):
        nt.assert_not_in(name, config)

    def test_init_app(self):
        app = Flask('bar')
        with app.app_context():
            INIConfig().init_app(app)

    def test_configparser_options(self):
        app = Flask('bar')
        with app.app_context():
            INIConfig(defaults={'a': 1}, dict_type=dict,
                    allow_no_value=True).init_app(app)

    def test_config_method(self):
        nt.ok_(hasattr(self.app.config, 'from_inifile'))

    def test_load_nofile_noerror(self):
        with self.app.app_context():
            self.app.config.from_inifile('nonexistant.ini')

    def test_load_flask_default(self):
        nt.ok_('DEBUG' in self.app.config)
        nt.ok_(self.app.config['DEBUG'])

    def test_load_section_case_sensitivity(self):
        settings = self.app.config.get('INTS')
        nt.assert_is_none(settings)

    def test_load_property_case_sensitivity(self):
        settings = self.app.config.get('ints')
        property = settings.get('G')
        nt.assert_is_none(property)

    def test_load_basic_types(self):
        for type_ in [int, float, bool, str]:
            settings = self.app.config['%ss' % type_.__name__]
            for key, value in settings.items():
                yield self.check_type, value, type_

    def test_load_json_list(self):
        settings = self.app.config['literals']
        nt.assert_is_instance(settings['o'], list)

    def test_load_json_dict(self):
        settings = self.app.config['literals']
        for name in ['p', 'q']:
            yield self.check_type, settings[name], dict

    def test_load_json_embedded_list(self):
        settings = self.app.config['literals']
        nt.assert_is_instance(settings['q']['b'], list)

    def test_load_json_embedded_dict(self):
        settings = self.app.config['literals']
        nt.assert_is_instance(settings['q']['c'], dict)

    def test_load_json_tuple(self):
        settings = self.app.config['literals']
        nt.assert_is_instance(settings['r'], tuple)

    def test_load_colon_separated(self):
        settings = self.app.config['colonsep']
        for name in ['v', 'w']:
            yield self.check_membership, settings, name

    def test_load_empty(self):
        settings = self.app.config['empty']
        nt.eq_(settings['x'], '')

    def test_load_settings_only(self):
        app = Flask('bar')
        with app.app_context():
            INIConfig().init_app(app)
            app.config.from_inifile_sections('test.ini', ['strs'])

            for name in ['DEBUG', 'S', 'T', 'U']:
                yield self.check_membership, app.config, name

            for name in ['debug', 's', 't', 'u']:
                yield self.check_no_membership, app.config, name

    def test_load_settings_only_with_preserve_case(self):
        app = Flask('bar')
        with app.app_context():
            INIConfig().init_app(app)
            app.config.from_inifile_sections('test.ini', ['strs'],
                    preserve_case=True)

            for name in ['DEBUG', 's', 't', 'u']:
                yield self.check_membership, app.config, name

            for name in ['debug', 'S', 'T', 'U']:
                yield self.check_no_membership, app.config, name
