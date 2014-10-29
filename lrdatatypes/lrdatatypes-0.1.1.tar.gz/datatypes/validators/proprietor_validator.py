from voluptuous import Required, Extra
from datatypes.core import DictionaryValidator

proprietor_schema = {
        Required("title"): unicode,
        Required("full_name"): unicode,
        Required("decoration"): unicode
}

class Proprietor(DictionaryValidator):

    def define_schema(self):
            return proprietor_schema

    def define_error_dictionary(self):
        return {
            "title": "title is a required field",
            "full_name": "full_name is a required field",
            "decoration": "decoration is a required field"
        }
