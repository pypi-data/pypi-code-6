


class WileECoyoteException(ValueError):
    '''Raised when a url has a bad scheme'''
    pass


class ZachMorrisException(ValueError):
    '''Raised when a url has too many schemes'''
    pass


class AmbiguousNavigationError(Exception):
    '''Raised when attempting to dereference a templated Navigator'''
    pass
