
import logging
from pyvisdk.exceptions import InvalidArgumentError

########################################
# Automatically generated, do not edit.
########################################

log = logging.getLogger(__name__)

def HostCnxFailedBadCcagentEvent(vim, *args, **kwargs):
    '''This event records a failure to connect to a host due to no response being
    received from the host agent.'''

    obj = vim.client.factory.create('{urn:vim25}HostCnxFailedBadCcagentEvent')

    # do some validation checking...
    if (len(args) + len(kwargs)) < 4:
        raise IndexError('Expected at least 5 arguments got: %d' % len(args))

    required = [ 'chainId', 'createdTime', 'key', 'userName' ]
    optional = [ 'changeTag', 'computeResource', 'datacenter', 'ds', 'dvs',
        'fullFormattedMessage', 'host', 'net', 'vm', 'dynamicProperty', 'dynamicType' ]

    for name, arg in zip(required+optional, args):
        setattr(obj, name, arg)

    for name, value in kwargs.items():
        if name in required + optional:
            setattr(obj, name, value)
        else:
            raise InvalidArgumentError("Invalid argument: %s.  Expected one of %s" % (name, ", ".join(required + optional)))

    return obj
