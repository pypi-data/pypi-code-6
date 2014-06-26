#!/usr/bin/env python

from suds.client import Client
from suds.wsse import *
import yaml


class SsoTokenError(Exception):
    pass


class NbUrnClient(object):

    def __init__(self, config_file=None, username=None, password=None):
        self.sso_token = None

        if config_file:
            self.config = yaml.load(open(config_file))['config']['urn']
        if username:
            self.config['username'] = username
        if password:
            self.config['password'] = password
        self.client = Client(self.config['wsdl'])

    def add_url(self, urn, url):
        """ Add a new URL that is to be associated with the specified URN.

        Keyword arguments:
        urn -- the URN to associate the new target to 
        url -- the URL pointing to the target

        """
        if self.sso_token:
            return self.client.service.addURL(self.sso_token, urn, url)
        else:
            raise SsoTokenError("No SSO token available. You need to login first.")
        
    def create_urn(self, series_code, url):
        """ Create a new URN under the specified series/prefix.

        Keyword arguments:
        series_code -- the series code / prefix under which to create a new URN
        url -- the URL pointing to the target of the URN

        NB: This will only work if:
        - the ID service supports assignment of serial numbers for the specified series, and
        - if the user has access to this series.

        The created URN is stored in the ID service.
        """
        if self.sso_token:
            return self.client.service.createURN(self.sso_token, series_code, url)
        else:
            raise SsoTokenError("No SSO token available. You need to login first.")

    def delete_url(self, urn, url):
        """ Delete a URL pointing to a target associated with the given URN.

        Keyword arguments:
        urn -- the URN associated with the URL to delete
        url -- The URL to delete

        This operation is only allowed as long as there is more than one registered target for the specified URN.
        """
        if self.sso_token:
            return self.client.service.deleteURL(self.sso_token, urn, url)
        else:
            raise SsoTokenError("No SSO token available. You need to login first.")

    def find_urn(self, urn):
        """Find a registered URN with all corresponding locations, along with
        other registered information regarding the URN.

        """
        return self.client.service.findURN(urn)

    def find_urns_for_url(self, url):
        return self.client.service.findURNsForURL(url)

    def get_next_urn(self, series_code):
        """Request the next available URN from a series/prefix.

        Keyword arguments:
        series_code -- a string containing the series code / prefix

        NB: This will only work if:
        - the ID service supports assignment of serial numbers for the specified series, and
        - if the user has access to this series.

        The returned URN is not stored in the ID service.

        """
        if self.sso_token:
            return self.client.service.getNextURN(self.sso_token, series_code)
        else:
            raise SsoTokenError("No SSO token available. You need to login first.")

    def login(self, username=None, password=None):
        """Used to log in to the ID-service.

        Keyword arguments:
        username -- a username string
        password -- a password string

        If no username and/or password is supplied to the method, the
        client tries to find the missing information from the YAML
        config file.

        """
        u = username if username else self.config['username']
        p = password if password else self.config['password']
        self.sso_token = self.client.service.login(u, p)
        return self.sso_token

    def logout(self):
        """
        Used to log out of the ID-service.
        """
        result = None
        if self.sso_token:
            result = self.client.service.logout(self.sso_token)
            self.sso_token = None
        return result

    def register_urn(self, urn, url):
        """ Register a new URN and attach it to a target pointed to by the URL.

        Keyword arguments:
        urn -- the URN to register
        url -- the URL pointing to the target of the URN
        
        The URN is stored in the ID service.
        """
        if self.sso_token:
            return self.client.service.registerURN(self.sso_token, urn, url)
        else:
            raise SsoTokenError("No SSO token available. You need to login first.")

    def replace_url(self, urn, old_url, new_url):
        """ Replace the location of an existing target identified with the specified URN.

        Keyword arguments:
        urn -- The URN whose target to replace
        old_url -- The old URL to be replaced
        new_url -- The new URL to replace the old URL with 
        """
        if self.sso_token:
            return self.client.service.replaceURL(self.sso_token, urn, old_url, new_url)
        else:
            raise SsoTokenError("No SSO token available. You need to login first.")

    def reserve_next_urn(self, series_code):
        """ Create a new URN under the specified series/prefix and reserve it for future use.

        Keyword arguments:
        series_code -- the series code / prefix under which to reserve a new URN

        NB: This will only work if:
        - the ID service supports assignment of serial numbers for the specified series, and
        - if the user has access to this series.

        The created URN is stored in the ID service, but is not attached to any locations.
        """
        if self.sso_token:
            return self.client.service.reserveNextURN(self.sso_token, series_code)
        else:
            raise SsoTokenError("No SSO token available. You need to login first.")

    def reserve_urn(self, urn):
        """ Reserve a URN for future use, without assigning any targets.

        Keyword arguments:
        urn -- the URN to reserve
        
        The URN is stored in the ID service without any associated targets.
        This is only allowed for URNs belonging to a series without serial numbers.
        """
        if self.sso_token:
            return self.client.service.reserveURN(self.sso_token, urn)
        else:
            raise SsoTokenError("No SSO token available. You need to login first.")

    def set_default_url(self, urn, url):
        """ Set a default URL for a URN.
        
        Keyword arguments:
        urn -- the URN to set a default URL for
        url -- the default URL to set for the URN

        The specified URL must be one that is already registered for the URN.
        """
        if self.sso_token:
            return self.client.service.setDefaultURL(self.sso_token, urn, url)
        else:
            raise SsoTokenError("No SSO token available. You need to login first.")

    def get_all_urn_series(self):
        """ Retrieve all series available for the current session. 

        The retrieved objecs contain all known information about the series.
        This call is currently unimplemented on the server side.
        """
        raise NotImplementedError("Not implemented on the server side.")

    def get_version(self):
        """ Returns the current API version.

        This call is currently unimplemented on the server side.
        """
        raise NotImplementedError("Not implemented on the server side.")
