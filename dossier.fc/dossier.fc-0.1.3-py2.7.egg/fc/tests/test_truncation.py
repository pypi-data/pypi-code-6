'''dossier.fc Feature Collections

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

'''
from __future__ import absolute_import, division, print_function
from collections import Counter
from operator import itemgetter
import time

import pytest

from dossier.fc.tests import counter_type


def test_truncation(counter_type):
    num = 100
    data = {str(x): x+1 for x in xrange(num)}

    counter = counter_type(data)
    assert len(counter) == num

    truncation_length = 10
    counter.truncate_most_common(truncation_length)
    assert len(counter) == truncation_length

    most_common = Counter(data).most_common(truncation_length)
    from_counter = map(itemgetter(1), counter.most_common(truncation_length))
    expected = map(itemgetter(1), most_common)
    assert from_counter == expected

    assert set(counter_type(dict(most_common)).items()) == set(counter.items())

    should_be_counter = counter_type({str(x): x+1 for x in xrange(90,100)})
    assert should_be_counter == counter


@pytest.mark.performance
def test_truncation_speed(counter_type):
    for x in range(4,7):
        num = 10**x
        data = {unicode(x): x+1 for x in xrange(num)}

        counter = counter_type(data)

        truncation_length = 10
        start_time = time.time()
        counter.truncate_most_common(truncation_length)
        elapsed = time.time() - start_time
        rate = num / elapsed
        print('%s truncated a counter of size %d in %.3f sec '
              '--> %.1f items/sec' % (counter_type, num, elapsed, rate))
        assert len(counter) == truncation_length
