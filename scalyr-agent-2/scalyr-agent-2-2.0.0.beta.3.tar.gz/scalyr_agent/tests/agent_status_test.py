# Copyright 2014, Scalyr, Inc.


import unittest

from scalyr_agent.agent_status import OverallStats


class TestOverallStats(unittest.TestCase):

    def test_read_file_as_json(self):
        a = OverallStats()
        b = OverallStats()

        a.total_bytes_copied = 1
        a.total_bytes_skipped = 2
        a.total_bytes_subsampled = 3
        a.total_bytes_failed = 4
        a.total_redactions = 5
        a.total_copy_requests_errors = 6
        a.total_monitor_reported_lines = 7
        a.total_monitor_errors = 8

        b.total_bytes_copied = 9
        b.total_bytes_skipped = 10
        b.total_bytes_subsampled = 11
        b.total_bytes_failed = 12
        b.total_redactions = 13
        b.total_copy_requests_errors = 14
        b.total_monitor_reported_lines = 15
        b.total_monitor_errors = 16

        c = a + b

        self.assertEquals(c.total_bytes_copied, 10)
        self.assertEquals(c.total_bytes_skipped, 12)
        self.assertEquals(c.total_bytes_subsampled, 14)
        self.assertEquals(c.total_bytes_failed, 16)
        self.assertEquals(c.total_redactions, 18)
        self.assertEquals(c.total_copy_requests_errors, 20)
        self.assertEquals(c.total_monitor_reported_lines, 22)
        self.assertEquals(c.total_monitor_errors, 24)