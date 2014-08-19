""" Special types for schemas. """


_NotSet = object()


AnyType = object


class DictOf:
    """ A dictionary with arbitrary keys. All values must conform to `schema`.
        """
    def __init__(self, schema):
        self.schema = schema


class ListOf:
    """ A list with arbitrary length. All values must conform to `schema`. """
    def __init__(self, schema):
        self.schema = schema


class Dict:
    def __init__(self, schema, *, strip_extras=_NotSet, optional_keys=_NotSet):
        self.schema = schema

        if optional_keys is not _NotSet:
            optional_keys = set(optional_keys)

        items = [
            ('strip_extras', strip_extras),
            ('optional_keys', optional_keys),
            ]

        self.validate_structure_kwargs = {
            key: value
            for key, value in items
            if value is not _NotSet
            }


class Call:
    def __init__(self, function, **kwargs):
        self.function = function
        self.kwargs = kwargs
