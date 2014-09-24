"""
Sphinx/docutils extension to create links to the SeqAn dox documentation using
a RestructuredText interpreted text role that looks like this:

    :dox:`seqan_link_text`

for example:

    :dox:`StringSet`

creates a link to the documentation entry of the Index class.

adapted from the traclinks extension.
"""

import urllib
from docutils import nodes, utils

def makeSeqAnLink(name, rawtext, text, lineno, inliner,
                  options={}, content=[]):
    env = inliner.document.settings.env
    dox_url = env.config.doxlinks_base_url
    tokens = text.split()
    target = tokens[0]
    text = tokens[0]
    if len(tokens) > 1:
      text = ' '.join(tokens[1:])
    ref = dox_url + '?p=' + urllib.quote(target, safe='')
    node = nodes.reference(rawtext, utils.unescape(text), refuri=ref, **options)
    return [node],[]


# setup function to register the extension

def setup(app):
    app.add_config_value('doxlinks_base_url',
                         'http://docs.seqan.de/seqan/dev3/',
                         'env')
    app.add_role('dox', makeSeqAnLink)

