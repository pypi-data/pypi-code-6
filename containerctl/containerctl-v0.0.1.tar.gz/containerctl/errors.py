"""Errors raised by the package."""


class Error(Exception):
    """Base error class."""


class ConfigError(Error):
    """Raised on config error."""


class ContainerError(Error):
    """Raised on container error."""


class VersionError(Error):
    """Raise on version detection failure."""
