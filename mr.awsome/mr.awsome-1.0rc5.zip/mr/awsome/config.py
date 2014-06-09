from mr.awsome.common import Hooks
from ConfigParser import RawConfigParser
from UserDict import DictMixin
from weakref import proxy
import inspect
import logging
import os
import sys
import warnings


log = logging.getLogger('mr.awsome')


def value_asbool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('true', 'yes', 'on'):
        return True
    elif value.lower() in ('false', 'no', 'off'):
        return False


class BaseMassager(object):
    def __init__(self, sectiongroupname, key):
        self.sectiongroupname = sectiongroupname
        self.key = key

    def path(self, config, sectionname):
        return config._dict[self.key].path

    def __call__(self, config, sectionname):
        value = config._dict[self.key]
        if isinstance(value, ConfigValue):
            return value.value
        return value


class BooleanMassager(BaseMassager):
    def __call__(self, config, sectionname):
        value = BaseMassager.__call__(self, config, sectionname)
        value = value_asbool(value)
        if value is None:
            raise ValueError("Unknown value %s for %s in %s:%s." % (value, self.key, self.sectiongroupname, sectionname))
        return value


class IntegerMassager(BaseMassager):
    def __call__(self, config, sectionname):
        value = BaseMassager.__call__(self, config, sectionname)
        return int(value)


def expand_path(value, base):
    value = os.path.expanduser(value)
    if not os.path.isabs(value):
        value = os.path.join(base, value)
    return value


class PathMassager(BaseMassager):
    def __call__(self, config, sectionname):
        value = BaseMassager.__call__(self, config, sectionname)
        return expand_path(value, self.path(config, sectionname))


def resolve_dotted_name(value):
    if '.' in value:
        prefix, name = value.rsplit('.', 1)
        _temp = __import__(prefix, globals(), locals(), [name], -1)
        return getattr(_temp, name)
    else:
        return __import__(value, globals(), locals(), [], -1)


class HooksMassager(BaseMassager):
    def __call__(self, config, sectionname):
        value = BaseMassager.__call__(self, config, sectionname)
        hooks = Hooks()
        for hook_spec in value.split():
            hooks.add(resolve_dotted_name(hook_spec)())
        return hooks


class StartupScriptMassager(BaseMassager):
    def __call__(self, config, sectionname):
        value = BaseMassager.__call__(self, config, sectionname)
        result = dict()
        if value.startswith('gzip:'):
            value = value[5:]
            result['gzip'] = True
        if not os.path.isabs(value):
            value = os.path.join(self.path(config, sectionname), value)
        result['path'] = value
        return result


class UserMassager(BaseMassager):
    def __call__(self, config, sectionname):
        value = BaseMassager.__call__(self, config, sectionname)
        if value == "*":
            import pwd
            value = pwd.getpwuid(os.getuid())[0]
        return value


class ConfigValue(object):
    __slots__ = ('path', 'value')

    def __init__(self, path, value):
        self.path = path
        self.value = value


class ConfigSection(DictMixin):
    def __init__(self, *args, **kw):
        self._dict = dict(*args, **kw)
        self.sectionname = None
        self.sectiongroupname = None
        self._config = None
        self.massagers = {}

    def add_massager(self, massager):
        key = (massager.sectiongroupname, massager.key)
        if key in self.massagers:
            raise ValueError("Massager for option '%s' in section group '%s' already registered." % (massager.key, massager.sectiongroupname))
        self.massagers[key] = massager

    def __delitem__(self, key):
        del self._dict[key]

    def __getitem__(self, key):
        if key == '__groupname__':
            return self.sectiongroupname
        if key == '__name__':
            return self.sectionname
        if key in self._dict:
            if self._config is not None:
                massage = self._config.massagers.get((self.sectiongroupname, key))
                if not callable(massage):
                    massage = self._config.massagers.get((None, key))
                    if callable(massage):
                        if len(inspect.getargspec(massage.__call__).args) == 3:
                            return massage(self, self.sectionname)
                        else:
                            return massage(self, self.sectiongroupname, self.sectionname)
                else:
                    return massage(self, self.sectionname)
            massage = self.massagers.get((self.sectiongroupname, key))
            if callable(massage):
                return massage(self, self.sectionname)
        value = self._dict[key]
        if isinstance(value, ConfigValue):
            return value.value
        return value

    def __setitem__(self, key, value):
        if not isinstance(value, ConfigValue):
            value = ConfigValue(None, value)
        self._dict[key] = value

    def keys(self):
        return self._dict.keys()

    def copy(self):
        new = ConfigSection()
        new._dict = self._dict.copy()
        new.sectionname = self.sectionname
        new.sectiongroupname = self.sectiongroupname
        new.massagers = self.massagers.copy()
        new._config = self._config
        return new


class Config(ConfigSection):
    def _expand(self, sectiongroupname, sectionname, section, seen):
        if (sectiongroupname, sectionname) in seen:
            raise ValueError("Circular macro expansion.")
        seen.add((sectiongroupname, sectionname))
        macronames = section['<'].split()
        for macroname in macronames:
            if ':' in macroname:
                macrogroupname, macroname = macroname.split(':')
            else:
                macrogroupname = sectiongroupname
            macro = self[macrogroupname][macroname]
            if '<' in macro:
                self._expand(macrogroupname, macroname, macro, seen)
            if sectiongroupname in self.macro_cleaners:
                macro = macro.copy()
                self.macro_cleaners[sectiongroupname](macro)
            for key in macro:
                if key not in section:
                    section._dict[key] = macro._dict[key]
        # this needs to be after the recursive _expand call, so circles are
        # properly detected
        del section['<']

    def __init__(self, config, path=None, bbb_config=False, plugins=None):
        ConfigSection.__init__(self)
        self.config = config
        if path is None:
            if getattr(config, 'read', None) is None:
                path = os.path.dirname(config)
        self.path = path
        self.macro_cleaners = {}
        if plugins is not None:
            for plugin in plugins.values():
                for massager in plugin.get('get_massagers', lambda: [])():
                    self.add_massager(massager)
                if 'get_macro_cleaners' in plugin:
                    self.macro_cleaners.update(plugin['get_macro_cleaners'](self))

    def read_config(self, config):
        result = []
        stack = [config]
        while 1:
            config = stack.pop()
            _config = RawConfigParser()
            _config.optionxform = lambda s: s
            if getattr(config, 'read', None) is not None:
                _config.readfp(config)
                path = self.path
            else:
                if not os.path.exists(config):
                    log.error("Config file '%s' doesn't exist.", config)
                    sys.exit(1)
                _config.read(config)
                path = os.path.dirname(config)
            for section in reversed(_config.sections()):
                for key, value in reversed(_config.items(section)):
                    result.append((path, section, key, value))
                result.append((path, section, None, None))
            if _config.has_option('global', 'extends'):
                extends = _config.get('global', 'extends').split()
            elif _config.has_option('global:global', 'extends'):
                extends = _config.get('global:global', 'extends').split()
            else:
                break
            stack[0:0] = [
                os.path.abspath(os.path.join(path, x))
                for x in reversed(extends)]
        return reversed(result)

    def get_section(self, sectiongroupname, sectionname):
        sectiongroup = self[sectiongroupname]
        if sectionname not in sectiongroup:
            section = ConfigSection()
            section.sectiongroupname = sectiongroupname
            section.sectionname = sectionname
            section._config = proxy(self)
            sectiongroup[sectionname] = section
        return sectiongroup[sectionname]

    def parse(self):
        _config = self.read_config(self.config)
        for path, configsection, key, value in _config:
            if ':' in configsection:
                sectiongroupname, sectionname = configsection.split(':')
            else:
                sectiongroupname, sectionname = 'global', configsection
            if sectiongroupname == 'global' and sectionname == 'global' and key == 'extends':
                continue
            sectiongroup = self.setdefault(sectiongroupname, ConfigSection())
            self.get_section(sectiongroupname, sectionname)
            if key is not None:
                if key == 'massagers':
                    for spec in value.splitlines():
                        spec = spec.strip()
                        if not spec:
                            continue
                        if '=' not in spec:
                            log.error("Invalid massager spec '%s' in section '%s:%s'.", spec, sectiongroupname, sectionname)
                            sys.exit(1)
                        massager_key, massager = spec.split('=')
                        massager_key = massager_key.strip()
                        massager = massager.strip()
                        if ':' in massager_key:
                            parts = tuple(x.strip() for x in massager_key.split(':'))
                            if len(parts) == 2:
                                massager_sectiongroupname, massager_key = parts
                                massager_sectionname = None
                            elif len(parts) == 3:
                                massager_sectiongroupname, massager_sectionname, massager_key = parts
                            else:
                                log.error("Invalid massager spec '%s' in section '%s:%s'.", spec, sectiongroupname, sectionname)
                                sys.exit(1)
                            if massager_sectiongroupname == '':
                                massager_sectiongroupname = sectiongroupname
                            if massager_sectiongroupname == '*':
                                massager_sectiongroupname = None
                            if massager_sectionname == '':
                                massager_sectionname = sectionname
                        else:
                            massager_sectiongroupname = sectiongroupname
                            massager_sectionname = sectionname
                        try:
                            massager = resolve_dotted_name(massager)
                        except ImportError as e:
                            log.error("Can't import massager from '%s'.\n%s", massager, e.message)
                            sys.exit(1)
                        except AttributeError as e:
                            log.error("Can't import massager from '%s'.\n%s", massager, e.message)
                            sys.exit(1)
                        massager = massager(massager_sectiongroupname, massager_key)
                        if massager_sectionname is None:
                            self.add_massager(massager)
                        else:
                            massager_section = self.get_section(
                                sectiongroupname, massager_sectionname)
                            massager_section.add_massager(massager)
                else:
                    sectiongroup[sectionname][key] = ConfigValue(path, value)
        if 'plugin' in self:  # pragma: no cover
            warnings.warn("The 'plugin' section isn't used anymore.")
            del self['plugin']
        seen = set()
        for sectiongroupname in self:
            sectiongroup = self[sectiongroupname]
            for sectionname in sectiongroup:
                section = sectiongroup[sectionname]
                if '<' in section:
                    self._expand(sectiongroupname, sectionname, section, seen)
        return self

    def get_section_with_overrides(self, sectiongroupname, sectionname, overrides):
        config = self[sectiongroupname][sectionname].copy()
        if overrides is not None:
            config._dict.update(overrides)
        return config
