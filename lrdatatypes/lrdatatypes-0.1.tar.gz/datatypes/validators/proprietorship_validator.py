from voluptuous import Required, All, Length
from datatypes.core import DictionaryValidator

from datatypes.validators import deed_validator
from datatypes.validators import proprietor_validator
from datatypes.validators import address_validator

proprietorship_schema = {
    Required("template"): All(unicode),
    Required("full_text"): All(unicode),
    Required("fields"): {
        Required("proprietors"): All( Length(min=1),
            [ { Required("name"): All(proprietor_validator.proprietor_schema, extra=True),
                Required("addresses"): All(Length(min=1), [address_validator.address_schema], extra=True)
              }
            ])
    },
    Required("deeds"): [deed_validator.deed_schema],
    Required("notes"): []
}

class Proprietorship(DictionaryValidator):
    def define_schema(self):
        return proprietorship_schema

    def define_error_dictionary(self):
        return {
            "tempate": "template is a required field",
            "full_text": "full_text is a required field",
            "fields": "fields are required",
            "fields.proprietors": "proprietors are required and there must be at least 1",
            "fields.proprietors.name": "proprietors name is required",
            "fields.proprietors.addresses": "proprietors addresses are required",
            "deeds": "deeds are required",
            "notes": "notes are required"
        }
