import abc


class ControllerNotFound(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Controller(object):
    """BaseClass for controller classes
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        # MAXIMUM NUMBER OF STATIONS
        self._MAX_NSTATIONS = 64
        self._MAX_ACTIVE = 2
        self._station_bits = [0]*self._MAX_NSTATIONS
        self._init_hardware()

    @property
    def platform(self):
        return self._platform

    @property
    def max_stations(self):
        return self._MAX_NSTATIONS

    @property
    def max_active(self):
        return self._MAX_ACTIVE

    @property
    def active(self):
        """Returns the number of active stations"""
        out = 0
        for bit in self._station_bits:
            out += bit
        return out

    @abc.abstractmethod
    def _init_hardware(self):
        """Sets up and initializes GPIO for platform.
        Also sets self._platform
        """
        return

    @abc.abstractmethod
    def enable(self, sid):
        """Enables the station id.
        """
        return

    @abc.abstractmethod
    def disable(self, sid):
        """Disables the station id.
        """
        return
