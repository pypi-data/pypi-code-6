# Rekall Memory Forensics
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Authors:
# Michael Cohen <scudette@gmail.com>

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


# This code is loosely based on the original Volatility code, except that it is
# much simpler, since all the information we need is taken directly from the
# profile.

from rekall.plugins.windows import common


class WinSSDT(common.WindowsCommandPlugin):
    """Enumerate the SSDT."""

    name = "ssdt"

    def _find_process_context(self, table_ptr, cc):
        for proc in self.session.plugins.pslist(
            proc_regex="csrss").filter_processes():

            cc.SwitchProcessContext(proc)
            table_ptr.obj_vm = self.session.GetParameter(
                "default_address_space")

            if table_ptr.is_valid():
                break

        return table_ptr

    def _render_x64_table(self, table, renderer):
        resolver = self.session.address_resolver

        for j, entry in enumerate(table):
            function_address = table.obj_offset + (entry >> 4)
            renderer.table_row(
                j, function_address,
                resolver.format_address(
                    function_address,
                    max_distance=0xFFFFFFFFFFFF) or "Unknown")

    def _render_x86_table(self, table, renderer):
        resolver = self.session.address_resolver

        for j, function_address in enumerate(table):
            renderer.table_row(
                j, function_address,
                resolver.format_address(
                    function_address,
                    max_distance=0xFFFFFFFFFFFF) or "Unknown")

    def render(self, renderer):
        # Directly get the SSDT.
        # http://en.wikipedia.org/wiki/System_Service_Dispatch_Table
        ssdt = self.session.address_resolver.get_constant_object(
            "nt!KeServiceDescriptorTableShadow",
            target="_SERVICE_DESCRIPTOR_TABLE")

        cc = self.session.plugins.cc()
        with cc:
            for i, descriptor in enumerate(ssdt.Descriptors):
                table_ptr = descriptor.KiServiceTable
                if not table_ptr.is_valid():
                    table_ptr = self._find_process_context(table_ptr, cc)

                table = table_ptr.deref()
                renderer.section("Table %s @ %#x" % (i, table_ptr.v()))

                renderer.table_header([("Entry", "entry", "[addr]"),
                                       ("Target", "target", "[addrpad]"),
                                       ("Symbol", "symbol", "")])

                if self.profile.metadata("arch") == "AMD64":
                    self._render_x64_table(table, renderer)
                else:
                    self._render_x86_table(table, renderer)
