from functools import wraps

from voluptuous import Invalid

from ukpostcodeutils.validation import is_valid_postcode

# If there are any extra UK postcodes that are valid but don't conform to the default algorithm
# then add them here.
extra_postcodes_that_are_valid = ()


def postcode_is_valid():
    @wraps(postcode_is_valid)
    def f(postcode):
        if not is_valid_postcode(postcode, extra_postcodes_that_are_valid):
            raise Invalid("Postcode is invalid: " + postcode)
        return postcode

    return f

