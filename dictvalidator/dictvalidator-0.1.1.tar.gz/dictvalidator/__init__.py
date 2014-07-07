__import__('pkg_resources').declare_namespace(__name__)

from meta import DictValidatorMeta
from exceptions import *


class DictValidator(object):
    __metaclass__ = DictValidatorMeta

    def __init__(self, dictionary):
        validation_errors = []

        if not isinstance(dictionary, dict):
            validation_errors.append(
                Exception('DictValidator attempted to validate non-dict type'))
        else:
            for fname in self._fields:
                field = self._fields[fname]

                # first check if it exists and add an error if it is absent
                exists = fname in dictionary
                if not exists:
                    if field.required:
                        validation_errors.append(FieldAbsentException(fname))
                    else:
                        setattr(self, fname, None)
                    continue

                # now that we know its there, validate it
                try:
                    setattr(self, fname, self._fields[fname](dictionary[fname]))
                except DictValidationException as e:
                    validation_errors.append(e)

        is_valid = len(validation_errors) == 0
        if not is_valid:
            raise DictValidationException(validation_errors)