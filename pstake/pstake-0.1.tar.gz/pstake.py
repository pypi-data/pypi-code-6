#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2014, Yung-Yu Chen <yyc@solvcon.net>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the SOLVCON nor the names of its contributors may be
#   used to endorse or promote products derived from this software without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Convert a pstricks LaTeX file (.tex) to an image file."""


import sys
import os
import glob
import contextlib
import argparse


__version__ = "0.1"


@contextlib.contextmanager
def remember_cwd():
    """
    FIXME: I am not used.
    """
    curdir = os.getcwd()
    try:
        yield
    finally:
        os.chdir(curdir)


class Command(object):
    def __init__(self, command, prefix_path=None):
        self.command = command
        self.prefix_path = prefix_path

    def __call__(self, *args):
        param = " ".join(args)
        with remember_cwd():
            if self.prefix_path:
                os.chdir(self.prefix_path)
            cmd = " ".join([self.command, param])
            sys.stdout.write(cmd + '\n')
            sys.stdout.flush()
            os.system(cmd)


_TEX_TEMPLATE = r'''\documentclass[%sletterpaper,dvips]{article}
\usepackage[usenames]{color}
\usepackage{pst-all}
\usepackage{pst-3dplot}
\usepackage{pst-eps}
\usepackage{pst-coil}
\usepackage{pst-bar}
\usepackage{multido}
\usepackage{cmbright}
\usepackage{fancyvrb}
\begin{document}
\pagestyle{empty}
\begin{TeXtoEPS}
%s
\end{TeXtoEPS}
\end{document}'''


class Pstricks(object):
    def __init__(self, verbosity=3, keep_tmp=False, **kw):
        self.verbosity = verbosity
        self.keep_tmp = keep_tmp
        self.tmp_main = 'makeeps_tmp'
        self.tex_template = _TEX_TEMPLATE
        self.cmd_latex = Command("latex")
        self.cmd_dvips = Command("dvips")
        self.cmd_convert = Command("convert")

    def pst(self, src, dst, options=None):
        # Sanitize options.
        options = ','.join([] if None is options else options)
        if options:
            options += ','
        # Prepare TeX data.
        tex = self.tex_template % (options, open(src).read())
        tmpf = open(self.tmp_main+'.tex', 'w').write(tex)
        self.cmd_latex(self.tmp_main+'.tex')
        self.cmd_dvips(self.tmp_main+'.dvi', '-E -o %s' % dst)
        if not self.keep_tmp:
            for fn in glob.glob(self.tmp_main+'.*'):
                os.unlink(fn)

    def imconvert(self, src, dst, dpi=300):
        self.cmd_convert('-density %d -units PixelsPerInch %s %s' % (
            dpi, src, dst))

    def __call__(self, src, dstmain=None, dstext='.png'):
        # Sanitize file names.
        srcmain = os.path.splitext(src)[0]
        dstmain = srcmain if not dstmain else dstmain
        # Convert.
        if dstext in ('.eps', '.png'):
            self.pst(src, dstmain+'.eps')
            if dstext == '.png':
                self.imconvert(dstmain+'.eps', dstmain+'.png')
                if not self.keep_tmp:
                    os.unlink(dstmain+'.eps')
        else:
            sys.stdout.write("Destination file type %s isn't supported.\n" %
                             dstext)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-V', '--version', action='version',
                        version='%%(prog)s %s' % __version__)
    parser.add_argument('src', type=str,
                        help='source file name')
    parser.add_argument('dst', type=str, nargs='?', default=None,
                        help='destination file name')
    parser.add_argument('-k', dest='keep_tmp', action='store_true',
                        default=False,
                        help='keep temporary files')
    parser.add_argument('-t', dest='dstext', type=str, action='store',
                        default='.png',
                        help='destination file type '
                             '(default = %(default)s)')
    parser.add_argument('-v', '--verbose', dest='verbosity', action='store',
                        type=int, default=3,
                        help='verbosity of output (1-5) '
                             '(default = %(default)d)') # FIXME: not used.
    args = parser.parse_args()

    runner = Pstricks(**vars(args))
    if args.dst:
        dstmain, dstext = os.path.splitext(args.dst)
    else:
        dstmain, dstext = args.dst, args.dstext
    runner(args.src, dstmain, dstext=dstext)

    return 0


if __name__ == '__main__':
    main()
