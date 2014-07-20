"""
aioawait.py
~~~~~~~~~~~

This module implements **await** and **spawn** on top of
Python 3's asyncio infrastructure. To learn more see:

    https://pypi.python.org/pypi/aioawait

:copyright: (c) 2014 by Carlo Pires <carlopires@gmail.com>.
:license: MIT, see COPYING for more details.
"""
from asyncio.tasks import iscoroutinefunction, Task, async
from asyncio.events import get_event_loop

__version__ = 2

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
            loop._run_once()
        Task._current_tasks[loop] = future
        return future.result()
    else:
        return loop.run_until_complete(coro)

def spawn(coro, loop=None):
    if loop is None:
        loop = get_event_loop()
    if iscoroutinefunction(coro):
        coro = coro()
    return async(coro, loop=loop)
