"""
.. module:: ldap_groups.groups
    :synopsis: LDAP Groups Group Objects.

    ldap-groups is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ldap-groups is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser Public License for more details.

    You should have received a copy of the GNU Lesser Public License
    along with ldap-groups. If not, see <http://www.gnu.org/licenses/>.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import ldap
import logging

from .exceptions import ObjectDoesNotExist, ImproperlyConfigured

logger = logging.getLogger(__name__)


class ADGroup:
    """Add members to, remove members from, and view members of Active Directory groups."""


    def __init__(self, group_dn, server_uri=None, base_dn=None, user_lookup_attr=None, attr_list=None, bind_dn=None, bind_password=None):
        """ Create an AD group object and establish an ldap search connection.
            Any arguments other than group_dn are pulled from django settings
            if they aren't passed in.

        :param group_dn: The distinguished name of the active directory group to be modified.
        :type group_dn: str
        
        :param server_uri: (Required) The ldap server uri. Pulled from Django settings if None.
        :type server_uri: str
        :param base_dn: (Required) The ldap base dn. Pulled from Django settings if None.
        :type base_dn: str
        :param user_lookup_attr: The attribute used in user searches. Default is 'sAMAccountName'.
        :type user_lookup_attr: str
        :param attr_list: A list of attributes to be pulled for each member of the AD group.
        :type attr_list: list
        :param bind_dn: A user used to bind to the AD. Necessary for any group modifications.
        :type bind_dn: str
        :param bind_password: The bind user's password. Necessary for any group modifications.
        :type bind_password: str

        """
        
        # Attempt to grab settings from Django, fall back to init arguments if django is not used
        try:
            from django.conf import settings
        except ImportError:
            if not (server_uri and base_dn):
                raise ImproperlyConfigured("A server_uri and base_dn must be passed as arguments if django settings are not used.")
            else:
                self.server_uri = server_uri
                self.base_dn = base_dn
            
            self.user_lookup_attr = user_lookup_attr if user_lookup_attr else 'sAMAccountName'
            self.attr_list = attr_list if attr_list else ['displayName', 'sAMAccountName', 'distinguishedName']
            
            self.bind_dn = bind_dn
            self.bind_password = bind_password
        else:
            if hasattr(settings, 'LDAP_GROUPS_SERVER_URI') and hasattr(settings, 'LDAP_GROUPS_BASE_DN'):
                if not server_uri:
                    self.server_uri = getattr(settings, 'LDAP_GROUPS_SERVER_URI')
                if not base_dn:
                    self.base_dn = getattr(settings, 'LDAP_GROUPS_BASE_DN')
            else:
                raise ImproperlyConfigured("LDAP Groups required settings LDAP_GROUPS_SERVER_URI and LDAP_GROUPS_BASE_DN are not configured in django settings file.")
        
            if not user_lookup_attr:
                self.user_lookup_attr = getattr(settings, 'LDAP_GROUPS_USER_LOOKUP_ATTRIBUTE', 'sAMAccountName')
            
            if not attr_list:
                self.attr_list = getattr(settings, 'LDAP_GROUPS_ATTRIBUTE_LIST', ['displayName', 'sAMAccountName', 'distinguishedName'])
            
            if not bind_dn:
                self.bind_dn = getattr(settings, 'LDAP_GROUPS_BIND_DN', None)
            
            if not bind_password:
                self.bind_password = getattr(settings, 'LDAP_GROUPS_BIND_PASSWORD', None)
        
        # Initialize search objects
        self.USER_SEARCH = {
            'base_dn': self.base_dn,
            'scope': ldap.SCOPE_SUBTREE,
            'filter_string': "(&(objectClass=user)(" + self.user_lookup_attr + "=%s))",
            'attribute_list': ['distinguishedName']
        }

        self.GROUP_MEMBER_SEARCH = {
            'base_dn': self.base_dn,
            'scope': ldap.SCOPE_SUBTREE,
            'filter_string': "(&(objectCategory=user)(memberOf=%s))",
            'attribute_list': self.attr_list
        }
        

        self.group_dn = group_dn        
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)
        self.ldap_connection = ldap.initialize(self.server_uri)

        if self.bind_dn and self.bind_password:
            self.ldap_connection.simple_bind_s(self.bind_dn, self.bind_password)
        else:
            logger.warning("LDAP Bind Credentials are not set. Group modification methods will most likely fail.")
            self.ldap_connection.simple_bind_s()

    def __del__(self):
        """Close the LDAP connection."""

        self.ldap_connection.unbind_s()

    def _get_user_dn(self, account_name):
        """ Search for a user and retrieve his distinguished name.

        :param account_name: The user's active directory account name.
        :type account_name: str

        :raises: **ObjectDoesNotExist** if the provided alias doesn't exist in the active directory.

        """

        try:
            try:
                return self.ldap_connection.search_s(self.USER_SEARCH['base_dn'], self.USER_SEARCH['scope'], self.USER_SEARCH['filter_string'] % account_name, self.USER_SEARCH['attribute_list'])[0][-1]['distinguishedName'][0]
            except ldap.OPERATIONS_ERROR, error_message:
                raise ImproperlyConfigured("The LDAP server does not accept anonymous connections: \n\t%s" % error_message[0]['info'])
        except (TypeError, IndexError):
            raise ObjectDoesNotExist("The alias provided does not exist in the Active Directory.")

    def _get_group_members(self):
        """ Search for a group and retrieve its members.

        :raises: **ObjectDoesNotExist** if the provided alias doesn't exist in the active directory.

        """

        try:
            results = self.ldap_connection.search_s(self.GROUP_MEMBER_SEARCH['base_dn'], self.GROUP_MEMBER_SEARCH['scope'], self.GROUP_MEMBER_SEARCH['filter_string'] % self.group_dn, self.GROUP_MEMBER_SEARCH['attribute_list'])
        except ldap.OPERATIONS_ERROR, error_message:
            raise ImproperlyConfigured("The LDAP server does not accept anonymous connections: \n\t%s" % error_message[0]['info'])
        else:
            if not results:
                raise ObjectDoesNotExist("The group provided does not exist in the Active Directory.")

            return results

    def add_member(self, account_name):
        """ Attempt to add a member to the AD group.

        :param account_name: The user's active directory account name.
        :type account_name: str

        :raises: **ObjectDoesNotExist** if the provided alias doesn't exist in the active directory. (inherited from get_user_dn)

        """

        add_member = [(ldap.MOD_ADD, 'member', self._get_user_dn(account_name))]

        try:
            self.ldap_connection.modify_s(self.group_dn, add_member)
        except ldap.LDAPError, error_message:
            logger.error("Error adding user '%s' to group '%s': %s" % (account_name, self.group_dn, error_message))

    def remove_member(self, account_name):
        """ Attempt to remove a member from the AD group.

        :param account_name: The user's active directory account name.
        :type account_name: str

        :raises: **ObjectDoesNotExist** if the provided alias doesn't exist in the active directory. (inherited from get_user_dn)

        """

        remove_member = [(ldap.MOD_DELETE, 'member', self._get_user_dn(account_name))]

        try:
            self.ldap_connection.modify_s(self.group_dn, remove_member)
        except ldap.LDAPError, error_message:
            logger.error("Error removing user '%s' from group '%s': %s" % (account_name, self.group_dn, error_message))

    def get_member_info(self):
        """ Retrieves member information from the AD group object.

        :returns: A dictionary of information on members of the AD group based on the LDAP_GROUPS_ATTRIBUTE_LIST setting.

        """

        member_info = []

        for member in self._get_group_members():
            if member[0]:
                info_dict = {}

                for attribute in self.GROUP_MEMBER_SEARCH['attribute_list']:
                    info_dict.update({attribute: member[-1][attribute][0]})

                member_info.append(info_dict)

        return member_info
