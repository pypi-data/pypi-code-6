from __future__ import unicode_literals
raise Exception('Not yet in use!!')

__all__ = ('KeyBindings', )


class KeyBindings(object):
    """
    Base class for all key bindings.

    :param cli_ref: (weakref) Back reference to the `CommandLineInterface` class.
    """
    def __init__(self, cli_ref):
        self.cli_ref = cli_ref

    @property
    def line(self):
        return self.cli_ref().line

    def register_in_registry(self, registry):
        """
        Register the bindings of this class in this registry.
        """
        pass
