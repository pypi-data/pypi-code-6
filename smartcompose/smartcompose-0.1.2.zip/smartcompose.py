"""Easy delegation with composition

 - Not compatible with Python 2!
 - https://github.com/hsharrison/smartcompose
 - Licensed under terms of the MIT License (see LICENSE.txt)
 - Copyright (c) 2014 Henry S. Harrison, henry.schafer.harrison@gmail.com

"""
from functools import partial
try:
    from functools import partialmethod
except ImportError:
    from partialmethod import partialmethod


__all__ = ['delegate']
__version__ = '0.1.2'


def _call_delegated_method(attribute_name, self, method_name, *args, **kwargs):
    return getattr(getattr(self, attribute_name), method_name)(*args, **kwargs)


def delegate(attribute_name, method_names):
    """
    Decorator factory to delegate methods to an attribute.

    Decorate a class to map every method in `method_names` to the attribute `attribute_name`.

    """
    call_attribute_method = partial(_call_delegated_method, attribute_name)

    def decorate(class_):
        for method in method_names:
            setattr(class_, method, partialmethod(call_attribute_method, method))

        return class_
    return decorate
