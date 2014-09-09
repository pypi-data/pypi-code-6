#! /usr/bin/python
# -*- coding: utf-8 -*-

# jp: a SAT command line tool
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014 Jérôme Poisson (goffi@goffi.org)
# Copyright (C) 2013, 2014 Adrien Cossa (souliane@mailoo.org)

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


import base
from sat.core.i18n import _

__commands__ = ["Params"]


class SaveTemplate(base.CommandBase):
    def __init__(self, host):
        super(SaveTemplate, self).__init__(host, 'save', use_profile=False, help=_('Save parameters template to xml file'))

    def add_parser_options(self):
        self.parser.add_argument("filename", type=str, help=_("Output file"))

    def run(self):
        """Save parameters template to xml file"""
        if self.host.bridge.saveParamsTemplate(self.args.filename):
            print _("Parameters saved to file %s") % self.args.filename
        else:
            print _("Can't save parameters to file %s") % self.args.filename


class LoadTemplate(base.CommandBase):

    def __init__(self, host):
        super(LoadTemplate, self).__init__(host, 'load', use_profile=False, help=_('Load parameters template from xml file'))

    def add_parser_options(self):
        self.parser.add_argument("filename", type=str, help=_("Input file"))

    def run(self):
        """Load parameters template from xml file"""
        if self.host.bridge.loadParamsTemplate(self.args.filename):
            print _("Parameters loaded from file %s") % self.args.filename
        else:
            print _("Can't load parameters from file %s") % self.args.filename


class Params(base.CommandBase):
    subcommands = (SaveTemplate, LoadTemplate)

    def __init__(self, host):
        super(Params, self).__init__(host, 'params', use_profile=False, help=_('Save/load parameters template'))
