#!/usr/bin/env python

# Station status constants.
DISABLED = 0
ENABLED = 1


class ActiveStationLimit(Exception):
    """Exception class to throw when active stations > max concurrent stations
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class StationMasterNotRegistered(Exception):
    """Exception class to throw when trying to register or interact with an unregistered master station.
    """
    def __init__(self, sid, master):
        self.sid = sid
        self.master = master

    def __str__(self):
        return repr("Station %d is trying to use unregistered station %d as a master." % (self.sid, self.master))


class StationNotRegistered(Exception):
    """Exception class to throw when trying to interact with an unregistered station.
    """
    def __init__(self, sid):
        self.sid = sid

    def __str__(self):
        return repr("Station %d is not a registered station." % (self.sid))


class StationMasterProhibited(Exception):
    """Exception class to throw when a master station is being enabled/disabled directly.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr("station %d is a master station and can not be directly enabled or disabled." % (self.value))


class Station(object):
    """Station class

    """
    def __init__(self, sid, controller, name='', description='', stype='zone', master=None):
        """Station Class Intializer

        """
        self._sid = sid

        if stype not in ['zone', 'master']:
            raise ValueError("Unknown station type: %s" % (stype))
        else:
            self._type = stype
        if name == '':
            self._name = str(sid)
        else:
            self._name = name
        self._description = description
        self._status = DISABLED
        self._master = master
        self._controller = controller

    def dict(self):
        """This function returns a dictionary representation of the station object.

        Args:
           None

        Returns:
           dict.  returns dictionary of station object
        """
        station_dict = {
            'sid': self._sid,
            'name': self._name,
            'description': self._description,
            'type': self._type
        }

        if self._master:
            station_dict['master'] = self._master

        return station_dict

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def sid(self):
        return self._sid

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if isinstance(value, str):
            stype = value.to_lower
            if stype in ['zone', 'master']:
                self._type = stype
            else:
                raise TypeError('Must be "zone" or master".')
        else:
            raise TypeError('Expected String.')

    @property
    def status(self):
        return self._status

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, value):
        self._master = value

    def enable(self):
        """Enables a station
        If the station has a master station it is enabled after the current station.
        """

        if self._controller.active >= self._controller.max_active:
            raise ActiveStationLimit("Controller only supports %d stations active at once." % (self._controller.max_active))
        else:
            self._controller.enable(self._sid)
            self._status = ENABLED
            if self._master:
                try:
                    self._controller.enable(self._master)
                except StationNotRegistered:
                    raise StationMasterNotRegistered(self._sid, self._master)

    def disable(self):
        """Disables a station
        If the station has a master station it is disabled first.
        """

        if self._master:
            self._controller.disable(self._master)
        self._controller.disable(self._sid)
        self._status = DISABLED
