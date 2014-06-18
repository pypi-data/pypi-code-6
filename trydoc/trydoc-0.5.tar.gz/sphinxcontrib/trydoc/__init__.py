# -*- coding: utf-8 -*-
"""
    trydoc
    ------

    :copyright: Copyright 2012-14 by NaN Projectes de Programari Lliure, S.L.
    :license: BSD, see LICENSE for details.
"""
from path import path
import ConfigParser
import os
import re
import sys
import tempfile

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Image
from docutils.transforms import Transform
from sphinx.util.compat import Directive

import proteus
import tryton
try:
    import gtk
    import gobject
except ImportError, e:
    print >> sys.stderr, ("gtk importation error (%s). Screenshots feature "
        "will not be available.") % e
    gtk = None
    gobject = None


screenshot_files = []


def get_field_data(model_name, field_name, show_help):
    if not proteus.config._CONFIG.current:
        raise ValueError('Proteus has not been initialized.')

    Model = proteus.Model.get('ir.model')
    models = Model.find([
            ('model', '=', model_name),
            ])
    if not models:
        return None

    ModelField = proteus.Model.get('ir.model.field')
    field = ModelField.find([
            ('name', '=', field_name),
            ('model', '=', models[0].id),
            ])[0]

    text = ''
    for field in models[0].fields:
        if field.name == field_name:
            if show_help:
                if field.help:
                    text = field.help
                else:
                    text = 'Field "%s" has no help available' % field.name
            else:
                if field.field_description:
                    text = field.field_description
                else:
                    text = ('Field "%s" has no description available'
                        % field.name)
            break

    return text


def get_ref_data(module_name, fs_id, field=None):
    if not proteus.config._CONFIG.current:
        raise ValueError('Proteus has not been initialized.')
    ModelData = proteus.Model.get('ir.model.data')

    records = ModelData.find([
            ('module', '=', module_name),
            ('fs_id', '=', fs_id),
            ])
    if not records:
        return None

    db_id = records[0].db_id
    # model cannot be unicode
    model = str(records[0].model)

    Model = proteus.Model.get(model)
    record = Model(db_id)
    if field:
        return getattr(record, field)
    return record


class FieldDirective(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'help': directives.flag,
        'class': directives.class_option,
        }

    def run(self):
        config = self.state.document.settings.env.config
        if 'help' in self.options:
            show_help = True
        else:
            show_help = False
        classes = [config.trydoc_fieldclass]
        if 'class' in self.options:
            classes.extend(self.options['class'])

        content = self.arguments[0]
        model_name, field_name = content.split('/')
        text = get_field_data(model_name, field_name, show_help)
        if text is None:
            return [self.state_machine.reporter.warning(
                    'Model "%s" not found.' % model_name, line=self.lineno)]

        return [nodes.inline(text, text, classes=classes)]


class TryRefDirective(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'class': directives.class_option,
        }

    def run(self):
        config = self.state.document.settings.env.config
        classes = [config.trydoc_refclass]
        if 'class' in self.options:
            classes.extend(self.options['class'])

        content = self.arguments[0]
        ref, field = content.split('/')
        module_name, fs_id = ref.split('.')

        text = get_ref_data(module_name, fs_id, field)
        if text is None:
            return [self.state_machine.reporter.warning(
                    'Reference "%s" not found.' % content, line=self.lineno)]

        return [nodes.inline(text, text, classes=classes)]


class ViewDirective(Image):
    option_spec = Image.option_spec.copy()
    option_spec.update({
        'field': directives.unchanged,
        'class': directives.class_option,
        })
    tryton_main = None
    filename = None

    def run(self):
        assert gtk is not None, "gtk not imported"
        assert gobject is not None, "gobject not imported"

        config = self.state.document.settings.env.config
        if 'class' in self.options:
            self.options['class'].insert(0, config.trydoc_viewclass)
        else:
            self.options['class'] = [config.trydoc_viewclass]

        view_xml_id = str(self.arguments[0])
        field_name = self.options.get('field')

        tryton_main = ViewDirective.get_tryton_main()

        url = self.calc_url(view_xml_id, field_name)

        source_document_path = path(self.state.document.current_source)
        prefix = 'screenshot-' + source_document_path.basename().split('.')[0]
        _, self.filename = tempfile.mkstemp(prefix=prefix,
            suffix='.png', dir=source_document_path.parent)

        self.screenshot(tryton_main, url)
        screenshot_files.append(self.filename)

        # if app.config.verbose:
        sys.stderr.write("Screenshot %s in tempfile %s"
            % (url, self.filename))
        self.arguments[0] = path(self.filename).basename()
        image_node_list = Image.run(self)
        return image_node_list

    @classmethod
    def get_tryton_main(cls):
        if cls.tryton_main is not None:
            return cls.tryton_main

        tryton_main = tryton.gui.Main(cls)

        cls.tryton_main = tryton_main
        return tryton_main

    @classmethod
    def sig_login(cls, tryton_main):
        # tryton.rpc.context_reload()
        prefs = tryton.common.RPCExecute('model', 'res.user',
            'get_preferences', False)
        tryton.common.ICONFACTORY.load_icons()
        tryton.common.MODELACCESS.load_models()
        tryton.common.VIEW_SEARCH.load_searches()
        if prefs and 'language_direction' in prefs:
            tryton.translate.set_language_direction(
                prefs['language_direction'])
        tryton_main.sig_win_menu(prefs=prefs)
        tryton_main.set_title(prefs.get('status_bar', ''))
        if prefs and 'language' in prefs:
            tryton.translate.setlang(prefs['language'], prefs.get('locale'))
            tryton_main.set_menubar()
            tryton_main.favorite_unset()
        tryton_main.favorite_unset()
        tryton_main.menuitem_favorite.set_sensitive(True)
        tryton_main.menuitem_user.set_sensitive(True)
        return True

    def calc_url(self, view_xml_id, field_name=None):
        module_name, fs_id = view_xml_id.split('.')
        view = get_ref_data(module_name, fs_id)

        # TODO: Hack to get some ID of view model
        Model = proteus.Model.get(view.model)
        record, = Model.find([], limit=1)

        return 'tryton://localhost:8000/%s/model/%s/%d' % (
            proteus.config._CONFIG.current.database_name, view.model,
            record.id)

    def screenshot(self, tryton_main, url):
        config = self.state.document.settings.env.config
        proteus_instance = proteus.config._CONFIG.current

        trytond_config = ConfigParser.ConfigParser()
        with open(proteus_instance.config_file, 'r') as f:
            trytond_config.readfp(f)
        trytond_port = (trytond_config.get('options', 'jsonrpc').split(':')[1]
            if (trytond_config.get('options', 'jsonrpc', False) and
                len(trytond_config.get('options', 'jsonrpc').split(':')) == 2)
            else 8000)

        # Now, it only works with local instances because it mixes RPC calls
        # and trytond module importation
        tryton.rpc.login('admin', config.trytond_admin_password, 'localhost',
            int(trytond_port), proteus_instance.database_name)
        # TODO: put some wait because sometimes the login window is raised
        ViewDirective.sig_login(tryton_main)

        # Use: tryton://localhost/test/model/party.party
        tryton_main.open_url(url)
        gobject.timeout_add(6000, self.drawWindow, tryton_main.window)
        gtk.main()
        return True

    def drawWindow(self, win):
        # Code below from:
        # http://stackoverflow.com/questions/7518376/creating-a-screenshot-of-a-gtk-window
        # More info here:
        # http://burtonini.com/computing/screenshot-tng.py

        width, height = win.get_size()
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width,
            height)

        # Retrieve the pixel data from the gdk.window attribute (win.window)
        # of the gtk.window object
        screenshot = pixbuf.get_from_drawable(win.window, win.get_colormap(),
            0, 0, 0, 0, width, height)

        screenshot.save(self.filename, 'png')
        tryton.rpc.logout()
        gtk.main_quit()
        # Return False to stop the repeating interval
        return False


class References(Transform):
    """
    Parse and transform tryref and field references in a document.
    """

    default_priority = 999

    def apply(self):
        config = self.document.settings.env.config
        pattern = config.trydoc_pattern
        if isinstance(pattern, basestring):
            pattern = re.compile(pattern)
        for node in self.document.traverse(nodes.Text):
            parent = node.parent
            if isinstance(parent, (nodes.literal, nodes.FixedTextElement)):
                # ignore inline and block literal text
                continue
            text = unicode(node)
            modified = False

            match = pattern.search(text)
            while match:
                if len(match.groups()) != 1:
                    raise ValueError(
                        'trydoc_issue_pattern must have '
                        'exactly one group: {0!r}'.format(match.groups()))
                # extract the reference data (excluding the leading dash)
                refdata = match.group(1)
                start = match.start(0)
                end = match.end(0)

                data = refdata.split(':')
                kind = data[0]
                content = data[1]
                if len(data) > 2:
                    options = data[2]
                else:
                    options = None

                if kind == 'field':
                    model_name, field_name = content.split('/')
                    if options == 'help':
                        show_help = True
                    else:
                        show_help = False
                    replacement = get_field_data(model_name, field_name,
                        show_help)
                elif kind == 'tryref':
                    ref, field = content.split('/')
                    module_name, fs_id = ref.split('.')
                    replacement = get_ref_data(module_name, fs_id, field)
                else:
                    replacement = refdata

                text = text[:start] + replacement + text[end:]
                modified = True

                match = pattern.search(text)

            if modified:
                parent.replace(node, [nodes.Text(text)])


def init_transformer(app):
    if app.config.trydoc_plaintext:
        app.add_transform(References)
    if (app.config.trydoc_modules and
            proteus.config._CONFIG.current.database_name == ':memory:'):
        module_model = proteus.Model.get('ir.module.module')
        modules_to_install = []
        for module_to_install in app.config.trydoc_modules:
            res = module_model.find([('name', '=', module_to_install)])
            # if app.config.verbose:
            sys.stderr.write("Module found with name '%s': %s.\n"
                    % (module_to_install, res))
            if res:
                modules_to_install.append(res[0].id)
        if modules_to_install:
            proteus_context = proteus.config._CONFIG.current.context
            # if app.config.verbose:
            sys.stderr.write("It will install the next modules: %s with "
                    "context %s.\n" % (modules_to_install,
                                proteus_context))
            module_model.install(modules_to_install, proteus_context)
        proteus.Wizard('ir.module.module.install_upgrade').execute('upgrade')


def remove_temporary_files(app, exception):
    for filename in screenshot_files:
        if os.path.exists(filename):
            os.remove(filename)


def setup(app):
    app.add_config_value('trydoc_plaintext', True, 'env')
    app.add_config_value('trydoc_pattern', re.compile(r'@(.|[^@]+)@'), 'env')
    app.add_config_value('trydoc_fieldclass', 'trydocfield', 'env')
    app.add_config_value('trydoc_refclass', 'trydocref', 'env')
    app.add_config_value('trydoc_viewclass', 'trydocview', 'env')
    app.add_config_value('trydoc_modules', [], 'env')
    app.add_config_value('trytond_admin_password', 'admin', 'env')
    # app.add_config_value('verbose', False, 'env'),

    app.add_directive('field', FieldDirective)
    app.add_directive('tryref', TryRefDirective)
    app.add_directive('view', ViewDirective)

    app.connect(b'builder-inited', init_transformer)
    app.connect(b'build-finished', remove_temporary_files)
