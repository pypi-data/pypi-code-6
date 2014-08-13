#!/usr/bin/env python
# Copyright 2014, Scalyr, Inc.
###
# chkconfig: 2345 98 02
# description: Manages the Scalyr Agent 2, which provides log copying
#     and basic system metric collection.
###
### BEGIN INIT INFO
# Provides: scalyr-agent-2
# Required-Start: $network
# Required-Stop: $network
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Description: Manages the Scalyr Agent 2, which provides log copying
#     and back system metric collection.
### END INIT INFO

import errno
import os
import sys
import inspect
import time

# This is suppose to be a system-independent way of adding the necessary parent directory
# to the python path so that everything executes properly.  We do not rely on __file__ because
# some folks report problems with that when running on some versions of Windows.
# Get the file for this script and make it absolute.
file_path = inspect.stack()[0][1]
if not os.path.isabs(file_path):
    file_path = os.path.abspath(file_path)
file_path = os.path.realpath(file_path)

# We rely on the fact that the agent_main.py file should be in a directory structure that looks like:
# py/scalyr_agent/agent_main.py  .  We wish to add 'py' to the path, so the parent of the parent.
sys.path.append(os.path.dirname(os.path.dirname(file_path)))

import scalyr_agent.scalyr_logging as scalyr_logging
import scalyr_agent.util as scalyr_util
import scalyr_agent.remote_shell as remote_shell

# We have to be careful to set this logger class very early in processing, even before other
# imports to ensure that any loggers created are AgentLoggers.
from scalyr_agent.monitors_manager import MonitorsManager

log = scalyr_logging.getLogger('scalyr_agent')
scalyr_logging.set_agent_log_destination(use_stdout=True)


from optparse import OptionParser

from scalyr_agent.scalyr_client import ScalyrClientSession
from scalyr_agent.copying_manager import CopyingManager
from scalyr_agent.configuration import Configuration
from scalyr_agent.unix_daemon import UnixDaemonController
from scalyr_agent.util import RunState
from scalyr_agent.util import Util
from scalyr_agent.agent_status import AgentStatus
from scalyr_agent.agent_status import ConfigStatus
from scalyr_agent.agent_status import OverallStats

import getpass

# Set up the main logger.  We set it up initially to log to standard out,
# but once we run fork off the daemon, we will use a rotating log file.

# This VERSION line must stay in this format.  Other tools grep for this
# pattern so do not change it, just update the contents of the str.
VERSION = '2.0.0.beta.3'

STATUS_FILE = 'last_status'


class ScalyrAgent(object):
    def __init__(self):
        # NOTE:  This abstraction is not thread safe, but it does not need to be.  Even the calls to
        # create the status file are always issued on the main thread since that's how signals are handled.

        # The current config being used to run the agent.  This may not be the latest
        # version of the config, if that latest version had parsing errors.
        self.__config = None
        # The platform-specific controller that does things like fork daemon processes, sleeps, etc.
        self.__controller = None
        self.__config_file_path = None
        # If the current contents of the configuration file has errors in it, then this will be set to the config
        # object produced by reading it.
        self.__current_bad_config = None
        # The last time the configuration file was checked to see if it had changed.
        self.__last_config_check_time = None
        self.__start_time = None
        # The path where the agent log file is being written.
        self.__log_file_path = None
        # The current copying manager.
        self.__copying_manager = None
        # The current monitors manager.
        self.__monitors_manager = None
        # Tracks whether or not the agent should still be running.  When a terminate signal is received,
        # the run state is set to false.  Threads are expected to notice this and finish as quickly as
        # possible.
        self.__run_state = None

        # Whether or not the unsafe debugging mode is running (meaning the RemoteShell is accepting connections
        # on the local host port and the memory profiler is turned on).  Note, this mode is very unsafe since
        # arbitrary python commands can be executed by any user on the system as the user running the agent.
        self.__unsafe_debugging_running = False
        # A reference to the remote shell debug server.
        self.__debug_server = None

    def main(self, config_file_path, command, options):
        quiet = options.quiet
        verbose = options.verbose
        no_fork = options.no_fork
        no_change_user = options.no_change_user

        if command == 'version':
            print 'The Scalyr Agent version is %s' % VERSION
            return 0

        if config_file_path is None:
            # TODO: Change this default
            config_file_path = Configuration.default_config_file_path()

        self.__config_file_path = config_file_path
        self.__config = self.__read_config(config_file_path, command != 'stop' and command != 'status')

        if self.__config is not None:
            pid_file = os.path.join(self.__config.agent_log_path, 'agent.pid')
        elif options.pid_file is None:
            pid_file = os.path.join(Configuration.default_agent_log_path(), 'agent.pid')
            print >> sys.stderr, 'Could not parse configuration file at \'%s\'' % config_file_path
            print >> sys.stderr, 'Assuming pid file is \'%s\'.  Use --pid-file to override.' % pid_file
        else:
            print >> sys.stderr, 'Could not parse configuration file at \'%s\'' % config_file_path
            pid_file = os.path.abspath(options.pid_file)
            print >> sys.stderr, 'Using pid file \'%s\'.' % pid_file

        try:
            # TODO: Change this default
            self.__controller = UnixDaemonController(pid_file)
            if command == 'start':
                return self.__start(quiet, no_fork, no_change_user)
            elif command == 'stop':
                return sys.exit(self.__stop(quiet))
            elif command == 'status' and not verbose:
                return self.__status()
            elif command == 'status' and verbose:
                if self.__config is not None:
                    agent_data_path = self.__config.agent_data_path
                else:
                    agent_data_path = Configuration.default_agent_data_path()
                    print >> sys.stderr, 'Assuming agent data path is \'%s\'' % agent_data_path
                return self.__detailed_status(agent_data_path)
            elif command == 'restart':
                return self.__restart(quiet, no_fork, no_change_user)
            elif command == 'condrestart':
                return self.__condrestart(quiet, no_fork, no_change_user)
            else:
                print >> sys.stderr, 'Unknown command given: "%s".' % command
                return 1
        except SystemExit:
            return 0
        except Exception:
            log.exception('Caught exception when attempt to execute command %s', command)
            return 1

    def __read_config(self, config_file_path, fail_on_error):
        try:
            config_file = Configuration(config_file_path, CopyingManager.build_log, MonitorsManager.build_monitor)
            config_file.parse()
            return config_file
        except Exception, e:
            if not fail_on_error:
                return None
            print >> sys.stderr, 'Error reading configuration file: %s' % str(e)
            print >> sys.stderr, 'Terminating agent, please fix the configuration file and restart agent.'
            sys.exit(1)

    def __start(self, quiet, no_fork, no_change_user):
        running_user = os.geteuid()
        desired_user = os.stat(self.__config.file_path).st_uid
        if no_change_user:
            if running_user != desired_user:
                print >> sys.stderr, 'No change user is selected by agent is not being run by correct user.'
                print >> sys.stderr, 'Terminating agent, please restart agent using correct user.'
        else:
            self.__controller.run_as_user(desired_user, os.path.realpath(__file__))
        self.__controller.fail_if_already_running()

        try:
            self.__verify_can_write_to_logs_and_data(self.__config)
        except Exception, e:
            print >> sys.stderr, '%s' % e.message
            print >> 'Terminating agent, please fix the error and restart the agent.'
            return 1

        def run_wrapper():
            self.__start_time = time.time()
            self.__run()

        def handle_terminate_wrapper():
            self.__handle_terminate()

        client = self.__create_client(quiet=True)
        result = client.ping()
        if client.ping() != 'success':
            print >> sys.stderr, 'Fail to connect to %s.  Error result was "%s".' % (self.__config.scalyr_server,
                                                                                     result)
            print >> sys.stderr, ('The server address could be wrong, there maybe a network connectivity issue, '
                                  'or the provided api_token could be incorrect.')
            print >> sys.stderr, 'Terminating agent, please fix connectivity or api_token issue and restart agent.'
            return 1
        client.close()

        if not quiet:
            print "Configuration and server connection verified, starting agent in background."

        if not no_fork:
            self.__controller.start_daemon(run_wrapper, handle_terminate_wrapper)
        else:
            run_wrapper()
        return 0

    def __handle_terminate(self):
        if self.__run_state.is_running():
            log.info('Received signal to shutdown, attempt to shutdown cleanly.')
            self.__run_state.stop()

    def __detailed_status(self, data_directory):
        # The status works by sending telling the running agent to dump the status into a well known file and
        # then we read it from there, echoing it to stdout.
        if not os.path.isdir(data_directory):
            print >> sys.stderr, ('Cannot get status due to bad config.  The data path "%s" is not a directory' %
                                  data_directory)
            return 1

        status_file = os.path.join(data_directory, STATUS_FILE)
        # This users needs to zero out the current status file (if it exists), so they need write access to it.
        # When we do create the status file, we give everyone read/write access, so it should not be an issue.
        if os.path.isfile(status_file) and not os.access(status_file, os.W_OK):
            print >> sys.stderr, ('Cannot get status due to insufficient permissions.  The current user does not '
                                  'have write access to "%s" as required.' % status_file)
            return 1

        # Zero out the current file so that we can detect once the agent process has updated it.
        if os.path.isfile(status_file):
            f = file(status_file, 'w')
            f.truncate(0)
            f.close()

        # Signal to the running process.  This should cause that process to write to the status file
        result = self.__controller.request_status()
        if result is not None:
            if result == errno.ESRCH:
                print >> sys.stderr, 'The agent does not appear to be running.'
                return 1
            elif result == errno.EPERM:
                # TODO:  We probably should just get the name of the user running the agent and output it
                # here, instead of hard coding it to root.
                print >> sys.stderr, 'To view agent status, you must be running as the same user as the agent. Try running this command as root.'
                return 2

        # We wait for five seconds at most to get the status.
        deadline = time.time() + 5

        # Now loop until we see it show up.
        while True:
            if os.path.isfile(status_file) and os.path.getsize(status_file) > 0:
                break

            if time.time() > deadline:
                if self.__config is not None:
                    agent_log = os.path.join(self.__config.agent_log_path, 'agent.log')
                else:
                    agent_log = os.path.join(Configuration.default_agent_log_path(), 'agent.log')
                print >> sys.stderr, ('Failed to get status within 5 seconds.  Giving up.  The agent process is '
                                      'possibly stuck.  See %s for more details.' % agent_log)
                return 1

            time.sleep(0.03)

        if not os.access(status_file, os.R_OK):
            print >> sys.stderr, ('Cannot get status due to insufficient permissions.  The current user does not '
                                  'have read access to "%s" as required.' % status_file)
            return 1

        fp = open(status_file)
        for line in fp:
            print line.rstrip()
        fp.close()

        return 0

    def __generate_status(self):
        result = AgentStatus()
        result.launch_time = self.__start_time
        result.user = getpass.getuser()
        result.version = VERSION
        result.server_host = self.__config.server_attributes['serverHost']
        result.scalyr_server = self.__config.scalyr_server
        result.log_path = self.__log_file_path

        config_result = ConfigStatus()
        result.config_status = config_result

        config_result.last_check_time = self.__last_config_check_time
        if self.__current_bad_config is not None:
            config_result.path = self.__current_bad_config.file_path
            config_result.additional_paths = list(self.__current_bad_config.additional_file_paths)
            config_result.last_read_time = self.__current_bad_config.read_time
            config_result.status = 'Error, using last good configuration'
            config_result.last_error = self.__current_bad_config.error
            config_result.last_good_read = self.__config.read_time
            config_result.last_check_time = self.__last_config_check_time
        else:
            config_result.path = self.__config.file_path
            config_result.additional_paths = list(self.__config.additional_file_paths)
            config_result.last_read_time = self.__config.read_time
            config_result.status = 'Good'
            config_result.last_error = None
            config_result.last_good_read = self.__config.read_time

        if self.__copying_manager is not None:
            result.copying_manager_status = self.__copying_manager.generate_status()
        if self.__monitors_manager is not None:
            result.monitor_manager_status = self.__monitors_manager.generate_status()

        return result

    def __log_overall_stats(self, base_overall_stats):
        stats = self.__calculate_overall_stats(base_overall_stats)

        log.info('agent_status launch_time="%s" version="%s" watched_paths=%ld copying_paths=%ld total_bytes_copied=%ld'
                 ' total_bytes_skipped=%ld total_bytes_subsampled=%ld total_redactions=%ld total_bytes_failed=%ld '
                 'total_copy_request_errors=%ld total_monitor_reported_lines=%ld running_monitors=%ld dead_monitors=%ld'
                 ' user_cpu_=%f system_cpu=%f ram_usage=%ld' % (scalyr_util.format_time(stats.launch_time),
                                                                stats.version, stats.num_watched_paths,
                                                                stats.num_copying_paths, stats.total_bytes_copied,
                                                                stats.total_bytes_skipped, stats.total_bytes_subsampled,
                                                                stats.total_redactions, stats.total_bytes_failed,
                                                                stats.total_copy_requests_errors,
                                                                stats.total_monitor_reported_lines,
                                                                stats.num_running_monitors,
                                                                stats.num_dead_monitors, stats.user_cpu,
                                                                stats.system_cpu, stats.rss_size))

    def __calculate_overall_stats(self, base_overall_stats):
        current_status = self.__generate_status()

        delta_stats = OverallStats()

        watched_paths = 0
        copying_paths = 0

        if current_status.copying_manager_status is not None:
            delta_stats.total_copy_requests_errors = current_status.copying_manager_status.total_errors
            watched_paths = len(current_status.copying_manager_status.log_matchers)
            for matcher in current_status.copying_manager_status.log_matchers:
                copying_paths += len(matcher.log_processors_status)
                for processor_status in matcher.log_processors_status:
                    delta_stats.total_bytes_copied += processor_status.total_bytes_copied
                    delta_stats.total_bytes_skipped += processor_status.total_bytes_skipped
                    delta_stats.total_bytes_subsampled += processor_status.total_bytes_dropped_by_sampling
                    delta_stats.total_bytes_failed += processor_status.total_bytes_failed
                    delta_stats.total_redactions += processor_status.total_redactions

        running_monitors = 0
        dead_monitors = 0

        if current_status.monitor_manager_status is not None:
            running_monitors = current_status.monitor_manager_status.total_alive_monitors
            dead_monitors = len(current_status.monitor_manager_status.monitors_status) - running_monitors
            for monitor_status in current_status.monitor_manager_status.monitors_status:
                delta_stats.total_monitor_reported_lines += monitor_status.reported_lines
                delta_stats.total_monitor_errors += monitor_status.errors

        result = delta_stats + base_overall_stats

        # Overwrite some of the stats that are not affected by the add operation.
        result.launch_time = current_status.launch_time
        result.version = current_status.version
        result.num_watched_paths = watched_paths
        result.num_copying_paths = copying_paths
        result.num_running_monitors = running_monitors
        result.num_dead_monitors = dead_monitors

        (result.user_cpu, result.system_cpu, result.rss_size) = self.__controller.get_usage_info()

        return result

    def __report_status(self, output):
        status = self.__generate_status()

        print >>output, 'Scalyr Agent status.  See https://www.scalyr.com/help/scalyr-agent-2 for help'
        print >>output, ''
        print >>output, 'Current time:     %s' % scalyr_util.format_time(time.time())
        print >>output, 'Agent started at: %s' % scalyr_util.format_time(status.launch_time)
        print >>output, 'Version:          %s' % status.version
        print >>output, 'Agent running as: %s' % status.user
        print >>output, 'Agent log:        %s' % status.log_path
        print >>output, 'ServerHost:       %s' % status.server_host
        print >>output, ''
        print >>output, 'View data from this agent at: %s/events?filter=$serverHost%%3D%%27%s%%27' % (
            status.scalyr_server, status.server_host)
        print >>output, ''
        print >>output, ''

        # Configuration file status:
        print >>output, ''
        print >>output, 'Agent configuration:'
        print >>output, '===================='
        print >>output, ''
        if len(status.config_status.additional_paths) == 0:
            print >>output, 'Configuration file:    %s' % status.config_status.path
        else:
            print >>output, 'Configuration files:   %s' % status.config_status.path
            for x in status.config_status.additional_paths:
                print >>output, '                       %s' % x

        if status.config_status.last_error is None:
            print >>output, 'Status:                Good (files parsed successfully)'
        else:
            print >>output, 'Status:                Bad (could not parse, using last good version)'
        print >>output, 'Last checked:          %s' % scalyr_util.format_time(status.config_status.last_check_time)
        print >>output, 'Last changed observed: %s' % scalyr_util.format_time(status.config_status.last_read_time)

        if status.config_status.last_error is not None:
            print >>output, 'Parsing error:         %s' % status.config_status.last_error

        if status.copying_manager_status is not None:
            print >>output, ''
            print >>output, ''
            self.__report_copying_manager(output, status.copying_manager_status, status.config_status.last_read_time)

        if status.monitor_manager_status is not None:
            print >>output, ''
            print >>output, ''
            self.__report_monitor_manager(output, status.monitor_manager_status, status.config_status.last_read_time)

    def __report_copying_manager(self, output, manager_status, read_time):
        print >>output, 'Log transmission:'
        print >>output, '================='
        print >>output, ''
        print >>output, '(these statistics cover the period from %s)' % scalyr_util.format_time(read_time)
        print >>output, ''

        print >>output, 'Bytes uploaded successfully:               %ld' % manager_status.total_bytes_uploaded
        print >>output, 'Last successful communication with Scalyr: %s' % scalyr_util.format_time(
            manager_status.last_success_time)
        print >>output, 'Last attempt:                              %s' % scalyr_util.format_time(
            manager_status.last_attempt_time)
        if manager_status.last_attempt_size is not None:
            print >>output, 'Last copy request size:                    %ld' % manager_status.last_attempt_size
        if manager_status.last_response is not None:
            print >>output, 'Last copy response size:                   %ld' % len(manager_status.last_response)
            print >>output, 'Last copy response status:                 %s' % manager_status.last_response_status
            if manager_status.last_response_status != 'success':
                print >>output, 'Last copy response:                        %s' % Util.remove_newlines_and_truncate(
                    manager_status.last_response, 1000)
        if manager_status.total_errors > 0:
            print >>output, 'Total responses with errors:               %d (see \'%s\' for details)' % (
                manager_status.total_errors, self.__config.file_path)
        print >>output, ''

        for matcher_status in manager_status.log_matchers:
            if not matcher_status.is_glob:
                for processor_status in matcher_status.log_processors_status:
                    output.write('Path %s: copied %ld bytes (%ld lines), %ld bytes pending, ' % (
                        processor_status.log_path, processor_status.total_bytes_copied,
                        processor_status.total_lines_copied, processor_status.total_bytes_pending))
                    if processor_status.total_bytes_skipped > 0:
                        output.write('%ld bytes skipped, ' % processor_status.total_bytes_skipped)
                    if processor_status.total_bytes_failed > 0:
                        output.write('%ld bytes failed, ' % processor_status.total_bytes_failed)
                    if processor_status.total_bytes_dropped_by_sampling > 0:
                        output.write('%ld bytes dropped by sampling (%ld lines), ' % (
                            processor_status.total_bytes_dropped_by_sampling,
                            processor_status.total_lines_dropped_by_sampling))

                    if processor_status.total_redactions > 0:
                        output.write('%ld redactions, ' % processor_status.total_redactions)
                    output.write('last checked %s' % scalyr_util.format_time(processor_status.last_scan_time))
                    output.write('\n')
                    output.flush()

        need_to_add_extra_line = True
        for matcher_status in manager_status.log_matchers:
            if matcher_status.is_glob:
                if need_to_add_extra_line:
                    need_to_add_extra_line = False
                    print >>output, ''
                print >>output, 'Glob: %s:: last scanned for glob matches at %s' % (
                    matcher_status.log_path, scalyr_util.format_time(matcher_status.last_check_time))

                for processor_status in matcher_status.log_processors_status:
                    output.write('  %s: copied %ld bytes (%ld lines), %ld bytes pending, ' % (
                        processor_status.log_path, processor_status.total_bytes_copied,
                        processor_status.total_lines_copied, processor_status.total_bytes_pending))
                    if processor_status.total_bytes_skipped > 0:
                        output.write('%ld bytes skipped, ' % processor_status.total_bytes_skipped)
                    if processor_status.total_bytes_failed > 0:
                        output.write('%ld bytes failed, ' % processor_status.total_bytes_failed)
                    if processor_status.total_bytes_dropped_by_sampling > 0:
                        output.write('%ld bytes dropped by sampling (%ld lines), ' % (
                            processor_status.total_bytes_dropped_by_sampling,
                            processor_status.total_lines_dropped_by_sampling))

                    if processor_status.total_redactions > 0:
                        output.write('%ld redactions, ' % processor_status.total_redactions)
                    output.write('last checked %s' % scalyr_util.format_time(processor_status.last_scan_time))
                    output.write('\n')
                    output.flush()

    def __report_monitor_manager(self, output, manager_status, read_time):
        print >>output, 'Monitors:'
        print >>output, '========='
        print >>output, ''
        print >>output, '(these statistics cover the period from %s)' % scalyr_util.format_time(read_time)
        print >>output, ''
        if manager_status.total_alive_monitors < len(manager_status.monitors_status):
            print >>output, 'Running monitors:'
            padding = '  '
        else:
            padding = ''

        for entry in manager_status.monitors_status:
            if entry.is_alive:
                print >>output, '%s%s: %d lines emitted, %d errors' % (
                    padding, entry.monitor_name, entry.reported_lines, entry.errors)

        dead_monitors = len(manager_status.monitors_status) - manager_status.total_alive_monitors
        if dead_monitors > 0:
            print >>output, ''
            print >>output, 'Failed monitors:'
            for entry in manager_status.monitors_status:
                if not entry.is_alive:
                    print >>output, '  %s %d lines emitted, %d errors' % (
                        entry.monitor_name, entry.reported_lines, entry.errors)

    def __report_status_to_file(self):
        tmp_file = None
        try:
            tmp_file_path = os.path.join(self.__config.agent_data_path, 'last_status.tmp')
            final_file_path = os.path.join(self.__config.agent_data_path, 'last_status')
            if os.path.isfile(final_file_path):
                os.remove(final_file_path)
            tmp_file = open(tmp_file_path, 'w')
            self.__report_status(tmp_file)
            tmp_file.close()
            tmp_file = None

            os.rename(tmp_file_path, final_file_path)
        except Exception:
            log.exception('Exception caught will try to report status', error_code='failedStatus')
            if tmp_file is not None:
                tmp_file.close()

    def __stop(self, quiet):
        status = self.__controller.stop_daemon(quiet)
        return status

    def __status(self):
        if self.__controller.is_running():
            print 'The agent is running. For details, use "scalyr-agent-2 status -v".'
            return 0
        else:
            print 'The agent does not appear to be running.'
            return 4

    def __condrestart(self, quiet, no_fork, no_change_user):
        if self.__controller.is_running():
            if not quiet:
                print 'Agent is running, restarting now.'
            if self.__stop(quiet) != 0:
                print >>sys.stderr, 'Failed to stop the running agent.  Cannot restart until it is killed'
                return 1

            return self.__start(quiet, no_fork, no_change_user)
        elif not quiet:
            print 'Agent is not running, not restarting.'
            return 0

    def __restart(self, quiet, no_fork, no_change_user):
        if self.__controller.is_running():
            if not quiet:
                print 'Agent is running, stopping it now.'
            if self.__stop(quiet) != 0:
                print >>sys.stderr, 'Failed to stop the running agent.  Cannot restart until it is killed'
                return 1

        return self.__start(quiet, no_fork, no_change_user)

    def __run(self):
        # The stats we track for the lifetime of the agent.  This variable tracks the accumulated stats since the
        # last stat reset (the stats get reset every time we read a new configuration).
        base_overall_stats = OverallStats()
        # We only emit the overall stats once ever ten minutes.  Track when we last reported it.
        last_overall_stats_report_time = time.time()
        # The thread that runs the monitors and and the log copier.
        worker_thread = None

        try:
            try:
                self.__run_state = RunState()
                self.__log_file_path = os.path.join(self.__config.agent_log_path, 'agent.log')
                scalyr_logging.set_agent_log_destination(file_path=self.__log_file_path)
                # We record where the log file currently is so that we can (in the worse case) start copying it
                # from this position.  That way we capture the first 'Starting scalyr agent' call.
                agent_log_position = self.__get_file_initial_position(self.__log_file_path)
                if agent_log_position is not None:
                    logs_initial_positions = {self.__log_file_path: agent_log_position}
                else:
                    logs_initial_positions = None

                log.info('Starting scalyr agent... (version=%s)' % VERSION)

                self.__start_or_stop_unsafe_debugging()

                worker_thread = WorkerThread(self.__config, self.__create_client(), logs_initial_positions)
                self.__copying_manager = worker_thread.copying_manager
                self.__monitors_manager = worker_thread.monitors_manager

                worker_thread.start()

                # Register handler for when we get an interrupt signal.  That indicates we should dump the status to
                # a file because a user has run the 'detailed_status' command.
                self.__controller.register_for_status_requests(self.__report_status_to_file)

                while not self.__run_state.sleep_but_awaken_if_stopped(30):
                    current_time = time.time()
                    self.__last_config_check_time = current_time

                    # Log the overall stats once every 10 mins.
                    if current_time > last_overall_stats_report_time + 600:
                        self.__log_overall_stats(base_overall_stats)
                        last_overall_stats_report_time = current_time

                    new_config = Configuration(self.__config_file_path, CopyingManager.build_log,
                                               MonitorsManager.build_monitor)
                    try:
                        new_config.parse()
                        self.__verify_can_write_to_logs_and_data(new_config)

                    except Exception, e:
                        log.error(
                            'Bad configuration file seen.  Ignoring, using last known good configuration file.  '
                            'Exception was "%s"', str(e), error_code='badConfigFile')
                        self.__current_bad_config = new_config
                        continue

                    self.__current_bad_config = None

                    if not self.__config.equivalent(new_config):
                        # We are about to reset the current workers, so we will lose their contribution
                        # to the stats, so recalculate the base.
                        base_overall_stats = self.__calculate_overall_stats(base_overall_stats)
                        log.info('New configuration file seen.')
                        log.info('Stopping copying and metrics threads.')
                        worker_thread.stop()
                        worker_thread = None
                        self.__config = new_config

                        self.__start_or_stop_unsafe_debugging()
                        log.info('Starting new copying and metrics threads')
                        worker_thread = WorkerThread(self.__config, self.__create_client())
                        self.__copying_manager = worker_thread.copying_manager
                        self.__monitors_manager = worker_thread.monitors_manager

                        worker_thread.start()

                # Log the stats one more time before we terminate.
                self.__log_overall_stats(self.__calculate_overall_stats(base_overall_stats))

            except Exception:
                log.exception('Main run method for agent failed due to exception', error_code='failedAgentMain')
        finally:
            if worker_thread is not None:
                worker_thread.stop()

    def __create_client(self, quiet=False):
        return ScalyrClientSession(self.__config.scalyr_server, self.__config.api_key, quiet=quiet)

    def __get_file_initial_position(self, path):
        try:
            return os.path.getsize(path)
        except OSError, e:
            if e.errno == errno.EPERM:
                log.warn('Insufficient permissions to read agent logs initial position')
                return None
            elif e.errno == errno.ENOENT:
                # If file doesn't exist, just return 0 as its initial position
                return 0
            else:
                log.exception('Error trying to read agent logs initial position')
                return None

    def __verify_can_write_to_logs_and_data(self, config):
        if not os.path.isdir(self.__config.agent_log_path):
            raise Exception('The agent log directory \'%s\' does not exist.' % self.__config.agent_log_path)

        if not os.access(self.__config.agent_log_path, os.W_OK):
            raise Exception('User cannot write to agent log directory \'%s\'.' % self.__config.agent_log_path)

        if not os.path.isdir(self.__config.agent_data_path):
            raise Exception('The agent data directory \'%s\' does not exist.' % self.__config.agent_data_path)

        if not os.access(self.__config.agent_data_path, os.W_OK):
            raise Exception('User cannot write to agent data directory \'%s\'.' % self.__config.agent_data_path)

    def __start_or_stop_unsafe_debugging(self):
        should_be_running = self.__config.use_unsafe_debugging

        if should_be_running and not self.__unsafe_debugging_running:
            self.__unsafe_debugging_running = True
            self.__debug_server = remote_shell.DebugServer()
            self.__debug_server.start()
        elif not should_be_running and self.__unsafe_debugging_running:
            if self.__debug_server is not None:
                self.__debug_server.stop()
                self.__debug_server = None
            self.__unsafe_debugging_running = False




class WorkerThread(object):
    """A thread used to run the log copier and the monitor manager.
    """
    def __init__(self, configuration, scalyr_client, logs_initial_positions=None):
        self.__scalyr_client = scalyr_client
        self.copying_manager = CopyingManager(scalyr_client, configuration, logs_initial_positions)
        self.monitors_manager = MonitorsManager(configuration)

    def start(self):
        self.copying_manager.start()
        # We purposely wait for the copying manager to begin copying so that if the monitors create any new
        # files, they will be guaranteed to be copying up to the server starting at byte index zero.
        # Note, if copying never begins then the copying manager will sys exit, so this next call will never just
        # block indefinitely will the process hangs around.
        self.copying_manager.wait_for_copying_to_begin()
        self.monitors_manager.start()

    def stop(self):
        log.debug('Shutting down monitors')
        self.monitors_manager.stop()

        log.debug('Shutting copy monitors')
        self.copying_manager.stop()

        log.debug('Shutting client')
        self.__scalyr_client.close()

if __name__ == '__main__':
    parser = OptionParser(usage='Usage: scalyr-agent-2 [options] (start|stop|status|restart|condrestart|version)',
                          version='scalyr-agent v' + VERSION)
    parser.add_option("-c", "--config-file", dest="config_filename",
                      help="Read configuration from FILE", metavar="FILE")
    parser.add_option("-p", "--pid-file", dest="pid_file",
                      help="The path storing the running agent's process id.  Only used if config cannot be parsed.")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False,
                      help="Only print error messages when running the start and stop commands")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                      help="For status command, prints detailed information about running agent.")
    parser.add_option("", "--no-fork", action="store_true", dest="no_fork", default=False,
                      help="For the run command, does not fork the program to the background.")
    parser.add_option("", "--no-change-user", action="store_true", dest="no_change_user", default=False,
                      help="Forces agent to not change which user is executing agent.  Requires the right user is "
                           "already being used.  This is used internally to prevent infinite loops in changing to"
                           "the correct user.  Users should not need to set this option.")

    (options, args) = parser.parse_args()
    if len(args) < 1:
        print >> sys.stderr, 'You must specify a command, such as "start", "stop", or "status".'
        parser.print_help(sys.stderr)
        sys.exit(1)
    elif len(args) > 1:
        print >> sys.stderr, 'Too many commands specified.  Only specify one of "start", "stop", "status".'
        parser.print_help(sys.stderr)
        sys.exit(1)
    elif args[0] not in ('start', 'stop', 'status', 'restart', 'condrestart', 'version'):
        print >> sys.stderr, 'Unknown command given: "%s"' % args[0]
        parser.print_help(sys.stderr)
        sys.exit(1)

    if options.config_filename is not None and not os.path.isabs(options.config_filename):
        options.config_filename = os.path.abspath(options.config_filename)
    sys.exit(ScalyrAgent().main(options.config_filename, args[0], options))
