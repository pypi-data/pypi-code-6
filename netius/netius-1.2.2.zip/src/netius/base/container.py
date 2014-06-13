#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Netius System
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Netius System.
#
# Hive Netius System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Netius System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Netius System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

from netius.base import server

from netius.base.common import * #@UnusedWildImport

class Container(Base):

    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)
        self.owner = None
        self.bases = []

    def __del__(self):
        Base.__del__(self)
        self.debug("Container (%s) '%s' deleted from memory" % (self.name, self._uuid))

    def start(self, owner):
        # registers for the start event on the current container so that when
        # the start operation is completed the proper propagation may occur
        self.bind("start", self.on_start)

        # sets the current polling structure of the owner in the container
        # it's important to use the already initialized poll in the container
        # so that the requested environment (host, port , etc.) is used note
        # that event the same logger is used for the container (logic propagation)
        self.owner = owner
        self.poll_c = owner.poll_c
        self.poll = owner.poll
        self.poll_name = owner.poll_name
        self.poll_timeout = owner.poll_timeout
        self.level = owner.level
        self.logger = owner.logger
        self._loaded = True

        # runs the starting operation in the complete set of base structures
        # registered under the container, this is the required operation in
        # order to propagate the changed in the container to the bases
        self.start_all()

        # calls the super method of the base for the current container this should
        # start the event loop for the container (blocking call)
        Base.start(self)

    def cleanup(self):
        Base.cleanup(self)

        # unsets the owner of the container, this should diminish the chance of
        # memory leaks due to cycle references (required to avoid problems)
        self.owner = None

        # iterates over all the bases registered and propagates the cleanup operation
        # over them, deleting the list of bases afterwards (no more usage for them)
        for base in self.bases: base.cleanup()
        del self.bases[:]

        # unbinds the start operation from the on start event, as this is no longer
        # required, should re-register for it on "next start" event
        self.unbind("start", self.on_start)

    def loop(self):
        # iterates continuously while the running flag
        # is set, once it becomes unset the loop breaks
        # at the next execution cycle
        while self._running:
            # calls the base tick int handler indicating that a new
            # tick loop iteration is going to be started, all the
            # "in between loop" operation should be performed in this
            # callback as this is the "space" they have for execution
            self.ticks()

            # updates the current state to poll to indicate
            # that the base service is selecting the connections
            self.set_state(STATE_POLL)

            # runs the "owner" based version of the poll operation
            # so that the poll results are indexed by their owner
            # reference to be easily routed to the base services
            result = self.poll.poll_owner()
            for base, values in result.items():
                reads, writes, errors = values
                base.reads(reads)
                base.writes(writes)
                base.errors(errors)

    def ticks(self):
        self.set_state(STATE_TICK)
        self._lid = (self._lid + 1) % 2147483647
        for base in self.bases: base.ticks()

    def on_start(self, service):
        self.apply_all()
        self.trigger_all("start")

    def on_stop(self, service):
        self.trigger_all("stop")

    def add_base(self, base):
        self.apply_base(base)
        self.bases.append(base)

    def remove_base(self, base):
        self.bases.remove(base)

    def start_base(self, base):
        base.level = self.level
        base.logger = self.logger
        base.load()

    def start_all(self):
        for base in self.bases: self.start_base(base)

    def apply_all(self):
        for base in self.bases: self.apply_base(base)

    def apply_base(self, base):
        base.tid = self.tid
        base.poll = self.poll

    def trigger_all(self, name, *args, **kwargs):
        for base in self.bases: base.trigger(name, base, *args, **kwargs)

class ContainerServer(server.StreamServer):

    def __init__(self, *args, **kwargs):
        server.StreamServer.__init__(self, *args, **kwargs)
        self.container = Container(*args, **kwargs)
        self.add_base(self)

    def start(self):
        # starts the container this should trigger the start of the
        # event loop in the container and the proper listening of all
        # the connections in the current environment
        self.container.start(self)

    def stop(self):
        # verifies if there's a container object currently defined in
        # the object and in case it does exist propagates the stop call
        # to the container so that the proper stop operation is performed
        if not self.container: return
        self.container.stop()

    def cleanup(self):
        server.StreamServer.cleanup(self)
        self.container = None

    def add_base(self, base):
        self.container.add_base(base)
