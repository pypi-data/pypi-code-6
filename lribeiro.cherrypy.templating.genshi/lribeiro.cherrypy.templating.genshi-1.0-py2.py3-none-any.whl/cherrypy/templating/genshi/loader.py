import importlib
import types
import os.path

import cherrypy
from genshi.template import TemplateLoader


TEMPLATE_DIRECTORIES = 'templating.genshi.template_directories'
DEFAULT_LOOKUP_DIRECTORY = 'templates'

LOADER_OPTIONS = 'templating.genshi.loader_options'

_template_loader = dict()


def clear_loader():
    _template_loader.clear()


def _get_real_directory(path):
    if not isinstance(path, str):
        return path

    if path.startswith('/'):  # absolute path, just return
        return path

    root_module = importlib.import_module(cherrypy.request.app.root.__class__.__module__)
    root_dir = os.path.dirname(root_module.__file__)

    # absolute path to get rid of '../../' stuff
    return os.path.abspath(os.path.join(root_dir, path))


def _get_template_directory():
    lookup_directory = cherrypy.request.config.get(TEMPLATE_DIRECTORIES, None)

    if not lookup_directory:
        return [_get_real_directory(DEFAULT_LOOKUP_DIRECTORY)]

    if isinstance(lookup_directory, str):
        return _get_real_directory(lookup_directory)
    elif isinstance(lookup_directory, list):
        return [_get_real_directory(d) for d in lookup_directory]
    elif isinstance(lookup_directory, (types.FunctionType, types.LambdaType, types.MethodType)):
        return lookup_directory
    else:
        raise Exception('"{0}" must be either str or list'.format(TEMPLATE_DIRECTORIES))


def get_loader():
    """
    Get or create a TemplateLoader

    :return: The TemplateLoader instance
    :rtype: TemplateLoader
    """
    if 'instance' in _template_loader:
        return _template_loader['instance']

    search_path = _get_template_directory()
    loader_kwargs = dict()

    config = cherrypy.request.config.get(LOADER_OPTIONS, None)
    if config and isinstance(config, dict):
        loader_kwargs.update(config)

    loader_kwargs['search_path'] = search_path

    _template_loader['instance'] = TemplateLoader(**loader_kwargs)

    return _template_loader['instance']