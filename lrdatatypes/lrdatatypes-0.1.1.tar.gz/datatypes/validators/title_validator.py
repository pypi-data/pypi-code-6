import datetime

from voluptuous import Required, All, Optional

from datatypes.core import DictionaryValidator
from datatypes.validators import geo_json_validator, entry_validator, proprietorship_validator, property_description_validator
from datatypes.validators.common_validators import Date, NotEmpty


title_schema = {

    Required("title_number"): All(unicode, NotEmpty()),

    Required("class_of_title"): All(unicode, NotEmpty()),

    Required("tenure"): All(unicode, NotEmpty()),

    Required("edition_date"): All(unicode, Date()),

    "extent": geo_json_validator.geo_json_schema,

    Required("proprietorship"): proprietorship_validator.proprietorship_schema,

    Required("property_description"): property_description_validator.property_description_schema,

    Required("restrictive_covenants"): [entry_validator.entry_schema],

    Required("restrictions"): [entry_validator.entry_schema],

    Required("bankruptcy"): [entry_validator.entry_schema],

    Required("easements"): [entry_validator.entry_schema],

    Required("provisions"): [entry_validator.entry_schema],

    Required("charges"): [entry_validator.entry_schema],

    Required("other"): [entry_validator.entry_schema],

    Optional("price_paid"): entry_validator.entry_schema,

    Optional("h_schedule"): entry_validator.entry_schema,

}


class Title(DictionaryValidator):
    def define_schema(self):
        return title_schema

    def define_error_dictionary(self):
        return {
            "title_number": "title_number is a required field, must not be an empty string",
            "edition_date": "edition is a required field, must be a valid date format",
            "tenure": "tenure is a required field, must not be an empty string",
            "class_of_title": "class_of_title is a required field, must not be an empty string",
            "proprietorship": "proprietorship is a required field",
            "property_description": "property_description is a required field",
            "price_paid": "price_paid is an optional entry field",
            "provisions": "provisions is a required field",
            "easements": "easements is a required field",
            "restrictive_covenants": "restrictive_covenants is a required field",
            "restrictions": "restrictions is a required field",
            "bankruptcy": "bankruptcy is a required field",
            "h_schedule": "h_schedule is an optional entry field",
            "charges": "charges is a required field",
            "other": "other is a required field"
        }
