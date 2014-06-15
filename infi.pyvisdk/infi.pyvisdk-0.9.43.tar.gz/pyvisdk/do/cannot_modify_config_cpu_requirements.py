
import logging
from pyvisdk.exceptions import InvalidArgumentError

########################################
# Automatically generated, do not edit.
########################################

log = logging.getLogger(__name__)

def CannotModifyConfigCpuRequirements(vim, *args, **kwargs):
    '''A virtual machine's total CPU feature requirements are determined by overlaying
    the requirements specified in its configuration (if any) on top of the
    requirements specified in the descriptor for its guest OS. It is therefore
    possible for a host change to implicitly change a virtual machine's CPU feature
    requirements. The guest OS descriptor may have different requirements on the
    new host. Or, if the virtual machine currently specifies requirements in its
    configuration, those requirements will be lost if the new host does not support
    this.This fault indicates that the virtual machine's CPU feature requirements
    would change because of a migration, and also that the destination host does
    not support storing CPU feature requirements in the virtual machine's
    configuration. (If the destination host does support such an action,
    WillModifyConfigCpuRequirements is used instead of this fault.)For a powered-
    off virtual machine, this is a warning. The migration may proceed, but the
    virtual machine will be operating under different CPU feature requirements if
    it is powered on after the migration.For a powered-on or suspended virtual
    machine, this is an error.'''

    obj = vim.client.factory.create('{urn:vim25}CannotModifyConfigCpuRequirements')

    # do some validation checking...
    if (len(args) + len(kwargs)) < 4:
        raise IndexError('Expected at least 5 arguments got: %d' % len(args))

    required = [ 'dynamicProperty', 'dynamicType', 'faultCause', 'faultMessage' ]
    optional = [  ]

    for name, arg in zip(required+optional, args):
        setattr(obj, name, arg)

    for name, value in kwargs.items():
        if name in required + optional:
            setattr(obj, name, value)
        else:
            raise InvalidArgumentError("Invalid argument: %s.  Expected one of %s" % (name, ", ".join(required + optional)))

    return obj
