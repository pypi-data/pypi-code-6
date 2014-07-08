from easy_test_selenium.core import CreateForm


# Messages definition

# Assign default values for fields
default = dict()

# Error definition
#   txtErrorName = {'item': FIELD_NAME, 'message': MESSAGE_NAME, 'value': 'Error Value'}

# Errors register
#   register.addError(**txtErrorName)
register = CreateForm(default)
