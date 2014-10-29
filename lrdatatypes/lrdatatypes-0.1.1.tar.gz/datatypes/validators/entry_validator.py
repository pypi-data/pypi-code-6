from voluptuous import Required, All
from datatypes.core import DictionaryValidator

from datatypes.validators import deed_validator

entry_schema = {
    Required("template"): All(unicode),
    Required("full_text"): All(unicode),
    Required("fields"): {unicode: object},
    Required("deeds"): [deed_validator.deed_schema],
    Required("notes"): []
}


class Entry(DictionaryValidator):

    def define_schema(self):
        return entry_schema

    def define_error_dictionary(self):
        return {
            "template": "template is a required field",
            "full_text": "full_text is a required field",
            "fields": "fields are required",
            "deeds": "deeds are required",
            "notes": "notes are required"
        }
