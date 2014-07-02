# -*- coding: utf-8 -*-
# :Progetto:  PatchDB -- Python script execution context
# :Creato:    sab 31 mag 2014 12:55:31 CEST
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

import sys
from . import ExecutionContext


class PythonContext(ExecutionContext):
    language_name = 'python'

    execution_context = { 'contexts': ExecutionContext.execution_contexts_registry }

    def __init__(self):
        ExecutionContext.__init__(self)
        self.assertions.update({
            'python_3_x': (3,) < sys.version_info < (4,),
            'python_2_x': (2,) < sys.version_info < (3,),
        })

    def apply(self, patch, options):
        """
        Execute the Python script.

        The script may refers to other `contexts`: in particular
        ``contexts['sql'].connection`` is the open connection to
        the database.
        """

        local_ns = {'options': options}
        if sys.version_info >= (3,):
            exec(patch.script, self.execution_context, local_ns)
        else:
            exec("exec patch.script in self.execution_context, local_ns")
        self.execution_contexts_registry['sql'].applied(patch)
        if not options.verbose:
            from sys import stderr
            stderr.write('.')
