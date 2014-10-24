"""
Personalized Markdown converter.

Converts markdown files to html, using the `codehilite`,
`extra`, `headerid`, `toc`, `meta`, and most importantly the Pelican
render_math extensions. The generated html page loads MathJax and is formatted
using bootstrap CSS, matching the formatting on <michaelgoerz.net>
"""
import os
import sys
import codecs
from optparse import OptionParser

import markdown
from mgmarkdown.pelican_mathjax_markdown_extension \
    import PelicanMathJaxExtension
from mgmarkdown.css import CSS

__version__ = "1.0.0"

PELICAN_CONFIG = {}

MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', 'headerid', 'toc',
                 'meta', PelicanMathJaxExtension(PELICAN_CONFIG) ]

MATHJAX = r"""
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    extensions: ['tex2jax.js','mml2jax.js','MathMenu.js','MathZoom.js'],
    jax: ["input/TeX", "output/HTML-CSS"],
    displayAlign: '{align}',
    displayIndent: '{indent}',
    tex2jax: {
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
      processEscapes: true
    },
    "HTML-CSS": { availableFonts: ["TeX"] }
  });
</script>
<script type="text/javascript"
  src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<title>{title}</title>
<style>
{style}
</style>
<meta charset="utf-8">
{mathjax}
</head>
<body>

<div class="container">
<div class="row">
<div class="col-sm-9">
{mainheader}
{body}
</div>
</div>
</div>

</body>
</html>
"""

def convert(infile, outfile=None, snippet=False):
    """
    Read markdown from infile (or stdin if infile is '--'), convert it to HTML,
    and write it to the given outfile, or stdout if no outfile is given. Both
    input and output are assumed to be encoded in UTF-8.
    """
    if infile == '--':
        infile = os.sys.stdin
    else:
        infile = codecs.open(infile, "r", "utf-8")
    if outfile is None:
        outfile = os.sys.stdout
    else:
        outfile = codecs.open(outfile, "w", "utf-8")
    mkd = markdown.Markdown(extensions=MD_EXTENSIONS)
    html = mkd.convert(infile.read())
    title = ""
    mainheader = ""
    if mkd.Meta.has_key("title"):
        title = mkd.Meta['title'][0]
        mainheader = "<h1>" + title + "</h1>"
    if snippet:
        outfile.write(html)
    else:
        outfile.write(TEMPLATE.format(body=html, title=title,
                      mainheader=mainheader, mathjax=MATHJAX,
                      style=CSS['bootstrap']
                     ))
    infile.close()
    outfile.close()


def main(argv=None):
    """
    Main routine
    """
    if argv is None:
        argv = sys.argv
    arg_parser = OptionParser(
    usage = "usage: %prog [options] [infile|--] [outfile]",
    description = __doc__)
    arg_parser.add_option(
        '--snippet', action='store_true', dest='snippet',
        default=False, help="Do not write a full HTML page")
    options, args = arg_parser.parse_args(argv)
    if len(args) > 1:
        infile = args[1]
        try:
            outfile = args[2]
        except IndexError:
            outfile = None
        convert(infile, outfile, options.snippet)
    else:
        arg_parser.print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())

