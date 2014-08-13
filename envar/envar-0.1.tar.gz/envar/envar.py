import os
import ast
import logging

try:
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    class ImproperlyConfigured(Exception):
        pass


def envar(key, ktype, default=None, verbose=False):
    """Looks for ENVIRONMENT VARIABLE named `key`;
    returns the value after coercing it to type `ktype`.

    Raises `ImproperlyConfigured` exception if environment
    does not have the variable name defined and `default`
    is set to None.

    If `verbose` is true, values loaded from the environment
    are echoed. This is useful to check which of the defaults
    are being overridden.

    Examples:
        envar('HELLO', str)  # Export HELLO="WORLD"
        envar('COUNT', int)  # Export COUNT=21
        enavr('DEBUG', bool)  # Export DEBUG="True"
    """
    value = os.getenv(key)
    # Hopeless situation
    if value is None and default is None:
        raise ImproperlyConfigured('Cannot load environment variable: %s' % (key))

    # Work with defaults, force through the typecast.
    if value is None:
        return convert_to_type(ktype, default)

    # Not using defaults, value is being overridden
    if verbose is True:
        logging.warn("VARIABLE-OVERRIDE:{0}:{1} => {2}".format(key, default, value))

    return convert_to_type(ktype, value)


def convert_to_type(ktype, value):
    try:
        evalue = ast.literal_eval(value)
        if ktype == type(evalue):
            return evalue
        else:
            raise ImproperlyConfigured('Value: {0} is not of type {1}'.format(evalue, ktype))
    except (ValueError, SyntaxError):
        try:
            if ktype == bool:
                try:
                    return {'true': True, 'false': False}[value.lower()]
                except:
                    raise ImproperlyConfigured('Boolean variable types must have values: "True" or "False", got "%s"' % value)
            return ktype(value)
        except:
            raise ImproperlyConfigured('Value: {0} is not of type {1}'.format(value, ktype))

