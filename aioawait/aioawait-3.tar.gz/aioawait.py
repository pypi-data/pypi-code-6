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
from asyncio.log import logger
from asyncio.tasks import iscoroutinefunction, Task, async
from asyncio.events import get_event_loop
from asyncio.base_events import _raise_stop_error, _StopError

def await(coro, loop=None):
    if loop is None:
        loop = get_event_loop()

    if iscoroutinefunction(coro):
        coro = coro()

    if loop.is_running():
        if isinstance(coro, Task):
            future = coro
        else:
            future = Task(coro, loop=loop)

        while not future.done():
            _run_once(loop)
        Task._current_tasks[loop] = future
        return future.result()
    else:
        return run_until_complete(loop, coro)

def spawn(coro, loop=None):
    if loop is None:
        loop = get_event_loop()
    if iscoroutinefunction(coro):
        coro = coro()
    return async(coro, loop=loop)

def _run_once(self):
    while self._scheduled and self._scheduled[0]._cancelled:
        heapq.heappop(self._scheduled)

    timeout = None
    if self._ready:
        timeout = 0
    elif self._scheduled:
        when = self._scheduled[0]._when
        timeout = max(0, when - self.time())

    if logger.isEnabledFor(logging.INFO):
        t0 = self.time()
        event_list = self._selector.select(timeout)
        t1 = self.time()
        if t1-t0 >= 1:
            level = logging.INFO
        else:
            level = logging.DEBUG
        if timeout is not None:
            logger.log(level, 'poll %.3f took %.3f seconds', timeout, t1-t0)
        else:
            logger.log(level, 'poll took %.3f seconds', t1-t0)
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

def run_until_complete(loop, future):
    future = async(future, loop=loop)
    future.add_done_callback(_raise_stop_error)

    if loop._running:
        raise RuntimeError('Event loop is running.')

    loop._running = True
    try:
        while True:
            try:
                _run_once(loop)
            except _StopError:
                break
    finally:
        loop._running = False

    future.remove_done_callback(_raise_stop_error)
    if not future.done():
        raise RuntimeError('Event loop stopped before Future completed.')
    return future.result()

