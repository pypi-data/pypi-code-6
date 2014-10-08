import json
from gitmodel.fields import Field
from gitmodel.exceptions import ValidationError


class ListField(Field):
    """
    A list of things to store in JSON.
    As a result, everything in the list must be JSON serialisable.
    """
    empty_value = []

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, list):
            return value
        try:
            return json.loads(value)
        except ValueError, e:
            raise ValidationError(e)
