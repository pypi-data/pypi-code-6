# -*- coding: utf-8 -*-

import sys
import os
import solar_theme

extensions = [
    'sphinx.ext.autodoc',
]

source_suffix = '.rst'

master_doc = 'index'

project = u'Sahuwai'

copyright = u'Teguh P. Alko'

version = '0.1'

release = '0.1'

exclude_patterns = ['build']

pygments_style = 'sphinx'

html_theme = 'solar_theme'

html_theme_path = [solar_theme.theme_path]

htmlhelp_basename = 'doc'

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

latex_documents = [
  ('index', 'rrda.tex', u'rrda Documentation',
   u'Author', 'manual'),
]

man_pages = [
    ('index', 'rrda', u'rrda Documentation',
     [u'Author'], 1)
]

texinfo_documents = [
  ('index', 'rrda', u'rrda Documentation',
   u'Author', 'rrda', 'One line description of project.',
   'Miscellaneous'),
]

epub_title = u'rrda'

epub_author = u'Author'

epub_publisher = u'Author'

epub_copyright = u'2014, Author'

epub_exclude_files = ['search.html']
