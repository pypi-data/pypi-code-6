from voluptuous import Required, Optional, All, Length, Coerce, Match, Any
from datatypes.core import DictionaryValidator
from datatypes.validators.common_validators import NotEmpty, IsPostcode


address_schema = {
    Required("full_address"): All(unicode, NotEmpty()),
    Required("house_no"): All(Coerce(unicode)),
    Required("street_name"): All(unicode),
    Required("town"): All(unicode),
    Required("postal_county"): All(unicode),
    Required("region_name"): All(unicode),
    Required("postcode"): All(unicode),
    Required("country"): All(unicode)
}

class Address(DictionaryValidator):
    def define_schema(self):
        return address_schema

    def define_error_dictionary(self):
        return {
            "full_address": "full_address is a required unicode field and must not be empty",
            "house_no": "house_no is a required unicode field",
            "street_name": "street_name is a required unicode field",
            "town": "town is a required unicode field",
            "postal_county": "postal_county is a required unicode field",
            "region_name": "region_name is a required unicode field",
            "postcode_schema": "postcode must be a valid UK postcode",
            "country": "country is a required unicode field"
        }
