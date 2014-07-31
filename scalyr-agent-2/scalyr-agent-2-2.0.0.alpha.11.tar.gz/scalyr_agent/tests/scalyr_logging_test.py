# Copyright 2014, Scalyr, Inc.

import re
import tempfile
import unittest

import scalyr_agent.scalyr_logging as scalyr_logging


class ScalyrLoggingTest(unittest.TestCase):
    def setUp(self):
        self.__log_path = tempfile.mktemp('.log')
        scalyr_logging.set_agent_log_destination(file_path=self.__log_path)
        self.__logger = scalyr_logging.getLogger('scalyr_agent.agent_main')

    def test_output_to_file(self):
        self.__logger.info('Hello world')
        self.assertTrue(self.__log_contains('Hello world'))

    def test_component_name(self):
        self.assertEquals(self.__logger.component, 'core')
        self.assertEquals(scalyr_logging.getLogger('scalyr_agent').component, 'core')
        self.assertEquals(scalyr_logging.getLogger('scalyr_agent.foo').component, 'core')
        self.assertEquals(scalyr_logging.getLogger('scalyr_agent.foo.bar').component, 'core')
        self.assertEquals(scalyr_logging.getLogger('scalyr_agent.builtin_monitors.foo').component, 'monitor:foo')
        self.assertEquals(scalyr_logging.getLogger('scalyr_agent.builtin_monitors.foo(ok)').component,
                          'monitor:foo(ok)')

    def test_formatter(self):
        # The format should be something like:
        # 2014-05-11 16:55:06.236 INFO [core] [scalyr_logging_test.py:28] Test line 5
        self.__logger.info('Test line %d', 5)
        self.assertTrue(self.__log_contains('\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}.\\d{3}Z INFO \[core\] '
                                            '\[.*\.py:\d+\] Test line 5'))

    def test_error_code(self):
        self.__logger.warn('Bad result', error_code='statusCode')
        self.assertTrue(self.__log_contains('\[error="statusCode"\] Bad result'))

    def test_child_modules(self):
        child = scalyr_logging.getLogger('scalyr_agent.foo.bar')
        child.info('Child statement')
        self.assertTrue(self.__log_contains('Child statement'))

    def test_sibling_modules(self):
        child = scalyr_logging.getLogger('external_package.my_monitor')
        child.info('Sibling statement')
        self.assertTrue(self.__log_contains('Sibling statement'))

    def test_metric_logging(self):
        monitor_instance = ScalyrLoggingTest.FakeMonitor('testing')
        metric_file_path = tempfile.mktemp('.log')

        monitor_logger = scalyr_logging.getLogger('scalyr_agent.builtin_monitors.foo(1)')
        monitor_logger.openMetricLogForMonitor(metric_file_path, monitor_instance)
        monitor_logger.emit_value('test_name', 5, {'foo': 5})

        self.assertEquals(monitor_instance.reported_lines, 1)

        # The value should only appear in the metric log file and not the main one.
        self.assertTrue(self.__log_contains('test_name 5', file_path=metric_file_path))
        self.assertTrue(self.__log_contains('foo=5', file_path=metric_file_path))
        self.assertFalse(self.__log_contains('foo=5'))

        monitor_logger.closeMetricLog()

    def test_metric_logging_with_bad_name(self):
        monitor_instance = ScalyrLoggingTest.FakeMonitor('testing')
        metric_file_path = tempfile.mktemp('.log')

        monitor_logger = scalyr_logging.getLogger('scalyr_agent.builtin_monitors.foo(1)')
        monitor_logger.openMetricLogForMonitor(metric_file_path, monitor_instance)

        self.assertRaises(scalyr_logging.BadMetricOrFieldName, monitor_logger.emit_value, '1name', 5)
        self.assertRaises(scalyr_logging.BadMetricOrFieldName, monitor_logger.emit_value, 'name-hi', 5)
        self.assertRaises(scalyr_logging.BadMetricOrFieldName, monitor_logger.emit_value, 'name', 5, {'hi-': 6})

        monitor_logger.closeMetricLog()

    def test_errors_for_monitor(self):
        monitor_instance = ScalyrLoggingTest.FakeMonitor('testing')
        metric_file_path = tempfile.mktemp('.log')

        monitor_logger = scalyr_logging.getLogger('scalyr_agent.builtin_monitors.foo(1)')
        monitor_logger.openMetricLogForMonitor(metric_file_path, monitor_instance)
        monitor_logger.error('Foo')

        self.assertEquals(monitor_instance.errors, 1)

        monitor_logger.closeMetricLog()

    def test_module_with_different_metric_logs(self):
        monitor_one = ScalyrLoggingTest.FakeMonitor('testing one')
        monitor_two = ScalyrLoggingTest.FakeMonitor('testing two')

        metric_file_one = tempfile.mktemp('.log')
        metric_file_two = tempfile.mktemp('.log')

        logger_one = scalyr_logging.getLogger('scalyr_agent.builtin_monitors.foo(1)')
        logger_two = scalyr_logging.getLogger('scalyr_agent.builtin_monitors.foo(2)')

        logger_one.openMetricLogForMonitor(metric_file_one, monitor_one)
        logger_two.openMetricLogForMonitor(metric_file_two, monitor_two)

        logger_one.report_values({'foo': 5})
        logger_two.report_values({'bar': 4})

        # The value should only appear in the metric log file and not the main one.
        self.assertTrue(self.__log_contains('foo=5', file_path=metric_file_one))
        self.assertTrue(self.__log_contains('bar=4', file_path=metric_file_two))

        self.assertFalse(self.__log_contains('foo=5', file_path=metric_file_two))
        self.assertFalse(self.__log_contains('bar=4', file_path=metric_file_one))

        self.assertFalse(self.__log_contains('foo=5'))
        self.assertFalse(self.__log_contains('bar=4'))

        logger_one.closeMetricLog()
        logger_two.closeMetricLog()

    def test_pass_in_module_with_metric(self):
        monitor_instance = ScalyrLoggingTest.FakeMonitor('testing')
        metric_file_path = tempfile.mktemp('.log')

        monitor_logger = scalyr_logging.getLogger('scalyr_agent.builtin_monitors.foo(1)')
        monitor_logger.openMetricLogForMonitor(metric_file_path, monitor_instance)
        scalyr_logging.getLogger('scalyr_agent.builtin_monitors.foo').report_values({'foo': 5},
                                                                                    monitor=monitor_instance)

        # The value should only appear in the metric log file and not the main one.
        self.assertTrue(self.__log_contains('foo=5', file_path=metric_file_path))
        self.assertFalse(self.__log_contains('foo=5'))

        monitor_logger.closeMetricLog()

    def test_rate_limit(self):
        self.__log_path = tempfile.mktemp('.log')
        scalyr_logging.set_agent_log_destination(file_path=self.__log_path, max_write_burst=250, log_write_rate=0)
        self.__logger = scalyr_logging.getLogger('scalyr_agent.agent_main')

        string_300 = ''

        for i in range(300):
            string_300 = '%sa' % string_300

        self.__logger.info('First message')
        self.assertTrue(self.__log_contains('First message'))

        self.__logger.info('Dropped message %s', string_300)
        self.assertFalse(self.__log_contains('Dropped message'))

        self.__logger.info('Second message')
        self.assertTrue(self.__log_contains('Second message'))
        self.assertTrue(self.__log_contains('Warning, skipped writing 1 log lines'))


    class FakeMonitor(object):
        """Just a simple class that we use in place of actual Monitor objects when reporting metrics."""
        def __init__(self, name):
            self.__name = name
            self.reported_lines = 0
            self.errors = 0

        def increment_counter(self, reported_lines=0, errors=0):
            """Increment some of the counters pertaining to the performance of this monitor.
            """
            self.reported_lines += reported_lines
            self.errors += errors

    def __log_contains(self, expression, file_path=None):
        if file_path is None:
            file_path = self.__log_path
        file = None
        try:
            matcher = re.compile(expression)
            file = open(file_path)
            for line in file:
                if matcher.search(line):
                    return True
            return False
        finally:
            if file is not None:
                file.close()


