
import logging
from pyvisdk.exceptions import InvalidArgumentError

########################################
# Automatically generated, do not edit.
########################################

log = logging.getLogger(__name__)

def DistributedVirtualSwitchProductSpec(vim, *args, **kwargs):
    '''This data object type is a subset of AboutInfo. An object of this type can be
    used to describe the specification for a proxy switch module of a
    DistributedVirtualSwitch.'''

    obj = vim.client.factory.create('{urn:vim25}DistributedVirtualSwitchProductSpec')

    # do some validation checking...
    if (len(args) + len(kwargs)) < 0:
        raise IndexError('Expected at least 1 arguments got: %d' % len(args))

    required = [  ]
    optional = [ 'build', 'bundleId', 'bundleUrl', 'forwardingClass', 'name', 'vendor',
        'version', 'dynamicProperty', 'dynamicType' ]

    for name, arg in zip(required+optional, args):
        setattr(obj, name, arg)

    for name, value in kwargs.items():
        if name in required + optional:
            setattr(obj, name, value)
        else:
            raise InvalidArgumentError("Invalid argument: %s.  Expected one of %s" % (name, ", ".join(required + optional)))

    return obj
