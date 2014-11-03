from __future__ import absolute_import
import unittest
from swisschard.scheduler import ChardScheduler, ENTRY_LIST_KEY
from redis import StrictRedis
from redlock import Redlock
from celery.task import Task
import time
from threading import Thread
import os
import subprocess
from datetime import datetime
from tests.app import app


class AppThread(Thread):
    app = None

    def run(self):
        cmd = ['celery', 'beat', '-A', 'tests.app', '--pidfile', './test_celery.pid']
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        process.communicate()

    def stop(self):
        cmd = ['kill', '-9']
        with open('./test_celery.pid', 'r') as fp:
            cmd.append(fp.read().strip())
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        process.communicate()
        os.remove('./test_celery.pid')
        return self.join()


class EchoTask(Task):

    def run(self, msg="heartbeat"):
        return msg


class TestChardScheduler(unittest.TestCase):
    
    def setUp(self):
        self.redis_connection = StrictRedis.from_url("redis://")
        self.redis_connection.flushdb()
        print self.redis_connection.keys("*")
        self.startup = datetime.utcnow()
        self.locker = Redlock(["redis://"])
        self.scheduler = ChardScheduler(self.redis_connection, self.locker, app)
        self.thread = AppThread()
        self.thread.start()
        time.sleep(4)
        print "app started"

    def test_schedule_synced(self):
        print "checking for synced schedule"
        schedule = self.redis_connection.hgetall(ENTRY_LIST_KEY)
        self.assertEquals(len(schedule.keys()), 1)
        self.assertEquals(schedule.keys()[0], "heart_beat")
        heart_beat = schedule.get("heart_beat")
        # self.assertEquals(heart_beat[])

    def test_tasks_queued(self):
        time.sleep(5)
        now = datetime.utcnow()
        lapsed = now - self.startup
        expected_tasks = int(lapsed.total_seconds())
        task_count = self.redis_connection.llen("celery")
        self.assertTrue((expected_tasks==task_count or expected_tasks>=task_count-2 or expected_task<=task_count+2))

    def tearDown(self):
        self.thread.stop()



if __name__ == '__main__':
    app.start()

