#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import time
from drove.data.value import Value
from nose.tools import raises


def test_value():
    """Testing Value: dump()"""
    value = Value("example", 42, nodename="test", timestamp=0)
    assert value.dump() == "V|0|test|example|42.0|g"

    value = Value("example", 42, nodename="test")
    assert value.dump() == "V|%d|test|example|42.0|g" % (int(time.time()),)
    assert value.value_id == "test.example"


def test_value_dump():
    """Testing Value: from_dump()"""
    value = Value.from_dump("V|0|test|example|42.0|g")
    assert value.dump() == "V|0|test|example|42.0|g" == repr(value)


@raises(ValueError)
def test_value_malformed():
    """Testing Value: malformed event"""
    Value.from_dump("E|0")


@raises(ValueError)
def test_value_invalid_type():
    """Testing Value: invalid value type"""
    Value.from_dump("V|0|test|example|42.0|ZZ")
