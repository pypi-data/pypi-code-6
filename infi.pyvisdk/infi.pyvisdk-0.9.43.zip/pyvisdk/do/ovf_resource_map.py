
import logging
from pyvisdk.exceptions import InvalidArgumentError

########################################
# Automatically generated, do not edit.
########################################

log = logging.getLogger(__name__)

def OvfResourceMap(vim, *args, **kwargs):
    '''Maps source child entities to destination resource pools and resource settings.
    If a mapping is not specified, a child is copied as a direct child of the
    parent.'''

    obj = vim.client.factory.create('{urn:vim25}OvfResourceMap')

    # do some validation checking...
    if (len(args) + len(kwargs)) < 1:
        raise IndexError('Expected at least 2 arguments got: %d' % len(args))

    required = [ 'source' ]
    optional = [ 'datastore', 'parent', 'resourceSpec', 'dynamicProperty', 'dynamicType' ]

    for name, arg in zip(required+optional, args):
        setattr(obj, name, arg)

    for name, value in kwargs.items():
        if name in required + optional:
            setattr(obj, name, value)
        else:
            raise InvalidArgumentError("Invalid argument: %s.  Expected one of %s" % (name, ", ".join(required + optional)))

    return obj
