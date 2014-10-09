#####################################################################
#                                                                   #
# profile.py                                                        #
#                                                                   #
# Copyright 2014, Chris Billington                                  #
#                                                                   #
# This file is part of the bprofile project (see                    #
# https://bitbucket.org/cbillington/bprofile) and is licensed under #
# the Simplified BSD License. See the LICENSE.txt file in the root  #
# of the project for the full license.                              #
#                                                                   #
#####################################################################

import sys
import os
import subprocess
import pstats
import threading
import time
import atexit
import weakref

try:
    import cProfile as profile
except ImportError:
    import profile

this_folder = os.path.dirname(os.path.realpath(__file__))
gprof2dot = os.path.join(this_folder, 'gprof2dot.py')


def find_dot():
    devnull = open(os.devnull)
    if os.name == 'nt':
        program_files = os.environ["ProgramFiles"]
        program_files_x86 = os.environ["ProgramFiles(x86)"]
        for folder in [program_files, program_files_x86]:
            for subfolder in os.listdir(folder):
                if 'graphviz' in subfolder.lower():
                    dot = os.path.join(folder, subfolder, 'bin', 'dot.exe')
                    if os.path.exists(dot):
                        return dot
        else:
            raise OSError('dot.exe not found, please install graphviz')
    else:
        if subprocess.call(['type', 'dot'], shell=True, stdout=devnull, stderr=devnull):
            raise OSError('\'dot\' not found, please install graphviz')
        return 'dot'


DOT_PATH = find_dot()


class BProfile(object):

    """A profiling context manager.

    A context manager that after it exits, outputs a .png file of a graph made
    via profile/cProfile, gprof2dot and graphviz. The context manager can be
    used multiple times, and if used repeatedly, regularly updates its output
    to include cumulative results.

    Parameters
    ----------

    output_path: str
        The name of the .png report file you would like to output. '.png' will
        be appended if not present.

    threshold_percent: int or float
        Nodes in which execution spends less than this percentage of the total
        profiled execution time will not be included in the output.

    report_interval: int or float
        The minimum time, in seconds, in between output file generation. If
        the context manager exits and it has not been at least this long since
        the last output was generated, output generation will be delayed until
        it has been. More profiling can run in the meantime. This is to
        decrease overhead on your program, (even though this overhead will
        only be incurred when no code is being profiled), while allowing you
        to have ongoing results of the profiling while your code is still
        running. If you only use the context manager once, then this argument
        has no effect. If you set it to zero, output will be produced after
        every exit of the context.


    Notes
    -----

    The profiler will return immediately after the context manager, and will
    generate its .png report in a separate thread. If the same context manager
    is used multiple times output will be generated at most every
    ``report_interval`` seconds (default: 5). The delay is to allow blocks to
    execute many times in between reports, rather than slowing your program
    down with generating graphs all the time. This means that if your profile
    block is running rapidly and repeatedly, a new report will be produced
    every ``report_interval`` seconds.

    Pending reports will be generated at interpreter shutdown.

    Note that even if ``report_interval`` is short, reporting will not
    interfere with the profiling results themselves, as a lock is acquired
    that will prevent profiled code from running at the same time as the
    report generation code. So the overhead produced by report generation does
    not affect the results of profiling - this overhead will only affect
    portions of your code that are not being profiled.

    The lock is shared between instances, and so you can freely instantiate
    many Profile objects to profile different parts of your code. Instances
    with the same output file name will share an underlying profile/cProfile
    profiler, and so their reports will be combined. Profile objects are
    thread safe, however, so a single instance can be shared as well anywhere
    in your program.

    .. warning::

        Since only one profiler can be running at a time, two profiled pieces
        of code waiting on each other in any way will deadlock.
    """

    _lock = threading.RLock()
    _report_required = threading.Event()
    _report_thread = None
    _instances_requiring_reports = set()
    _profilers = weakref.WeakValueDictionary()

    def __init__(self, output_path, threshold_percent=2.5, report_interval=5):
        if not output_path.lower().endswith('.png'):
            output_path += '.png'
        output_path = os.path.abspath(os.path.realpath(output_path))
        with self._lock:
            self.output_path = output_path
            self.threshold_percent = threshold_percent
            self.report_interval = report_interval
            self.time_of_last_report = time.time() - report_interval
            # Only one profiler per output file:
            try:
                self.profiler = self._profilers[self.output_path]
            except KeyError:
                self.profiler = profile.Profile()
                self._profilers[self.output_path] = self.profiler
            # only one reporting thread to be shared between instances:
            if self._report_thread is None:
                report_thread = threading.Thread(target=self._report_loop)
                report_thread.daemon = True
                report_thread.start()
                self.__class__._report_thread = report_thread

    def __enter__(self):
        self._lock.acquire()
        self.profiler.enable()

    def __exit__(self, type, value, traceback):
        self.profiler.disable()
        self._instances_requiring_reports.add(self)
        self._report_required.set()
        self._lock.release()

    def do_report(self):
        """Collect statistics and output a .png file of the profiling report.

        Notes
        -----

        This occurs automatically at a rate of report_interval, but one can
        call this method to report results sooner. The report will include
        results from all BProfile instances that have the same output
        filepath, and no more automatic reports (if further profiling is done)
        will be produced until after the minimum delay_interval of those
        instances.

        This method can be called at any time and is threadsafe, but it will
        acquire the class lock and so will block until any profiling in other
        threads is complete. The lock is re-entrant, so this method can be
        called during profiling in the current thread. This is not advisable
        however, as the overhead incorred will skew profiling results."""
        with self._lock:
            output_path = self.output_path
            profiler = self.profiler

            pstats_file = '%s.pstats' % output_path
            dot_file = '%s.dot' % output_path
            pstats.Stats(profiler).dump_stats(pstats_file)

            # All instances with this output file that have a pending report:
            instances = [o for o in self._instances_requiring_reports if o.output_path == self.output_path]
            threshold_percent = str(min(o.threshold_percent for o in instances))
            subprocess.check_call([sys.executable, gprof2dot, '-n', threshold_percent, '-f', 'pstats',
                                   '-o', dot_file, pstats_file])
            subprocess.check_call([DOT_PATH, '-o', output_path, '-Tpng', dot_file])
            os.unlink(dot_file)
            os.unlink(pstats_file)

            for o in self._instances_requiring_reports.copy():
                if o.output_path == output_path:
                    o.time_of_last_report = time.time()
                    self._instances_requiring_reports.remove(o)

    @classmethod
    def _atexit(cls):
        # Finish pending reports:
        with cls._lock:
            while cls._instances_requiring_reports:
                instance = cls._instances_requiring_reports.pop()
                instance.do_report()

    @classmethod
    def _report_loop(cls):
        atexit.register(cls._atexit)
        timeout = None
        while True:
            cls._report_required.wait(timeout)
            with cls._lock:
                cls._report_required.clear()
                if not cls._instances_requiring_reports:
                    timeout = None
                    continue
                for instance in cls._instances_requiring_reports.copy():
                    next_report_time = instance.time_of_last_report + instance.report_interval
                    time_until_report = next_report_time - time.time()
                    if time_until_report < 0:
                        instance.do_report()
                    elif timeout is None:
                        timeout = time_until_report
                    else:
                        timeout = min(timeout, time_until_report)


if __name__ == '__main__':
    # Test:
    profiler = BProfile('test.png')

    def foo():
        time.sleep(0.05)

    def bar():
        time.sleep(0.1)

    start_time = time.time()
    for i in range(100):
        print(i)
        with profiler:
            time.sleep(0.1)
            foo()
            bar()
    print(time.time() - start_time)
