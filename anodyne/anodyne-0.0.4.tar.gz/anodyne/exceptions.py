class ConfigurationException(Exception):
    """
    Happens when someone attempts to use any core functions out of the `engines`
    module, but the system has yet to be configured.
    """


class EmptyEngineException(Exception):
    """
    Occurs when someone asks for a connection, and the engine being used
    to create that connection was not generated for some reason.
    """


class NoValidEnginesException(Exception):
    """
    Should be raised when connections attempt to retrieve engine metadata
    and that metadata is empty.
    """