# Rekall Memory Forensics
# Copyright 2014 Google Inc. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

"""This module implements profile indexing.

Rekall relies on accurate profiles for reliable analysis of memory artifacts. We
depend on selecting the correct profile from the profile repository, but
sometimes its hard to determine the exact profile to use. For windows, the
profile must match exactly the GUID in the driver.

However, sometimes, the GUID is unavailable or it could be manipulated. In that
case we would like to determine the profile version by applying the index.

The profile repository has an index for each kernel module stored. We can use
this index to determine the exact version of the profile very quickly - even if
the RSDS GUID is not available or incorrect.
"""

__author__ = "Michael Cohen <scudette@google.com>"

from rekall import obj
from rekall import testlib
from rekall.plugins.windows import common


class GuessGUID(common.WindowsCommandPlugin):
    """Try to guess the exact version of a kernel module by using an index."""

    name = "guess_guid"

    @classmethod
    def args(cls, parser):
        super(GuessGUID, cls).args(parser)
        parser.add_argument("module_name", default=None,
                            help="The name of the module to guess.")

    def __init__(self, module_name=None, **kwargs):
        super(GuessGUID, self).__init__(**kwargs)
        self.module = module_name

    def ScanProfile(self):
        """Scan for module using version_scan for RSDS scanning."""
        module_name = self.module.split(".")[0]
        for _, guid in self.session.plugins.version_scan(
            name_regex="^%s.pdb" % module_name).ScanVersions():
            yield obj.NoneObject(), "%s/GUID/%s" % (module_name, guid)

    def LookupIndex(self):
        """Loookup the profile from an index."""
        try:
            index = self.session.LoadProfile("%s/index" % self.module)
        except ValueError:
            return

        cc = self.session.plugins.cc()
        for session in self.session.plugins.sessions().session_spaces():
            # Switch the process context to this session so the address
            # resolver can find the correctly mapped driver.
            with cc:
                cc.SwitchProcessContext(iter(session.processes()).next())

                # Get the image base of the win32k module.
                image_base = self.session.address_resolver.get_address_by_name(
                    self.module)

                for profile in index.LookupIndex(image_base):
                    yield self.session.GetParameter("process_context"), profile

    def GuessProfiles(self):
        """Search for suitable profiles using a variety of methods."""
        # Usually this plugin is invoked from ParameterHooks which will take the
        # first hit. So we try to do the fast methods first, then fall back to
        # the slower methods.
        for x in self.LookupIndex():
            yield x

        # Looking up the index failed because it was not there, or the index did
        # not contain the right profile - fall back to RSDS scanning.
        for x in self.ScanProfile():
            yield x


    def render(self, renderer):
        renderer.table_header([
            ("PID", "context", "20"),
            ("Session", "context", "20"),
            ("Profile", "profile", ""),
            ])
        for context, possibility in self.GuessProfiles():
            renderer.table_row(context.pid, context.SessionId, possibility)


class TestGuessGUID(testlib.SimpleTestCase):
    PARAMETERS = dict(
        commandline="guess_guid win32k"
        )

