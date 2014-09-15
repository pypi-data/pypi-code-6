# Copyright (c) 2014 Ian C. Good
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

"""Provides an implementation of the |Auth| interface that validates
credentials using a slimta lookup mechanism. If the lookup fields include
``password``, it is assumed to be an `RFC 2307`_ compatible password hash of
the basic format ``{SCHEME}HASH}``. If authentication is successful, the
optional lookup field ``user`` may rewrite the authentication identity.

.. _RFC 2307: http://tools.ietf.org/html/rfc2307

"""

from __future__ import absolute_import

from passlib.apps import ldap_context

from slimta.smtp.auth import Auth, CredentialsInvalidError

__all__ = ['LookupAuth']


class LookupAuth(Auth):
    """Instances of this class may be passed in as the ``auth_obj`` argument of
    :class:`~slimta.edge.smtp.SmtpEdge` or :class:`~slimta.smtp.server.Server`.
    This class is not compatible with ``CRAM-MD5`` or other auth mechanisms
    that require plain text passwords.

    :param lookup: The slimta lookup driver, implementing the
                   :class:`~slimta.lookup.drivers.LookupBase` interface.

    """

    def __init__(self, lookup):
        super(LookupAuth, self).__init__()
        self.lookup = lookup

    def verify_secret(self, authcid, secret, authzid=None):
        ret = self.lookup.lookup_address(authcid, authzid=authzid)
        if not ret or 'password' not in ret:
            raise CredentialsInvalidError()
        if not ldap_context.verify(secret, ret['password']):
            raise CredentialsInvalidError()
        return ret.get('user', authcid)


# vim:et:fdm=marker:sts=4:sw=4:ts=4
