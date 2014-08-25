
class Error(Exception):
    """ Baseclass for sshpubkey Exceptions."""


class PublicKeyError(Error):
    """ Baseclass for PublicKey Errors."""


class PublicKeyParseError(PublicKeyError):
    """ Raised when there's a failure parsing a public key."""


class PublicKeyInvalid(PublicKeyError):
    """ Raised when a Public Key is invalid for any reason."""
