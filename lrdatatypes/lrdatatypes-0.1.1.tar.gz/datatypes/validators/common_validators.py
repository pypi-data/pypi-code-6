import dateutil.parser
from datatypes.validators.postcode_validator import Postcode

def Date():
    return lambda value: dateutil.parser.parse(value)

def NotEmpty():
    return lambda value: value.strip().isspace()

def IsPostcode():
    postcode_validator = Postcode()
    return lambda value: postcode_validator.validate(value)
