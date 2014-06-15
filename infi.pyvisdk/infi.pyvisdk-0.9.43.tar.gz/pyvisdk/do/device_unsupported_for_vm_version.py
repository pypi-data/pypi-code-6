
import logging
from pyvisdk.exceptions import InvalidArgumentError

########################################
# Automatically generated, do not edit.
########################################

log = logging.getLogger(__name__)

def DeviceUnsupportedForVmVersion(vim, *args, **kwargs):
    '''A DeviceUnsupportedForVmVersion exception is thrown if a specific device is not
    supported for a given version of the virtual machine.'''

    obj = vim.client.factory.create('{urn:vim25}DeviceUnsupportedForVmVersion')

    # do some validation checking...
    if (len(args) + len(kwargs)) < 8:
        raise IndexError('Expected at least 9 arguments got: %d' % len(args))

    required = [ 'currentVersion', 'expectedVersion', 'deviceIndex', 'property',
        'dynamicProperty', 'dynamicType', 'faultCause', 'faultMessage' ]
    optional = [  ]

    for name, arg in zip(required+optional, args):
        setattr(obj, name, arg)

    for name, value in kwargs.items():
        if name in required + optional:
            setattr(obj, name, value)
        else:
            raise InvalidArgumentError("Invalid argument: %s.  Expected one of %s" % (name, ", ".join(required + optional)))

    return obj
