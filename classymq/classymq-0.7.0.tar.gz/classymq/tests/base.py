#!/usr/bin/env python
from unittest import TestCase
from classymq.common import resolve_setting
from twisted.internet import reactor
from classymq import factory

__author__ = 'gdoermann'

TEST_RABBIT_MQ_HOST = resolve_setting('TEST_RABBIT_MQ_HOST', 'localhost')
TEST_RABBIT_MQ_PORT = resolve_setting('TEST_RABBIT_MQ_PORT', 5672)

TEST_VHOST = resolve_setting('TEST_VHOST', '/')

class TestFactory(factory.AmqpFactory):
    def clientConnectionFailed(self, connector, reason):
        self.continueTrying = False
        factory.AmqpFactory.clientConnectionFailed(self, connector, reason)
        raise RuntimeError('AMQP connection failed')

    def clientConnectionLost(self, connector, reason):
        self.continueTrying = False
        factory.AmqpFactory.clientConnectionFailed(self, connector, reason)
        raise RuntimeError('Lost AMQP connection')


class ClassyTestCase(TestCase):

    connection = None
    defer_until_connected = None

    def setUp(self):
        self.connection = self.get_factory()
        super(ClassyTestCase, self).setUp()

    def get_factory(self):
        con = TestFactory(vhost=TEST_VHOST, host=TEST_RABBIT_MQ_HOST, port=TEST_RABBIT_MQ_PORT)
        self.defer_until_connected = con.connect()
        return con

