# Run tasks in a background process, passing the data they require via fork().
#
#
# Quick start
# -----------
#
#   import backtask
#
#   def a_task(arg, kwd=true):
#     :
#     :
#
#   def on_complete(result):
#     a_task_return_value = result()
#     if isinstance(a_task_return_value, backtask):
#       # a_task raised the exception a_task_return_value.exc_info[]
#     else:
#       # a_task_return_value is the return value of a_task()
#
#   bt = backtask.BackgroundTasks()
#   result = bt.submit_job(a_task, 1, kwd=false)
#   result.on_complete = on_complete
#
#
# Unit Test
# ---------
#
#   python backtask.py
#
#   When testing with coverage, use "run --parallel-mode" and then
#   run again with the "combine" option.
#
#
# License
# -------
#
# Copyright (c) 2014 Russell Stuart
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# The copyright holders grant you an additional permission under Section 7
# of the GNU Affero General Public License, version 3, exempting you from
# the requirement in Section 6 of the GNU General Public License, version 3,
# to accompany Corresponding Source with Installation Information for the
# Program or any work based on the Program. You are still required to
# comply with all other Section 6 requirements to provide Corresponding
# Source.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
import cPickle
import cStringIO
import errno
import fcntl
import os
import select
import sys
import threading
import traceback


class RaisedException(object):
    """
      This class is returned by TaskResult if the func passed to submit_job
      raises and exception instead of returning normally.  It's members are
      exception, the BaseException raised, and traceback, the traceback (a
      string).
    """
    exception = None
    traceback = None

    def __init__(self, exc_info):
        self.exception = exc_info[1]
        string_file = cStringIO.StringIO()
        traceback.print_exception(
            exc_info[0], exc_info[1], exc_info[2], None, string_file)
        self.traceback = string_file.getvalue()

    def __repr__(self):
        return 'RaisedException(%r)' % (self.traceback,)


class TaskResult(object):
    """
       BackgroundTasks.submit_task() returns an instance of this class.  This
       is a function like object that when called returns TaskResult.RUNNING
       until the task completes, then it returns whatever the func given to
       submit_task() returned.  If the func threw an exception instead of
       returning normally this will be an instance of RaisedException.  The
       member on_complete can be set to a function that will be called when the
       task completes.  It's one argument is this instance.  Beware that if
       BackgroundTasks uses a background thread, the function may be called
       from that thread.
    """
    RUNNING = object()
    __background_task = None
    __notified = False
    __on_complete = None
    __result = RUNNING

    def __init__(self, background_task):
        self.__background_task = background_task

    def __call__(self):
        self.__background_task._dispatch()
        self.__background_task._lock.acquire()
        try:
            result = self.__result
        finally:
            self.__background_task._lock.release()
        return result

    def _set_result(self, result):
        self.__background_task._lock.acquire()
        try:
            self.__result = result
            on_complete = self.__on_complete
            if on_complete is not None:
                self.__notified = True
        finally:
            self.__background_task._lock.release()
        if on_complete is not None:
            on_complete(self)

    def on_complete(self, on_complete):
        """
            Arrange for on_complete to be called when the task completes.
            It's one argument is this instance.
        """
        self.__background_task._lock.acquire()
        try:
            result = self.__result
            self.__on_complete = on_complete
            if result is self.RUNNING or self.__notified:
                on_complete = None
            elif on_complete is not None:
                self.__notified = True
        finally:
            self.__background_task._lock.release()
        if on_complete is not None:
            on_complete(self)
    on_complete = property(lambda self: self.__on_complete, on_complete)


class BackgroundTasks(object):
    """
        Run tasks in a background worker.  The data is passed to the worker
        using fork(), so it can be passed data that can't be pickled.
        Tasks are started using BackgroundTasks.submit_task().  When you
        are done with this object it should be disposed of using
        BackgroundTasks.close().
    """
    NO_RESULT = object()
    max_processes = None
    __LEN = 8
    _lock = None
    __queue = None
    __results = None
    __processes = None
    __thread_lock = None
    __thread_pipe = None

    def __init__(self, max_processes=1, background_thread=True):
        """
          Create a new background tasks object.  max_processes is the
          maximum number of processes that can be running at once.
          If background_thread is True new tasks will be fired off by
          a background thread, otherwise we depend on clients polling
          us.
        """
        self.max_processes = max_processes
        self.__queue = []
        self.__results = {}
        self.__processes = {}
        self.__coverage = self._fugly_hack_for_my_son_ryan()
        self._lock = threading.Lock()
        if background_thread:
            try:
                self.__thread_lock = threading.Lock()
                self.__thread_pipe = os.pipe()
                self.__thread_lock.acquire()
                try:
                    threading.Thread(target=self._thread).start()
                    # Wait the thread to acquire _thread_lock,
                    # so close() can wait on it.
                    os.read(self.__thread_pipe[0], 1)
                finally:
                    self.__thread_lock.release()
                self._nonblock(self.__thread_pipe[1])
            except:
                if self.__thread_pipe is not None:
                    os.close(self.__thread_pipe[0])
                    os.close(self.__thread_pipe[1])
                raise

    def submit_task(self, func, *args, **kwds):
        """
          Submit a new task to be run in the background.  The task is:
            result = func(*args, **kwds)
          The return value is a TaskResult object that can be interrogated
          to find the return value of func(), when it becomes available.
          Normally if the submitting process exits before the result can
          be reported the worker process will raise a "Broken Pipe" OSError,
          after processing all tasks it has been given.  If the func()
          returns BackgroundTasks.NO_RESULT then failure to report it doesn't
          result in a broken pipe.
        """
        result = TaskResult(self)
        self._lock.acquire()
        try:
            self.__queue.append((id(result), func, args, kwds))
            self.__results[id(result)] = result
        finally:
            self._lock.release()
        self._dispatch()
        return result

    def close(self):
        """Shutdown nicely.  If you don't call this you may get
        "sys.excepthook is missing" messages.   If you call this before
        all tasks have completed the background tasks will fail with
        broken pipes."""
        if self.__thread_pipe is not None:
            os.write(self.__thread_pipe[1], "x")
            self.__thread_lock.acquire()
            self.__thread_lock.release()
            os.close(self.__thread_pipe[1])
            os.close(self.__thread_pipe[0])
            self.__thread_pipe = None
        if self.__processes:
            for r in self.__processes:
                os.close(r)
            self.__processes = None

    def __len__(self):
        self._lock.acquire()
        try:
            return len(self.__queue) + len(self.__results)
        finally:
            self._lock.release()

    def _dispatch(self):
        """See if any background tasks can be started."""
        self._poll()
        self._lock.acquire()
        try:
            # Is there work to be done?
            if not self.__queue or len(self.__processes) >= self.max_processes:
                return
            # Pass an appropriate amount of work to the background task.
            if self.max_processes == 1:
                task_count = len(self.__queue)
            else:
                task_count = len(self.__queue) // self.max_processes + 1
            tasks, self.__queue[:task_count] = self.__queue[:task_count], []
        finally:
            self._lock.release()
        # fork() a new worker task
        pipe = os.pipe()
        child_pid = os.fork()
        if child_pid == 0:
            # Release resources that aren't relevant to the fork()'ed worker.
            self.__queue = None
            for r in self.__processes:
                self._close(r)
            self.__processes = None
            for h in self.__thread_pipe or ():
                self._close(h)
            self.__thread_pipe = None
            self._close(pipe[0])
            self.__results = None
            sys.stdin.close()
            sys.stdin = open(os.devnull)
            self._process_tasks(pipe[1], tasks)
            self._close(pipe[1])
            sys.stdout.flush()
            sys.stderr.flush()
            ((self.__coverage.stop(),) and
                (self.__coverage.save(),) and
                os._exit(0))
        os.close(pipe[1])
        self._nonblock(pipe[0])
        self._lock.acquire()
        try:
            self.__processes[pipe[0]] = (child_pid, [""])
        finally:
            self._lock.release()
        if self.__thread_pipe is not None:
            os.write(self.__thread_pipe[1], "n")

    def _process_tasks(self, pipe, tasks):
        """
            Process the tasks passed, and report the results to the parent
            process via out pipe.
        """
        exc_info = None
        while tasks:
            result_id, func, args, kwds = tasks.pop(0)
            try:
                result = func(*args, **kwds)
            except BaseException as e:
                result = RaisedException(sys.exc_info())
            data = cPickle.dumps((result_id, result))
            length = "%0*x" % (self.__LEN, len(data))
            # If the listening process has died just continue.
            try:
                os.write(pipe, length + data)
            except OSError as e:
                if e.errno != errno.EPIPE:
                    raise
                if result is not self.NO_RESULT and exc_info is None:
                    exc_info = sys.exc_info()
        if exc_info is not None:
            raise exc_info[0], exc_info[1], exc_info[2]

    def _poll(self):
        """Process any reports from the background tasks."""
        set_results = []
        try:
            self._lock.acquire()
            while True:
                if not self.__processes:
                    break
                # Does anyone have anything to report?
                ready, _, _ = select.select(list(self.__processes), [], [], 0)
                if not ready:
                    break
                for r in ready:
                    # Find the reporting process
                    child_pid, data_list = self.__processes[r]
                    data_list_len = sum(len(d) for d in data_list)
                    if data_list_len < self.__LEN:
                        # He is telling us how big the pickled results are
                        read_amount = self.__LEN - data_list_len
                    else:
                        # Read the pickled results.
                        data_len = int(data_list[0], 16)
                        read_amount = data_len + self.__LEN - data_list_len
                    d = self._read(r, read_amount)
                    if d is None:
                        continue
                    # An empty read means the process has exited.
                    if not d:
                        os.close(r)
                        os.waitpid(child_pid, 0)
                        del self.__processes[r]
                        if self.__thread_pipe is not None:
                            os.write(self.__thread_pipe[1], "e")
                    else:
                        if data_list_len < self.__LEN:
                            data_list[0] += d
                        else:
                            data_list.append(d)
                        data_list_len += len(d)
                    # If we have read all of the picked data, process it.
                    if data_list_len >= self.__LEN:
                        data_len = int(data_list[0], 16)
                        if data_list_len == data_len + self.__LEN:
                            tid, result = cPickle.loads(''.join(data_list[1:]))
                            task_result = self.__results.pop(tid)
                            set_results.append((task_result, result))
                            data_list[:] = [""]
        finally:
            self._lock.release()
        # Delay calling _set_result until we are outside of the lock,
        # so there is no chance of calling TaskResult.on_complete while
        # owning the lock.
        for task_result, result in set_results:
            task_result._set_result(result)

    def _thread(self):
        """Fire off worker processes in the background."""
        os.write(self.__thread_pipe[1], "s")
        self.__thread_lock.acquire()
        try:
            # Tell main thread we have starteed.
            self._nonblock(self.__thread_pipe[0])
            while True:
                self._lock.acquire()
                try:
                    rlist = list(self.__processes) + [self.__thread_pipe[0]]
                finally:
                    self._lock.release()
                # Wait until some child is ready, or self.__process changes.
                ready, _, _ = select.select(rlist, [], [])
                if self.__thread_pipe[0] in ready:
                    ready.remove(self.__thread_pipe[0])
                    # Main thread closes the pipe to tell us to exit.
                    if self._read(self.__thread_pipe[0], 1) in ("", "x"):
                        break
                if ready:
                    self._dispatch()
        finally:
            # Tell main thread we have exited.
            self.__thread_lock.release()

    def _read(cls, fd, max_byte_count):
        """
            Read from a non-blocking file descriptor,
            returning NONE for EAGAIN
        """
        try:
            return os.read(fd, max_byte_count)
        except OSError as e:
            if e.errno != errno.EAGAIN:
                raise
        return None
    _read = classmethod(_read)

    def _close(cls, fd):
        """Close a file, ignore errors caused by it already being closed."""
        try:
            os.close(fd)
        except OSError as e:
            if e.errno != errno.EBADF:
                raise
    _close = classmethod(_close)

    def _nonblock(cls, fd):
        """Make the passed file descriptor non blocking"""
        orig = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, orig | os.O_NONBLOCK)
    _nonblock = classmethod(_nonblock)

    def _fugly_hack_for_my_son_ryan(cls):
        """God awful hack to make coverage and py.test work together."""
        class Cov(object):
            stop = lambda self: None
            save = lambda self: None
        cov = Cov()
        if "coverage" in sys.modules:
            import coverage
            try:
                raise ZeroDivisionError
            except ZeroDivisionError:
                f = sys.exc_info()[2].tb_frame
            tb = []
            while f:
                tb.append(f)
                f = f.f_back
            t = tb[-3]
            if 'self' in t.f_locals:
                slf = t.f_locals['self']
                if hasattr(slf, "coverage"):
                    if isinstance(slf.coverage, coverage.coverage):
                        cov = slf.coverage
        return cov
    _fugly_hack_for_my_son_ryan = classmethod(_fugly_hack_for_my_son_ryan)


# -----------------------------------------------------------------------------
#
# Unit test.
#
def test_backtask():
    """
        100% code coverage unit test.

        =====
        Hi 0!
        *****
        Hi 1!
        [0, 1]
        =====
        Hi 2!
        *****
        Hi 3!
        [0, 1, 2, 3, RaisedException('...')]
    """
    class ErrorRaiser(object):

        def os_raise(cls, errno):
            e = OSError()
            e.errno = errno
            raise e
        os_raise = classmethod(os_raise)

    class NonblockReadTester(ErrorRaiser):
        i = 0
        read = os.read

        def __call__(self, fd, byte_count):
            self.i = (self.i + 1) % 2
            if fcntl.fcntl(fd, fcntl.F_GETFL) & os.O_NONBLOCK and self.i == 0:
                self.os_raise(errno.EAGAIN)
            return self.read(fd, byte_count)
    save_os_read, os.read = os.read, NonblockReadTester()

    class BadCloseTester(ErrorRaiser):
        i = 0
        close = os.close
        pid = os.getpid()

        def __call__(self, fd):
            self.i = (self.i + 1) % 2
            self.close(fd)
            if os.getpid() != self.pid and self.i == 0:
                self.os_raise(errno.EBADF)
    save_os_close, os.close = os.close, BadCloseTester()

    try:
        import time
        save_Thread, threading.Thread = threading.Thread, lambda: XXZ()
        try:
            b = BackgroundTasks()
        except:
            pass
        threading.Thread = save_Thread
        b = BackgroundTasks()
        len(b)
        r = [b.submit_task(lambda i: i, i) for i in range(2)]
        r[0].on_complete = lambda _: sys.stdout.write('Hi 0!\n')
        sys.stdout.write('=====\n')
        time.sleep(1)
        sys.stdout.write('*****\n')
        r[1].on_complete = lambda _: sys.stdout.write('Hi 1!\n')
        sys.stdout.write("%r\n" % ([rr() for rr in r],))
        b.close()
        b.close()
        b = BackgroundTasks(2)
        r = [b.submit_task(lambda i: time.sleep(.1) or i, i) for i in range(4)]
        r.append(b.submit_task(lambda: 1 // 0))
        r[0].on_complete = lambda _: sys.stdout.write('Hi 2!\n')
        sys.stdout.write('=====\n')
        time.sleep(5)
        sys.stdout.write('*****\n')
        r[4].on_complete = lambda _: sys.stdout.write('Hi 3!\n')
        sys.stdout.write("%r\n" % ([rr() for rr in r],))
        r.append(b.submit_task(lambda: 1 // 0))
        b.close()
        os.read = lambda fd, bytes: ErrorRaiser.os_raise(errno.EPERM)
        try:
            BackgroundTasks._read(0, 0)
        except OSError as e:
            pass
        os.close = lambda fd: ErrorRaiser.os_raise(errno.EPERM)
        try:
            BackgroundTasks._close(0)
        except OSError as e:
            pass
        b = BackgroundTasks(background_thread=False)
        try:
            b._process_tasks(-1, [(0, lambda: None, (), {})])
        except OSError as e:
            pass
        b.close()
    except OSError as e:
        pass
    finally:
        os.read, os.close = save_os_read, save_os_close

__name__ != "__main__" or test_backtask()
