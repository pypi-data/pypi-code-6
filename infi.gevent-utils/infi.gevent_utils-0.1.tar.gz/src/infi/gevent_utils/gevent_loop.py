import gevent
from gevent.event import Event
from infi.pyutils.contexts import contextmanager

from .safe_greenlets import uncaught_greenlet_exception_context


class GeventLoopBase(object):
    """A base class for implementing an operation that sleeps for `interval` between callback executions."""
    def __init__(self, interval):
        super(GeventLoopBase, self).__init__()
        self._interval = interval
        self._stop_event = None
        self._greenlet = None

    def _loop(self):
        """Main loop - used internally."""
        while True:
            try:
                with uncaught_greenlet_exception_context():
                    self._loop_callback()
            except gevent.GreenletExit:
                break
            if self._stop_event.wait(self._interval):
                break

    def _loop_callback(self):
        """Subclasses should implement this function - called every loop iteration."""
        raise NotImplementedError()

    def start(self):
        assert not self.has_started(), "called start() on an active GeventLoop"
        self._stop_event = Event()
        # note that we don't use safe_greenlets.spawn because we take care of it in _loop by ourselves
        self._greenlet = gevent.spawn(self._loop)

    def stop(self):
        assert self.has_started(), "called stop() on a non-active GeventLoop"
        self._stop_event.set()
        if gevent.getcurrent() != self._greenlet:
            self._greenlet.join()
            self._clear()

    def kill(self):
        assert self.has_started(), "called kill() on a non-active GeventLoop"
        self._stop_event.set()
        self._greenlet.kill()
        self._clear()

    def join(self, timeout):
        assert self.has_started(), "called join() on a non-active GeventLoop"
        self._greenlet.join(timeout=timeout)
        if self._greenlet.ready():
            self._clear()
            return True
        return False

    def has_started(self):
        return self._greenlet is not None

    def _clear(self):
        self._greenlet = None
        self._stop_event = None


class GeventLoop(GeventLoopBase):
    """Loop class that expects an interval and a callback. A more usable scenario is to use `do_in_background`.

    For example:

    ```
    def do_some_period_maintenance():
        ...

    maintenance_job = GeventLoop(5, do_some_period_maintenance)
    maintenance_job.start()
    maintenance_job.stop()
    ```
    """
    def __init__(self, interval, callback):
        super(GeventLoop, self).__init__(interval)
        self._callback = callback

    def _loop_callback(self):
        self._callback()

    def __repr__(self):
        return "GeventLoop(interval={}, callback={!r})".format(self._interval, self._callback)


@contextmanager
def loop_in_background(interval, callback):
    """
    When entering the context, spawns a greenlet that sleeps for `interval` seconds between `callback` executions.
    When leaving the context stops the greenlet.
    The yielded object is the `GeventLoop` object so the loop can be stopped from within the context.

    For example:
    ```
    with loop_in_background(60.0, purge_cache) as purge_cache_job:
        ...
        ...
        if should_stop_cache():
            purge_cache_job.stop()
    ```
    """
    loop = GeventLoop(interval, callback)
    loop.start()
    try:
        yield loop
    finally:
        if loop.has_started():
            loop.stop()
