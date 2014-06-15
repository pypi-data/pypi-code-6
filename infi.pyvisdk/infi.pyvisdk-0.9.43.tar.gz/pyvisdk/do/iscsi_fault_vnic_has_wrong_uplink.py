
import logging
from pyvisdk.exceptions import InvalidArgumentError

########################################
# Automatically generated, do not edit.
########################################

log = logging.getLogger(__name__)

def IscsiFaultVnicHasWrongUplink(vim, *args, **kwargs):
    '''This fault indicates the given Virtual NIC has the wrong Physical uplink for
    iSCSI multi-pathing configuration. The Physical uplink is not associated with
    the iSCSI Host Bus Adapter.'''

    obj = vim.client.factory.create('{urn:vim25}IscsiFaultVnicHasWrongUplink')

    # do some validation checking...
    if (len(args) + len(kwargs)) < 5:
        raise IndexError('Expected at least 6 arguments got: %d' % len(args))

    required = [ 'vnicDevice', 'dynamicProperty', 'dynamicType', 'faultCause', 'faultMessage' ]
    optional = [  ]

    for name, arg in zip(required+optional, args):
        setattr(obj, name, arg)

    for name, value in kwargs.items():
        if name in required + optional:
            setattr(obj, name, value)
        else:
            raise InvalidArgumentError("Invalid argument: %s.  Expected one of %s" % (name, ", ".join(required + optional)))

    return obj
