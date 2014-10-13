# coding: utf-8
'''
ConfigParser to Module
UsageExample
files(_config.ini) content
```
[db]
dbtype = mysql
```

files(_config.default.ini) content
```
[db]
dbtype = sqlite
user = guest
```

sample code
```
import gcfg
gcfg.DEFAULTFILES = ['_config.ini', '_config.default.ini']
print gcfg.db.dbtype # expect mysql
print gcfg.db.user   # expect guest
```
'''
import sys
from ConfigParser import ConfigParser
from types import ModuleType

__version__ = '0.2'

DEFAULTFILES = ['config.ini', 'config.default.ini']
_cfgparsers = {}

class _Section(object):
    def __init__(self, section):
        self._section = section
    
    def __getattr__(self, key):
        value = None
        for filename in reversed(DEFAULTFILES):
            if not _cfgparsers.get(filename):
                cf = ConfigParser()
                cf.read(filename)
                _cfgparsers[filename] = cf
            cf = _cfgparsers[filename]
            try:
                value = cf.get(self._section, key)
            except:
                pass
        if not value:
            raise RuntimeError("Value for %s-%s not exists" %(self._section, key))
        return value

class SelfWrapper(ModuleType):
    def __init__(self, self_module, baked_args={}):
        for attr in ["__file__", "__hash__", "__buildins__", "__doc__", "__name__", "__package__"]:
            setattr(self, attr, getattr(self_module, attr, None))

        self.self_module = self_module

    def __getattr__(self, name):
        if name in globals():
            return globals()[name]
        #if name == 'DEFAULTFILES':
        #    return DEFAULTFILES
        return _Section(name)

    def __call__(self, **kwargs):
        return SelfWrapper(self.self_module, kwargs)

self = sys.modules[__name__]
sys.modules[__name__] = SelfWrapper(self)

