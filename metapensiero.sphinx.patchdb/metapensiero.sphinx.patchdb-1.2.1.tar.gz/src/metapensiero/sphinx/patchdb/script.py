# -*- coding: utf-8 -*-
# :Progetto:  PatchDB -- Implementation of docutils ``script`` directive
# :Creato il: Fri Oct  3 00:34:12 2003
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

from __future__ import absolute_import

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinx import addnodes
from sphinx.domains import Domain, ObjType
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_refnode

from .patch import MAX_PATCHID_LEN, make_patch, DependencyError


class Script(nodes.topic):
    pass

def visit_script_node(self, node):
    self.visit_topic(node)

def depart_script_node(self, node):
    self.depart_topic(node)


class ScriptContents(nodes.container):
    pass


class ScriptDirective(Directive):
    "Implementation of the ``script`` directive."

    # One mandatory argument, the script ID; an optional one, its title,
    # where spaces are allowed
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    # It has a content body
    has_content = True

    # Allowed options
    option_spec = {
        'always': lambda arg: directives.choice(arg, (
            'first',
            'last',
        )),
        'brings': directives.unchanged_required,
        'conditions': directives.unchanged_required,
        'depends': directives.unchanged_required,
        'description': directives.unchanged_required,
        'encoding': directives.encoding,
        'file': directives.path,
        'language': lambda arg: directives.choice(arg, (
            'python',
            'sql',
        )),
        'mimetype': lambda arg: directives.choice(arg, (
            'application/x-python',
            'application/x-python3',
            'text/x-mysql',
            'text/x-plpgsql',
            'text/x-postgresql',
            'text/x-python',
            'text/x-python3',
            'text/x-sql',
        )),
        'onerror': directives.unchanged_required,
        'preceeds': directives.unchanged_required,
        'revision': directives.nonnegative_int,
        }

    def run(self):
        """
        Implement ``script`` directive.

        The ``script`` directive introduces a piece of code that shall be
        executed on some target, taken from its body. This content gets
        beautified with `pygments` and inserted in the document tree as a
        ``raw`` node.

        The language of the script is mandatory, and must be specified as
        ``language`` in the `options` argument. Currently it can be one of
        following:

        - *python*
        - *sql*
        """

        name = self.name
        arguments = self.arguments
        lineno = self.lineno
        state = self.state
        document = state.document
        source = document.current_source
        env = document.settings.env

        if not arguments:
            error = document.reporter.error(
                u'Missing mandatory ID for the directive "%s".' % (name),
                line=lineno)
            return [error]

        scriptid = arguments[0].lower()
        options = self.options
        content = self.content

        if len(scriptid)>MAX_PATCHID_LEN:
            error = document.reporter.error(
                u'Script ID "%s" is too long, maximum allowed length'
                u' is %d characters!' % (scriptid, MAX_PATCHID_LEN),
                line=lineno)
            return [error]

        if u',' in scriptid:
            error = document.reporter.error(
                u'Commas are not allowed within a script ID: "%s"'
                % (scriptid,), line=lineno)
            return [error]

        if content and 'file' in options:
            error = document.reporter.error(
                u'Refuse to guess: both content and file option present in "%s"'
                % (scriptid,), line=lineno)
            return [error]

        if 'file' in options:
            from codecs import open
            from os import sep
            from os.path import dirname, normpath, join

            filename = options['file']
            if not document.settings.file_insertion_enabled:
                return [document.reporter.warning(u'File insertion disabled',
                                                  line=lineno)]
            if filename.startswith('/') or filename.startswith(sep):
                rel_fn = filename[1:]
            else:
                docdir = dirname(env.doc2path(env.docname, base=None))
                rel_fn = normpath(join(docdir, filename))

            try:
                fn = join(env.srcdir, rel_fn)
            except UnicodeDecodeError:
                # the source directory is a bytestring with non-ASCII
                # characters; let's try to encode the rel_fn in the
                # file system encoding
                from sys import getfilesystemencoding
                rel_fn = rel_fn.encode(getfilesystemencoding())
                fn = join(env.srcdir, rel_fn)

            encoding = self.options.get('encoding', env.config.source_encoding)
            try:
                f = open(fn, 'rU', encoding)
                text = f.read()
                f.close()
            except (IOError, OSError):
                return [document.reporter.warning(
                    'Include file %r not found or reading it failed' % filename,
                    line=lineno)]
            except UnicodeError:
                return [document.reporter.warning(
                    'Encoding %r used for reading included file %r seems to '
                    'be wrong, try giving an :encoding: option' %
                    (encoding, filename))]

            env.note_dependency(rel_fn)
        else:
            text = '\n'.join(content)

        if text:
            scripts = env.domaindata['patchdb']['scripts']

            patch = make_patch(scriptid, text, options,
                               description=arguments[0])
            patch.source = source
            patch.line = lineno

            # Insert the html version of the script in a raw node
            if scriptid in scripts and patch.checksum == scripts[scriptid]['patch'].checksum:
                htmltext = scripts[scriptid]['htmltext']
            else:
                try:
                    htmltext = patch.beautify()
                except ImportError:
                    htmltext = text

            html = nodes.raw(text, htmltext)
            html['format'] = 'html'

            caption = nodes.caption(scriptid, "Script ID: ")
            caption += nodes.strong(scriptid, u"“%s”" % scriptid)

            title_text = patch.description
            if patch.revision > 1:
                title_text += ' (revision %d)' % patch.revision
            text_nodes, messages = state.inline_text(title_text, lineno)
            title = nodes.title(title_text, '', *text_nodes)

            # Place a topic, that will be the target of the references
            # to this script
            topic = Script('', title, classes=["script"])
            topic['scriptid'] = scriptid
            topicid = nodes.make_id('script ' + scriptid)
            name = nodes.fully_normalize_name(caption.astext())
            if not state.document.has_name(name):
                topic['names'].append(name)
            topic['ids'] = [topicid]

            # Sanity check
            if scriptid in scripts and scripts[scriptid]['docname'] != env.docname:
                error = document.reporter.error(
                    u'Script ID "%s" in "%s" is not unique, there is one in "%s" too!' %
                    (scriptid, env.docname, scripts[scriptid]['docname']))
                return [error]

            if scriptid not in scripts or patch.checksum != scripts[scriptid]['patch'].checksum:
                scripts[scriptid] = dict(
                    patch=patch, htmltext=htmltext, docname=env.docname)

            if patch.description != scriptid:
                topic += caption

            topic += html

            indexnode = addnodes.index()
            indexnode['entries'] = [('single', scriptid, topicid, name)]

            return [indexnode, topic]
        else:
            return []


class ScriptContentsDirective(Directive):
    "Implementation of the ``scriptcontents`` directive."

    has_content = False
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'class': directives.class_option,
        'local': directives.flag,
        }

    def run(self):
        arguments = self.arguments
        options = self.options
        lineno = self.lineno
        state = self.state

        document = state.document

        if arguments:
            title_text = arguments[0]
            text_nodes, messages = state.inline_text(title_text, lineno)
            title = nodes.title(title_text, '', *text_nodes)
        else:
            if options.has_key('local'):
                title = None
            else:
                title = nodes.title('', 'Script index')

        topic = nodes.topic(classes=['contents'])

        cls = options.get('class')
        if cls:
            topic.set_class(cls)

        if title:
            name = title.astext()
            topic += title
        else:
            name = 'Scripts'

        name = nodes.fully_normalize_name(name)
        if not document.has_name(name):
            topic['names'].append(name)
        document.note_implicit_target(topic)

        contents = ScriptContents()
        contents.local = options.has_key('local')
        contents.docname = document.settings.env.docname

        topic += contents

        return [topic]


def add_scripts_crossrefs(app, doctree, fromdocname):
    env = app.builder.env

    scripts = env.domaindata['patchdb']['scripts']
    if not scripts:
        return

    get_relative_uri = app.builder.get_relative_uri

    def add_detail(dlist, detname, detvalue):
        if detvalue:
            item = nodes.definition_list_item()
            term = nodes.term('', detname)
            if len(detvalue)>1:
                value = nodes.bullet_list()
                for v in detvalue:
                    sid, rev = v
                    try:
                        docname = scripts[sid]['docname']
                    except KeyError:
                        raise DependencyError(sid)
                    refid = nodes.make_id("script " + sid)
                    refuri = get_relative_uri(fromdocname, docname) + '#' + refid
                    li = nodes.list_item()
                    ref = nodes.paragraph('', '')
                    reftxt = sid
                    if rev is not None:
                        reftxt += ' (revision %d)' % rev
                    ref += nodes.reference('', reftxt, refid=refid, refuri=refuri)
                    li += ref
                    value += li
            else:
                sid, rev = detvalue[0]
                try:
                    docname = scripts[sid]['docname']
                except KeyError:
                    raise DependencyError(sid)
                refid = nodes.make_id("script " + sid)
                refuri = get_relative_uri(fromdocname, docname) + '#' + refid
                value = nodes.paragraph('', '')
                reftxt = sid
                if rev is not None:
                    reftxt += ' (revision %d)' % rev
                value += nodes.reference('', reftxt, refid=refid, refuri=refuri)
            defn = nodes.definition('', value)
            item += term
            item += defn

            dlist += item

    # Add scripts details
    for node in doctree.traverse(Script):
        patch = scripts[node['scriptid']]['patch']

        dlist = nodes.definition_list()

        try:
            add_detail(dlist, 'depends on', patch.depends)
            add_detail(dlist, 'preceeds', patch.preceeds)
            add_detail(dlist, 'brings', patch.brings)
        except DependencyError as e:
            raise DependencyError(u'%s (defined in %s at line %s)'
                                  u' references an unknown script "%s"'
                                  % (patch, patch.source, patch.line, e))

        if patch.conditions:
            item = nodes.definition_list_item()
            if len(patch.conditions)>1:
                item += nodes.term('', 'conditions')
                clist = nodes.bullet_list()
                for c in patch.conditions:
                    li = nodes.list_item()
                    li += nodes.paragraph('', c)
                    clist += li
                item += nodes.definition('', clist)
            else:
                item += nodes.term('', 'condition')
                item += nodes.definition('', nodes.paragraph('', patch.conditions[0]))
            dlist += item

        if patch.always:
            item = nodes.definition_list_item()
            item += nodes.term('', 'execute always')
            if patch.always == 'first':
                value = nodes.paragraph('', "Before any other script")
            elif patch.always == 'last':
                value = nodes.paragraph('', "After any other script")
            else:
                value = nodes.paragraph('', patch.always)
            item += nodes.definition('', value)
            dlist += item

        if patch.onerror != 'abort':
            item = nodes.definition_list_item()
            item += nodes.term('', 'errors policy')
            if patch.onerror == 'skip':
                value = nodes.paragraph('', "Go on with the next script,"
                                        " skipping any succeding statement"
                                        " of the failing script")
            elif patch.onerror == 'ignore':
                value = nodes.paragraph('', "Ignore the error and keeps going"
                                        " with the remaining statements in the"
                                        " script")
            else:
                value = nodes.paragraph('', patch.onerror)
            item += nodes.definition('', value)
            dlist += item

        node += dlist

    # Fill script indexes
    sids = scripts.keys()
    sids.sort()

    for node in doctree.traverse(ScriptContents):
        entries = []
        for sid in sids:
            docname = scripts[sid]['docname']
            if node.local and node.docname != docname:
                continue
            patch = scripts[sid]['patch']
            refid = nodes.make_id("script " + sid)
            refuri = get_relative_uri(fromdocname, docname) + '#' + refid
            ref = nodes.reference('', patch.description,
                                  refdocname=docname,
                                  refid=refid,
                                  refuri=refuri)
            entry = nodes.paragraph('', '', ref)
            item = nodes.list_item('', entry)
            entries.append(item)
        if entries:
            node.replace_self(nodes.bullet_list('', *entries))


def mark_as_dirty(app, env):
    "Mark the script collection as dirty, will be dumped at end."

    app.patchdb_dump_scripts = True


def dump_scripts_collection(app, env):
    "Dump the collected scripts into a new pickle archive."

    from .manager import patch_manager

    scripts = env.domaindata['patchdb']['scripts']
    if not scripts or not app.config.patchdb_storage:
        return

    if not getattr(app, 'patchdb_dump_scripts', False):
        return

    mgr = patch_manager(app.config.patchdb_storage, overwrite=True)
    for sid in scripts:
        mgr[sid] = scripts[sid]['patch']
    mgr.save()


def purge_doc(app, env, docname):
    "Remove references to scripts defined in purged document."

    scripts = env.domaindata['patchdb']['scripts']
    if not scripts:
        return

    obsolete_ids = [sid for sid in scripts if scripts[sid]['docname']==docname]
    for sid in obsolete_ids:
        del scripts[sid]


class ScriptRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        refnode['patchdb:script'] = target
        title, target = super(ScriptRole, self).process_link(
            env, refnode, has_explicit_title, title, target)
        target = nodes.make_id("script " + target)
        return title, target


class PatchDBDomain(Domain):
    name = 'patchdb'
    label = 'PatchDB'

    object_types = {
        'script': ObjType('script', 'script'),
    }

    directives = {
        'script': ScriptDirective,
        'scriptcontents': ScriptContentsDirective,
    }

    roles = {
        'script': ScriptRole(lowercase=True),
    }

    data_version = 1
    initial_data = {'scripts': {}}

    def get_objects(self):
        for scriptid, script in self.data['scripts'].iteritems():
            yield (scriptid, script['patch'].description, 'script',
                   script['docname'], scriptid, 1)

    def resolve_xref(self, env, fromdocname, builder, type, target, node, contnode):
        ref = node.get('patchdb:script')
        script = self.data['scripts'].get(ref)
        if script:
            return make_refnode(builder, fromdocname, script['docname'], target,
                                contnode, script['patch'].description)
        else:
            env.warn_node('Reference to an unknown script: %r' % ref, node)


def setup(app):
    app.add_domain(PatchDBDomain)

    app.add_node(Script,
                 html=(visit_script_node, depart_script_node),
                 latex=(visit_script_node, depart_script_node),
                 text=(visit_script_node, depart_script_node))
    app.add_node(ScriptContents)

    app.connect('env-purge-doc', purge_doc)
    app.connect('env-updated', dump_scripts_collection)
    app.connect('doctree-read', mark_as_dirty)
    app.connect('doctree-resolved', add_scripts_crossrefs)
