#!/usr/bin/python
# -*- coding: utf-8 -*-

# Libervia: a Salut à Toi frontend
# Copyright (C) 2013  Emmanuel Gil Peyrot <linkmauve@linkmauve.fr>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from twisted.internet import defer
if defer.Deferred.debug:
    # if we are in debug mode, we want to use ipdb instead of pdb
    try:
        import ipdb
        import pdb
        pdb.set_trace = ipdb.set_trace
        pdb.post_mortem = ipdb.post_mortem
    except ImportError:
        pass

import os.path

from libervia.server.constants import Const as C

from sat.core.i18n import _
from sat.tools.config import getConfig

from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError


def coerceConnectionType(value):  # called from Libervia.OPT_PARAMETERS
    allowed_values = ('http', 'https', 'both')
    if value not in allowed_values:
        raise ValueError("%(given)s not in %(expected)s" % {'given': value, 'expected': str(allowed_values)})
    return value

def coerceDataDir(value):  # called from Libervia.OPT_PARAMETERS
    html = os.path.join(value, C.HTML_DIR)
    if not os.path.isfile(os.path.join(html, 'libervia.html')):
        raise ValueError("%s is not a Libervia's browser HTML directory" % os.path.realpath(html))
    server_css = os.path.join(value, C.SERVER_CSS_DIR)
    if not os.path.isfile(os.path.join(server_css, 'blog.css')):
        raise ValueError("%s is not a Libervia's server data directory" % os.path.realpath(server_css))
    return value

DATA_DIR_DEFAULT = ''
OPT_PARAMETERS_BOTH = [['connection_type', 't', 'https', _(u"'http', 'https' or 'both' (to launch both servers).").encode('utf-8'), coerceConnectionType],
                       ['port', 'p', 8080, _(u'The port number to listen HTTP on.').encode('utf-8'), int],
                       ['port_https', 's', 8443, _(u'The port number to listen HTTPS on.').encode('utf-8'), int],
                       ['port_https_ext', 'e', 0, _(u'The external port number used for HTTPS (0 means port_https value).').encode('utf-8'), int],
                       ['ssl_certificate', 'c', 'libervia.pem', _(u'PEM certificate with both private and public parts.').encode('utf-8'), str],
                       ['redirect_to_https', 'r', 1, _(u'Automatically redirect from HTTP to HTTPS.').encode('utf-8'), int],
                       ['security_warning', 'w', 1, _(u'Warn user that he is about to connect on HTTP.').encode('utf-8'), int],
                       ['passphrase', 'k', '', (_(u"Passphrase for the SàT profile named '%s'") % C.SERVICE_PROFILE).encode('utf-8'), str],
                       ['data_dir', 'd', DATA_DIR_DEFAULT, _(u'Data directory for Libervia').encode('utf-8'), coerceDataDir],
                      ]  # options which are in sat.conf and on command line, see https://twistedmatrix.com/documents/current/api/twisted.python.usage.Options.html
OPT_PARAMETERS_CFG = [['empty_password_allowed_warning_dangerous_list', None, '', None]]  # Options which are in sat.conf only

def initialise(options):
    """Method to initialise global modules"""
    from twisted.internet import glib2reactor
    glib2reactor.install()
    # XXX: We need to configure logs before any log method is used, so here is the best place.
    from sat.core import log_config
    log_config.satConfigure(C.LOG_BACKEND_TWISTED, C, backend_data=options)
    from libervia.server import server
    # we can't import this file from libervia.server.server because it's not a true module
    # (there is no __init__.py file, as required by twistd plugin system), so we set the
    # global values from here
    server.DATA_DIR_DEFAULT = DATA_DIR_DEFAULT
    server.OPT_PARAMETERS_BOTH = OPT_PARAMETERS_BOTH
    server.OPT_PARAMETERS_CFG = OPT_PARAMETERS_CFG
    server.coerceDataDir = coerceDataDir


class Options(usage.Options):
    # optArgs is not really useful in our case, we need more than a flag
    optParameters = OPT_PARAMETERS_BOTH

    def __init__(self):
        """Read SàT configuration file in order to overwrite the hard-coded default values.

        Priority for the usage of the values is (from lowest to highest):
            - hard-coded default values
            - values from SàT configuration files
            - values passed on the command line
        """
        # If we do it the reading later: after the command line options have been parsed, there's no good way to know
        # if the  options values are the hard-coded ones or if they have been passed on the command line.

        # FIXME: must be refactored + code can be factorised with backend
        config = SafeConfigParser()
        config.read(C.CONFIG_FILES)
        for param in self.optParameters + OPT_PARAMETERS_CFG:
            name = param[0]
            try:
                value = getConfig(config, 'libervia', name)
                try:
                    param[2] = param[4](value)
                except IndexError: # the coerce method is optional
                    param[2] = value
            except (NoSectionError, NoOptionError):
                pass
        usage.Options.__init__(self)


class LiberviaMaker(object):
    implements(IServiceMaker, IPlugin)

    tapname = C.APP_NAME_FILE
    description = _(u'The web frontend of Salut à Toi')
    options = Options

    def makeService(self, options):
        initialise(options.parent)
        from libervia.server import server
        return server.Libervia(**dict(options))  # get rid of the usage.Option overload


# affectation to some variable is necessary for twisted introspection to work
serviceMaker = LiberviaMaker()
