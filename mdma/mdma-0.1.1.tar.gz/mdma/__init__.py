# Our own
from IPython.config.configurable import Configurable
from IPython.core import magic_arguments
from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.utils.traitlets import Unicode
from IPython.utils.io import capture_output, CapturedIO
from IPython import display
from markdown import markdown
#------------------------------------------------------------------------------
# CapturedIO
#------------------------------------------------------------------------------

def load_captured_io(captured_io):
    try:
        return CapturedIO(captured_io.get('stdout', None),
                          captured_io.get('stderr', None),
                          outputs=captured_io.get('outputs', []),
        )
    except TypeError:
        return CapturedIO(captured_io.get('stdout', None),
                          captured_io.get('stderr', None),
        )


@magics_class
class MarkdownMagics(Magics, Configurable):
    """Variable caching.

    Provides the %markdown magic."""

    cachedir = Unicode('', config=True)

    def __init__(self, shell=None):
        Magics.__init__(self, shell)
        Configurable.__init__(self, config=shell.config)

    @cell_magic
    def markdown(self, line, cell):
        """Cache user variables in a file, and skip the cell if the cached
        variables exist.

        Usage:

            %%cache myfile.pkl var1 var2
            # If myfile.pkl doesn't exist, this cell is executed and
            # var1 and var2 are saved in this file.
            # Otherwise, the cell is skipped and these variables are
            # injected from the file to the interactive namespace.
            var1 = ...
            var2 = ...

        """
        args = magic_arguments.parse_argstring(self.markdown, line)
        code = cell if cell.endswith('\n') else cell + '\n'
        error = False
        with capture_output() as io:
            try:
                self.shell.run_cell(cell)
            except:
                error = True
        if error:
            io()
        else:
            txt = io.stdout + io.stderr
            display.publish_display_data('', {'text/plain': txt ,
                                              'text/html': markdown(txt)}, {})


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(MarkdownMagics)