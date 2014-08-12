# flake8: noqa

# Generic tasks
from .basics import dump, glob, log, noop, sync, walk, write
from .filters import exclude, match
from .files import rename_replace, strip_dirs
from .text import concat, contents_replace, footer, header, regex

# Specific tasks
from .gzip import gzip
from .angular import ng_annotate, ng_min, ng_template_cache
from .css import autoprefixer, cleancss, lessc
from .html import minify_html
from .javascript import coffee, traceur, uglify
from .web import cachebust
