from inspect import getmodule
from sys import modules
from os import stat

from _term import is_module, is_str

import logging
logger = logging.getLogger('fanery.autoreload')

# modules files stats
_mf_stats = dict()


def deep_reload(module, loaded=None, parent=None):
    """Deep reload of module.

    Adapted from
    http://stackoverflow.com/questions/5364050/reloading-submodules-in-ipython
    """
    if is_str(module):
        if module in modules:
            module = modules[module]
        else:
            return

    if not is_module(module):
        module = getmodule(module)

    if parent is None:
        parent = module.__name__

    if parent == '__main__':
        return
    elif loaded is None:
        loaded = set()

    if module.__name__.startswith(parent):
        for name in dir(module):
            member = getattr(module, name)
            if is_module(member) and member not in loaded:
                deep_reload(member, loaded, parent)
            try:
                m_file = module.__file__
                m_mtime = stat(m_file).st_mtime
                if m_file in _mf_stats and m_mtime > _mf_stats[m_file]:
                    reload(module)
                _mf_stats[m_file] = m_mtime
                loaded.add(module)
            except:
                logger.error('reload module %s' % module, exc_info=True)
