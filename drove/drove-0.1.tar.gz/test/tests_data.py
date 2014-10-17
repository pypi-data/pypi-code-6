#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from drove.data import Data
from nose.tools import raises


def test_data_dump_value():
    """Testing Data: Value from_dump()"""
    value = Data.from_dump("V|0|test|example|42.0|g")
    assert value.__class__.__name__ == "Value"


def test_data_dump_event():
    """Testing Data: Event from_dump()"""
    event = Data.from_dump("E|0|test|example|CRITICAL|message")
    assert event.__class__.__name__ == "Event"


@raises(ValueError)
def test_data_malformed_type():
    """Testing Data: malformed data type"""
    Data.from_dump("ZZ|0")


@raises(ValueError)
def test_data_malformed_value():
    """Testing Data: malformed value"""
    Data.from_dump("V|0")


@raises(ValueError)
def test_data_malformed_event():
    """Testing Data: malformed event"""
    Data.from_dump("E|0")
