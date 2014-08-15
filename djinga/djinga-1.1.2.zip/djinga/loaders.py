"""
Jinja2 template loaders

(c) Thomas Khyn 2014
"""

from jinja2 import TemplateNotFound

from django.template.loaders import app_directories
from django.template.loaders import filesystem
from django.template.base import TemplateDoesNotExist

from .environment import Environment as env


class DjingaLoaderBase(object):
    """
    Overrides django default template loader with Jinja2 depending on a
    user-defined condition (function returning a boolean)
    """

    def load_template(self, template_name, template_dirs=None):

        if env.use_jinja(template_name):
            try:
                template = env.get_template(template_name)
            except TemplateNotFound:
                raise TemplateDoesNotExist(template_name)
            return template, template.filename

        return super(DjingaLoaderBase, self). \
            load_template(template_name, template_dirs)


class FileSystemLoader(DjingaLoaderBase, filesystem.Loader):
    pass


class AppLoader(DjingaLoaderBase, app_directories.Loader):
    pass
