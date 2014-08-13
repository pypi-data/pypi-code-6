# Copyright 2014, Scalyr, Inc.
#
# The Scalyr-specific extensions to the normal python Logger classes.  In particular, this provides
# a new AgentLogger class that extends logging.Logger to implement new features:
#   - Reporting metric values in a standard format (which can be parsed by the Scalyr servers)
#   - Rate limiting the number of bytes written to the agent log file (using a "leaky bucket" algorithm to
#       calculate the allowed number of bytes to write)
#   - Aggregating records reported from different modules into a central agent log
#

import logging
import logging.handlers
import os
import re
import sys
import time
import threading

from cStringIO import StringIO
from scalyr_agent.util import RateLimiter

import scalyr_agent.json_lib as json_lib


def getLogger(name):
    """Returns a logger instance to use for the given name that implements the Scalyr agent's extra logging features.

    This should be used in place of logging.getLogger when trying to retrieve a logging instance that implements
    Scalyr agent's extra features.

    Note, the logger instance will be configured to emit records at INFO level and above.

    Arguments:
        name:  The name of the logger, such as the module name.  If this is for a particular monitor instance, then
            the monitor id should be append at the end surrounded by brackets, such as "my_monitor[1]"

    Returns:
        A logger instance implementing the extra features.
    """
    logging.setLoggerClass(AgentLogger)
    result = logging.getLogger(name)
    result.setLevel(logging.INFO)
    return result


def set_agent_log_destination(use_stdout=False, file_path=None, max_bytes=20*1024*1024, backup_count=2,
                              log_write_rate=2000, max_write_burst=100000):
    """Updates where the log records destined for the main agent log are written.

    Any records created by logger instances associated with the agent log (which are typically passed to
    agent related modules or retrieved using agent_logging.getLogger) will be included in the agent log.
    This log is typically written to 'agent.log' but during startup, is sent to stdout.

    This method is not thread safe.

    Arguments:
        use_stdout:  True if the log should be sent to standard out.
        file_path:  If not None, then the path of the file where the log should be written.  The file will be
            rotated using a RotatingLogHandler scheme, with parameters specified by max_bytes and backup_count.
        max_bytes:  The maximum number of bytes written to file_path before it is rotated.
        backup_count:  The number of previously rotated logs to keep.
        log_write_rate:  The average number of bytes per second to allow to be written to the agent log.
            When this rate limit is exceeded, new log records are ignored.  When log records can be accepted again,
            an additional line is written to the log to record how many records were ignored.  This variable is
            essentially the fill rate used by the "leaky-bucket" algorithm used to rate limit the log write rate.
        max_write_burst:  The short term maximum burst write rate allowed to be written to the log.
            This is essentially the maximum bucket size used by the "leaky-bucket" algorithm used to rate
            limit the log write rate.
    """
    if use_stdout and file_path is not None:
        raise Exception('You cannot specify both stdout and file_path')

    root_logger = logging.getLogger()

    global __agent_log_handler__
    # Close the old handler if there is one.
    if __agent_log_handler__ is not None:
        root_logger.removeHandler(__agent_log_handler__)
        __agent_log_handler__.close()

    if use_stdout:
        __agent_log_handler__ = logging.StreamHandler()
    elif file_path is not None:
        __agent_log_handler__ = logging.handlers.RotatingFileHandler(file_path, maxBytes=max_bytes,
                                                                     backupCount=backup_count)
    if __agent_log_handler__ is not None:
        __agent_log_handler__.addFilter(AgentLogFilter())
        formatter = AgentLogFormatter()
        __agent_log_handler__.addFilter(RateLimiterLogFilter(formatter, max_write_burst=max_write_burst,
                                                             log_write_rate=log_write_rate))
        __agent_log_handler__.setFormatter(formatter)
        root_logger.addHandler(__agent_log_handler__)

__metric_logs_use_stdout__ = False

def set_metric_logs_destination(use_stdout):
    global __metric_logs_use_stdout__
    __metric_logs_use_stdout__ = use_stdout

#
# _srcfile is used when walking the stack to check when we've got the first
# caller stack frame.  This is copied from the logging/__init__.py
#
if hasattr(sys, 'frozen'): #support for py2exe
    _srcfile = "scalyr_agent%sscaly_logging%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)


# next bit filched from 1.5.2's inspect.py
def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back

def alternateCurrentFrame():
    return sys._getframe(3)

if hasattr(sys, '_getframe'):
    currentframe = alternateCurrentFrame
# done filching


class AgentLogger(logging.Logger):
    """Custom logger to use for logging information, errors, and metrics from the Scalyr agent.

    The main additions are:
        metrics:  Using the 'emit_value' method, metric values may be emitted to the appropriate log file using
            a standard format that can be easily parsed by the Scalyr servers.  Note,
            not all Logger instances are allowed to invoke 'emit_value'.  Only ones whose 'openMetricFileForMonitor'
            method has been invoked.  This is typically done for all Logger instances passed to Scalyr monitor modules.
        component:  We define our own concept of component which is suppose to record the general subsystem
            that generated the log record.  The components could be 'core' or one of the metric monitors.
        error_code:  All log methods (such as log, warn, error) can take in a keyword-value argument with
            key 'error_code' which will record the error code (a str) for the log record.  This error code will
            be included in the emitted output, formatted in a consistent way.
        custom format:  Our own custom format is automatically added to all outputted lines.
    """
    def __init__(self, name):
        """Initializes the logger instance with the specified name.

        The logger will base the component and the monitor id on the name.  If the name ends in "[.*]" then
        the monitor id will be set to whatever is inside the brackets.  If the name refers to module in the Scalyr
        Agent package, then component will be set to core, otherwise it will be set to 'monitor:XXX' where XXX is
        the last component of the name split by periods (and excluding the monitor id).

        Arguments:
            name:  The name, typically the module name with the possible addition of the monitor id sourrouned by
                brackets.
        """
        self.__logger_name = name

        # Look for the monitor id, which is at the end surrounded by brackets.
        m = re.match('([^\[]*)(\(.*\))', name)
        if m:
            module_path = m.group(1)
            self.__monitor_id = m.group(2)[1:-1]
        else:
            module_path = name
            self.__monitor_id = None

        # If it is from the scaly_agent module, then it is 'core' unless it is one of the monitors.
        if module_path.find('scalyr_agent') == 0 and not module_path.find('scalyr_agent.builtin_monitors.') == 0:
            self.component = 'core'
            self.monitor_name = None
        else:
            # Note, we only use the last part of the module name for the name we use in the logs.  We rely on the
            # monitor_id to make it unique.  This is calculated in configuration.py.  We need to make sure this
            # code is in sync with that file.
            if self.__monitor_id is not None:
                self.monitor_name = '%s(%s)' % (module_path.split('.')[-1], self.__monitor_id)
            else:
                self.monitor_name = module_path.split('.')[-1]

            self.component = 'monitor:%s' % self.monitor_name


        # If this logger is for a particular monitor instance, then we will eventually call openMetricLoggerForMonitor
        # on it to set which output file its metrics should be reported.  When that happens, these will be set to
        # which monitor it is reporting for and the associated log handler.
        self.__monitor = None
        self.__metric_handler = None

        # The regular expression that must match for metric and field names.  Esentially, it has to begin with
        # a letter, and only contain letters, digits, periods, and underscores.
        self.__metric_or_field_name_rule = re.compile('[a-zA-Z][\w\.]*$')
        logging.Logger.__init__(self, name)

    def emit_value(self, metric_name, metric_value, extra_fields=None, monitor=None):
        """Emits a metric and its value to the underlying log to be transmitted to Scalyr.

        Adds a new line to the metric log recording the specified value for the metric.  Additional fields
        may be added to this line using extra_fields, which can then be used in Scalyr searches to further limit
        the metric values being aggregated together.  For example, you may wish to report a free memory metric,
        but have an additional field of 'type=buffer' so that you can easily graph all free memory as well as
        free memory just from buffers.

        Note, this method may only be called after the metric file for the monitor has been opened.  This is always
        done before the monitor's "run" method is invoked.

        Arguments:
            metric_name:  The string containing the name for the metric.
            metric_value:  The value for the metric.  The only allowed types are int, long, float, str, bool and unicde.
            extra_fields:  An optional dict that if specified, will be included as extra fields on the log line.
                These fields can be used in future searches/graphs expressions to restrict which specific instances
                of the metric are matched/aggregated together.  The keys for the dict must be str and the only
                allowed value types are int, long, float, str, bool, and unicode.
            monitor:  The ScalyrMonitor instance that is reporting the metric.  Typically, this does not need to
                be supplied because it defaults to whatever monitor for each the logger was created.

        Raises:
            UnsupportedValueType if the value type is not one of the supported types.
        """
        if monitor is None:
            monitor = self.__monitor

        if monitor is None or monitor not in AgentLogger.__opened_monitors__:
            raise Exception('Cannot report metric values until metric log file is opened.')

        string_buffer = StringIO()
        if not type(metric_name) in (str, unicode):
            raise UnsupportedValueType(metric_name=metric_name)
        if not self.__is_valid_metric_or_field_name(metric_name):
            raise BadMetricOrFieldName(metric_name)

        if not type(metric_value) in (str, unicode, bool, int, long, float):
            raise UnsupportedValueType(metric_name=metric_name, metric_value=metric_value)

        string_buffer.write("%s %s" % (metric_name, json_lib.serialize(metric_value)))

        if extra_fields is not None:
            for field_name in extra_fields:
                if not type(field_name) in (str, unicode):
                    raise UnsupportedValueType(field_name=field_name)
                if not self.__is_valid_metric_or_field_name(field_name):
                    raise BadMetricOrFieldName(field_name)

                field_value = extra_fields[field_name]
                if not type(field_value) in (str, unicode, bool, int, long, float):
                    raise UnsupportedValueType(field_name=field_name, field_value=field_value)

                string_buffer.write(' %s=%s' % (field_name, json_lib.serialize(field_value)))

        self.info(string_buffer.getvalue(), metric_log_for_monitor=monitor)
        string_buffer.close()

    def _log(self, level, msg, args, exc_info=None, extra=None, error_code=None, metric_log_for_monitor=None,
             error_for_monitor=None):
        """The central log method.  All 'info', 'warn', etc methods funnel into this method.

        New arguments (beyond inherited arguments):
            error_code:  The Scalyr agent error code for this record, if any.
            metric_log_for_monitor:  If not None, indicates the record is for a metric and the value of this
                argument is the ScalyrMonitor instance that generated it.  This is used to make sure the
                metric is recorded to the correct log.
            error_for_monitor:  If this is an error, then associate it with the specified monitor.  If this is
                none but this is a logger specific for a monitor instance, then that monitor's error count will
                be incremented.
        """
        # We override the _log method so that we can accept the error_code argument.  Normally, we could
        # use extra to pass the value through to makeRecord, however, that is not available in 2.4, so we have
        # to do our own hack.  We just stick it in a thread local variable and read it out in makeRecord.
        thread_local.last_error_code_seen = error_code
        thread_local.last_metric_log_for_monitor = metric_log_for_monitor

        # Only associate an monitor with the error if it is in fact an error.
        if level >= logging.ERROR:
            if metric_log_for_monitor is not None:
                thread_local.last_error_for_monitor = error_for_monitor
            else:
                thread_local.last_error_for_monitor = self.__monitor
        else:
            thread_local.last_error_for_monitor = None

        if extra is not None:
            result = logging.Logger._log(self, level, msg, args, exc_info, extra)
        elif exc_info is not None:
            result = logging.Logger._log(self, level, msg, args, exc_info)
        else:
            result = logging.Logger._log(self, level, msg, args)
        thread_local.last_error_code_seen = None
        thread_local.last_metric_log_for_monitor = None
        thread_local.last_error_for_monitor = None
        return result

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        # Invoke the super class's method to make the base record.
        if extra is not None:
            result = logging.Logger.makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra)
        elif func is not None:
            result = logging.Logger.makeRecord(self, name, level, fn, lno, msg, args, exc_info, func)
        else:
            result = logging.Logger.makeRecord(self, name, level, fn, lno, msg, args, exc_info)

        # Attach the special fields for the scalyr agent logging code.  These are passed from _log through a thread
        # local variable.
        result.error_code = thread_local.last_error_code_seen
        result.metric_log_for_monitor = thread_local.last_metric_log_for_monitor
        result.error_for_monitor = thread_local.last_error_for_monitor

        result.component = self.component
        result.monitor_name = self.monitor_name

        # We also mark this record as being generated by a AgentLogger.  We use this in the root logger to
        # decide if it should be included in the agent.log output.
        result.agent_logger = True

        # If this was a metric for a particular monitor, update its records.
        if result.metric_log_for_monitor is not None:
            result.metric_log_for_monitor.increment_counter(reported_lines=1)
        if result.error_for_monitor is not None:
            result.error_for_monitor.increment_counter(errors=1)
        return result

    def exception(self, msg, *args, **kwargs):
        kwargs['exc_info'] = 1
        self.error(msg, *args, **kwargs)

    # The set of ScalyrMonitor instances that current have only metric logs associated with them.  This is used
    # for error checking.
    __opened_monitors__ = {}

    def openMetricLogForMonitor(self, path, monitor, max_bytes=20*1024*1024, backup_count=5):
        """Open the metric log for this logger instance for the specified monitor.

        This must be called before any metrics are reported using the 'emit_value' method.  This opens the
        correct log file and prepares it to have metrics emitted to it.  Only one metric log file can be opened at
        any time per Logger instance, so any previous one is automatically closed.

        Warning, this method accesses global variables that are not thread-safe.  All calls to any logger's
        'openMetricLogForMonitor' must occur on the same thread for correctness.

        Warning, you must invoke 'closeMetricLog' to close the log file.

        Arguments:
            path:  The file path for the metric log file.  A rotating log file will be created at this path.
            monitor:  The ScalyrMonitor instance that will emit metrics to the log.
            max_bytes:  The maximum number of bytes to write to the log file before it is rotated.
            backup_count:  The number of old log files to keep around.
        """
        if self.__metric_handler is not None:
            self.closeMetricLog()

        global __metric_logs_use_stdout__

        if not __metric_logs_use_stdout__:
            self.__metric_handler = MetricLogHandler.getHandlerForPath(path, max_bytes=max_bytes,
                                                                       backup_count=backup_count)
        else:
            self.__metric_handler = MetricLogHandlerStdout.getHandlerForPath(path)

        self.__metric_handler.openForMonitor(monitor)
        # TODO:  The below line may be a bug.
        # self.addHandler(self.__metric_handler)
        self.__monitor = monitor
        AgentLogger.__opened_monitors__[monitor] = True

    def closeMetricLog(self):
        """Closes the metric log file assicated with this logger."""
        if self.__metric_handler is not None:
            self.__metric_handler.closeForMonitor(self.__monitor)
            self.__metric_handler = None
            del AgentLogger.__opened_monitors__[self.__monitor]
            self.__monitor = None

    def __is_valid_metric_or_field_name(self, name):
        """Returns true if name is a valid metric or field name"""
        return self.__metric_or_field_name_rule.match(name) is not None

    def report_values(self, values, monitor=None):
        """Records the specified values (a dict) to the underlying log.

        NOTE:  This is being deprecated in favor of emit_value.

        This may only be called after the metric file for the monitor has been opened.

        Arguments:
            values:  A dict containing a mapping from metric name to its value.  The only allowed value types
                are: int, long, float, str, bool, and unicode.
            monitor:  The ScalyrMonitor instance that created the values.  This does not have to be passed in
                if the monitor instance specific logger is used.  It defaults to that monitor.  However,
                if the logger is the general one for the module, then a monitor instance is required.

        Raises:
            UnsupportedValueType if the value type is not one of the supported types.
        """
        self.emit_values(values, monitor=monitor)

    def emit_values(self, values, monitor=None):
        """Records the specified values (a dict) to the underlying log.

        NOTE:  This is being deprecated in favor of emit_value.

        This may only be called after the metric file for the monitor has been opened.

        Arguments:
            values:  A dict containing a mapping from metric name to its value.  The only allowed value types
                are: int, long, float, str, bool, and unicode.
            monitor:  The ScalyrMonitor instance that created the values.  This does not have to be passed in
                if the monitor instance specific logger is used.  It defaults to that monitor.  However,
                if the logger is the general one for the module, then a monitor instance is required.

        Raises:
            UnsupportedValueType if the value type is not one of the supported types.
        """
        if monitor is None:
            monitor = self.__monitor

        if monitor is None or monitor not in AgentLogger.__opened_monitors__:
            raise Exception('Cannot report metric values until metric log file is opened.')

        string_entries = []
        for key in values:
            value = values[key]
            value_type = type(value)
            if value_type is int or value_type is long or value_type is float:
                string_entries.append("%s=%s" % (key, str(value)))
            elif value_type is bool:
                value_str = 'true'
                if not value:
                    value_str = 'false'
                string_entries.append("%s=%s" % (key, value_str))
            elif value_type is str or value_type is unicode:
                string_entries.append("%s=%s" % (key, str(value).replace('"', '\\"')))
            else:
                raise UnsupportedValueType(key, value)
        self.info(" ".join(string_entries), metric_log_for_monitor=monitor)

    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normpath(os.path.normcase(co.co_filename))
            if filename == _srcfile or filename == logging._srcfile:
                f = f.f_back
                continue
            rv = (filename, f.f_lineno, co.co_name)
            break
        return rv


# The handler currently on the root logger that was inserted by the agent code, if any.
__agent_log_handler__ = None

# To help with a hack of extending the Logger class, we need a thread local storage
# to store the last error status code and metric information seen by this thread.
thread_local = threading.local()


class BaseFormatter(logging.Formatter):
    """Commom formatter base class used by the Scalyr log formatters.

    This base class provides some common functionality to be used in conjunction with the RateLimiterFilter.
    Specifically, it caches the result of the format operation so that multiple calls do not result in reformatting.
    Also, it appends a warning message when records were dropped due to rate limiting.
    """
    def __init__(self, fmt, format_name):
        """Creates an instance of the formatter.

        Params:
            fmt:  The format string to use for the format.
            format_name: A name that is unique to the derived format class.  This is used to
                make sure different format results are cached under different keys.
        """
        self.__cache_key = 'cached_format_%s' % format_name
        logging.Formatter.__init__(self, fmt=fmt)

    def format(self, record):
        # Check to see if there is a cached result already for this format.
        if hasattr(record, self.__cache_key):
            return getattr(record, self.__cache_key)

        # Otherwise, build the format.  Prepend a warning if we had to skip lines.
        if hasattr(record, 'rate_limited_dropped_records') and record.rate_limited_dropped_records > 0:
            result = '.... Warning, skipped writing %ld log lines due to log rate limit ...\n%s' % (
                record.rate_limited_dropped_records, logging.Formatter.format(self, record))
        else:
            result = logging.Formatter.format(self, record)

        setattr(record, self.__cache_key, result)
        return result


class AgentLogFormatter(BaseFormatter):
    """Formatter used for the logs produced by the agent both for diagnostic information.

    In general, it formats each line as:
        time (with milliseconds)
        levelname (DEBUG, INFO, etc)
        component (which component of the agent produced the problem such as 'core' or a monitor.)
        line (file name and line number that produced the log message)
        error (the error code)
        message (the logged message)
    """
    def __init__(self):
        # TODO: It seems on Python 2.4 the filename and line number do not work correctly.  I think we need to
        # define a custom findCaller method to actually fix the problem.
        BaseFormatter.__init__(self, '%(asctime)s %(levelname)s [%(component)s] [%(filename)s:%(lineno)d] '
                                     '%(error_message)s%(message)s%(stack_token)s', 'agent_formatter')

    def format(self, record):
        # Optionally add in the error code if there is one present.
        if record.error_code is not None:
            record.error_message = '[error="%s"] ' % record.error_code
        else:
            record.error_message = ''

        if record.exc_info:
            record.stack_token = ' :stack_trace:'
        else:
            record.stack_token = ''
        return BaseFormatter.format(self, record)

    def formatTime(self, record, datefmt=None):
        # We define our own custom time format in order to use a period for separate seconds from milliseconds.
        # Yes, the comma annoys us -- most other Scalyr logs used a period.
        ct = time.gmtime(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
            s = "%s.%03dZ" % (t, record.msecs)
        return s

    def formatException(self, ei):
        # We just want to indent the stack trace to make it easier to write a parsing rule to detect it.
        output = StringIO()
        try:
            for line in logging.Formatter.formatException(self, ei).splitlines(True):
                output.write('  ')
                output.write(line)
            return output.getvalue()
        finally:
            output.close()


class MetricLogFormatter(BaseFormatter):
    """Formatter used for the logs produced by the agent both for metric reporting.

    In general, it formats each line as:
        time (with milliseconds)
        component (which component of the agent produced the problem such as 'core' or a monitor.)
        message (the logged message)
    """
    def __init__(self):
        # TODO: It seems on Python 2.4 the filename and line number do not work correctly.  I think we need to
        # define a custom findCaller method to actually fix the problem.
        BaseFormatter.__init__(self, '%(asctime)s [%(monitor_name)s] %(message)s', 'metric-formatter')

    def formatTime(self, record, datefmt=None):
        # We define our own custom time format in order to use a period for separate seconds from milliseconds.
        # Yes, the comma annoys us -- most other Scalyr logs used a period.
        ct = time.gmtime(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
            s = "%s.%03dZ" % (t, record.msecs)
        return s


class AgentLogFilter(object):
    """A filter that includes any record emitted by an AgentLogger instance unless it was a metric record.
    """
    def filter(self, record):
        return hasattr(record, 'agent_logger') and record.agent_logger and record.metric_log_for_monitor is None


class RateLimiterLogFilter(object):
    """A filter that rejects records when a maximum write rate has been exceeded, as calculated by
    a leaky bucket algorithm."""
    def __init__(self, formatter, max_write_burst=100000, log_write_rate=2000):
        """Creates an instance.

        Params:
            formatter:  The formatter instance used by the Logger to generate the string used to represent
                a particular record.  This is used to determine how many bytes the record will consume.  This should
                be derived from BaseFormatter since it has some features to make sure we do not serialize the
                record twice.
            max_write_burst:  The maximum burst of bytes to allow to be written into the log.  This is the
                bucket size in the "leaky bucket" algorithm.
            log_write_rate:   The average number of bytes per second to allow to be written to the log.  This is
                the bucket fill rate in the "leaky bucket" algorithm.

        Returns:  A new instance.
        """
        self.__rate_limiter = RateLimiter(bucket_size=max_write_burst, bucket_fill_rate=log_write_rate)
        self.__dropped_records = 0
        self.__formatter = formatter

    def filter(self, record):
        if hasattr(record, 'rate_limited_set'):
            return record.rate_limited_result
        record.rate_limited_set = True
        # Note, it is important we set rate_limited_droppped_records before we invoke the formatter since the
        # formatting is dependent on that value and our formatters cache the result.
        record.rate_limited_dropped_records = self.__dropped_records
        record_str = self.__formatter.format(record)
        record.rate_limited_result = self.__rate_limiter.charge_if_available(len(record_str))

        if record.rate_limited_result:
            self.__dropped_records = 0
            return True
        else:
            self.__dropped_records += 1
            return False


class MetricLogHandler(logging.handlers.RotatingFileHandler):
    """The LogHandler to use for recording metric values emitted by Scalyr agent monitors.  Uses a rotating log file.

    The handler has several features such as a way to guarantee there is only one handler instance for each metric
    log file being used, tracking the Scalyr monitor instances associated with it, etc.
    """
    def __init__(self, file_path, max_bytes, backup_count):
        """Creates the handler instance.  This should not be used directly.  Use MetricLogHandler.getHandlerForPath
        instead.
        """
        logging.handlers.RotatingFileHandler.__init__(self, file_path, maxBytes=max_bytes, backupCount=backup_count)
        # The monitor instances that should emit their metrics to this log file.
        self.__monitors = {}
        # True if this handler has been added to the root logger.  To allow for multiple different modules and
        # Scalyr monitors to emit to the same metric file, we do not place this handler in each of the loggers for
        # those modules, but instead put one instance on the root logger and just filter it to emit only those metrics
        # for the monitors in self.__monitors.
        self.__added_to_root = False
        self.__file_path = file_path

        class Filter(object):
            """The filter used by the MetricLogHandler that only returns true if the record is for a metric for one of
            the monitors associated with the metric log file.
            """
            def __init__(self, allowed_monitors):
                self.__monitors = allowed_monitors

            def filter(self, record):
                return hasattr(record, 'metric_log_for_monitor') and record.metric_log_for_monitor in self.__monitors

        # Add the filter and our formatter to this handler.
        self.addFilter(Filter(self.__monitors))
        formatter = MetricLogFormatter()
        self.addFilter(RateLimiterLogFilter(formatter))
        self.setFormatter(formatter)

    __metric_log_handlers__ = {}

    @staticmethod
    def getHandlerForPath(file_path, max_bytes=20*1024*1024, backup_count=5):
        """Returns the MetricLogHandler to use for the specified file path.  This must be used to get
        MetricLogHandler instances.

        This method is not thread-safe so all calls to getHandlerPath must be issued from the same thread.

        Note, openForMonitor must be invoked in order to allow a particular monitor to emit metric values to this
        log.

        Arguments:
            file_path:  The file path for the metric log file.
            max_bytes:  The maximum number of bytes to write to the log file before it is rotated.
            backup_count:  The number of previous log files to keep.

        Returns:
            The handler instance to use.
        """
        if not file_path in MetricLogHandler.__metric_log_handlers__:
            MetricLogHandler.__metric_log_handlers__[file_path] = MetricLogHandler(file_path, max_bytes=max_bytes,
                                                                                   backup_count=backup_count)
        return MetricLogHandler.__metric_log_handlers__[file_path]

    def openForMonitor(self, monitor):
        """Configures this instance to allow the specified monitor to emit its metrics to it.

        This method is not thread-safe.

        Arguments:
            monitor:  The monitor instance that should emit its values to the log file handled by this instance.
        """
        # In order to support multiple modules using the same log file to record their metrics, we add this
        # handler to the root logger and then just use a filter to decide which metrics to emit once they propogate
        # up to the root.
        if not self.__added_to_root:
            logging.getLogger().addHandler(self)

        self.__monitors[monitor] = True

    def closeForMonitor(self, monitor):
        """Configures this instance to no longer log metrics for the specified monitor instance.

        If this is the last monitor that was being handled by this instance, then the underlying log file will
        be closed.

        This method is not thread safe.

        Arguments:
            monitor:  The monitor instance.
        """
        if monitor in self.__monitors:
            del self.__monitors[monitor]

        # If this handler no longer has any monitors, then it is no longer needed and we should close/remove it.
        if len(self.__monitors) == 0:
            if self.__added_to_root:
                logging.getLogger().removeHandler(self)

            self.close()

            del MetricLogHandler.__metric_log_handlers__[self.__file_path]


# TODO:  This is an expedient copy and paste of code to get the metric logs able to emit to stdout out
# for the purpose of running the monitors in standalone mode.  We need to combine this with the above class
# somehow.
class MetricLogHandlerStdout(logging.StreamHandler):
    """The LogHandler to use for recording metric values emitted by Scalyr agent monitors.  Uses a rotating log file.

    The handler has several features such as a way to guarantee there is only one handler instance for each metric
    log file being used, tracking the Scalyr monitor instances associated with it, etc.
    """
    def __init__(self, file_path):
        """Creates the handler instance.  This should not be used directly.  Use MetricLogHandler.getHandlerForPath
        instead.
        """
        logging.StreamHandler.__init__(self, sys.stdout)
        self.propagate = False
        # The monitor instances that should emit their metrics to this log file.
        self.__monitors = {}
        # True if this handler has been added to the root logger.  To allow for multiple different modules and
        # Scalyr monitors to emit to the same metric file, we do not place this handler in each of the loggers for
        # those modules, but instead put one instance on the root logger and just filter it to emit only those metrics
        # for the monitors in self.__monitors.
        self.__added_to_root = False
        self.__file_path = file_path

        class Filter(object):
            """The filter used by the MetricLogHandler that only returns true if the record is for a metric for one of
            the monitors associated with the metric log file.
            """
            def __init__(self, allowed_monitors):
                self.__monitors = allowed_monitors

            def filter(self, record):
                return hasattr(record, 'metric_log_for_monitor') and record.metric_log_for_monitor in self.__monitors

        # Add the filter and our formatter to this handler.
        self.addFilter(Filter(self.__monitors))
        formatter = MetricLogFormatter()
        self.addFilter(RateLimiterLogFilter(formatter))
        self.setFormatter(formatter)

    __metric_log_handlers__ = {}

    @staticmethod
    def getHandlerForPath(file_path):
        """Returns the MetricLogHandler to use for the specified file path.  This must be used to get
        MetricLogHandler instances.

        This method is not thread-safe so all calls to getHandlerPath must be issued from the same thread.

        Note, openForMonitor must be invoked in order to allow a particular monitor to emit metric values to this
        log.

        Arguments:
            file_path:  The file path for the metric log file.
            max_bytes:  The maximum number of bytes to write to the log file before it is rotated.
            backup_count:  The number of previous log files to keep.

        Returns:
            The handler instance to use.
        """
        if not file_path in MetricLogHandlerStdout.__metric_log_handlers__:
            MetricLogHandlerStdout.__metric_log_handlers__[file_path] = MetricLogHandlerStdout(file_path)
        return MetricLogHandlerStdout.__metric_log_handlers__[file_path]

    def openForMonitor(self, monitor):
        """Configures this instance to allow the specified monitor to emit its metrics to it.

        This method is not thread-safe.

        Arguments:
            monitor:  The monitor instance that should emit its values to the log file handled by this instance.
        """
        # In order to support multiple modules using the same log file to record their metrics, we add this
        # handler to the root logger and then just use a filter to decide which metrics to emit once they propogate
        # up to the root.
        if not self.__added_to_root:
            logging.getLogger().addHandler(self)

        self.__monitors[monitor] = True

    def emit(self, record):
        logging.StreamHandler.emit(self, record)

    def closeForMonitor(self, monitor):
        """Configures this instance to no longer log metrics for the specified monitor instance.

        If this is the last monitor that was being handled by this instance, then the underlying log file will
        be closed.

        This method is not thread safe.

        Arguments:
            monitor:  The monitor instance.
        """
        if monitor in self.__monitors:
            del self.__monitors[monitor]

        # If this handler no longer has any monitors, then it is no longer needed and we should close/remove it.
        if len(self.__monitors) == 0:
            if self.__added_to_root:
                logging.getLogger().removeHandler(self)

            self.close()

            del MetricLogHandlerStdout.__metric_log_handlers__[self.__file_path]

class BadMetricOrFieldName(Exception):
    """Exception raised when a metric or field name used to report a metric value is invalid."""
    def __init__(self, metric_or_field_name):
        Exception.__init__(self, 'A bad metric or field name of "%s" was seen when reporting metrics.  '
                           'It must begin with a letter and only contain alphanumeric characters as well as periods'
                           'and underscores.' % metric_or_field_name)


class UnsupportedValueType(Exception):
    """Exception raised when an MetricValueLogger is asked to emit a metric with an unsupported type."""
    def __init__(self, metric_name=None, metric_value=None, field_name=None, field_value=None):
        """Constructs an exception.

        There are several different modes of operation for this exception.  If only metric_name or field_name
        are given, then the error message will indicate the name is bad because it is not str or unicode.
        If a metric_name and metric_value are given, then the value is assumed to be a bad type and an
        appropriate error message is generated.  Same with field_name and field_value.
        """
        self.metric_name = metric_name
        self.metric_value = metric_value
        self.field_name = field_name
        self.field_value = field_value

        if metric_name is not None and metric_value is None:
            message = ('An unsupported type for a metric name was given.  It must be either str or unicode, but was'
                       '"%s".  This was for metric "%s"' % (str(type(metric_name)), str(metric_name)))
        elif field_name is not None and field_value is None:
            message = ('An unsupported type for a field name was given.  It must be either str or unicode, but was'
                       '"%s".  This was for field "%s"' % (str(type(field_name)), str(field_name)))
        elif metric_name is not None and metric_value is not None:
            message = ('Unsupported metric value type of "%s" with value "%s" for metric="%s".'
                       'Only int, long, float, and str are supported.' % (str(type(metric_value)), str(metric_value),
                                                                          metric_name))
        elif field_name is not None and field_value is not None:
            message = ('Unsupported field value type of "%s" with value "%s" for field="%s".'
                       'Only int, long, float, and str are supported.' % (str(type(field_value)), str(field_value),
                                                                          field_name))
        else:
            raise Exception('Bad combination of fields given for UnsupportedValueType: "%s" "%s" "%s" "%s"' %
                            (str(metric_name), str(metric_value), str(field_name), str(field_value)))
        Exception.__init__(self, message)
