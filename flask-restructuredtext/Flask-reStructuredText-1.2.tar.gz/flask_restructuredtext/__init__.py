# -*- coding: utf-8 -*-
"""Easy integration of reStructuredText.

flaskext.restructuredtext
~~~~~~~~~~~~~~~~~~~~~~~~~

reStructuredText filter class for Flask.

:copyright: (c) 2014 by Dennis Fink.
:license: BSD, see LICENSE for more details.

"""

from collections.abc import Sequence, Set, Mapping

from importlib import import_module
from importlib.util import resolve_name

from flask import Markup
from jinja2 import evalcontextfilter, escape

from docutils.core import publish_parts
from docutils.parsers.rst import directives as docutils_directives
from docutils.parsers.rst import roles as docutils_roles
from docutils.writers.html4css1 import Writer as HTMLWriter


def _multiple_names(object):
    return isinstance(object, (Sequence, Set)) and not isinstance(object, str)


class ReStructuredText(object):

    """Easy integration of reStructuredText.

    This class is used to control the ReStructuredText integration to one
    or more Flask applications. Depending on how you initialize the
    object it  is usable right away or will attach as needed to a
    Flask application.

    There are two usage modes which work very similiar. One is binding
    the instance to a very specific Flask application::

        app = Flask(name)
        rst = ReStructuredText(app)

    The second possibility is to create the object once and configure the
    application later to support it::

        rst = ReStructuredText()

        def create_app():
            app = Flask(__name__)
            rst.init_app(app)
            return app

    """

    def __init__(self, app=None, writer='html', auto_escape=False,
                 directives=None, roles=None):
        self.writer = writer
        self.directives = directives
        self.roles = roles
        self.loaded_extensions = []
        self.auto_escape = auto_escape

        if app is not None:
            self.init_app(app, writer, auto_escape, directives, roles)

    def init_app(self, app, writer=None, auto_escape=False,
                 directives=None, roles=None):
        """
        Configure an application.

        This registers an jinja2 filter, and attaches this `ReStructuredText`
        to `app.extensions['rst']`.

        :param app: The :class:`flask.Flask` object configure.
        :type app: :class:`flask.Flask`
        :param writer: The :class:`docutils.writers.Writer` object to use.
            Defaults to :class:`docutils.writers.html4css1.Writer`.
        :type writer: :class:`docutils.writers.Writer`
        :param auto_escape:Whether to auto_escape. Defaults to ``False``.
        :type auto_escape: bool

        """

        self.app = app

        if not hasattr(self.app, 'extensions'):
            self.app.extensions = {}

        if writer is not None:
            self.writer = writer

        if self.writer == 'html5':
            from .writers.html5 import Writer as HTML5Writer
            self.writer = HTML5Writer()
        else:
            self.writer = HTMLWriter()

        if auto_escape is not None:
            self.auto_escape = auto_escape

        if directives is not None:
            self.directives = directives

        if roles is not None:
            self.roles = roles

        self.app.extensions['rst'] = self
        self.app.add_template_filter(self.__build_filter(self.auto_escape),
                                     name='rst')

        self.load_extensions(self.directives, 'directives')
        self.load_extensions(self.roles, 'roles')

    def __call__(self, stream):
        return publish_parts(stream, writer=self.writer)['html_body']

    def __build_filter(self, app_auto_escape):
        @evalcontextfilter
        def rst_filter(eval_ctx, stream):
            if app_auto_escape and eval_ctx.autoescape:
                return Markup(self(escape(stream)))
            else:
                return Markup(self(stream))
        return rst_filter

    def load_extensions(self, names, extension_type):

        if names is not None:
            if _multiple_names(names):
                for name in names:
                    self.load_extension(name, extension_type)
            else:
                self.load_extension(names, extension_type)

    def load_extension(self, name, extension_type):

        relative_name = ''.join(['.', '.'.join([extension_type, name])])
        absolute_name = resolve_name(relative_name, __package__)

        try:
            mod = import_module(absolute_name)
        except (ImportError, Exception) as e:
            print('Module {module} could not be loaded! {e}'.format(
                module=name, e=e))
            return

        if extension_type == 'directives':
            self.add_directive(mod.NAME)
        else:
            self.add_role(mod.NAME)

        if hasattr(mod, 'DEFAULT_CONFIG'):
            for config_name, value in mod.DEFAULT_CONFIG.items():
                self.app.config.setdefault(config_name, value)

        if hasattr(mod, 'CONTEXT_PROCESSOR'):
            self.app.context_processor(lambda: mod.CONTEXT_PROCESSOR)

        self.loaded_extensions.append(name)

    def add_directive(self, directive_class, name=None):
        """
        Register a directive.

        Works exactly like the :meth:`directive` decorator.

        If the directive_class is a mapping, the keys should be the
        name to register the role under and the value should be the
        class to use

        :param directive_class: The object or mapping to use.
        :param name: The name(s) to register the directive under.
            Defaults to the class name.
        :type name: str, list, tuple, set, frozenset

        """
        if isinstance(directive_class, Mapping):
            for name, directive in directive_class.items():
                self.add_directive(directive, name)

            return

        if _multiple_names(name):
            for directive_name in name:
                docutils_directives.register_directive(directive_name,
                                                       directive_class)
        else:
            docutils_directives.register_directive(
                name or directive_class.__name__, directive_class)

    def directive(self, name=None):
        """
        Decorator to register directives.

        You can specify a name for the directive, otherwise the class
        name will be used. Example::

            @rst.directive()
            class Image(Directive):

                required_arguments = 1
                optional_arguments = 0
                final_argument_whitespace = True
                option_spec = {'alt': directive unchanged,
                    'height': directives.nonnegative_int,
                    'width': directives.nonnegative_int,
                    'scale': directivs.nonnegative_int,
                    'align': align,
                    }
                has_content = False

                def run(self):
                    reference = directives.uri(self.arguments[0])
                    self.options['uri'] = reference
                    image_node = nodes.image(rawsource=self.block_text,
                        **self.options)
                    return [image_node]

        You can also register a directive under more names, by setting the
        name parameter to an iterable with names in it. Example::

            @rst.directive(names=['image', 'img'])
            class Image(Directive):
                ...

        :param name:The name(s) to register a directive under.
            Defaults to the class name.
        :type name: str, list, tuple, set, frozenset

        """
        def decorator(f):
            self.add_directive(f, name=name)
            return f
        return decorator

    def add_role(self, role_function, name=None):
        """
        Register a role.

        Works exactly like the :meth:`role` decorator.

        If the role_function is a mapping, the keys should be the
        name to register the role under and the value should
        be the function to use.

        :param role_function: The function or mapping to use.
        :param name: The name(s) to register the role under.
            Defaults to the function name.
        :type name: str, list, tuple, set, frozenset

        """

        if isinstance(role_function, Mapping):
            for name, role in role_function.items():
                self.add_role(role, name)

            return

        if _multiple_names(name):
            for role_name in name:
                docutils_roles.register_local_role(role_name, role_function)
        else:
            docutils_roles.register_local_role(
                name or role_function.__name, role_function)

    def role(self, name=None):
        """
        Decorator for registering roles.

        You can specify a name for the role, otherwise the function
        name will be used. Example::

            @rst.role()
            def rfc(role, rawtext, text, lineno, inliner,
                    options={}, content=[]):
                try:
                    rfcnum = int(text)
                    if rfcnum <= 0:
                        raise ValueError
                except ValueError:
                    msg = inliner.reporter.error(
                     'RFC number must be number greater than or equal to 1;'
                     '"%s" is invalid.' % text, line=lineno)
                    return [prb], [msg]
                # Base URL mainly used by inliner.rfc_reference, so this is
                # correct:
                ref = (inliner.document.settings.rfc_base_url + inliner.rfc_url
                        % rfcnum
                set_classes(options)
                node = nodes.reference(rawtext, 'RFC' + utils.unescape(text),
                                       refuri=uri, **options)
                return [node], []

        You can also register a role under more names, by setting the name
        parameter to an iterable with names in it. Example::

            @rst.role(name=['rfc', 'rfc-reference'])
            def rfc(role, rawtext, text, lineno, inliner,
                    options={}, content={}):
                ...

        :param name:The name(s) to register to role under.
            Defaults to the function name.
        :type name: str, list, tuple, set, frozenset

        """

        def decorator(f):
            self.add_role(f, name=name)
            return f
        return decorator
