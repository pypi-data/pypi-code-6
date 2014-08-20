#!/usr/bin/env python

"""A libary for the opensprinkler project.

.. module:: opensprinkler
    :synopsis: Opensprinkler module

.. moduleauthor:: David Miller <david3d@gmail.com>

"""

import json
from station import *
from controller import Controller


class OpenSprinkler(object):
    """opensprinkler class.

    This is the class that provides the interface layer for the library.

    """

    def __init__(self, name=None):
        """Class Initializer"""
        self._controller = Controller()
        self.stations = dict()

    @property
    def platform(self):
        """Identifies the hardware platform of controller.

        Returns:
            string: "rpi", "bb", or "unknown"

            rpi = RasberryPi
            bb = Beaglebone Black
            unknown = no platform detected using mock controller class
        """
        return self._controller.platform

    def register_station(self, sid, name="", description="", stype="zone", master=None):
        """This function registers a station.

        Args:
           sid (int):  The station id .

        Raises:
           ValueError, TypeError

        Before you can call any other function that interacts with a station it
        must be registered.

        """
        if isinstance(sid, int):
            if sid < 1:
                raise ValueError("station id must be between 1 and %d.  Got %d" % (self._controller.max_stations, sid))
            elif sid > self._controller.max_stations:
                raise ValueError("station id must be between 1 and %d.  Got %d" % (self._controller.max_stations, sid))
        else:
            raise TypeError("station id must be an int")

        # If station has a master verify that it's been registered first
        if master:
            if str(master) not in self.stations.keys():
                raise StationMasterNotRegistered(sid, master)

        self.stations[str(sid)] = Station(sid, self._controller, name=name, description=description, stype=stype, master=master)

    def enable_station(self, sid):
        """Enables the given station.

        Args:
           sid (int):  The station id .

        Raises:
           StationNotRegisteredError

        Enables the station.
        If the station has a master station it is enabled after the
        current station.

        """
        station_sid = str(sid)
        try:
            if self.stations[station_sid].type == "master":
                raise StationMasterProhibited(sid)

            self.stations[station_sid].enable()
        except KeyError:
            raise StationNotRegistered(sid)

    def disable_station(self, sid):
        """Disables the given station.

        Args:
           sid (int):  The station id .

        Raises:
           StationNotFoundError

        Disables the station.
        If the station has a master station it is disabled before the
        current station.
        """
        station_sid = str(sid)
        try:
            if self.stations[station_sid].type == "master":
                raise StationMasterProhibited(sid)

            self.stations[station_sid].disable()
        except KeyError:
            raise StationNotFound(sid)

    def disable_all(self):
        """Deactivates all stations"""
        for station in self.stations.values():
            station.disable()

    def load_config(self, conf_object):
        """This function loads a station config file.

        Args:
            conf_object (string):  Expects a json string of the config.

        Returns:
            int of the number of stations in configuration.

        Reads in the json config file for the stations.
        """
        config = json.loads(conf_object)
        # register masters first
        for station in config["stations"]:
            if station["type"] == "master":
                self.register_station(
                    station["id"],
                    name=station["name"],
                    description=station["description"],
                    stype=station["type"]
                )

        # register zones
        for station in config["stations"]:
            if station["type"] == "zone":
                self.register_station(
                    station["id"],
                    name=station["name"],
                    description=station["description"],
                    stype=station["type"]
                )

        return len(config["stations"])

    def get_config(self):
        """This function returns the configuration as a json string.

        Returns:
            Returns a json object of the current running config.
        """
        config = dict()
        # Deal with stations
        station_list = list()
        for station in self.stations.values():
            station_list.append(station.dict())

        config["stations"] = station_list

        return json.dumps(config)

    def enabled_stations(self):
        """This function returns a list of the enabled stations.

        Args:
           None

        Returns:
            List of enabled station objects.
        """
        enabled_list = list()
        for station in self.stations.itervalues():
            if station.status == 1:
                enabled_list.append(station)
        return enabled_list

    def get_stations(self):
        return self.stations.itervalues()
