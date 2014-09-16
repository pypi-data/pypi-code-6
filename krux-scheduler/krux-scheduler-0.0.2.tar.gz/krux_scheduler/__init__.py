######################
# Standard Libraries #
######################
from __future__ import absolute_import

import os
import sys
import time

from pprint     import pprint
from functools  import wraps
from contextlib import contextmanager


#########################
# Third Party Libraries #
#########################

import psutil
import krux.cli
import apscheduler.scheduler

from apscheduler.events import *
from krux.logging       import get_logger, LEVELS
from krux.stats         import get_stats
from krux.cli           import get_parser, get_group

#########################
# Constants
#########################

### Designed to be called from krux.cli, or programs inheriting from it
def add_scheduler_cli_arguments(parser):

    group = get_group(parser, 'scheduler')

    ### All our jobs only use minute & hour at this point
    ### so don't bother exposing more than that
    group.add_argument(
        '--scheduler-minute',
        default = None,
        help    = 'Comma separated list of minute mark(s) to run on. '
                    'This overrides any hardcoded arguments (default: %(default)s)',
    )

    group.add_argument(
        '--scheduler-hour',
        default = None,
        help    = 'Comma separated list of hour mark(s) to run on. '
                    'This overrides any hardcoded arguments (default: %(default)s)',
    )

    group.add_argument(
        '--scheduler-daemonize',
        default = False,
        action  = 'store_true',
        help    = 'Run scheduled jobs in separate threads (default: %(default)s)',
    )

    group.add_argument(
        '--scheduler-exit-after-job',
        default = False,
        action  = 'store_true',
        help    = 'Exit the application after a job has completed. Very useful for '
                    'RAM hungry applications whose only purpose is to run a single job '
                    'but not otherwise. Requires a process monitor to restart if it exits '
                    '(default: %(default)s)',
    )

class Application(krux.cli.Application):
    """
    Application built around krux.cli.Application that provides
    an inteface to APScheduler
    """

    def __init__(self, name):
        ### Call to the superclass to bootstrap.
        super(Application, self).__init__(name = name)

        ### get all the configuration from the CLI
        self.scheduler = Scheduler( application = self )

    def add_cli_arguments(self, parser):

        ### add the arguments for the scheduler
        add_scheduler_cli_arguments(parser)

    def exit(self, code=None, *args, **kwargs):
        """
        Wrap krux.cli.Application.exit, and provide the exit
        code of the last job, if no specific code was provided
        """
        code = code or self.exit_code()
        super(Application, self).exit(code = code, *args, **kwargs)

    ### So, this lets you determine the exit code of the last
    ### job you ran, which you can then use together like this:
    ### app.exit( app.exit_code() )
    def exit_code(self):
        log   = self.logger
        event = self.scheduler.last_job_event

        ### No event ran, must be fine then
        if not event:
            log.debug('No job ran yet - exit code 0')
            return 0

        elif event.exception:
            ### an error happened
            log.debug('Last job (%s) generated an exception (%s) - exit code 1',
                        event, event.exception)
            return 1

        else:
            log.debug('Last job ran without exceptions - exit code 0')
            return 0

class Scheduler(object):

    ### Taken from here - there does not appear to be a lookup table
    ### in the other direction :(
    ### https://bitbucket.org/agronholm/apscheduler/src/11c5c1e7b8c33205293168e044d90b7f2c84a21b/apscheduler/events.py?at=2.1
    event_map = {
        EVENT_SCHEDULER_START:      'events.scheduler.start',      # The scheduler was started
        EVENT_SCHEDULER_SHUTDOWN:   'events.scheduler.shutdown',   # The scheduler was shut down
        EVENT_JOBSTORE_ADDED:       'events.jobstore.added',       # A job store was added to the scheduler
        EVENT_JOBSTORE_REMOVED:     'events.jobstore.removed',     # A job store was removed from the scheduler
        EVENT_JOBSTORE_JOB_ADDED:   'events.jobstore.job_added',   # A job was added to a job store
        EVENT_JOBSTORE_JOB_REMOVED: 'events.jobstore.job_removed', # A job was removed from a job store
        EVENT_JOB_EXECUTED:         'events.job.executed',         # A job was executed successfully
        EVENT_JOB_ERROR:            'events.job.error',            # A job raised an exception during execution
        EVENT_JOB_MISSED:           'events.job.missed',           # A job's execution was missed
    }

    def __init__(self, logger = None, stats = None, parser = None, application = None):
        """
        Either pass in a krux.cli.Application, or separate stats/logger/parser instances.
        If you pass in none of those, we'll create new instances here.

        If you pass the Application class, exit hooks can be run if you ask the scheduler
        to exit after its job completes. This is recommended.
        """

        ### to keep line length short below
        _a = application

        self.application = application
        self.name        = getattr(_a, 'name', 'krux-scheduler')
        self.logger      = logger or getattr(_a, 'logger', get_logger(self.name))
        self.stats       = stats  or getattr(_a, 'stats',  get_stats( prefix = self.name))
        self.parser      = parser or getattr(_a, 'parser', get_parser(description = self.name))

        ### we keep track of the last job that was run, so we can use that
        ### as part of the exit status in the App.
        self.last_job_event = None

        ### in case we got some of the information via the CLI
        self.args = self.parser.parse_args()

        ### Own process information - always record this when we have
        ### a chance to do so.
        self.proc = psutil.Process(os.getpid())

        ### the AP scheduler object
        _standalone = True if not self.args.scheduler_daemonize else False

        self.___apscheduler  = apscheduler.scheduler.Scheduler(
                                standalone = _standalone,
                                daemonic   = not _standalone,
                             )

        ### catch any events that come up
        self.___setup_event_listener(
            terminate_on_finish = self.args.scheduler_exit_after_job,
        )

    def __getattr__(self, attr, *args, **kwargs):
        """Proxies calls to ``APScheduler`` methods. Silently pass'es.
        """

        log  = self.logger
        log.debug('Potential APScheduler method "%s" called', attr)

        attr = getattr(self.___apscheduler, attr)

        if callable(attr):
            log.debug('APScheduler method "%s" is callable', attr)

            # We define @contextmanager:
            # see http://docs.python.org/2/library/contextlib.html for details.
            # 'yield' makes sure the decorated function is called
            @contextmanager
            def wrapper(*args, **kwargs):
                log.debug('Dispatching "%s" to APScheduler', attr)
                attr(*args, **kwargs)

            return wrapper

        ### else, just return the attribute
        return attr

    def ___record_memory_usage(self):
        log     = self.logger
        stats   = self.stats
        memory  = self.proc.memory_info().rss

        log.debug('Current memory usage: %s bytes', memory)
        stats.gauge('scheduler.memory.usage', memory)

    def ___setup_event_listener(self, terminate_on_finish = False):
        """
        This sets up the event listeners for events from APScheduler.
        If terminate_on_finish is True, we'll exit the application
        as soon as a job has finished.

        This is only useful for applications whose sole purpose it is
        to run a job, who are memory hungry and need to free up the
        memory between runs.

        This will require a service manager, like Supervisor, to manage
        the jobs so they're restarted.
        """

        log   = self.logger
        stats = self.stats

        ### we get a callback to this function everytime an event happens
        ### we use that to track those events in logs & statsd. See here:
        ### http://pythonhosted.org//APScheduler/modules/events.html
        def ___event_listener(event):

            ### What event did we just get passed? Record that.
            for (code, name) in self.event_map.iteritems():
                if event.code == code:
                    log.info('Event received: %s', name)
                    stats.incr('scheduler.%s' % name)

            ### Record our memory usage:
            self.___record_memory_usage()

            ### We particularly care about JobEvents - that's the actual
            ### jobs we run. So check for errors/problems explicitly
            if isinstance(event, apscheduler.events.JobEvent):

                ### keep track of this event
                self.last_job_event = event

                ### This means we had a problem - notify!
                if event.exception:

                    error = 'Job scheduled at %s failed: %s' % \
                                (event.scheduled_run_time, event.exception)

                    ### Send an extra stat so we capture errors for these events
                    stats.incr('scheduler.errors.%s' % name)

                    ### PagerDuty/email integration here!
                    log.error(error)

                ### You want us to exit after the job completed?
                if terminate_on_finish:
                    log.info('Scheduler explicitly exiting the application')

                    ### pass shutdown_threadpool = False or there's an error
                    ### saying:
                    # 2014-04-23 01:51:55,006: apscheduler.scheduler/ERROR    : Error notifying listener
                    # Traceback (most recent call last):
                    #   File "build/bdist.linux-x86_64/egg/apscheduler/scheduler.py", line 239, in _notify_listeners
                    #     cb(event)
                    #   File "/home/host_home/sources/git/python-krux-scheduler/krux_scheduler/__init__.py",
                    #       line 212, in ___event_listener
                    #     self.___apscheduler.shutdown( shutdown_threadpool = True)
                    #   File "build/bdist.linux-x86_64/egg/apscheduler/scheduler.py", line 135, in shutdown
                    #     self._threadpool.shutdown(wait)
                    #   File "build/bdist.linux-x86_64/egg/apscheduler/threadpool.py", line 125, in shutdown
                    #     thread.join()
                    #   File "/usr/lib/python2.6/threading.py", line 635, in join
                    #     raise RuntimeError("cannot join current thread")
                    self.___apscheduler.shutdown( shutdown_threadpool = False )

        ### and now register that listener
        self.___apscheduler.add_listener( ___event_listener )


    def add_cron_job(self, func, *args, **kwargs):
        """
        Wrapper around APSchedulers add_cron_job, which overides the
        hour/minute argument from CLI arguments if passed, and wraps
        the execution in diagnostics & timers.
        """

        log   = self.logger
        stats = self.stats

        ### CLI arguments override what you provided - this way we can force it
        ### to run at other times explicitly, without a code change

        _hour = self.args.scheduler_hour
        if _hour is not None:
            log.info('Explicitly setting cronjob hour to: %s', _hour)
            kwargs['hour'] = _hour

        _minute = self.args.scheduler_minute
        if _minute is not None:
            log.info('Explicitly setting cronjob minute to: %s', _minute)
            kwargs['minute'] = _minute

        ### Wrap the function so we get a runtime on it. Using @wraps is
        ### considered best practice for stack trace purposes.
        @wraps(func)
        def wrapped_func():
            with stats.timer('scheduler.cron_job.runtime'):
                ### execute the actual function you wanted to run
                func()

        return self.___apscheduler.add_cron_job(wrapped_func, *args, **kwargs)


###
### Test the scheduler setup
###

def main():
    app     = Application( name = 'krux-scheduler-test' )
    log     = app.logger

    ### a little bit we flip to do one or the other action
    ### (msg or raise an error).
    ### So, we have to use a list because of pythons.. interesting
    ### scoping bugs^Wrules. See here for details:
    ### http://me.veekun.com/blog/2011/04/24/gotcha-python-scoping-closures/
    flip    = [1]

    log.info('Testing scheduler')

    def periodic_job():
        """
        This alternates between a print and an exception, for testing purposes
        """

        msg = 'Test: %s at %s' % (app.name, time.asctime())

        print "\n\n\n\n*** Next test iteration ***\n\n"

        ### If true, exception
        if flip[0]:
            flip[0] = 0
            raise Exception(msg)

        ### If false, print
        else:
            flip[0] = 1
            print msg

    ### Run it 'always', so we can test scheduler arguments
    app.scheduler.add_cron_job(
        func   = periodic_job,
        hour   = ','.join([ str(i) for i in range(0,24) ]),
        minute = ','.join([ str(i) for i in range(0,60) ]),
        second = ','.join([ str(i) for i in range(0,60, 2) ]),
    )

    app.scheduler.start()

    print "Scheduler process either backgrounded or ended"
    app.exit()


### Run the application stand alone
if __name__ == '__main__':
    main()
