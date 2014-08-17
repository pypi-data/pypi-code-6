import platform
import asyncio
from pybone.utils.filesystem import find_first_file

_loop = asyncio.get_event_loop()


class PlatformError(Exception):
    pass


class Config(object):
    """
    Base class for board configuration
    """
    def __init__(self, system_name, kernel_release, processor):
        self.system_name = system_name
        self.kernel_release = kernel_release
        self.processor = processor

    def __repr__(self):
        return "%s(system_name=%r,kernel_release=%r,processor=%r)" % \
               (self.__class__.__name__,
                self.system_name,
                self.kernel_release,
                self.processor)


local_system = platform.system()
local_release = platform.release()
local_processor = platform.processor()
try:
    from pybone.bone_3_8.config import Linux38Config
    local_config = Linux38Config(local_system, local_release, local_processor)
except PlatformError:
    local_config = Config(local_system, local_release, local_processor)
