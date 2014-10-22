# flake8: noqa

# Generic tasks
from .basics import dump, glob, log, noop, sync, walk, write
from .files import directory, rename_replace, strip_dirs
from .filters import exclude, match
from .text import concat, contents_replace, footer, header, regex

# Specific tasks
from .angular import ng_annotate, ng_min, ng_template_cache
from .css import autoprefixer, cleancss, lessc
from .gzip import gzip
from .html import minify_html
from .javascript import coffee, traceur, uglify
from .markdown import markdown
from .png import optipng, pngquant
from .textile import textile
from .web import cachebust
