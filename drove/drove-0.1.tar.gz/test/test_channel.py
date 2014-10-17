#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from drove.channel import Channel
from nose.tools import raises


def test_channel_subscription():
    """Testing Channel: subscription"""
    channel = Channel()
    channel.subscribe("test")
    assert "test" in channel.queues


def test_channel_broadcast():
    """Testing Channel: publish broadcast"""
    channel = Channel()
    channel.subscribe("test")
    channel.publish("hello")
    assert [x for x in channel.receive("test")][0] == "hello"


def test_channel_publish():
    """Testing Channel: publish topic"""
    channel = Channel()
    channel.subscribe("test")
    channel.subscribe("test2")
    channel.publish("hello", topic="test")
    assert [x for x in channel.receive("test")][0] == "hello"
    assert channel.queues["test2"].qsize() == 0


@raises(KeyError)
def test_channel_publish_none():
    """Testing Channel: publish non-existant"""
    channel = Channel()
    channel.publish("bye", topic="fail")


@raises(KeyError)
def test_channel_receive_none():
    """Testing Channel: receive non-existant"""
    channel = Channel()
    channel.subscribe("test")
    channel.publish("bye")
    [x for x in channel.receive("bye")]


def test_channel_receive_empty():
    """Testing Channel: receive in empty queue"""
    channel = Channel()
    channel.subscribe("test")
    assert [x for x in channel.receive("test")] == []
