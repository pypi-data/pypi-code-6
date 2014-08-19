
class KernelVersion:
    """ Returns the version of the kernel """

    def getVariableTuple(self):

        with open('/proc/sys/kernel/osrelease') as fp:

            kernel_version = fp.read().strip()

            return [('KERNEL_VERSION', kernel_version)]