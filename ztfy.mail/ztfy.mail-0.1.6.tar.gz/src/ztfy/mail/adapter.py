#
# Copyright (c) 2012 Thierry Florac <tflorac AT onf.fr>
# All Rights Reserved.
#


# import standard packages

# import Zope3 interfaces
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from zope.security.interfaces import IPrincipal

# import local interfaces
from ztfy.mail.interfaces import IPrincipalMailInfo

# import Zope3 packages
from zope.component import getUtilitiesFor

# import local packages


def getPrincipalAddress(principal):
    """Get email address of given principal"""
    if IPrincipal.providedBy(principal):
        principal = principal.id
    for _name, plugin in getUtilitiesFor(IAuthenticatorPlugin):
        principal_info = plugin.principalInfo(principal)
        if principal_info is not None:
            principal_email = IPrincipalMailInfo(principal_info, None)
            if principal_email is not None:
                return principal_email.getAddresses()
