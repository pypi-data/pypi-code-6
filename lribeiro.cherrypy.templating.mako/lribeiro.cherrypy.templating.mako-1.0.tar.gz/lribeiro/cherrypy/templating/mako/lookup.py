import importlib
import os.path

import cherrypy
from mako.lookup import TemplateLookup


TEMPLATE_DIRECTORIES = 'templating.mako.template_directories'
DEFAULT_LOOKUP_DIRECTORY = 'templates'
MAKO_CONFIG = 'templating.mako.config'

_template_lookup = dict()


def _get_real_directory(path):
    if path.startswith('/'):  # absolute path, just return
        return path

    root_module = importlib.import_module(cherrypy.request.app.root.__class__.__module__)
    root_dir = os.path.dirname(root_module.__file__)

    # absolute path to get rid of '../../' stuff
    return os.path.abspath(os.path.join(root_dir, path))


def _get_lookup_directory():
    lookup_directory = cherrypy.request.config.get(TEMPLATE_DIRECTORIES, None)

    if not lookup_directory:
        return [_get_real_directory(DEFAULT_LOOKUP_DIRECTORY)]

    if isinstance(lookup_directory, str):
        return [_get_real_directory(lookup_directory)]
    elif isinstance(lookup_directory, list):
        return [_get_real_directory(d) for d in lookup_directory]
    else:
        raise Exception('"{0}" must be either str or list'.format(TEMPLATE_DIRECTORIES))


def get_lookup():
    """
    Get or create a TemplateLookup

    :return: The TemplateLookup instance
    :rtype: TemplateLookup
    """
    if 'instance' in _template_lookup:
        return _template_lookup['instance']

    directories = _get_lookup_directory()
    lookup_kwargs = dict()

    config = cherrypy.request.config.get(MAKO_CONFIG, None)
    if config and isinstance(config, dict):
        lookup_kwargs.update(config)

    lookup_kwargs['directories'] = directories

    _template_lookup['instance'] = TemplateLookup(**lookup_kwargs)

    return _template_lookup['instance']