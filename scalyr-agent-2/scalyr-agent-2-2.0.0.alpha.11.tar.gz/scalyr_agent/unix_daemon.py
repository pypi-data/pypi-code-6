# Copyright 2014, Scalyr, Inc.

import errno
import sys
import pwd
import os
import time
import atexit
import resource
import signal



# Based on code by Sander Marechal posted at
# http://web.archive.org/web/20131017130434/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/

class UnixDaemonController:
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def __daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def __read_pidfile(self):
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        return pid

    def run_as_user(self, user_id, script_file):
        user_name = pwd.getpwuid(user_id).pw_name
        if os.geteuid() != user_id:
            if os.geteuid() != 0:
                print >>sys.stderr, ('Failing, cannot start scalyr_agent as correct user.  The current user (%s) does '
                                     'not own the config file and cannot change to that user because '
                                     'not root.' % user_name)
                sys.exit(1)
            # Use sudo to re-execute this script with the correct user.  We also pass in --no-change-user so that
            # there is no change we go into an infinite loop due to bugs in how we change the user.
            arguments = [ 'sudo', '-u', user_name, sys.executable, script_file, '--no-change-user'] + sys.argv[1:]

            print >>sys.stderr, ('Running as %s' % user_name)
            os.execvp("sudo", arguments)


    def is_running(self):
        pid = self.__read_pidfile()
        # TODO: Add in check for the pid file exists but the process is not running.
        return pid is not None

    def fail_if_already_running(self):
        pid = self.__read_pidfile()
        if pid:
            message = "The agent appears to be running pid=%d.  pidfile %s does exists.\n"
            sys.stderr.write(message % (pid, self.pidfile))
            sys.exit(1)

    def start_daemon(self, run_method, handle_terminate_method):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        self.fail_if_already_running()

        def handle_terminate(signal, frame):
            handle_terminate_method()

        original = signal.signal(signal.SIGTERM, handle_terminate)

        # Start the daemon
        self.__daemonize()
        result = run_method()

        signal.signal(signal.SIGTERM, original)

        if result is not None:
            sys.exit(result)
        else:
            sys.exit(99)

    def stop_daemon(self, quiet):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "The agent does not appear to be running.  pidfile %s does not exist.\n"
            sys.stderr.write(message % self.pidfile)
            return 0  # not an error in a restart

        if not quiet:
            print 'Sending signal to terminate agent.'

        # Try killing the daemon process
        try:
            # Do 5 seconds worth of TERM signals.  If that doesn't work, KILL it.
            term_attempts = 50
            while term_attempts > 0:
                os.kill(pid, signal.SIGTERM)
                UnixDaemonController.__sleep(0.1)
                term_attempts -= 1

            if not quiet:
                print 'Still waiting for agent to terminate, sending KILL signal.'

            while 1:
                os.kill(pid, signal.SIGKILL)
                UnixDaemonController.__sleep(0.1)

        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print 'Unable to terminate agent.'
                print str(err)
                return 1

        if not quiet:
            print 'Agent has stopped.'

        return 0

    @staticmethod
    def __sleep(seconds):
        try:
            time.sleep(seconds)
        except Exception:
            print 'Ignoring exception while sleeping'

    def restart_daemon(self, run_method):
        """
        Restart the daemon
        """
        self.stop_daemon()
        self.start_daemon(run_method)

    def sleep(self, seconds):
        """Sleeps for at most the specified number of seconds while also handling signals.

        Python does not do a great job of handling signals quickly when you invoke the normal time.sleep().
        This method is a Unix-specific implementation of a sleep that should do better quickly handling signals while
        sleeping.

        This method may return earlier than the requested number of seconds if a signal is received.

        Arguments:
            seconds:  The number of seconds to sleep for.
        """

        # We schedule an alarm signal for x=seconds out in the future.
        def handle_alarm(signal, frame):
            pass

        signal.signal(signal.SIGALRM, handle_alarm)
        signal.alarm(seconds)

        # Wait for either the alarm to go off or for us to receive a SIGINT.
        signal.pause()

        # Remove the alarm if it is still pending.
        signal.alarm(0)

    def request_status(self):
        """Invoked by a process that is not the agent to request the agent dump the current detail status to the status
        file.

        Returns:
            If there is an error, an errno that describes the error.  errno.EPERM indicates the current does not
            have permission to request the status.  errno.ESRCH indicates the agent is not running.
        """

        pid = self.__read_pidfile()
        if pid is None:
            return errno.ESRCH

        try:
            os.kill(pid, signal.SIGINT)
        except OSError, e:
            if e.errno == errno.ESRCH or e.errno == errno.EPERM:
                return e.errno
            raise e
        return None

    def register_for_status_requests(self, handler):
        def wrapped_handler(signal, frame):
            handler()
        signal.signal(signal.SIGINT, wrapped_handler)

    def get_usage_info(self):
        """Returns CPU and memory usage information.

        It returns the results in a tuple, with the first element being the number of
        CPU seconds spent in user land, the second is the number of CPU seconds spent in system land,
        and the third is the current resident size of the process in bytes."""

        usage_info = resource.getrusage(resource.RUSAGE_SELF)
        user_cpu = usage_info[0]
        system_cpu = usage_info[1]
        rss_size = usage_info[2]

        return user_cpu, system_cpu, rss_size


