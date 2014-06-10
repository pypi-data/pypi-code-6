# -*- coding: utf-8 -*-

#    Copyright (C) 2013 Rackspace Hosting Inc. All Rights Reserved.
#    Copyright (C) 2013 Yahoo! Inc. All Rights Reserved.
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

import abc

import six

from taskflow.utils import misc


@six.add_metaclass(abc.ABCMeta)
class JobBoard(object):
    """A jobboard is an abstract representation of a place where jobs
    can be posted, reposted, claimed and transferred. There can be multiple
    implementations of this job board, depending on the desired semantics and
    capabilities of the underlying jobboard implementation.
    """

    def __init__(self, name, conf):
        self._name = name
        self._conf = conf

    @abc.abstractmethod
    def iterjobs(self, only_unclaimed=False, ensure_fresh=False):
        """Returns an iterator that will provide back jobs that are currently
        on this jobboard.

        NOTE(harlowja): the ordering of this iteration should be by posting
        order (oldest to newest) if possible, but it is left up to the backing
        implementation to provide the order that best suits it (so don't depend
        on it always being oldest to newest).

        NOTE(harlowja): the iterator that is returned may support other
        attributes which can be used to further customize how iteration can
        be accomplished; check with the backends iterator object to determine
        what other attributes are supported.

        :param only_unclaimed: boolean that indicates whether to only iteration
            over unclaimed jobs.
        :param ensure_fresh: boolean that requests to only iterate over the
            most recent jobs available, where the definition of what is recent
            is backend specific. It is allowable that a backend may ignore this
            value if the backends internal semantics/capabilities can not
            support this argument.
        """

    @abc.abstractmethod
    def wait(self, timeout=None):
        """Waits a given amount of time for job/s to be posted, when jobs are
        found then an iterator will be returned that contains the jobs at
        the given point in time.

        NOTE(harlowja): since a jobboard can be mutated on by multiple external
        entities at the *same* time the iterator that can be returned *may*
        still be empty due to other entities removing those jobs after the
        iterator has been created (be aware of this when using it).

        :param timeout: float that indicates how long to wait for a job to
            appear (if None then waits forever).
        """

    @abc.abstractproperty
    def job_count(self):
        """Returns how many jobs are on this jobboard (this count may change as
        new jobs appear or are removed).
        """

    @abc.abstractmethod
    def find_owner(self, job):
        """Gets the owner of the job if one exists."""

    @property
    def name(self):
        """The non-uniquely identifying name of this jobboard."""
        return self._name

    @abc.abstractmethod
    def consume(self, job, who):
        """Permanently (and atomically) removes a job from the jobboard,
        signaling that this job has been completed by the entity assigned
        to that job.

        Only the entity that has claimed that job is able to consume a job.

        A job that has been consumed can not be reclaimed or reposted by
        another entity (job postings are immutable). Any entity consuming
        a unclaimed job (or a job they do not have a claim on) will cause an
        exception.

        :param job: a job on this jobboard that can be consumed (if it does
            not exist then a NotFound exception will be raised).
        :param who: string that names the entity performing the consumption,
            this must be the same name that was used for claiming this job.
        """

    @abc.abstractmethod
    def post(self, name, book, details=None):
        """Atomically creates and posts a job to the jobboard, allowing others
        to attempt to claim that job (and subsequently work on that job). The
        contents of the provided logbook must provide enough information for
        others to reference to construct & work on the desired entries that
        are contained in that logbook.

        Once a job has been posted it can only be removed by consuming that
        job (after that job is claimed). Any entity can post/propose jobs
        to the jobboard (in the future this may be restricted).

        Returns a job object representing the information that was posted.
        """

    @abc.abstractmethod
    def claim(self, job, who):
        """Atomically attempts to claim the given job for the entity and either
        succeeds or fails at claiming by throwing corresponding exceptions.

        If a job is claimed it is expected that the entity that claims that job
        will at sometime in the future work on that jobs flows and either fail
        at completing them (resulting in a reposting) or consume that job from
        the jobboard (signaling its completion).

        :param job: a job on this jobboard that can be claimed (if it does
            not exist then a NotFound exception will be raised).
        :param who: string that names the claiming entity.
        """

    @abc.abstractmethod
    def abandon(self, job, who):
        """Atomically abandons the given job on the jobboard, allowing that job
        to be reclaimed by others. This would typically occur if the entity
        that has claimed the job has failed or is unable to complete the job
        or jobs it has claimed.

        Only the entity that has claimed that job can abandon a job. Any entity
        abandoning a unclaimed job (or a job they do not own) will cause an
        exception.

        :param job: a job on this jobboard that can be abandoned (if it does
            not exist then a NotFound exception will be raised).
        :param who: string that names the entity performing the abandoning,
            this must be the same name that was used for claiming this job.
        """

    @abc.abstractproperty
    def connected(self):
        """Returns if this jobboard is connected."""

    @abc.abstractmethod
    def connect(self):
        """Opens the connection to any backend system."""

    @abc.abstractmethod
    def close(self):
        """Close the connection to any backend system.

        Once closed the jobboard can no longer be used (unless reconnection
        occurs).
        """


# Jobboard events
POSTED = 'POSTED'  # new job is/has been posted
REMOVAL = 'REMOVAL'  # existing job is/has been removed


class NotifyingJobBoard(JobBoard):
    """A jobboard subclass that can notify about jobs being created
    and removed, which can remove the repeated usage of iterjobs() to achieve
    the same operation.

    NOTE(harlowja): notifications that are emitted *may* be emitted on a
    separate dedicated thread when they occur, so ensure that all callbacks
    registered are thread safe.
    """
    def __init__(self, name, conf):
        super(NotifyingJobBoard, self).__init__(name, conf)
        self.notifier = misc.Notifier()
