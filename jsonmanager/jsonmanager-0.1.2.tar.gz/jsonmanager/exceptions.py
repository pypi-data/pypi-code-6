""" Exceptions. """


class Error(Exception):
    """ Base class for errors. """


class ValidationError(Error):
    """ `data` does not conform to `schema`. """

    def __init__(self, *errors):
        """ Stash `args` in `errors` attribute. """
        self.errors = errors


class StructureValidationError(ValidationError):
    """ `data` structure does not conform to `schema` structure. """


class RulesValidationError(ValidationError):
    """ `data` violates one or more rules from `schema`. """


class InputValidationError(ValidationError):
    """ Input `data` does not conform to input `schema`. """


class InputStructureValidationError(
    InputValidationError, StructureValidationError
    ):
    """ Input `data` structure does not conform to input `schema` structure. """


class InputRulesValidationError(
    InputValidationError, RulesValidationError
    ):
    """ Input `data` violates one or more rules from input `schema`. """


class OutputValidationError(ValidationError):
    """ Output `data` does not conform to output `schema`. """


class OutputStructureValidationError(
    OutputValidationError, StructureValidationError
    ):
    """ Output `data` structure does not conform to output `schema` structure.
        """


class OutputRulesValidationError(
    OutputValidationError, RulesValidationError
    ):
    """ Output `data` violates one or more rules from output `schema`. """


class RuleViolation(Error):
    """ `data` violates a rule. """

    def __init__(self, *, code=None, message=None, data=None, key=None):
        self.code = code
        self.message = message
        self.data = data
        self.location = _key_location(key)

    def __str__(self):
        return self.message


def _key_location(key):
    if key is None:
        return tuple()

    return tuple([key])


class StopValidation(Error):
    """ `data` passes rule validation. """


class SchemaError(Error):
    """ `schema` is not a valid schema.

        `schema` may only include these things:
        - types (class objects)
        - dictionaries
        - lists
        - `DictOf` and `ListOf` instances
        - tuples composed of one type and several rules
        """
