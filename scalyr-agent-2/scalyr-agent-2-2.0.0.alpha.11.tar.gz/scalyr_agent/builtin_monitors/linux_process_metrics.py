# Copyright 2014, Scalyr, Inc.

from scalyr_agent.scalyr_monitor import ScalyrMonitor

from subprocess import Popen, PIPE

import os
import re
import time


# The base class for all readers.  Each reader class is responsible for
# collecting a set of statistics from a single per-process proc file such
# as /proc/self/stat.  We create an instance for a reader for each application
# that is being monitored.  This instance is created once and then used from
# then on until the monitored process terminates.
class BaseReader:
    # Initialize the base class.  The file_pattern should be a string that
    # specifies which file should be read for the statistics.  It should
    # contain a %d somewhere in it to hold the process id number, such as
    # "/proc/%d/stat".
    # Pid is the id of the process that has been found to be monitored.
    # Id is the name of the process to be used in reporting its stats.
    def __init__(self, pid, monitor_id, logger, file_pattern):
        self.pid = pid
        self.id = monitor_id
        self.file_pattern = file_pattern
        self.file = None
        self.timestamp = None
        self.failed = False
        self.logger = logger

    # The main loop for the readers.  This will run a single sample collection
    # cycle.
    def run_single_cycle(self):
        self.timestamp = int(time.time())

        # There are certain error conditions, such as the system not supporting
        # a particular proc file type, that we will never recover from.  So,
        # just always early exit.
        if self.failed:
            return

        filename = self.file_pattern % self.pid

        if self.file is None:
            try:
                self.file = open(filename, "r")
            except IOError as e:
                # We take a simple approach.  If we don't find the file or
                # don't have permissions for it, then just don't collect this
                # stat from now on.  If the user changes the configuration file
                # we will try again to read the file then.
                if e.errno == 13:
                    self.logger.error("Tcollector does not have permission to read %s.  "
                                      "Maybe you should run it as root.", filename)
                    self.failed = True
                elif e.errno == 2:
                    self.logger.error("Tcollector cannot read %s.  Your system may not support that proc file type",
                                      filename)
                    self.failed = True
                else:
                    raise e

        if self.file is not None:
            self.file.seek(0)
            self.gather_sample(self.file)

    # Derived reader classes must override this method to perform the actual
    # work of collecting its specific samples.  It should use file to read
    # the stats.
    def gather_sample(self, my_file):
        return None

    # Must be called to close all necessary files opened by the reader.
    def close(self):
        try:
            self.failed = True
            if self.file is not None:
                self.file.close()
            self.failed = False
        finally:
            self.file = None

    # Properly emit the specified metric to stdout.  You may also specify
    # a type value which will be emitted as 'type=type_value'.
    def print_sample(self, metric_name, metric_value, type_value=None):
        # For backward compatibility, we also publish the monitor id as 'app' in all reported stats.
        extra = {
            'app': self.id,
        }
        if type_value is not None:
            extra['type'] = type_value

        self.logger.emit_value(metric_name, metric_value, extra)



# Reads statistics from /proc/$pid/stat.
# - app.cpu type=user app=id    (number of 1/100ths seconds of user cpu time)
# - app.cpu type=system app=id  (number of 1/100ths seconds of system cpu time)
# - app.uptime app=id           (number of milliseconds of uptime)
# - app.threads app=id
# - app.nice app=id
class StatReader(BaseReader):
    def __init__(self, pid, monitor_id, logger):
        BaseReader.__init__(self, pid, monitor_id, logger, "/proc/%ld/stat")
        self.jiffies_per_sec = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
        self.boot_time_ms = None

    # Returns the number of centiseconds for the given number of jiffies.
    def calculate_time_cs(self, jiffies):
        return int((jiffies * 100.0) / self.jiffies_per_sec)

    # Returns the number of milliseconds for the given number of jiffies.
    def calculate_time_ms(self, jiffies):
        return int((jiffies * 1000.0) / self.jiffies_per_sec)

    # Returns the number of milliseconds the system has been up.
    def get_uptime_ms(self):
        if self.boot_time_ms is None:
            # We read /proc/uptime once to get the current boot time.
            uptime_file = None
            try:
                uptime_file = open("/proc/uptime", "r")
                # The first number in the file is the number of seconds since
                # boot time.  So, we just use that to calculate the milliseconds
                # past epoch.
                self.boot_time_ms = int(time.time()) * 1000 - int(float(uptime_file.readline().split()[0]) * 1000.0)
            finally:
                if uptime_file is not None:
                    uptime_file.close()

        # Calculate the uptime by just taking current time and subtracting out
        # the boot time.
        return int(time.time()) * 1000 - self.boot_time_ms

    def gather_sample(self, stat_file):
        # The file format is just a single line of all the fields.
        line = stat_file.readlines()[0]
        # Chop off first part which is the pid and executable file. The
        # executable file is terminated with a paren so just search for that.
        line = line[(line.find(") ")+2):]
        fields = line.split()
        # Then the fields we want are just at fixed field positions in the
        # string.  Just grap them.
        self.print_sample("app.cpu",
                          self.calculate_time_cs(int(fields[11])), "user")
        self.print_sample("app.cpu",
                          self.calculate_time_cs(int(fields[12])), "system")
        process_uptime = self.get_uptime_ms() - self.calculate_time_ms(int(fields[19]))
        self.print_sample("app.uptime", process_uptime)

        self.print_sample("app.nice", fields[16])
        self.print_sample("app.threads", fields[17])


# Reads stats from /proc/$pid/status:
# - app.fd app=[id]
# - app.mem.bytes type=vmsize app=[id]
# - app.mem.bytes type=resident app=[id]
# - app.mem.bytes type=peak_vmsize app=[id]
# - app.mem.bytes type=peak_resident app=[id]
class StatusReader(BaseReader):
    def __init__(self, pid, monitor_id, logger):
        BaseReader.__init__(self, pid, monitor_id, logger, "/proc/%ld/status")

    def gather_sample(self, stat_file):
        # Each line is formated:
        #    FieldName:      value
        for line in stat_file:
            m = re.search('^(\w+):\s*(\d+)', line)
            if m is None:
                continue

            field_name = m.group(1)
            int_value = int(m.group(2))
# FDSize is not the same as the number of open file descriptors. Disable
# for now.
#            if field_name == "FDSize":
#                self.print_sample("app.fd", int_value)
            if field_name == "VmSize":
                self.print_sample("app.mem.bytes", int_value * 1024,
                                  "vmsize")
            elif field_name == "VmPeak":
                self.print_sample("app.mem.bytes", int_value * 1024,
                                  "peak_vmsize")
            elif field_name == "VmRSS":
                self.print_sample("app.mem.bytes", int_value * 1024,
                                  "resident")
            elif field_name == "VmHWM":
                self.print_sample("app.mem.bytes", int_value * 1024,
                                  "peak_resident")


# Reads stats from /proc/$pid/io.  Note, this io file is only supported on
# kernels 2.6.20 and beyond, but that kernel has been around since 2007.
# - app.disk.bytes type=read app=[id]
# - app.disk.requests type=read app=[id]
# - app.disk.bytes type=write app=[id]
# - app.disk.requests type=write app=[id]
class IoReader(BaseReader):
    def __init__(self, pid, monitor_id, logger):
        BaseReader.__init__(self, pid, monitor_id, logger, "/proc/%ld/io")

    def gather_sample(self, stat_file):
        # File format is single value per line with "fieldname:" prefix.
        for x in stat_file:
            fields = x.split()
            if fields[0] == "rchar:":
                self.print_sample("app.disk.bytes", fields[1], "read")
            elif fields[0] == "syscr:":
                self.print_sample("app.disk.requests", fields[1], "read")
            elif fields[0] == "wchar:":
                self.print_sample("app.disk.bytes", fields[1], "write")
            elif fields[0] == "syscw:":
                self.print_sample("app.disk.requests", fields[1], "write")


# Reads stats from /proc/$pid/net/netstat:
# - app.net.bytes type=in app=[id]
# - app.net.bytes type=out app=[id]
# - app.net.tcp_retransmits app=[id]
# Disabled for now!  This is not a per-app stat.
class NetStatReader(BaseReader):
    def __init__(self, pid, monitor_id, logger):
        BaseReader.__init__(self, pid, monitor_id, logger, "/proc/%ld/net/netstat")

    def gather_sample(self, stat_file):
        # This file format is weird.  Each set of stats is outputted in two
        # lines.  First, a header line that list the field names.  Then a
        # a value line where each value is specified in the appropriate column.
        # You have to match the column name from the header line to determine
        # what that column's value is.  Also, each pair of lines is prefixed
        # with the same name to make it clear they are tied together.
        all_lines = stat_file.readlines()
        # We will create an array of all of the column names in field_names
        # and all of the corresponding values in field_values.
        field_names = []
        field_values = []

        # To simplify the stats, we add together the two forms of retransmit
        # I could find in the netstats.  Those to fast retransmit Reno and those
        # to selective Ack.
        retransmits = 0
        found_retransmit_metric = False

        # Read over lines, looking at adjacent lines.  If their row names match,
        # then append their column names and values to field_names
        # and field_values.  This will break if the two rows are not adjacent
        # but I do not think that happens in practice.  If it does, we just
        # won't report the stats.
        for i in range(0, len(all_lines) - 1):
            names_split = all_lines[i].split()
            values_split = all_lines[i+1].split()
            # Check the row names are the same.
            if names_split[0] == values_split[0] and len(names_split) == len(values_split):
                field_names.extend(names_split)
                field_values.extend(values_split)

        # Now go back and look for the actual stats we care about.
        for i in range(0, len(field_names)):
            if field_names[i] == "InOctets":
                self.print_sample("app.net.bytes", field_values[i], "in")
            elif field_names[i] == "OutOctets":
                self.print_sample("app.net.bytes", field_values[i], "out")
            elif field_names[i] == "TCPRenoRecovery":
                retransmits += int(field_values[i])
                found_retransmit_metric = True
            elif field_names[i] == "TCPSackRecovery":
                retransmits += int(field_values[i])
                found_retransmit_metric = True

        # If we found both forms of retransmit, add them up.
        if found_retransmit_metric:
            self.print_sample("app.net.tcp_retransmits", retransmits)


# Reads stats from /proc/$pid/sockstat
# - app.net.sockets_in_use type=* app=[id]
# Disabled for now!  This is not a per-process stat.
class SockStatReader(BaseReader):
    def __init__(self, pid, monitor_id, logger):
        BaseReader.__init__(self, pid, monitor_id, logger, "/proc/%ld/net/sockstat")

    def gather_sample(self, stat_file):
        for line in stat_file:
            # We just look for the different "inuse" lines and output their
            # socket type along with the count.
            m = re.search('(\w+): inuse (\d+)', line)
            if m is not None:
                self.print_sample("app.net.sockets_in_use", m.group(2),
                                  m.group(1).lower())


class ProcessMonitor(ScalyrMonitor):
    """A Scalyr agent monitor that records metrics about a running process.
    """

    def __init__(self, monitor_config, log):
        ScalyrMonitor.__init__(self, monitor_config, log, sample_interval_secs=30)
        self.__gathers = []
        self.__pid = None
        self.__id = monitor_config['id']
        if 'commandline' not in monitor_config and 'pid' not in monitor_config:
            raise Exception('One of the fields "commandline" or "id" must be specified in the '
                            'process_metric configuration')
        if 'commandline' in monitor_config:
            self.__commandline_matcher = monitor_config["commandline"]
        else:
            self.__commandline_matcher = None

        if 'pid' in monitor_config:
            self.__target_pid = monitor_config['pid']
        else:
            self.__target_pid = None

        self.log_config = {
            'parser': 'agent-metrics',
            'path': 'linux_process_metrics.log',
        }

    def __set_process(self, pid):
        self.__pid = pid
        self.__gathers = []
        self.__gathers.append(StatReader(self.__pid, self.__id, self._logger))
        self.__gathers.append(StatusReader(self.__pid, self.__id, self._logger))
        self.__gathers.append(IoReader(self.__pid, self.__id, self._logger))
        # TODO: Re-enable these if we can find a way to get them to truly report
        # per-app statistics.
        #        self.gathers.append(NetStatReader(self.pid, self.id, self._logger))
        #        self.gathers.append(SockStatReader(self.pid, self.id, self._logger))

    def gather_sample(self):
        if self.__pid is not None and not self.__is_running():
            self.__pid = None
            for gather in self.__gathers:
                gather.close()
            self.__gathers = []

        if self.__pid is None:
            new_proc_id = self.__select_process()
            if new_proc_id is not None:
                self.__set_process(new_proc_id)

        for gather in self.__gathers:
            gather.run_single_cycle()

    # Returns a process id (or None) of a running process whose commandline
    # matches the regular expression in commandline_matcher or the process id in
    # target_id.
    def __select_process(self):
        sub_proc = None
        if self.__commandline_matcher is not None:
            try:
                sub_proc = Popen(['ps', 'ax', '-o', 'pid,command'],
                                 shell=False, stdout=PIPE)

                sub_proc.stdout.readline()
                for line in sub_proc.stdout:
                    line = line.strip()
                    if line.find(' ') > 0:
                        pid = int(line[:line.find(' ')])
                        line = line[(line.find(' ') + 1):]
                        if re.search(self.__commandline_matcher, line) is not None:
                            return pid
                return None
            finally:
                if sub_proc is not None:
                    sub_proc.wait()
        else:
            # See if the specified target pid is running.  If so, then return it.
            try:
                # Special case '$$' to mean this process.
                if self.__target_pid == '$$':
                    pid = os.getpid()
                else:
                    pid = int(self.__target_pid)
                os.kill(pid, 0)
                return pid
            except OSError:
                return None

    # Close all reads.
    def __close_gathers(self):
        for gather in self.__gathers:
            gather.close()

    # Returns true if the process this monitor maps to is still running.
    def __is_running(self):
        try:
            os.kill(self.__pid, 0)
            return True
        except OSError as e:
            # Errno #3 corresponds to the process not running.  We could get
            # other errors like this process does not have permission to send
            # a signal to self.pid.  But, if that error is returned to us, we
            # know the process is running at least, so we ignore the error.
            return e.errno != 3
