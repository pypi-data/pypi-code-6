# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Red Hat, Inc.
# All Rights Reserved.
# Copyright 2013 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
gettext for openstack-common modules.

Usual usage in an openstack.common module:

    from os_collect_config.openstack.common.gettextutils import _
"""

import copy
import gettext
import logging.handlers
import os
import UserString

_localedir = os.environ.get('os_collect_config'.upper() + '_LOCALEDIR')
_t = gettext.translation('os_collect_config', localedir=_localedir, fallback=True)


def _(msg):
    return _t.ugettext(msg)


def install(domain):
    """Install a _() function using the given translation domain.

    Given a translation domain, install a _() function using gettext's
    install() function.

    The main difference from gettext.install() is that we allow
    overriding the default localedir (e.g. /usr/share/locale) using
    a translation-domain-specific environment variable (e.g.
    NOVA_LOCALEDIR).
    """
    gettext.install(domain,
                    localedir=os.environ.get(domain.upper() + '_LOCALEDIR'),
                    unicode=True)


"""
Lazy gettext functionality.

The following is an attempt to introduce a deferred way
to do translations on messages in OpenStack. We attempt to
override the standard _() function and % (format string) operation
to build Message objects that can later be translated when we have
more information. Also included is an example LogHandler that
translates Messages to an associated locale, effectively allowing
many logs, each with their own locale.
"""


def get_lazy_gettext(domain):
    """Assemble and return a lazy gettext function for a given domain.

    Factory method for a project/module to get a lazy gettext function
    for its own translation domain (i.e. nova, glance, cinder, etc.)
    """

    def _lazy_gettext(msg):
        """Create and return a Message object.

        Message encapsulates a string so that we can translate it later when
        needed.
        """
        return Message(msg, domain)

    return _lazy_gettext


class Message(UserString.UserString, object):
    """Class used to encapsulate translatable messages."""
    def __init__(self, msg, domain):
        # _msg is the gettext msgid and should never change
        self._msg = msg
        self._left_extra_msg = ''
        self._right_extra_msg = ''
        self.params = None
        self.locale = None
        self.domain = domain

    @property
    def data(self):
        # NOTE(mrodden): this should always resolve to a unicode string
        # that best represents the state of the message currently

        localedir = os.environ.get(self.domain.upper() + '_LOCALEDIR')
        if self.locale:
            lang = gettext.translation(self.domain,
                                       localedir=localedir,
                                       languages=[self.locale],
                                       fallback=True)
        else:
            # use system locale for translations
            lang = gettext.translation(self.domain,
                                       localedir=localedir,
                                       fallback=True)

        full_msg = (self._left_extra_msg +
                    lang.ugettext(self._msg) +
                    self._right_extra_msg)

        if self.params is not None:
            full_msg = full_msg % self.params

        return unicode(full_msg)

    def _save_parameters(self, other):
        # we check for None later to see if
        # we actually have parameters to inject,
        # so encapsulate if our parameter is actually None
        if other is None:
            self.params = (other, )
        else:
            self.params = copy.deepcopy(other)

        return self

    # overrides to be more string-like
    def __unicode__(self):
        return self.data

    def __str__(self):
        return self.data.encode('utf-8')

    def __getstate__(self):
        to_copy = ['_msg', '_right_extra_msg', '_left_extra_msg',
                   'domain', 'params', 'locale']
        new_dict = self.__dict__.fromkeys(to_copy)
        for attr in to_copy:
            new_dict[attr] = copy.deepcopy(self.__dict__[attr])

        return new_dict

    def __setstate__(self, state):
        for (k, v) in state.items():
            setattr(self, k, v)

    # operator overloads
    def __add__(self, other):
        copied = copy.deepcopy(self)
        copied._right_extra_msg += other.__str__()
        return copied

    def __radd__(self, other):
        copied = copy.deepcopy(self)
        copied._left_extra_msg += other.__str__()
        return copied

    def __mod__(self, other):
        # do a format string to catch and raise
        # any possible KeyErrors from missing parameters
        self.data % other
        copied = copy.deepcopy(self)
        return copied._save_parameters(other)

    def __mul__(self, other):
        return self.data * other

    def __rmul__(self, other):
        return other * self.data

    def __getitem__(self, key):
        return self.data[key]

    def __getslice__(self, start, end):
        return self.data.__getslice__(start, end)

    def __getattribute__(self, name):
        # NOTE(mrodden): handle lossy operations that we can't deal with yet
        # These override the UserString implementation, since UserString
        # uses our __class__ attribute to try and build a new message
        # after running the inner data string through the operation.
        # At that point, we have lost the gettext message id and can just
        # safely resolve to a string instead.
        ops = ['capitalize', 'center', 'decode', 'encode',
               'expandtabs', 'ljust', 'lstrip', 'replace', 'rjust', 'rstrip',
               'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
        if name in ops:
            return getattr(self.data, name)
        else:
            return UserString.UserString.__getattribute__(self, name)


class LocaleHandler(logging.Handler):
    """Handler that can have a locale associated to translate Messages.

    A quick example of how to utilize the Message class above.
    LocaleHandler takes a locale and a target logging.Handler object
    to forward LogRecord objects to after translating the internal Message.
    """

    def __init__(self, locale, target):
        """Initialize a LocaleHandler

        :param locale: locale to use for translating messages
        :param target: logging.Handler object to forward
                       LogRecord objects to after translation
        """
        logging.Handler.__init__(self)
        self.locale = locale
        self.target = target

    def emit(self, record):
        if isinstance(record.msg, Message):
            # set the locale and resolve to a string
            record.msg.locale = self.locale

        self.target.emit(record)
