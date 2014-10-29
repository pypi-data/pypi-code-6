from voluptuous import In, All
import pycountry

from datatypes.core import SingleValueValidator


countries = pycountry.countries

valid_countries = [c.alpha2 for c in countries]

country_schema = All(In(valid_countries))


class IsoCountryCode(SingleValueValidator):
    def define_schema(self):
        return country_schema

    def define_error_message(self):
        return "Country must be a valid ISO country code"

