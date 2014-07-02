# -*- coding: utf-8 -*-
# :Progetto:  PatchDB -- Script execution contexts
# :Creato:    Wed Nov  5 17:32:16 2003
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

import logging

logger = logging.getLogger('context')


class ExecutionError(Exception):
    """
    Exception raised on execution errors.
    """


class ExecutionContext(object):
    """
    An instance of this class is able to execute a script in some
    particular language. This is somewhat abstract and must be
    subclassed and attached to a database...

    Another responsibility of this class instances is to keep
    a persistent knowledge about last applied revision of
    a given script.
    """

    language_name = None

    execution_contexts_registry = {}
    user_assertions = {}

    @classmethod
    def for_language(cls, language):
        """
        Return the right execution context for the given `language`.
        """

        return cls.execution_contexts_registry.get(language)

    @classmethod
    def execute(cls, patch, options):
        """
        Execute the given `patch` in the right context.
        """

        ctx = cls.execution_contexts_registry.get(patch.language)
        if ctx:
            if options.assume_already_applied:
                logger.warning(u"Considering %s %s as applied", patch.language, patch)
                cls.execution_contexts_registry['sql'].applied(patch)
            else:
                logger.info(u"Executing %s %s", patch.language, patch)
                ctx.apply(patch, options)
        else:
            raise ExecutionError(u"Not able to execute %s %s" %
                                 (patch.language, patch))

    def __init__(self):
        """
        Insert this context instance in the registry.
        """

        if self.language_name:
            registry = self.execution_contexts_registry
            assert self.language_name not in registry
            registry[self.language_name] = self
        self.assertions = {}

    def __getitem__(self, patchid):
        """
        Always return None, used by doctests.
        """

    def __setitem__(self, patchid, revision):
        """
        Do nothing, used by doctests.
        """

    def addAssertions(self, assertions):
        """
        Add given `assertions` to the set of assertions managed by the context.
        """

        for assertion in assertions:
            if "=" in assertion:
                assertion, state = assertion.split('=')
                state = state.lower() in ('true', 't', '1', 'yes', 'y')
            else:
                state = True
            if assertion in self.assertions:
                raise ValueError(u'Cannot override existing "%s" assertion' %
                                 assertion)
            self.user_assertions[assertion] = state

    def verifyCondition(self, condition):
        """
        Verify given `condition`, returning False if it is not satisfied.
        """

        return (self.assertions.get(condition, False)
                or self.user_assertions.get(condition, False))

    def apply(self, patch, options):
        "Try to execute the given `patch` script"

        raise NotImplementedError(u'Subclass responsibility')


# Register the context for Python, always available
from .python import PythonContext
PythonContext()
