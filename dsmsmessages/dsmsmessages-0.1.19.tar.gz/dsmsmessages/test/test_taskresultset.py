# -*- coding: utf-8 -*-

import unittest
import logging

from ..taskresultset import TaskResultSet
from ..taskresult import TaskResult
from ..schemas import build_schema


log = logging.getLogger(name=__name__)


class TestTaskResultSet(unittest.TestCase):
    def setUp(self):
        self.task_name_1 = "test"

    def test_init(self):
        m = TaskResultSet(4, 5000)
        self.assertIsNotNone(m)

    def test_target_id_job_id_set(self):
        m = TaskResultSet(3, 1000)

        self.assertEqual(m.target_id, 3)
        self.assertEqual(m.job_id, 1000)

    def test_target_id_non_num(self):
        try:
            TaskResultSet("a", 1000)
        except ValueError:
            assert(True)
        else:
            assert(False)

    def test_job_id_non_num(self):
        try:
            TaskResultSet(87, "z")
        except ValueError:
            assert(True)
        else:
            assert(False)

    def test_single_key(self):
        m = TaskResultSet(4, 5000)
        tr = TaskResult(self.task_name_1, "1.1.1", 100)
        tr.add("a", "result")
        tr.finish()
        m.add(tr)

        # now extract the test
        tr_extract = m.get_task_tmoid(self.task_name_1, 100)
        self.assertIsNotNone(tr_extract)
        self.assertEqual(tr_extract.success, True)
        self.assertEqual(tr_extract.get_data("a"), "result")

    def test_replacement_key(self):
        # check we can overwrite an old result with a new one
        m = TaskResultSet(4, 5000)
        tr = TaskResult(self.task_name_1, "1.1.1", 100)
        tr.add("a", "result")
        tr.finish()
        m.add(tr)

        tr2 = TaskResult(self.task_name_1, "1.1.1", 100)
        tr2.add("a", "result2")
        tr2.finish()
        m.add(tr2)

        # now extract the test
        tr_extract = m.get_task_tmoid(self.task_name_1, 100)
        self.assertIsNotNone(tr_extract)
        self.assertEqual(tr_extract.success, True)
        self.assertEqual(tr_extract.get_data("a"), "result2")

    def test_missing_task(self):
        m = TaskResultSet(4, 5000)
        try:
            m.get_task_tmoid(self.task_name_1, 100)
        except ValueError:
            assert(True)
        else:
            assert(False)

    def test_missing_val(self):
        m = TaskResultSet(4, 5000)
        tr = TaskResult(self.task_name_1, "1.1.1", 100)
        tr.add("a", "result")
        tr.finish()
        m.add(tr)

        try:
            m.get_task_tmoid(self.task_name_1, 999)
        except ValueError:
            assert(True)
        else:
            assert(False)

    def test_unicode(self):
        task = "unicoder"
        key = u"俺"
        val = u"鍵"

        UnicodeSchema = build_schema({
            "properties": {
                "z": {"type": "string"}
            }
        })

        m = TaskResultSet(4, 5000)
        tr = TaskResult(task, "1.1.1", 100, schema=UnicodeSchema)
        tr.add("a", "result")
        tr.add(key, val)
        tr.finish()
        m.add(tr)

        tr_extract = m.get_task_tmoid(task, 100, schema=UnicodeSchema)

        self.assertEqual(tr_extract.get_data(key), val)

    def test_task_item_loop(self):
        TaskLoop1Schema = build_schema({
            "properties": {
                "y": {"type": "string"},
                "z": {"type": ["string", "null"]},
            }
        })

        TaskLoop2Schema = build_schema({
            "properties": {
                "y": {"type": ["string", "null"]},
                "z": {"type": ["string", "null"]},
            }
        })

        m = TaskResultSet(4, 5000)
        tr = TaskResult("task1", "1.1.1", 100, schema=TaskLoop1Schema)
        tr.add("y", "a")
        tr.add("z", "b")
        tr.finish()

        tr2 = TaskResult("task2", "1.1.1", 100, schema=TaskLoop2Schema)
        tr2.add("y", "hello")
        tr2.add("z", None)
        tr2.finish()

        m.add(tr)
        m.add(tr2)

        self.assertEqual(set(m.tasks()), set(["task1", "task2"]))
        self.assertEqual(set(m.task_tmoids("task1")), set([100]))
        self.assertEqual(set(m.task_tmoids("task2")), set([100]))

    def test_task_multi_tmoid(self):
        TaskLoop1Schema = build_schema({
            "properties": {
                "y": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "string"}
                    }
                },
                "z": {"type": ["string", "null"]},
            }
        })

        TaskLoop2Schema = build_schema({
            "properties": {
                "a": {"type": ["string", "null"]},
                "b": {"type": ["string", "null"]},
            }
        })

        m = TaskResultSet(4, 5000)
        tr = TaskResult("task1", "1.1.1", 100, schema=TaskLoop1Schema)
        tr.add("y", {"a": "1a"})
        tr.add("z", "b")
        tr.finish()

        tr2 = TaskResult("task1", "1.1.1", 101, schema=TaskLoop1Schema)
        tr2.add("y", {"a": "9z"})
        tr2.add("z", "x")
        tr2.finish()

        tr3 = TaskResult("task2", "1.1.1", 100, schema=TaskLoop2Schema)
        tr3.add("a", "hello")
        tr3.add("b", "foo")
        tr3.finish()

        m.add(tr)
        m.add(tr2)
        m.add(tr3)

        self.assertEqual(set(m.task_tmoids("task1")), set([100, 101]))
        log.debug(m)
        tr_extract = m.get_task_tmoid("task1", 100, schema=TaskLoop1Schema)
        tr2_extract = m.get_task_tmoid("task1", 101, schema=TaskLoop1Schema)
        tr3_extract = m.get_task_tmoid("task2", 100, schema=TaskLoop2Schema)

        self.assertEqual(tr_extract.get_data_strict("y"), {"a": "1a"})
        self.assertEqual(tr_extract.get_data_strict("z"), "b")
        self.assertEqual(tr2_extract.get_data_strict("y"), {"a": "9z"})
        self.assertEqual(tr2_extract.get_data_strict("z"), "x")
        self.assertEqual(tr3_extract.get_data_strict("a"), "hello")
        self.assertEqual(tr3_extract.get_data_strict("b"), "foo")

    def test_task_level_err(self):
        trs = TaskResultSet(4, 5000)
        trs.add_task_err("whois", "No domains received")

        self.assertEqual(trs.task_errs("whois"), ["No domains received"])

    def test_task_level_success_false(self):
        trs = TaskResultSet(4, 5000)
        trs.add_task_err("whois", "No domains received")

        self.assertFalse(trs.task_success("whois"))

    def test_task_level_success_true(self):
        TaskASchema = build_schema({
            "properties": {
                "a": {"type": "string"}
            }
        })
        print TaskASchema
        trs = TaskResultSet(4, 5000)

        tr = TaskResult("task2", "1.1.1", 100, schema=TaskASchema)
        tr.add("a", "hello")
        tr.finish()
        trs.add(tr)

        self.assertTrue(trs.task_success("task2"))

    def test_result_array(self):
        IpSchema = build_schema({
            "properties": {
                "ips": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
            }
        })

        trs = TaskResultSet(4, 5000)

        ips = TaskResult("task1", "1.1.1", 100, schema=IpSchema)
        ips.add("ips", ["1.1.1.1", "2.2.2.2"])
        ips.finish()

        trs.add(ips)

        ipset_tmoid = trs.get_task_tmoid("task1", 100, schema=IpSchema)
        ip_tmoid = ipset_tmoid.get_data("ips")

        self.assertEqual(ip_tmoid, ["1.1.1.1", "2.2.2.2"])

    def test_result_nested_obj(self):
        IpSchema = build_schema({
            "properties": {
                "ip": {"type": "string"},
            }
        })

        IpSetSchema = build_schema({
            "properties": {
                "ips": {
                    "type": "object",
                    "patternProperties": {
                        "^(\d{1,3}\.){1,3}(\d{1,3})$": IpSchema
                    },
                    "additionalProperties": False,
                },
            },
            "additionalProperties": False,
        })

        trs = TaskResultSet(4, 5000)
        ipset = TaskResult("task1", "1.1.1", 100, schema=IpSetSchema)

        ip = TaskResult("task1", "1.1.1", 100, schema=IpSchema)
        ip.add("ip", "1.1.1.1")
        ip.finish()

        ip2 = TaskResult("task1", "1.1.1", 100, schema=IpSchema)
        ip2.add("ip", "2.2.2.2")
        ip2.finish()

        ipset.add("ips", {"1.1.1.1": ip, "2.2.2.2": ip2})
        ipset.finish()

        trs.add(ipset)

        ipset_tmoid = trs.get_task_tmoid("task1", 100, schema=IpSetSchema)
        ip_tmoid = ipset_tmoid.get_data("ips").keys()

        self.assertEqual(ip_tmoid, ["1.1.1.1", "2.2.2.2"])
