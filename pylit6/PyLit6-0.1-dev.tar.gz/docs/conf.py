import re
import os
import sys
import sphinx_bootstrap_theme

sys.path.insert(0,'..')
import pylit6.__about__ as about
version = about.__version__
author = about.__author__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
]
if os.getenv('SPELLCHECK'):
    extensions += 'sphinxcontrib.spelling',
    spelling_show_suggestions = True,
    spelling_lang = 'en_US'

source_suffix = '.rst'
master_doc = 'index'
project = u'PyLit6'
copyright = u'2014, %s' % author
version = release = version
today_fmt = '%B %d, %Y'

html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_htmlhtml_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_theme_options = {
    'navbar_title': "PyLit",
    'navbar_site_name': "PyLit",
    'navbar_pagenav_name': "Page",
    'globaltoc_depth': 2,
    'navbar_class': "navbar navbar-inverse",
    'navbar_fixed_top': "true",
    'navbar_sidebarrel': True,
    'source_link_position': "nav",
    'bootswatch_theme': "flatly",
    'bootstrap_version': "3",
    }
html_sidebars = {'sidebar': ['localtoc.html', 'sourcelink.html', 'searchbox.html']}
html_title = "PyLit6 - LP using RST"
html_short_title = ""
#html_logo = 'ACClogo.png'
html_static_path = ['_static']
html_last_updated_fmt = '%b %d, %Y'
html_show_sourcelink = False
html_show_sphinx = True
html_show_copyright = True

