from voluptuous import All

from datatypes.core import SingleValueValidator
from datatypes.voluptuous_helpers.postcode_schema_validator import postcode_is_valid

postcode_schema = All(unicode, postcode_is_valid())


class Postcode(SingleValueValidator):
    def clean_input(self, postcode):
        return unicode(postcode).replace(' ', '').upper()

    def to_canonical_form(self, postcode):
        self.validate(postcode)
        out = postcode.upper()
        if ' ' not in postcode:
            i = len(postcode) - 3
            out = out[:i] + ' ' + out[i:]

        return out

    def define_schema(self):
        return postcode_schema

    def define_error_message(self):
        return "Postcode should be a valid UK postcode"


