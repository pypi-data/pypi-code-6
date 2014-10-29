from voluptuous import Required, All, Length
from datatypes.core import DictionaryValidator

from datatypes.validators import deed_validator
from datatypes.validators import address_validator

property_description_schema = {
    Required("template"): All(unicode),
    Required("full_text"): All(unicode),
    Required("fields"): {
        Required("addresses"): All(Length(min=1), [address_validator.address_schema], extra=True)
    },
    Required("deeds"): [deed_validator.deed_schema],
    Required("notes"): []
}

class PropertyDescription(DictionaryValidator):
    def define_schema(self):
        return property_description_schema

    def define_error_dictionary(self):
        return {
            "tempate": "template is a required field",
            "full_text": "full_text is a required field",
            "fields": "fields are required",
            "fields.addresses": "addresses are required and there must be at least 1",
            "deeds": "deeds are required",
            "notes": "notes are required"
        }
