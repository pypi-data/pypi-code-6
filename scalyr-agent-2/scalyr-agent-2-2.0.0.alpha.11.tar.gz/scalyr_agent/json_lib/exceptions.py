# Copyright 2014, Scalyr, Inc.

# Add appropriate license here.
#
# The Scalyr JSON-related abstractions.  This file contains the followin exceptions:
#    JsonConversionException:  Raised when a field cannot be converted to a desired type.
#    JsonMissingFieldException:  Raised when a value is not present for a request field.
#    JsonParseException:  Raised when parsing a string as JSON fails.
#
# author: Steven Czerwinski <czerwin@scalyr.com>


class JsonConversionException(Exception):
    """Raised when a field in a JsonObject does not have a compatible type
    which the requested return type by the caller."""
    def __init__(self, message):
        Exception.__init__(self, message)


class JsonMissingFieldException(Exception):
    """Raised when a value is not present for a requested field in a
    JsonObject."""

    def __init__(self, message):
        Exception.__init__(self, message)


class JsonParseException(Exception):
    """Raised when a parsing problem occurs."""
    def __init__(self, message, position, line_number):
        self.position = position
        self.line_number = line_number
        self.raw_message = message
        position_message = " (line %i, byte position %i)" % (line_number,
                                                             position)

        Exception.__init__(self, message + position_message)