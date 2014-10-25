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

__version__ = "1.1.0"


# mathjax_script_template
MATHJAX = r"""
if (!document.getElementById('mathjaxscript_pelican_#%@#$@#')) {{
    var mathjaxscript = document.createElement('script');
    mathjaxscript.id = 'mathjaxscript_pelican_#%@#$@#';
    mathjaxscript.type = 'text/javascript';
    mathjaxscript.src = {source};
    mathjaxscript[(window.opera ? "innerHTML" : "text")] =
        "MathJax.Hub.Config({{" +
        "    config: ['MMLorHTML.js']," +
        "    TeX: {{" +
        "          extensions: ['AMSmath.js','AMSsymbols.js','noErrors.js','noUndefined.js'], " +
        "          equationNumbers: {{ autoNumber: 'AMS' }}," +
        "          Macros: {{{macros}}}," +
        "    }}," +
        "    jax: ['input/TeX','input/MathML','output/HTML-CSS']," +
        "    extensions: ['tex2jax.js','mml2jax.js','MathMenu.js','MathZoom.js']," +
        "    displayAlign: '{align}'," +
        "    displayIndent: '{indent}'," +
        "    showMathMenu: {show_menu}," +
        "    tex2jax: {{ " +
        "        inlineMath: [ ['\\\\(','\\\\)'] ], " +
        "        displayMath: [ ['$$','$$'] ]," +
        "        processEscapes: {process_escapes}," +
        "        preview: '{latex_preview}'," +
        "    }}, " +
        "    'HTML-CSS': {{ " +
        "        styles: {{ '.MathJax_Display, .MathJax .mo, .MathJax .mi, .MathJax .mn': {{color: '{color} ! important'}} }}" +
        "    }} " +
        "}}); ";
    (document.body || document.getElementsByTagName('head')[0]).appendChild(mathjaxscript);
}}
"""
MACROS = r"""
trace: "\\operatorname{tr}",
diag: "\\operatorname{diag}",
abs: "\\operatorname{abs}",
opt: "\\operatorname{opt}",
dd:    "\\, \\textnormal{d}",
Op:   ["{\\boldsymbol{\\mathsf{\\hat{#1}}}}", 1],
op:   ["{\\boldsymbol{\\mathsf{\\hat{#1}}}}", 1],
Ket:  ["{\\left\\vert#1\\right\\rangle}", 1],
bra:  ["{\\left\\langle#1\\right\\vert}", 1],
Bra:  ["{\\left\\langle#1\\right\\vert}", 1],
ket:  ["{\\left\\vert#1\\right\\rangle}", 1],
Norm: ["{\\lVert#1\\rVert}", 1],
"""
mathjax_settings = {}
mathjax_settings['align'] = 'center'  # controls alignment of of displayed equations (values can be: left, right, center)
mathjax_settings['indent'] = '0em'  # if above is not set to 'center', then this setting acts as an indent
mathjax_settings['show_menu'] = 'true'  # controls whether to attach mathjax contextual menu
mathjax_settings['process_escapes'] = 'true'  # controls whether escapes are processed
mathjax_settings['latex_preview'] = 'TeX'  # controls what user sees while waiting for LaTex to render
mathjax_settings['color'] = 'black'  # controls color math is rendered in
mathjax_settings['source'] = "'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'"
mathjax_settings['macros'] = " ".join(MACROS.split("\n")).replace('\\', '\\\\').replace('"', '\\"')

config = {}
config['mathjax_script'] = MATHJAX.format(**mathjax_settings)
config['math_tag_class'] = 'math'

MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', 'headerid', 'toc',
                 'meta', PelicanMathJaxExtension(config) ]


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<title>{title}</title>
<style>
{style}
</style>
<meta charset="utf-8">
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
    if "title" in mkd.Meta:
        title = mkd.Meta['title'][0]
        mainheader = "<h1>" + title + "</h1>"
    if snippet:
        outfile.write(html)
    else:
        html = TEMPLATE.format(body=html, title=title,
                               mainheader=mainheader, style=CSS['bootstrap'])
        outfile.write(html)
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

