from controller import *


class mock(Controller):
    """Mock Controller class.
    """

    def __init__(self):
        """Mock Controller Class Initializer
        """
        super(mock, self).__init__()

    def _init_hardware(self):
        self._platform = "unknown"
        return

    def enable(self, sid):
        """Enables the station id.
        """
        self._station_bits[sid - 1] = 1

    def disable(self, sid):
        """Disables the station id.
        """
        self._station_bits[sid - 1] = 0
