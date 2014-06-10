from StringIO import StringIO
from mock import patch
from mr.awsome.config import Config
from unittest2 import TestCase
import os
import pytest
import shutil
import tempfile


class ConfigTests(TestCase):
    def testEmpty(self):
        contents = StringIO("")
        config = Config(contents).parse()
        assert config == {}

    def testPlainSection(self):
        contents = StringIO("[foo]")
        config = Config(contents).parse()
        assert config == {'global': {'foo': {}}}

    def testGroupSection(self):
        contents = StringIO("[bar:foo]")
        config = Config(contents).parse()
        config == {'bar': {'foo': {}}}

    def testMixedSections(self):
        contents = StringIO("[bar:foo]\n[baz]")
        config = Config(contents).parse()
        assert config == {
            'bar': {'foo': {}},
            'global': {'baz': {}}}

    def testMacroExpansion(self):
        from mr.awsome.config import ConfigValue
        contents = StringIO("\n".join([
            "[macro]",
            "macrovalue=1",
            "[baz]",
            "<=macro",
            "bazvalue=2"]))
        config = Config(contents).parse()
        assert config == {
            'global': {
                'macro': {'macrovalue': '1'},
                'baz': {'macrovalue': '1', 'bazvalue': '2'}}}
        assert isinstance(config['global']['baz']._dict['macrovalue'], ConfigValue)
        assert isinstance(config['global']['baz']._dict['bazvalue'], ConfigValue)

    def testGroupMacroExpansion(self):
        contents = StringIO("\n".join([
            "[group:macro]",
            "macrovalue=1",
            "[baz]",
            "<=group:macro",
            "bazvalue=2"]))
        config = Config(contents).parse()
        assert config == {
            'global': {
                'baz': {'macrovalue': '1', 'bazvalue': '2'}},
            'group': {
                'macro': {'macrovalue': '1'}}}

    def testCircularMacroExpansion(self):
        contents = StringIO("\n".join([
            "[macro]",
            "<=macro",
            "macrovalue=1"]))
        with self.assertRaises(ValueError):
            Config(contents).parse()

    def testMacroCleaners(self):
        dummyplugin = DummyPlugin()
        plugins = dict(
            dummy=dict(
                get_macro_cleaners=dummyplugin.get_macro_cleaners))

        def cleaner(macro):
            if 'cleanvalue' in macro:
                del macro['cleanvalue']

        dummyplugin.macro_cleaners = {'global': cleaner}
        contents = StringIO("\n".join([
            "[group:macro]",
            "macrovalue=1",
            "cleanvalue=3",
            "[baz]",
            "<=group:macro",
            "bazvalue=2"]))
        config = Config(contents, plugins=plugins).parse()
        assert config == {
            'global': {
                'baz': {'macrovalue': '1', 'bazvalue': '2'}},
            'group': {
                'macro': {'macrovalue': '1', 'cleanvalue': '3'}}}

    def testOverrides(self):
        contents = StringIO("\n".join([
            "[section]",
            "value=1"]))
        config = Config(contents).parse()
        assert config == {'global': {'section': {'value': '1'}}}
        result = config.get_section_with_overrides(
            'global',
            'section',
            overrides=None)
        assert result == {
            'value': '1'}
        result = config.get_section_with_overrides(
            'global',
            'section',
            overrides={'value': '2'})
        assert result == {
            'value': '2'}
        result = config.get_section_with_overrides(
            'global',
            'section',
            overrides={'value2': '2'})
        assert result == {
            'value': '1',
            'value2': '2'}
        # make sure nothing is changed afterwards
        assert config == {'global': {'section': {'value': '1'}}}

    def testSpecialKeys(self):
        contents = StringIO("\n".join([
            "[section]",
            "value=1"]))
        config = Config(contents).parse()
        assert config['global']['section']['__name__'] == 'section'
        assert config['global']['section']['__groupname__'] == 'global'


class DummyPlugin(object):
    def __init__(self):
        self.macro_cleaners = {}
        self.massagers = []

    def get_macro_cleaners(self, main_config):
        return self.macro_cleaners

    def get_massagers(self):
        return self.massagers


@pytest.mark.parametrize("value, expected", [
    (True, True),
    (False, False),
    ("true", True),
    ("yes", True),
    ("on", True),
    ("false", False),
    ("no", False),
    ("off", False),
    ("foo", None)])
def test_value_asbool(value, expected):
    from mr.awsome.config import value_asbool
    assert value_asbool(value) == expected


class MassagerTests(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.dummyplugin = DummyPlugin()
        self.plugins = dict(
            dummy=dict(
                get_massagers=self.dummyplugin.get_massagers))

    def tearDown(self):
        TestCase.tearDown(self)
        del self.plugins
        del self.dummyplugin

    def testBaseMassager(self):
        from mr.awsome.config import BaseMassager

        self.dummyplugin.massagers.append(BaseMassager('section', 'value'))
        contents = StringIO("\n".join([
            "[section:foo]",
            "value=1"]))
        config = Config(contents, plugins=self.plugins).parse()
        assert config['section'] == {'foo': {'value': '1'}}

    def testBooleanMassager(self):
        from mr.awsome.config import BooleanMassager

        self.dummyplugin.massagers.append(BooleanMassager('section', 'value'))
        test_values = (
            ('true', True),
            ('True', True),
            ('yes', True),
            ('Yes', True),
            ('on', True),
            ('On', True),
            ('false', False),
            ('False', False),
            ('no', False),
            ('No', False),
            ('off', False),
            ('Off', False))
        for value, expected in test_values:
            contents = StringIO("\n".join([
                "[section:foo]",
                "value=%s" % value]))
            config = Config(contents, plugins=self.plugins).parse()
            assert config['section'] == {'foo': {'value': expected}}
        contents = StringIO("\n".join([
            "[section:foo]",
            "value=foo"]))
        config = Config(contents, plugins=self.plugins).parse()
        with self.assertRaises(ValueError):
            config['section']['foo']['value']

    def testIntegerMassager(self):
        from mr.awsome.config import IntegerMassager

        self.dummyplugin.massagers.append(IntegerMassager('section', 'value'))
        contents = StringIO("\n".join([
            "[section:foo]",
            "value=1"]))
        config = Config(contents, plugins=self.plugins).parse()
        assert config['section'] == {'foo': {'value': 1}}
        contents = StringIO("\n".join([
            "[section:foo]",
            "value=foo"]))
        config = Config(contents, plugins=self.plugins).parse()
        with self.assertRaises(ValueError):
            config['section']['foo']['value']

    def testPathMassager(self):
        from mr.awsome.config import PathMassager

        self.dummyplugin.massagers.append(PathMassager('section', 'value1'))
        self.dummyplugin.massagers.append(PathMassager('section', 'value2'))
        contents = StringIO("\n".join([
            "[section:foo]",
            "value1=foo",
            "value2=/foo"]))
        config = Config(contents, path='/config', plugins=self.plugins).parse()
        assert config['section'] == {
            'foo': {
                'value1': '/config/foo',
                'value2': '/foo'}}

    def testStartupScriptMassager(self):
        from mr.awsome.config import StartupScriptMassager

        self.dummyplugin.massagers.append(StartupScriptMassager('section', 'value1'))
        self.dummyplugin.massagers.append(StartupScriptMassager('section', 'value2'))
        self.dummyplugin.massagers.append(StartupScriptMassager('section', 'value3'))
        self.dummyplugin.massagers.append(StartupScriptMassager('section', 'value4'))
        contents = StringIO("\n".join([
            "[section:foo]",
            "value1=gzip:foo",
            "value2=foo",
            "value3=gzip:/foo",
            "value4=/foo"]))
        config = Config(contents, path='/config', plugins=self.plugins).parse()
        assert config['section'] == {
            'foo': {
                'value1': {'gzip': True, 'path': '/config/foo'},
                'value2': {'path': '/config/foo'},
                'value3': {'gzip': True, 'path': '/foo'},
                'value4': {'path': '/foo'}}}

    def testUserMassager(self):
        from mr.awsome.config import UserMassager
        import pwd

        self.dummyplugin.massagers.append(UserMassager('section', 'value1'))
        self.dummyplugin.massagers.append(UserMassager('section', 'value2'))
        contents = StringIO("\n".join([
            "[section:foo]",
            "value1=*",
            "value2=foo"]))
        config = Config(contents, plugins=self.plugins).parse()
        assert config['section'] == {
            'foo': {
                'value1': pwd.getpwuid(os.getuid())[0],
                'value2': 'foo'}}

    def testCustomMassager(self):
        from mr.awsome.config import BaseMassager

        class DummyMassager(BaseMassager):
            def __call__(self, config, sectionname):
                value = BaseMassager.__call__(self, config, sectionname)
                return int(value)

        self.dummyplugin.massagers.append(DummyMassager('section', 'value'))
        contents = StringIO("\n".join([
            "[section:foo]",
            "value=1"]))
        config = Config(contents, plugins=self.plugins).parse()
        assert config['section'] == {'foo': {'value': 1}}

    def testCustomMassagerForAnyGroup(self):
        from mr.awsome.config import BaseMassager

        class DummyMassager(BaseMassager):
            def __call__(self, config, sectiongroupname, sectionname):
                value = BaseMassager.__call__(self, config, sectionname)
                return (sectiongroupname, value)

        self.dummyplugin.massagers.append(DummyMassager(None, 'value'))
        contents = StringIO("\n".join([
            "[section1:foo]",
            "value=1",
            "[section2:bar]",
            "value=2"]))
        config = Config(contents, plugins=self.plugins).parse()
        assert config == {
            'section1': {
                'foo': {'value': ('section1', '1')}},
            'section2': {
                'bar': {'value': ('section2', '2')}}}

    def testConflictingMassagerRegistration(self):
        from mr.awsome.config import BaseMassager

        config = Config(StringIO('')).parse()
        config.add_massager(BaseMassager('section', 'value'))
        with pytest.raises(ValueError) as e:
            config.add_massager(BaseMassager('section', 'value'))
        assert e.value.message == "Massager for option 'value' in section group 'section' already registered."

    def testMassagedOverrides(self):
        from mr.awsome.config import IntegerMassager

        self.dummyplugin.massagers.append(IntegerMassager('global', 'value'))
        self.dummyplugin.massagers.append(IntegerMassager('global', 'value2'))
        contents = StringIO("\n".join([
            "[section]",
            "value=1"]))
        config = Config(contents, plugins=self.plugins).parse()
        assert config['global'] == {'section': {'value': 1}}
        result = config.get_section_with_overrides(
            'global',
            'section',
            overrides=None)
        assert result == {
            'value': 1}
        result = config.get_section_with_overrides(
            'global',
            'section',
            overrides={'value': '2'})
        assert result == {
            'value': 2}
        result = config.get_section_with_overrides(
            'global',
            'section',
            overrides={'value2': '2'})
        assert result == {
            'value': 1,
            'value2': 2}
        # make sure nothing is changed afterwards
        assert config['global'] == {'section': {'value': 1}}

    def testSectionMassagedOverrides(self):
        from mr.awsome.config import IntegerMassager

        contents = StringIO("\n".join([
            "[section]",
            "value=1"]))
        config = Config(contents, plugins=self.plugins).parse()
        config['global']['section'].add_massager(IntegerMassager('global', 'value'))
        config['global']['section'].add_massager(IntegerMassager('global', 'value2'))
        assert config['global'] == {'section': {'value': 1}}
        result = config.get_section_with_overrides(
            'global',
            'section',
            overrides=None)
        assert result == {
            'value': 1}
        result = config.get_section_with_overrides(
            'global',
            'section',
            overrides={'value': '2'})
        assert result == {
            'value': 2}
        result = config.get_section_with_overrides(
            'global',
            'section',
            overrides={'value2': '2'})
        assert result == {
            'value': 1,
            'value2': 2}
        # make sure nothing is changed afterwards
        assert config['global'] == {'section': {'value': 1}}


def _make_config(massagers):
    return Config(StringIO("\n".join([
        "[section1]",
        "massagers = %s" % massagers,
        "value = 1",
        "[section2]",
        "value = 2",
        "[foo:bar]",
        "value = 3"]))).parse()


def _expected(first, second, third):
    return {
        'global': {
            'section1': {
                'value': first('1')},
            'section2': {
                'value': second('2')}},
        'foo': {
            'bar': {
                'value': third('3')}}}


@pytest.mark.parametrize("description, massagers, expected", [
    (
        'empty',
        '', (str, str, str)),
    (
        'current section',
        'value=mr.awsome.config.IntegerMassager', (int, str, str)),
    (
        'current section alternate',
        '::value=mr.awsome.config.IntegerMassager', (int, str, str)),
    (
        'different section',
        ':section2:value = mr.awsome.config.IntegerMassager', (str, int, str)),
    (
        'different section alternate',
        'global:section2:value = mr.awsome.config.IntegerMassager', (str, int, str)),
    (
        'multiple massagers',
        'value = mr.awsome.config.IntegerMassager\n    :section2:value = mr.awsome.config.IntegerMassager', (int, int, str)),
    (
        'for section group',
        'global:value = mr.awsome.config.IntegerMassager', (int, int, str)),
    (
        'for everything',
        '*:value = mr.awsome.config.IntegerMassager', (int, int, int))])
def test_valid_massagers_specs_in_config(description, massagers, expected):
    config = _make_config(massagers)
    expected = _expected(*expected)
    print "Description of failed test:\n   ", description
    print
    assert dict(config) == expected


class MassagersFromConfigTests(TestCase):
    def testInvalid(self):
        contents = StringIO("\n".join([
            "[section]",
            "massagers = foo",
            "value = 1"]))
        with patch('mr.awsome.config.log') as LogMock:
            with pytest.raises(SystemExit):
                Config(contents).parse()
        self.assertEquals(
            LogMock.error.call_args_list,
            [
                (("Invalid massager spec '%s' in section '%s:%s'.", 'foo', 'global', 'section'), {})])

    def testTooManyColonsInSpec(self):
        contents = StringIO("\n".join([
            "[section]",
            "massagers = :::foo=mr.awsome.config.IntegerMassager",
            "value = 1"]))
        with patch('mr.awsome.config.log') as LogMock:
            with pytest.raises(SystemExit):
                Config(contents).parse()
        self.assertEquals(
            LogMock.error.call_args_list,
            [
                (("Invalid massager spec '%s' in section '%s:%s'.", ':::foo=mr.awsome.config.IntegerMassager', 'global', 'section'), {})])

    def testUnknownModuleFor(self):
        contents = StringIO("\n".join([
            "[section]",
            "massagers = foo=bar",
            "value = 1"]))
        with patch('mr.awsome.config.log') as LogMock:
            with pytest.raises(SystemExit):
                Config(contents).parse()
        self.assertEquals(
            LogMock.error.call_args_list,
            [
                (("Can't import massager from '%s'.\n%s", 'bar', 'No module named bar'), {})])

    def testUnknownAttributeFor(self):
        contents = StringIO("\n".join([
            "[section]",
            "massagers = foo=mr.awsome.foobar",
            "value = 1"]))
        with patch('mr.awsome.config.log') as LogMock:
            with pytest.raises(SystemExit):
                Config(contents).parse()
        self.assertEquals(
            LogMock.error.call_args_list,
            [
                (("Can't import massager from '%s'.\n%s", 'mr.awsome.foobar', "'module' object has no attribute 'foobar'"), {})])


class ConfigExtendTests(TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.directory)
        del self.directory

    def _write_config(self, conf, content):
        with open(os.path.join(self.directory, conf), 'w') as f:
            f.write(content)

    def testExtend(self):
        awsconf = 'aws.conf'
        self._write_config(
            awsconf,
            '\n'.join([
                '[global]',
                'extends = foo.conf',
                'ham = egg']))
        self._write_config(
            'foo.conf',
            '\n'.join([
                '[global]',
                'foo = bar',
                'ham = pork']))
        config = Config(os.path.join(self.directory, awsconf)).parse()
        assert config == {
            'global': {
                'global': {
                    'foo': 'bar', 'ham': 'egg'}}}

    def testDoubleExtend(self):
        awsconf = 'aws.conf'
        self._write_config(
            awsconf,
            '\n'.join([
                '[global]',
                'extends = foo.conf',
                'ham = egg']))
        self._write_config(
            'foo.conf',
            '\n'.join([
                '[global]',
                'extends = bar.conf',
                'foo = blubber',
                'ham = pork']))
        self._write_config(
            'bar.conf',
            '\n'.join([
                '[global]',
                'foo = bar',
                'ham = pork']))
        config = Config(os.path.join(self.directory, awsconf)).parse()
        assert config == {
            'global': {
                'global': {
                    'foo': 'blubber', 'ham': 'egg'}}}

    def testExtendFromDifferentDirectoryWithMassager(self):
        from mr.awsome.config import PathMassager
        os.mkdir(os.path.join(self.directory, 'bar'))
        awsconf = 'aws.conf'
        self._write_config(
            awsconf,
            '\n'.join([
                '[global]',
                'extends = bar/foo.conf',
                'ham = egg']))
        self._write_config(
            'bar/foo.conf',
            '\n'.join([
                '[global]',
                'foo = blubber',
                'ham = pork']))
        config = Config(os.path.join(self.directory, awsconf)).parse()
        config.add_massager(PathMassager('global', 'foo'))
        config.add_massager(PathMassager('global', 'ham'))
        assert config == {
            'global': {
                'global': {
                    'foo': os.path.join(self.directory, 'bar', 'blubber'),
                    'ham': os.path.join(self.directory, 'egg')}}}

    def testExtendFromMissingFile(self):
        awsconf = 'aws.conf'
        self._write_config(
            awsconf,
            '\n'.join([
                '[global:global]',
                'extends = foo.conf',
                'ham = egg']))
        with patch('mr.awsome.config.log') as LogMock:
            with pytest.raises(SystemExit):
                Config(os.path.join(self.directory, awsconf)).parse()
        self.assertEquals(
            LogMock.error.call_args_list,
            [
                (("Config file '%s' doesn't exist.", os.path.join(self.directory, 'foo.conf')), {})])
