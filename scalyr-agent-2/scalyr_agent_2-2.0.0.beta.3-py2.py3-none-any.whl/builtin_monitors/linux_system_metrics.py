# Copyright 2014, Scalyr, Inc.

import os
import re
import threading
import time
import scalyr_agent.third_party.tcollector.tcollector as tcollector
from Queue import Empty
from scalyr_agent.scalyr_monitor import ScalyrMonitor
from scalyr_agent.third_party.tcollector.tcollector import ReaderThread
from scalyr_agent.json_lib.objects import JsonObject
from scalyr_agent.util import StoppableThread


class TcollectorOptions(object):
    """Bare minimum implementation of an object to represent the tcollector options."""
    def __init__(self):
        # The collector directory.
        self.cdir = None
        # An option we created to prevent the tcollector code from failing on fatal in certain locations.
        # Instead, an exception will be thrown.
        self.no_fatal_on_error = True


class WriterThread(StoppableThread):
    """A thread that pulls lines off of a reader thread and writes them to the log.  This is needed
    to replace tcollector's SenderThread which sent the lines to a tsdb server.  Instead, we write them
    to our log file.
    """
    def __init__(self, monitor, queue, logger, error_logger):
        """Initializes the instance.

        Arguments:
            monitor:  The monitor instance associated with this tcollector.
            queue:  The Queue of lines (strings) that are pending to be written to the log.  These should
                come from the ReaderThread as it reads and transforms the data from the running collectors.
            logger:  The Logger to use to report metric values.
            error_logger:  The Logger to use to report diagnostic information about the running of the monitor.
        """
        StoppableThread.__init__(self, name='tcollector writer thread')
        self.__monitor = monitor
        self.__queue = queue
        self.__max_uncaught_exceptions = 100
        self.__logger = logger
        self.__error_logger = error_logger
        self.__timestamp_matcher = re.compile('(\\S+)\\s+\\d+\\s+(.*)')
        self.__key_value_matcher = re.compile('(\\S+)=(\\S+)')

    def __rewrite_tsdb_line(self, line):
        """Rewrites the TSDB line emitted by the collectors to the format used by the agent-metrics parser."""
        # Strip out the timestamp that is the second token on the line.
        match = self.__timestamp_matcher.match(line)
        if match is not None:
            line = '%s %s' % (match.group(1), match.group(2))

        # Now rewrite any key/value pairs from foo=bar to foo="bar"
        line = self.__key_value_matcher.sub('\\1="\\2"', line)
        return line

    def run(self):
        errors = 0  # How many uncaught exceptions in a row we got.
        while self._run_state.is_running():
            try:
                try:
                    line = self.__rewrite_tsdb_line(self.__queue.get(True, 5))
                except Empty:
                    continue
                # It is important that we check is_running before we act upon any element
                # returned by the queue.  See the 'stop' method for details.
                if not self._run_state.is_running():
                    continue
                self.__logger.info(line, metric_log_for_monitor=self.__monitor)
                while True:
                    try:
                        line = self.__rewrite_tsdb_line(self.__queue.get(False))
                    except Empty:
                        break
                    if not self._run_state.is_running():
                        continue
                    self.__logger.info(line, metric_log_for_monitor=self.__monitor)

                errors = 0  # We managed to do a successful iteration.
            except (ArithmeticError, EOFError, EnvironmentError, LookupError,
                    ValueError):
                errors += 1
                if errors > self.__max_uncaught_exceptions:
                    raise
                self.__error_logger.exception('Uncaught exception in SenderThread, ignoring')
                self._run_state.sleep_but_awaken_if_stopped(1)
                continue

    def stop(self, wait_on_join=True, join_timeout=5):
        self._run_state.stop()
        # This thread may be blocking on self.__queue.get, so we add a fake entry to the
        # queue to get it to return.  Since we set run_state to stop before we do this, and we always
        # check run_state before acting on an element from queue, it should be ignored.
        if self._run_state.is_running():
            self.__queue.put('ignore this')
        StoppableThread.stop(self, wait_on_join=wait_on_join, join_timeout=join_timeout)


class SystemMetricsMonitor(ScalyrMonitor):
    """A Scalyr agent monitor that records system metrics using tcollector.
    """

    def __init__(self, monitor_config, logger):
        """Creates an instance of the monitor.

        Arguments:
            module_config:  The dict containing the configuration for this monitor as given in configuration file.
            error_logger:  The Logger instance to use to report diagnostic information about the running of this
                monitor.
        """
        ScalyrMonitor.__init__(self, monitor_config, logger)

        # Set up tags for this file.
        tags = JsonObject()

        if 'tags' in monitor_config:
            tags = monitor_config['tags']
            if not type(tags) is dict:
                raise Exception('The tags field in the configuration for the system_metrics module is not a dict '
                                'as expected')
            # Make a copy just to be safe.
            tags = JsonObject(content=tags)

        tags['parser'] = 'agent-metrics'

        self.log_config = {
            'attributes': tags,
            'parser': 'agent-metrics',
            'path': 'linux_system_metrics.log',
        }

        collector_directory = SystemMetricsMonitor.__get_collectors_directory()
        if 'collectors_directory' in monitor_config:
            collector_directory = os.path.realpath(monitor_config['collectors_directory'])

        if not os.path.isdir(collector_directory):
            raise Exception('No such directory for collectors: %s' % collector_directory)

        self.options = TcollectorOptions()
        self.options.cdir = collector_directory

        self.modules = tcollector.load_etc_dir(self.options, tags)
        self.tags = tags

    def run(self):
        """Begins executing the monitor, writing metric output to logger.

        Arguments:
            logger:  The Logger instance to use to write all information
                gathered by the monitor.  All non-diagnostic output should
                be emitted here.
        """
        tcollector.override_logging(self._logger)
        tcollector.reset_for_new_run()

        # At this point we're ready to start processing, so start the ReaderThread
        # so we can have it running and pulling in data from reading the stdins of all the collectors
        # that will be soon running.
        reader = ReaderThread(0, 300, self._run_state)
        reader.start()

        # Start the writer thread that grabs lines off of the reader thread's queue and emits
        # them to the log.
        writer = WriterThread(self, reader.readerq, self._logger, self._logger)
        writer.start()

        # Now run the main loop which will constantly watch the collector module files, reloading / spawning
        # collectors as necessary.  This should only terminate once is_stopped becomes true.
        tcollector.main_loop(self.options, self.modules, None, self.tags, False, self._run_state)

        self._logger.debug('Shutting down')

        tcollector.shutdown(invoke_exit=False)
        writer.stop(wait_on_join=False)

        self._logger.debug('Shutting down -- joining the reader thread.')
        reader.join(1)

        self._logger.debug('Shutting down -- joining the writer thread.')
        writer.stop(join_timeout=1)

    @staticmethod
    def __get_collectors_directory():
        # We determine the collectors directory by looking at the parent directory of where this file resides
        # and then going down third_party/tcollector/collectors.
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, 'third_party', 'tcollector',
                            'collectors')

if __name__ == "__main__":
    # Run in stand-alone mode for testing, just emitting log to stdout.
    ScalyrMonitor.run_standalone_monitor(SystemMetricsMonitor)
