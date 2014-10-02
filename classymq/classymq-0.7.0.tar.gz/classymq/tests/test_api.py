#!/usr/bin/env python
from twisted.internet.defer import inlineCallbacks
from classymq.tests import base
from twisted.internet import reactor
from classymq.api import consumer, producer, common

__author__ = 'gdoermann'

class TestAPIExchange(common.AMQPAPIExchange):
    KEY = "test-amqpapi"


class TestAMQPAPIQueue(common.AMQPAPIQueue):
    KEY = "test-amqpapi-%(prefix)s-%(uuid)s"


class TestAPIConsumer(consumer.AMQPAPIConsumer):
    EXCHANGE = TestAPIExchange
    QUEUE = TestAMQPAPIQueue
    MESSAGE_CLASS = common.AMQPAPIRequest


class ApiTest(base.ClassyTestCase):

    @inlineCallbacks
    def test_connection(self):
        yield self.defer_until_connected
