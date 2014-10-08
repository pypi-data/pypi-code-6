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
        if subprocess.call("type dot", shell=True, stdout=devnull, stderr=devnull):
            raise OSError('\'dot\' not found, please install graphviz')
        return 'dot'

        
DOT_PATH = find_dot()
        
        
class BProfile(object):
    """A profiling context manager. Outputs .png graph made via profile/cProfile, gprof2dot
        and graphviz. graphviz is the only external dependency.
        
        arguments:
            - output_path:       the name of the .png file you would like to output. '.png'
                                 will be appended if not present
                                 
            - threshold_percent: int or float for the minimum percentage of total cumulative
                                 time a call should have to be included in the output. 
                                 Defaults to 2.5.
                                 
            - report_delay:      How frequently output files should be produced. This is to
                                 minimise overhead on your program, (even though this overhead
                                 will only be incurred when no code is being profiled), while
                                 allowing you to have somewhat immedaite results of the profiling
                                 while your code is still running. Defaults to 5 (seconds).
        
        usage example:
        
            profiler = BProfile('output.png')
            
            with profiler:
                do_some_stuff()
            
            do_some_stuff_that_wont_be_profiled()
            
            with profiler:
                do_some_more_stuff()
            
        The profiler will return immediately after the context manager, and will generate
        its .png output after a delay (report_delay, default is 5 seconds) in a separate thread.
        The delay is to allow the block to execute many times before report generation,
        rather than slowing your program down with generating output all the time. This means
        that if your profile block is running repeatedly, a new output file will be produced
        every <report_delay> seconds.
        
        Pending reports will be generated at interpreter shutdown if delay_time has not yet
        elapsed.
        
        Note that even if report_delay is short, it will not interfere with the profiling
        results themselves, as a lock is acquired that will prevent profiled code from running
        at the same time as the output generation code. So the overhead produced by output
        generation does not affect the results of profiling - this overhead will only affect
        portions of your code that are not being profiled.
        
        The lock is shared between instances, and so you can freely instantiate many
        Profile objects to profile different parts of your code (but give them different output
        filenames!).
        Profile objects are threadsafe, so you can also pass the same Profile object to different
        parts of your code to profile them on the same graph.
        
        Note that since only one profiler can be running at a time, two profiled pieces of code
        waiting on each other in any way will cause a deadlock.
    """
    
    class_lock = threading.Lock()
    report_required = threading.Event()
    report_thread = None
    instances_requiring_reports = set()
    
    def __init__(self, output_path, threshold_percent=2.5, report_delay=5):
        if not output_path.lower().endswith('.png'):
            output_path += '.png'
        self.output_path = output_path
        self.threshhold_percent = threshold_percent
        self.profiler = profile.Profile()
        self.time_of_last_report = time.time()
        self.report_delay = report_delay
        with self.class_lock:
            # only one reporting thread to be shared between instances:
            if self.report_thread is None:
                report_thread = threading.Thread(target=self._report_loop)
                report_thread.daemon = True
                report_thread.start()
                self.__class__.report_thread = report_thread
        
    def __enter__(self):
        self.class_lock.acquire()
        self.profiler.enable()
        
    def __exit__(self, type, value, traceback):
        self.profiler.disable()
        self.instances_requiring_reports.add(self)
        self.report_required.set()
        self.class_lock.release()
    
    def do_report(self):
        pstats_file = '%s.pstats'%self.output_path
        dot_file = '%s.dot'%self.output_path
        pstats.Stats(self.profiler).dump_stats(pstats_file)
        threshhold_percent = str(self.threshhold_percent)
        subprocess.check_call([sys.executable, gprof2dot, '-n', threshhold_percent, '-f', 'pstats', 
                               '-o', dot_file, pstats_file])
        subprocess.check_call([DOT_PATH, '-o', self.output_path, '-Tpng', dot_file])
        os.unlink(dot_file)
        os.unlink(pstats_file)
        self.time_of_last_report = time.time()
    
    @classmethod
    def _atexit(cls):
        # Finish pending reports:
        with cls.class_lock:
            for instance in cls.instances_requiring_reports:
                instance.do_report()
        
    @classmethod
    def _report_loop(cls):
        atexit.register(cls._atexit)
        timeout = None
        while True:
            cls.report_required.wait(timeout)
            with cls.class_lock:
                cls.report_required.clear()
                if not cls.instances_requiring_reports:
                    timeout = None
                    continue
                for instance in cls.instances_requiring_reports.copy():
                    next_report_time = instance.time_of_last_report + instance.report_delay
                    time_until_report =  next_report_time - time.time()
                    if time_until_report < 0:
                        instance.do_report()
                        cls.instances_requiring_reports.remove(instance)
                    else:
                        if timeout is None:
                            timeout = time_until_report
                        else:
                            timeout = min(timeout, time_until_report)
                
                
if __name__ == '__main__':
    # Test:
    profile = BProfile('test.png')
    def foo():
        time.sleep(0.05)
    def bar():
        time.sleep(0.1)
        
    start_time = time.time()    
    for i in range(100):
        print(i)
        with profile:
            time.sleep(0.1)
            foo()
            bar()
    print(time.time() - start_time)