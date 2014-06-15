#!/usr/bin/python2
# vim: set et sts=4:
"""
This python module provides a trivial interface to the systemd netctl
network control script, which allows listing, starting and stopping
network connections which are already defined as netctl connections.

Stephen Blythe 2014
"""

# Standard libraries
import subprocess
import re

class Netctl:
    """Functions to control netctl."""

    @classmethod
    def _get_raw_netctl_connections(cls):
        return subprocess.check_output(["netctl","list"]).split('\n')[:-1]
    
    @classmethod
    def get_matching_connections(cls,regex):
        """Return a list of connections whose names match the regex."""
        return [l for l in cls.get_all_connections() \
                        for m in [re.search(regex,l)] if m]

    @classmethod
    def get_active_connections(cls):
        """Return a list of active, i.e. running, connections."""
        return [l[2:] for l in cls._get_raw_netctl_connections() \
                        for m in [re.search(r'^\*',l)] if m]
    
    @classmethod
    def get_all_connections(cls):
        """Return a list of all configured connections."""
        return [l[2:] for l in cls._get_raw_netctl_connections()]
    
    @classmethod
    def stop_active_connection(cls):
        """Stop the first active connection."""
        subprocess.check_call(["netctl","stop",cls.get_active_connections()[0]])

    @classmethod
    def start_connection(cls,name):
        """Start a configured connection by name."""
        subprocess.check_call(["netctl","start",name])

    @classmethod
    def start_connection_by_index(cls,index):
        """
        Start a configured connection by index.

        Keyword arguments:
        index -- index to the connection to start, following the order
        produced by the get_all_connections method.
        """
        cls.start_connection(cls.get_all_connections()[index])
            
    @classmethod
    def start_connection_by_match_index(cls,regex,index):
        """
        Start a configured connection by index, which matches the regex.

        Keyword arguments:
        regex -- the regular expression to match the connection names
        index -- index to the connection to start, following the order
        produced by the get_matching_connections method.
        """
        cls.start_connection(cls.get_matching_connections(regex)[index])
            

