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

from optparse import OptionParser

parser = OptionParser()
parser.add_option(u"-f", u"--filename",
                    action=u"store",
                    dest=u"filename",
                    help=u"The CSV file to import.")
parser.add_option(u"-s", u"--separator",
                    action=u"store",
                    dest=u"delimiter",
                    help=u"The delimiter of the CSV file.")
parser.add_option(u"-g", u"--quotechar",
                    action=u"store",
                    dest=u"quotechar",
                    help=u"The quotechar of the CSV file.")
parser.add_option(u"-n", u"--quoting",
                    action=u"store",
                    dest=u"quoting",
                    help=u"The quoting of the CSV file.")
parser.add_option(u"-e", u"--encoding",
                    action=u"store",
                    dest=u"encoding",
                    help=u"The encoding of the CSV file.")
parser.add_option(u"-o", u"--offset",
                    action=u"store",
                    type=u"int",
                    dest=u"offset",
                    default=0,
                    help=u"Offset (Usually used for header omission, default=1)")
parser.add_option(u"-d", u"--debug",
                    action=u"store_true",
                    dest=u"debug",
                    default=False,
                    help=u"debug mode")
parser.add_option(u"-v", u"--verbose",
                    action=u"store_true",
                    dest=u"verbose",
                    default=False,
                    help=u"verbose mode")
parser.add_option(u"-q", u"--quiet",
                    action=u"store_true",
                    dest=u"quiet",
                    default=False,
                    help=u"don't print anything to stdout")
parser.add_option(u"-l", u"--limit",
                    action=u"store",
                    dest=u"limit",
                    type=u"int",
                    default=None,
                    help=u"Limit")
# Connection options
parser.add_option(u"-u", u"--username",
                    action=u"store",
                    dest=u"username",
                    default=u'admin',
                    help=u"Username")
parser.add_option(u"-p", u"--password",
                    action=u"store",
                    dest=u"password",
                    default=u'admin',
                    help=u"Password")
parser.add_option(u"-r", u"--host",
                    action=u"store",
                    dest=u"host",
                    default=u'localhost',
                    help=u"Host to contact")
parser.add_option(u"-t", u"--port",
                    action=u"store",
                    dest=u"port",
                    default=8069,
                    help=u"Port used")
parser.add_option(u"-b", u"--database",
                    action=u"store",
                    dest=u"dbname",
                    default=u'test',
                    help=u"Database name")

(OPTS, ARGS) = parser.parse_args()
