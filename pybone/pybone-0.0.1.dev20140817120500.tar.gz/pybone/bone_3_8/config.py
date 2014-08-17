from pybone.config import Config

__author__ = 'nico'

class Linux38Config(Config):
    """
    Linux running on BeagleBone platform
    This should match the system configuration running on a beagleboard
    """
    _board_name_file_pattern = '/sys/devices/bone_capemgr.*/baseboard/board-name'
    _revision_file_pattern = '/sys/devices/bone_capemgr.*/baseboard/revision'
    _serial_number_file_pattern = '/sys/devices/bone_capemgr.*/baseboard/serial-number'
    _pins_file_pattern = '/sys/kernel/debug/pinctrl/44e10800.pinmux/pins'
    _pinmux_pins_file_pattern = '/sys/kernel/debug/pinctrl/44e10800.pinmux/pinmux-pins'

    def __init__(self, system_name, kernel_release, processor):
        super(Linux38Config, self).__init__(system_name, kernel_release, processor)
        if 'Linux' not in self.system_name:
            raise PlatformError("Unexpected system name '%r'" % self.system_name)
        elif '3.8' not in self.kernel_release:
            raise PlatformError("Unexpected kernel release '%r'" % self.kernel_release)
        elif 'arm' not in self.processor:
            raise PlatformError("Unexpected processor '%r'" % self.processor)

        _loop.run_until_complete(self.__init_async())

    def __init_async(self):
        self.board_name_file = yield from find_first_file(Linux38Config._board_name_file_pattern)
        self.revision_file = yield from find_first_file(Linux38Config._revision_file_pattern)
        self.serial_number_file = yield from find_first_file(Linux38Config._serial_number_file_pattern)
        self.pins_file = yield from find_first_file(Linux38Config._pins_file_pattern)
        self.pinmux_pins_file = yield from find_first_file(Linux38Config._pinmux_pins_file_pattern)

