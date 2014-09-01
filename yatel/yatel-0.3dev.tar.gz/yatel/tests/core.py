#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#===============================================================================
# DOC
#===============================================================================

"""All yatel tests"""


#===============================================================================
# IMPORTS
#===============================================================================

import unittest
import random
import functools
import tempfile
import os

import numpy as np

try:
    from mock import patch, Mock
    MOCK = True
except ImportError:
    MOCK = False

from yatel import db, dom, weight


#==============================================================================
# MOCKS
#==============================================================================

TO_MOCK = {}

if MOCK:
    TO_MOCK.update({
        "yatel.cluster.kmeans.vq.kmeans": {
            "patch": {},
            "mock": {
                "return_value": [None, None]
            }
        },
        "requests.post": {
            "patch": {},
            "mock": {
                "return_value": Mock(json=lambda: {
                    "error": False,
                    "result": {"type": "literal", "value": None},
                    "id": None,
                    "error_msg": "",
                    "stack_trace": "",
                })
            }
        }
    })


#===============================================================================
# BASE CLASS
#===============================================================================

class YatelTestCase(unittest.TestCase):

    @classmethod
    def subclasses(self):
        return set(self.__subclasses__())

    def conn(self):
        return {"engine": "memory"}

    def add_elements(self, nw):

        lorem_ipsum = [
            'takimata', 'sea', 'ametlorem', 'magna', 'ea', 'consetetur', 'sed',
            'accusam', 'et', 'diamvoluptua', 'labore', 'diam', 'sit', 'dolores',
            'sadipscing', 'aliquyam', 'dolore', 'stet', 'lorem', 'elitr',
            'elitr', 'est', 'no', 'dolor', 'kasd', 'invidunt', 'amet', 'vero',
            'ipsum', 'rebum', 'erat', 'gubergren', 'duo', 'justo', 'tempor',
            'eos', 'sanctus', 'at', 'clita', 'ut', 'nonumyeirmod', 'amet'
        ]

        def gime_fake_hap_attrs():
            attrs_generator = {
                "name": lambda: random.choice(lorem_ipsum).title(),
                "number": lambda: random.choice(range(10, 100)),
                "color": lambda: random.choice('rgbcmyk'),
                "special": lambda: random.choice([True, False]),
                "size": lambda: random.choice(range(10, 100)) + random.random(),
                "height": lambda: random.choice(range(10, 100)) + random.random(),
                "description": lambda: (
                    random.choice(lorem_ipsum).title() + " ".join(
                        [random.choice(lorem_ipsum) for _
                         in range(random.randint(10, 50))]
                    )
                )
            }

            attrs = {}
            for k, v in attrs_generator.items():
                if random.choice([True, False]):
                    attrs[k] = v()
            if not attrs:
                k, v = random.choice(attrs_generator.items())
                attrs[k] = v()
            return attrs

        def gimme_fake_fact_attrs():
            attrs_generator = {
                "place": lambda: random.choice([
                    'Mordor', 'Ankh-Morpork', 'Genosha',
                    'Gotham City', 'Hogwarts', 'Heaven',
                    'Tatooine', 'Vulcan', 'Valhalla'
                ]),
                "category": lambda: random.choice('SABCDEF'),
                "native": lambda: random.choice([True, False]),
                "align": lambda: random.choice([-1, 0, 1]),
                "variance": lambda: random.choice(range(10, 100)) + random.random(),
                "coso": lambda: random.choice(lorem_ipsum),
            }
            attrs = {}
            for k, v in attrs_generator.items():
                if random.choice([True, False]):
                    attrs[k] = v()
            if not attrs:
                k, v = random.choice(attrs_generator.items())
                attrs[k] = v()
            return attrs

        haps_n = 5
        facts_n = 10
        weight_calc = "ham"

        haps = []
        for hap_id in range(haps_n):
            attrs = gime_fake_hap_attrs()
            hap = dom.Haplotype(hap_id, **attrs)
            nw.add_element(hap)
            haps.append(hap)

        for hap_id in range(haps_n):
            for _ in range(random.randint(0, facts_n)):
                attrs = gimme_fake_fact_attrs()
                fact = dom.Fact(hap_id, **attrs)
                nw.add_element(fact)

        for hs, w in weight.weights(weight_calc, haps):
            haps_id = map(lambda h: h.hap_id, hs)
            edge = dom.Edge(w, haps_id)
            nw.add_element(edge)

        return [h.hap_id for h in haps]

    def get_random_nw(self, conn):
        conn["mode"] = db.MODE_WRITE
        nw = db.YatelNetwork(**conn)
        haps_ids = self.add_elements(nw)
        nw.confirm_changes()
        return nw, haps_ids

    def setUp(self):
        self.nw, self.haps_ids = self.get_random_nw(self.conn())
        if MOCK:
            for target, options in TO_MOCK.items():
                mock = patch(target, **options["patch"]).start()
                mock.configure_mock(**options["mock"])

    def tearDown(self):
        if MOCK:
            patch.stopall()
        if self.conn()["engine"] == "sqlite":
            os.remove(self.conn()["database"])

    #==========================================================================
    # CUSTOM ASSERTS
    #==========================================================================

    def assertAllTheSame(self, iterable, *args, **kwargs):
        result = all(x == iterable[0] for x in iterable)
        self.assertTrue(result, *args, **kwargs)

    def assertAproxDatetime(self, dt0, dt1):
        self.assertEqual(
            dt0.isoformat().rsplit(".", 1)[0],
            dt1.isoformat().rsplit(".", 1)[0]
        )

    def assertSameUnsortedContent(self, i0, i1):
        i0 = list(sorted(i0))
        i1 = list(i1)
        while i0:
            elem = i0.pop()
            if elem in i1:
                i1.remove(elem)
            else:
                msg = "'{}' only in one collection".format(repr(elem))
                raise AssertionError(msg)
        if i1:
            elem = i1.pop()
            msg = "'{}' only in one collection".format(repr(elem))
            raise AssertionError(msg)

    def assertNDArrayEquals(self, arr0, arr1):
        self.assertEquals(len(arr0), len(arr1))
        self.assertTrue(np.allclose(arr0, arr1, rtol=1e-01))

    def assertUnsortedNDArray(self, arr0, arr1):
        # happy to compare disorder floats in numpy...
        used = set()
        for idx, coordo in enumerate(arr0):
            fail = True
            for jdx, coordr in enumerate(arr1):
                if np.allclose(coordo, coordr, rtol=1e-01) and jdx not in used:
                    fail = False
                    used.add(jdx)
                    break
            self.assertFalse(fail, "{} != {}".format(arr0, arr1))

    #==========================================================================
    # UTILS
    #==========================================================================

    def rrange(self, li, ls):
        top = random.randint(li, ls)
        return xrange(top)

    def rchoice(self, iterable):
        return random.choice(tuple(iterable))


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
