from io import BytesIO

from ..core import ExternalCommandTask
from ..io import lazy_read
from ..utils import write_to_tmp_dir
from .basics import walk


class autoprefixer(ExternalCommandTask):
    def __init__(self, browsers=None):
        self.browsers = browsers

    def lazy_prefix(self, contents):
        cmd = ['autoprefixer']
        if self.browsers:
            cmd += ['--browsers', self.browsers]

        output = self.run_external(cmd, input=b''.join(contents))
        yield output

    def process(self, inputs):
        for t, c in inputs:
            yield t, self.lazy_prefix(c)


class cleancss(ExternalCommandTask):
    """Minifies CSS input files."""

    def __init__(self, *, s0=None, s1=None, keep_line_breaks=None):
        self.s0 = s0
        self.s1 = s1
        self.keep_line_breaks = keep_line_breaks

    def lazy_clean(self, c):
        cmd = ['cleancss']
        if self.s0:
            cmd += ['--s0']
        if self.s1:
            cmd += ['--s1']
        if self.keep_line_breaks:
            cmd += ['--keep-line-breaks']
        yield self.run_external(cmd, input=b''.join(c))

    def process(self, inputs):
        for t, c in inputs:
            if t.suffix != '.css':
                yield t, c
                continue

            yield t, self.lazy_clean(c)


class lessc(ExternalCommandTask):
    """
    Compile LESS files to CSS.

    There are two modes to invoke the LESS compiler.

    The default mode passes the input .less files to lessc's stdin.  This
    method has the advantage of being slightly quicker, as no temporary files
    have to be created.

    The second method writes the input files to a temporary directory before
    invoking the less compiler, meaning you can use @import statements in the
    .less files.
    """

    def __init__(self, *files, line_numbers=None, source_map=False):
        self.files = files
        self.line_numbers = line_numbers
        self.source_map = source_map

    def process_via_stdin(self, inputs):
        for t, c in inputs:
            if t.suffix != '.less':
                yield t, c
                continue

            t2 = t.with_suffix('.css')
            t2_smap = t2.with_name(t2.name + '.map')

            cmd = ['lessc']
            if self.source_map:
                # TODO: Change this to write to a safer temporary directory
                cmd += ['--source-map=/tmp/_sm.map',
                        '--source-map-url=' + str(t2_smap.name)]
            if self.line_numbers:
                cmd += ['--line-numbers=' + self.line_numbers]
            cmd += ['-']

            output = self.run_external(cmd, input=b''.join(c))
            yield t2, BytesIO(output)
            if self.source_map:
                yield t2_smap, lazy_read('/tmp/_sm.map')

    def process_via_tmp_dir(self, inputs):
        tmp_dir, paths = write_to_tmp_dir(inputs)

        cmd = ['lessc']
        if self.line_numbers:
            cmd += ['--line-numbers=' + self.line_numbers]
        cmd += [str(f) for f in self.files]
        cmd += ['iron_output.css']

        self.run_external(cmd, cwd=tmp_dir)

        for t, c in walk(tmp_dir):
            if t not in paths:  # filter out any input files, returning only the new files
                yield t, c

    def process(self, inputs):
        if self.files:
            return self.process_via_tmp_dir(inputs)
        else:
            return self.process_via_stdin(inputs)
