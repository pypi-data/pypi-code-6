from __future__ import print_function
from IPython import get_ipython
from IPython.core.magic import (Magics, magics_class, line_cell_magic,
                                cell_magic, line_magic)


from os import name as os_name

if os_name == 'nt':
    SHELL = 'bash'
    print('WARNING: This magic assumes that you have git or msys installed') 
elif os_name == 'posix':
    SHELL = 'bash'
else:
    raise OSError("Your OS is not supported")

MAKE_TEST = "{0} --interp < {1}.psl 1> {1}.psl.expected \
                2> {1}.psl.error"

@magics_class
class ParselTongueMagics(Magics):
    """Magic for the hylang lisp language
    """
    def __init__(self, shell):
        """
        Parameters
        ----------
        shell : IPython shell

        """
        super(ParselTongueMagics, self).__init__(shell)
        self.ip = get_ipython()
        self.EXE = None

    @line_magic
    def psl_exe(self, line):
        self.EXE = line

    @line_cell_magic
    def psl(self, line,  cell=None, filename='<input>', symbol='single'):
        """ The is the line magic for parselTongue.  It will interpret a line of
        psl and print the resulting output. """
        if not self.EXE:
            raise ValueError("Please use %psl_exe to register the \
                             ParselTongue executable address")
        source = cell if cell else line
        script = "echo '{0}' | {1} --interp".format(source, self.EXE)
        self.call_script(script, get_output=True)

    @cell_magic
    def psl_create_test(self, line, cell):
        ''' Magic for creating a ParselTongue test out of the cell contents.
        The argument for magic is the file_base.
        The result will be 3 files:
            * file_base.psl
            * file_base.psl.excepted
            * file_base.psl.error
        An exception will be thrown if a file_base is not given
        or file_base.psl already exists.'''
        filename = line + ".psl"
        import os.path
        if os.path.isfile(filename):
            raise OSError("The {1} already exists".format(filename))
        with open(filename, 'w') as f:
            f.write(cell)
        script = MAKE_TEST.format(self.EXE, line)
        self.call_script(script)

    def call_script(self, script, get_output=False):
        flags = ''
        if get_output:
            flags = ' --out output --err error'
        self.ip.run_cell_magic('script', SHELL + flags, script)
        if get_output:
            output, error = self.ip.user_ns['output'], self.ip.user_ns['error']
            if error:
                raise SyntaxError(error)
            else:
                print(output)

    @line_magic
    def psl_run_tests(self, line):
        ''' Magic for running the ParselTongue tests versus the 25 incorrect
        interpreters.  Syntax is:
            %psl_run_tests <dir>'''
        script = "{0} --test-interps {1}".format(self.EXE, line)
        self.call_script(script, True)


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    print("WARNING:Please register the address of the ParselTongue executable\
            using %psl_exe <address>")
    ip.register_magics(ParselTongueMagics)
