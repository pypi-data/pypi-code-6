from voluptuous import All, Match, Coerce

from datatypes.core import SingleValueValidator


price_schema = All(Coerce(float), Coerce(unicode), Match('^[0-9]+(,[0-9]+)?(\.\d{1,2})?$'))


class Price(SingleValueValidator):
    def define_schema(self):
        return price_schema

    def define_error_message(self):
        return "Price must be a numeric value in pounds"
