"""
aioawait.py
~~~~~~~~~~~

This module implements **await** and **spawn** on top of
Python 3's asyncio infrastructure. To learn more see:

    https://pypi.python.org/pypi/aioawait

:copyright: (c) 2014 by Carlo Pires <carlopires@gmail.com>.
:license: MIT, see COPYING for more details.
"""
import heapq
import logging
import time
from asyncio.log import logger
from asyncio.tasks import iscoroutinefunction, Task, async
from asyncio.events import get_event_loop


def await(coro, loop=None):
    if loop is None:
        loop = get_event_loop()

    if iscoroutinefunction(coro):
        coro = coro()

    if isinstance(coro, Task):
        future = coro
    else:
        future = Task(coro, loop=loop)

    def _run_until_complete():
        add_delay = False

        while not future.done():
            timeout = 0.1 if add_delay else None
            t0 = time.monotonic()

            _run_once(loop, timeout=timeout)

            add_delay = (time.monotonic()-t0) < 0.001

        return future.result()

    if loop.is_running():
        old_task = Task._current_tasks[loop]
        try:
            return _run_until_complete()
        finally:
            Task._current_tasks[loop] = old_task
    else:
        loop._running = True
        try:
            return _run_until_complete()
        finally:
            loop._running = False


def spawn(coro, loop=None):
    if loop is None:
        loop = get_event_loop()
    if iscoroutinefunction(coro):
        coro = coro()
    return async(coro, loop=loop)


def _run_once(self, timeout=None):
    while self._scheduled and self._scheduled[0]._cancelled:
        heapq.heappop(self._scheduled)

    if self._ready:
        timeout = 0
    elif self._scheduled:
        when = self._scheduled[0]._when
        timeout = max(0, when - self.time())

    if logger.isEnabledFor(logging.INFO):
        t0 = self.time()
        event_list = self._selector.select(timeout)
        t1 = self.time()
        tdiff = t1-t0
        if tdiff > 0.001:
            if tdiff >= 1:
                level = logging.INFO
            else:
                level = logging.DEBUG
            if timeout is not None:
                logger.log(level,
                           'poll %.4f took %.4f seconds', timeout, tdiff)
            else:
                logger.log(level, 'poll took %.4f seconds', tdiff)
    else:
        event_list = self._selector.select(timeout)

    self._process_events(event_list)

    end_time = self.time() + self._clock_resolution
    while self._scheduled:
        handle = self._scheduled[0]
        if handle._when >= end_time:
            break
        handle = heapq.heappop(self._scheduled)
        self._ready.append(handle)

    while self._ready:
        handle = self._ready.popleft()
        if not handle._cancelled:
            handle._run()
