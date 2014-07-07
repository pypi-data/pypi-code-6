import posixpath as posixp

from docutils import nodes, utils
from docutils.parsers.rst.roles import register_canonical_role, set_classes


def wiki_page_reference_role(role, rawtext, text, lineno, inliner,
                             options={}, content=[]):
    text = text.strip()
    try:
        wikipath, rest = text.split(u':', 1)
    except:
        wikipath, rest = text, text
    context = inliner.document.settings.context # VersionContent instance
    if not (context.cw_etype == 'VersionContent'
            and context.repository.reverse_content_repo):
        return [nodes.Text(rest)], []
    vcwiki = context.repository.reverse_content_repo[0]
    # Allow users to link to a page with file extension
    ext = '.' + vcwiki.content_file_extension
    if wikipath.endswith(ext):
        wikipath = wikipath[:-len(ext)]
    # Return url and markup options
    if not wikipath.startswith('/'):
        vcpath = posixp.join(context.content_for[0].directory, wikipath)
    else:
        vcpath = wikipath[1:]
    vcpath = posixp.normpath(vcpath)
    set_classes(options)
    if vcwiki.content(vcwiki.vcpage_path(vcpath)) is None:
        options['classes'] = ['doesnotexist']
    else:
        options.pop('classes', None)
    return [nodes.reference(rawtext, utils.unescape(rest),
                            refuri=vcwiki.page_url(vcpath),
                            **options)], []


register_canonical_role('wiki', wiki_page_reference_role)
