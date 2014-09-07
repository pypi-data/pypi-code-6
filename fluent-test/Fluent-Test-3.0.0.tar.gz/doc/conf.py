# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sphinx_rtd_theme

import fluenttest


needs_sphinx = '1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]
source_suffix = '.rst'
master_doc = 'index'
project = 'Fluent Test'
copyright = '2013, 2014, Dave Shawley'

# The short X.Y version.
version = '.'.join(str(x) for x in fluenttest.version_info[:2])
# The full version, including alpha/beta/rc tags.
release = fluenttest.__version__

exclude_patterns = []
pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True

htmlhelp_basename = 'FluentTestdoc'

latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
}

latex_documents = [
    ('index', 'FluentTest.tex', 'Fluent Test Documentation',
     'Dave Shawley', 'manual'),
]

texinfo_documents = [
    ('index', 'FluentTest', 'Fluent Test Documentation',
     'Dave Shawley', 'FluentTest', 'One line description of project.',
     'Miscellaneous'),
]

intersphinx_mapping = {
    'python': ('http://docs.python.org/', None),
    'mock': ('http://mock.readthedocs.org/en/latest/', None),
}
