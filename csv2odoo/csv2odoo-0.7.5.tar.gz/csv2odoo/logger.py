# -*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2012 STEPHANE MANGIN. (http://le-spleen.net) All Rights Reserved
#                    Stéphane MANGIN <stephane.mangin@freesbee.fr>
# Copyright (c) 2012 OSIELL SARL. (http://osiell.com) All Rights Reserved
#                    Eric Flaux <contact@osiell.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
################################################################################

import logging
import os
from constants_and_vars import STATS, FORMAT

logging.basicConfig(level=logging.WARNING,
            format=FORMAT,
            #datefmt='%m-%d %H:%M',
            filename=os.path.join(os.getcwd(), "output.log"),
            filemode='w')

formatter = logging.Formatter(FORMAT)
# Syslog handler for total outputting
if syslog:
    syslog_hdlr = logging.handlers.SysLogHandler(
        address=self._syslog_mode,
        facility=logging.handlers.SysLogHandler.LOG_USER
    )
    syslog_hdlr.setLevel(logging.INFO)
    syslog_hdlr.setFormatter(formatter)
    logging.getLogger('').addHandler(syslog_hdlr)

# Finally command line outputting
if not self._opts.quiet or quiet:
    cli_hdlr = logging.StreamHandler()
    cli_hdlr.setFormatter(formatter)
    # In all times, show WARNING and ERROR messages
    cli_hdlr.setLevel(logging.WARNING)

    if self._opts.verbose or verbose:
        cli_hdlr.setLevel(logging.INFO)

    if self._opts.debug or debug:
        cli_hdlr.setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(cli_hdlr)
