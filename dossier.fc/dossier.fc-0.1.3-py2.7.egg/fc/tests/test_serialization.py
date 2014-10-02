'''dossier.fc Feature Collections

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

'''
from __future__ import absolute_import, division, print_function
import json
import time

import pytest

from dossier.fc import FeatureCollection, SerializationError, StringCounter
from dossier.fc.feature_collection import registry


class Thing(object):
    def __init__(self, blob=None):
        self.data = dict()
        if blob is not None:
            self.loads(blob)

    def dumps(self):
        return json.dumps(self.data)

    def loads(self, blob):
        self.data = json.loads(blob)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def do_more_things(self):
        self.data['doing'] = 'something'

    def __eq__(self, other):
        return self.data == other.data

    def __repr__(self):
        return 'Thing({!r})'.format(self.dumps())


class ThingSerializer(object):
    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def loads(blob):
        return Thing(blob)

    @staticmethod
    def dumps(thing):
        return thing.dumps()        

    constructor = Thing


class JsonSerializer(object):
    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def loads(bytes):
        return StringCounter(json.loads(bytes))

    @staticmethod
    def dumps(sc):
        return json.dumps(sc)

    constructor = staticmethod(lambda: StringCounter)


def test_string_counter_serialize():
    fc = FeatureCollection()
    fc['thing1'] = StringCounter()
    fc['thing1']['foo'] += 1
    fc_str = fc.dumps()

    fc2 = FeatureCollection.loads(fc_str)
    assert fc2['thing1']['foo'] == 1


def test_thing_serializer():
    with registry:
        registry.add('StringCounter', ThingSerializer)

        fc = FeatureCollection()
        fc['thing1'] = Thing(json.dumps(dict(hello='people')))
        fc['thing1']['another'] = 'more'
        fc['thing1'].do_more_things()
        fc_str = fc.dumps()
        
        fc2 = FeatureCollection.loads(fc_str)

        assert fc2['thing1']['another'] == 'more'
        assert fc2['thing1']['hello'] == 'people'
        assert fc2['thing1']['doing'] == 'something'


def test_json_serializer():
    with registry:
        registry.add('StringCounter', JsonSerializer)

        fc = FeatureCollection()
        fc['thing2'] = StringCounter(dict(hello='people'))
        fc['thing2']['another'] = 5
        fc['thing3'] = StringCounter(dict(hello='people2'))
        fc_str = fc.dumps()
        
        fc2 = FeatureCollection.loads(fc_str)

        assert fc2['thing2']['another'] == 5
        assert fc2['thing2']['hello'] == 'people'
        assert fc2['thing3']['hello'] == 'people2'


def test_no_bytes_allowed():
    fc = FeatureCollection({'foo': u'bar'})
    fc.dumps()  # OK!

    with pytest.raises(SerializationError):
        fc = FeatureCollection({'foo': 'bar'})

    fc = FeatureCollection()
    fc['foo'] = 'bar'
    with pytest.raises(SerializationError):
        fc.dumps()


def test_ignored():
    fc = FeatureCollection()
    fc['foo'] = 'bar'
    with pytest.raises(SerializationError):
        fc.dumps()

    fc = FeatureCollection()
    fc['_foo'] = 'bar'
    fc.dumps()  # _foo is ignored!


# TODO: explain how this number is picked
EXPECTED_INSTANCE_COLLECTION_SERIALIZATION_SPEED = 50


@pytest.mark.performance
def test_throughput_feature_collection():
    with registry:
        registry.add('StringCounter', ThingSerializer)
        fc = FeatureCollection()
        fc['thing1'] = Thing(json.dumps(dict(one_mb=' ' * 2**20)))
        fc_str = fc.dumps()

        start_time = time.time()
        num = 100
        for i in range(num):
            print(i)
            fc2 = FeatureCollection.loads(fc_str)
            fc2.dumps()
        elapsed = time.time() - start_time
        rate = float(num) / elapsed
        print('%d MB in %.1f sec --> %.1f MB per sec' % (num, elapsed, rate))
        assert rate > EXPECTED_INSTANCE_COLLECTION_SERIALIZATION_SPEED
