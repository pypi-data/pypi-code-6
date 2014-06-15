
import logging
from pyvisdk.exceptions import InvalidArgumentError

########################################
# Automatically generated, do not edit.
########################################

log = logging.getLogger(__name__)

def VirtualMachineIdeDiskDeviceInfo(vim, *args, **kwargs):
    '''The IdeDiskDeviceInfo class contains detailed information about a specific IDE
    disk hardware device. These devices are for the
    vim.vm.device.VirtualDisk.RawDiskVer2BackingInfo and
    vim.vm.device.VirtualDisk.PartitionedRawDiskVer2BackingInfo backings.'''

    obj = vim.client.factory.create('{urn:vim25}VirtualMachineIdeDiskDeviceInfo')

    # do some validation checking...
    if (len(args) + len(kwargs)) < 1:
        raise IndexError('Expected at least 2 arguments got: %d' % len(args))

    required = [ 'name' ]
    optional = [ 'partitionTable', 'capacity', 'vm', 'configurationTag', 'dynamicProperty',
        'dynamicType' ]

    for name, arg in zip(required+optional, args):
        setattr(obj, name, arg)

    for name, value in kwargs.items():
        if name in required + optional:
            setattr(obj, name, value)
        else:
            raise InvalidArgumentError("Invalid argument: %s.  Expected one of %s" % (name, ", ".join(required + optional)))

    return obj
