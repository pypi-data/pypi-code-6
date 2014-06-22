class ParameterValidationError(Exception):
    pass

class UnknownRequestedOutputFileError(Exception):
    pass

class UnspecifiedGGOObjectError(Exception):
    pass

class UnspecifiedOutputFileError(Exception):
    pass

class UnacceptableOutputFormatError(Exception):
    pass

class NoAvailableOutputHandlerError(Exception):
    pass

class UnknownStrategyError(Exception):
    pass

class AuthorParameterSpecificationError(Exception):
    pass

class WriterProcessingIncompleteError(Exception):
    pass

class UnimplementedException(Exception):
    """Maybe this should email me?"""
    pass

class RepeatRequestedFromNonMultiple(Exception):
    pass

class UnknownDataHandlerException(Exception):
    pass

class UnknownDataFormatException(Exception):
    pass
