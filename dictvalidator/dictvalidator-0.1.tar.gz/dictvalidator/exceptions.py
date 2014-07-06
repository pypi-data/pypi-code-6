

class DictValidationException(Exception):
    def __init__(self, validation_errors):
        self.validation_errors = validation_errors

    def __str__(self):
        return 'DictValidationException with errors : %s' \
               % [str(e) for e in self.validation_errors]


class FieldValidationException(DictValidationException):
    def __init__(self, field):
        Exception.__init__(self)
        self.field = field


class FieldAbsentException(FieldValidationException):
    def __str__(self):
        return 'Field absent: %s' % self.field


class FieldTypeValidationException(FieldValidationException):
    def __init__(self, field, expected_type, observed_type):
        FieldValidationException.__init__(self, field)
        self.expected_type = expected_type
        self.observed_type = observed_type

    def __str__(self):
        return 'Invalid type for field {0}, expected {1} found {2}'.format(
            self.field,
            self.expected_type,
            self.observed_type
            )