"""
python-glibc based pure-python select.py

Only features in scope for Linux are implemented. Obsolete select/poll
interfaces are not implemented.
"""
from ctypes import POINTER
from ctypes import byref
from ctypes import cast

from glibc import EPOLLERR
from glibc import EPOLLET
from glibc import EPOLLHUP
from glibc import EPOLLIN
from glibc import EPOLLMSG
from glibc import EPOLLONESHOT
from glibc import EPOLLOUT
from glibc import EPOLLPRI
from glibc import EPOLLRDBAND
from glibc import EPOLLRDHUP
from glibc import EPOLLRDNORM
from glibc import EPOLLWRBAND
from glibc import EPOLLWRNORM
from glibc import EPOLL_CLOEXEC
from glibc import EPOLL_CTL_ADD
from glibc import EPOLL_CTL_DEL
from glibc import EPOLL_CTL_MOD
from glibc import FD_SETSIZE
from glibc import close
from glibc import epoll_create1
from glibc import epoll_ctl
from glibc import epoll_event
from glibc import epoll_wait

__all__ = ['epoll', 'EPOLL_CLOEXEC', 'EPOLLIN', 'EPOLLOUT', 'EPOLLPRI',
           'EPOLLERR', 'EPOLLHUP', 'EPOLLET', 'EPOLLONESHOT', 'EPOLLRDNORM',
           'EPOLLRDBAND', 'EPOLLWRNORM', 'EPOLLWRBAND', 'EPOLLMSG']

# Extra features not present in python3.4
__all__ += ['EPOLLRDHUP']


class epoll(object):
    """
    Linux's epoll-based poll
    """

    def __init__(self, sizehint=-1, flags=0):
        """
        :param sizehint:
            Dummy argument for compatibility with select.epoll, ignored.
        :param flags:
            Flags passed to ``epoll_create1()``. You always want to pass
            EPOLL_CLOEXEC here but it is not default for compatibility with
            python's stdlib.
        """
        self._fd = -1
        self._fd = epoll_create1(flags)

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def close(self):
        if not self.closed:
            close(self._fd)

    @property
    def closed(self):
        return self._fd == -1

    def fileno(self):
        """
        Descriptor number of the underlying epoll object
        """
        return self._fd

    @classmethod
    def fromfd(cls, fd):
        self = cls.__new__()
        object.__init__(self)
        self._fd = fd
        return self

    def register(self, fd, eventmask=None):
        """
        Registers a new fd or raises an OSError if the fd is already
        registered.  fd is the target file descriptor of the operation.  events
        is a bit set composed of the various EPOLL constants; the default is
        EPOLL_IN | EPOLL_OUT | EPOLL_PRI.

        The epoll interface supports all file descriptors that support poll.
        """
        if eventmask is None:
            eventmask = EPOLLIN | EPOLLOUT | EPOLLPRI
        ev = epoll_event()
        ev.events = eventmask
        # NOTE: we're not using 64 bits of user data that we might be using
        # here. Perhaps we could do that to somehow save resources?
        epoll_ctl(self._fd, EPOLL_CTL_ADD, fd, byref(ev))

    def unregister(self, fd):
        ev = epoll_event()
        epoll_ctl(self._fd, EPOLL_CTL_DEL, fd, byref(ev))

    def modify(self, fd, eventmask):
        ev = epoll_event()
        ev.events = eventmask
        epoll_ctl(self._fd, EPOLL_CTL_MOD, fd, byref(ev))

    def poll(self, timeout=-1, maxevents=-1):
        if timeout != -1:
            # 1000.0 because epoll_wait2) wants milliseconds
            timeout = int(timeout * 1000.0)
        if maxevents == -1:
            maxevents = FD_SETSIZE - 1
        events = (epoll_event * maxevents)()
        num_events = epoll_wait(
            self._fd, cast(byref(events)), POINTER(epoll_event),
            maxevents, timeout)
        return [(events[i].data.fd, events[i].events)
                for i in range(num_events)]
