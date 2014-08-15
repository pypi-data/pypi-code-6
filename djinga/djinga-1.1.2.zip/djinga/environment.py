"""
Jinja2 environment container and functions, settings defaults and loader

(c) Thomas Khyn 2014
"""

import os
from importlib import import_module

import jinja2

from django.template import loader
from django.conf import settings
from django.template.context import BaseContext
from django.template import Origin
from django.core.exceptions import ImproperlyConfigured
from django.utils import six

DEFAULT_EXTS = {'J': ('jjhtml', 'jjhtm'),  # jinja2
                'D': ('html', 'htm', 'djhtml', 'djhtm')}  # django


def ctxt_to_dict(ctxt):
    """
    Helper function to convert a django context into a dictionary
    """
    if isinstance(ctxt, BaseContext):
        ctxt_dict = {}
        for d in ctxt.dicts:
            ctxt_dict.update(d)
        return ctxt_dict
    return dict(ctxt)


class DjingaTemplate(jinja2.Template):
    """
    Adapter class for jinja2 templates
    """

    def render(self, context=None):
        if context == None:
            context = {}

        new_ctxt = ctxt_to_dict(context)

        if settings.TEMPLATE_DEBUG:
            # send django signal on template rendering if in debug mode
            from django.test import signals
            self.origin = Origin(self.filename)
            signals.template_rendered.send(sender=self,
                                           template=self,
                                           context=context)

        return super(DjingaTemplate, self).render(new_ctxt)

    def stream(self, context=None):
        if context == None:
            context = {}

        new_ctxt = ctxt_to_dict(context)

        if settings.TEMPLATE_DEBUG:
            # send django signal on template rendering if in debug mode
            from django.test import signals
            self.origin = Origin(self.filename)
            signals.template_rendered.send(sender=self,
                                           template=self,
                                           context=context)

        return super(DjingaTemplate, self).stream(new_ctxt)


builtin_attrs = list(object.__dict__.keys()) + \
                list(type.__dict__.keys()) + \
                ['instance']


class EnvMetaClass(type):
    """
    Jinja2 environment metaclass (will be a singleton)
    """

    instance = None

    def __call__(self, *args, **kw):
        if self.instance is None:
            self.instance = type.__call__(self, *args, **kw)
        return self.instance

    def __getattribute__(self, attr):
        if attr in builtin_attrs:
            return type.__getattribute__(self, attr)
        instance = self.instance
        if not instance:
            instance = type.__call__(self)
            type.__setattr__(self, 'instance', instance)
        return self.__getattribute__(instance, attr)


class Environment(six.with_metaclass(EnvMetaClass, jinja2.Environment)):
    """
    Jinja2 environment singleton subclass
    """

    def __init__(self, *args, **kwargs):
        # environment initialisation
        # this will be called on first request of an environment attribute
        # (see metaclass implementation above)

        kwargs.update(getattr(settings, 'JINJA2_ENV_ARGS', {}))
        kwargs['extensions'] = set(kwargs.get('extensions', [])) \
            .union(getattr(settings, 'JINJA2_EXTENSIONS', {}))

        super(Environment, self).__init__(*args, **kwargs)

        # install i18n if USE_I18N is true
        if settings.USE_I18N:
            self.add_extension('jinja2.ext.i18n')
            from django.utils import translation
            self.install_gettext_translations(translation,
                newstyle=getattr(settings, 'JINJA2_I18N_NEWSTYLE', False))

        # template loader
        template_dirs = [x for ldr_str in settings.TEMPLATE_LOADERS\
            for x in loader.find_template_loader(ldr_str)\
            .get_template_sources('')]
        self.loader = jinja2.FileSystemLoader(template_dirs)

        # template class
        self.template_class = DjingaTemplate

        # add globally defined filters and globals from the settings
        self.filters.update(getattr(settings, 'JINJA2_FILTERS', {}))
        self.globals.update(getattr(settings, 'JINJA2_GLOBALS', {}))

        # add filters and globals from custom modules
        load_from = getattr(settings, 'JINJA2_LOAD_FROM', ())
        for module_path in load_from:
            mod = import_module(module_path)
            for x in dir(mod):
                o = getattr(mod, x)
                if hasattr(o, '_jj_filter'):
                    self.filters[o._jj_name] = o
                elif hasattr(o, '_jj_global'):
                    self.globals[o._jj_name] = o

        # fetch template extensions
        self.template_exts = []
        for s in 'DJ':  # 'J' must be in last position (see after the loop)
            s_name = 'JINJA2_%sJ_EXTS' % s
            exts = getattr(settings, s_name, DEFAULT_EXTS[s])

            if isinstance(exts, tuple):
                exts = list(exts)
            elif not isinstance(exts, list):
                raise ImproperlyConfigured(
                    'JINJA_%sJ_EXTS should be a tuple or list' % s)
            for i, ext in enumerate(exts):
                exts[i] = ext.lstrip('.')
            self.template_exts.extend(exts)

        self.use_jinja = getattr(settings, 'JINJA2_CONDITION',
            lambda path: os.path.basename(path).split('.')[-1] in exts)
