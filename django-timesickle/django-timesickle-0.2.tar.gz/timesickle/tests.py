import datetime

import logging

from django.shortcuts import render_to_response
from django.test import Client
from django.test import SimpleTestCase
from django.test import TestCase

from . import datetime as sickle

from .templatetags import timesickle as tags


logger = logging.getLogger("test." + __name__)


class TestSickleObjects(SimpleTestCase):

    def _test_attribute(self, attr, attrtype):
        a = getattr(sickle, attr)()
        logger.info("%s: %s", attr, str(a))
        self.assertTrue(isinstance(a, attrtype))

    def test_now(self):
        self._test_attribute('now', datetime.datetime)

    def test_today(self):
        self._test_attribute('today', datetime.date)

    def test_yesterday(self):
        self._test_attribute('yesterday', datetime.date)

    def test_yesterday_sametime(self):
        self._test_attribute('yesterday_sametime', datetime.datetime)

    def test_tomorrow(self):
        self._test_attribute('tomorrow', datetime.date)

    def test_tomorrow_sametime(self):
        self._test_attribute('tomorrow_sametime', datetime.datetime)

    # def test_christmas(self):
    #     c = sickle.dates.christmas
    #     self.assertTrue(isinstance(c, datetime.date))


class TestTags(SimpleTestCase):

    def test_default_now(self):
        now = tags.now()
        logger.info("now: %s" % now)

    def test_default_today(self):
        today = tags.now()
        logger.info("today: %s" % today)


class TestRender(TestCase):

    def test_default_now(self):
        render_to_response("timesickle-test-default-now.html")

    def test_default_today(self):
        render_to_response("timesickle-test-default-today.html")
