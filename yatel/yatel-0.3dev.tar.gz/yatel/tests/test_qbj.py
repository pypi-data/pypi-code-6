#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#==============================================================================
# DOC
#==============================================================================

"""yatel.qbj package tests"""


#==============================================================================
# IMPORTS
#==============================================================================

import hashlib
import random
import datetime
import collections
import unittest

from yatel import stats
from yatel import typeconv
from yatel.cluster import kmeans
from yatel import qbj
from yatel.qbj import functions

from yatel.tests import core


#==============================================================================
# FUNCTION_TESTS
#==============================================================================

class FunctionTest(core.YatelTestCase):

    def execute(self, name, nw=None, **kwargs):
        nw = self.nw if nw is None else nw
        return functions.execute(name, nw, **kwargs)

    def test_ping(self):
        orig = functions.ping(self.nw)
        rs = self.execute("ping")
        self.assertEquals(orig, rs)

    def test_help(self):
        orig = list(functions.FUNCTIONS.keys())
        rs = self.execute("help")
        self.assertSameUnsortedContent(orig, rs)
        for fname, fdata in functions.FUNCTIONS.items():
            orig = functions.pformat_data(fname)
            rs = self.execute("help", fname=fname)
            self.assertEquals(orig, rs)

    def test_haplotypes(self):
        orig = tuple(self.nw.haplotypes())
        rs = tuple(self.execute("haplotypes"))
        self.assertSameUnsortedContent(rs, orig)

    def test_haplotype_by_id(self):
        orig = self.rchoice(self.nw.haplotypes())
        rs = self.execute("haplotype_by_id", hap_id=orig.hap_id)
        self.assertEqual(rs, orig)

    def test_haplotypes_by_environment(self):
        for env in list(self.nw.environments()) + [None]:
            orig = tuple(self.nw.haplotypes_by_environment(env))
            rs = tuple(self.execute("haplotypes_by_environment", env=env))
            self.assertSameUnsortedContent(rs, orig)

    def test_edges(self):
        orig = tuple(self.nw.edges())
        rs = tuple(self.execute("edges"))
        self.assertSameUnsortedContent(rs, orig)

    def test_edges_by_haplotype(self):
        hap = self.rchoice(self.nw.haplotypes())
        orig = tuple(self.nw.edges_by_haplotype(hap))
        rs = tuple(self.execute("edges_by_haplotype", hap=hap))
        self.assertEqual(rs, orig)

    def test_edges_by_environment(self):
        for env in list(self.nw.environments()) + [None]:
            orig = tuple(self.nw.edges_by_environment(env))
            rs = tuple(self.execute("edges_by_environment", env=env))
            self.assertSameUnsortedContent(rs, orig)

    def test_facts(self):
        orig = tuple(self.nw.facts())
        rs = tuple(self.execute("facts"))
        self.assertSameUnsortedContent(rs, orig)

    def test_facts_by_haplotype(self):
        hap = self.rchoice(self.nw.haplotypes())
        orig = tuple(self.nw.facts_by_haplotype(hap))
        rs = tuple(self.execute("facts_by_haplotype", hap=hap))
        self.assertEqual(rs, orig)

    def test_facts_by_environment(self):
        for env in list(self.nw.environments()) + [None]:
            orig = tuple(self.nw.facts_by_environment(env))
            rs = tuple(self.execute("facts_by_environment", env=env))
            self.assertSameUnsortedContent(rs, orig)

    def test_describe(self):
        orig = self.nw.describe()
        rs = self.execute("describe")
        self.assertEqual(rs, orig)

    def test_environments(self):
        orig = tuple(self.nw.environments())
        rs = tuple(self.execute("environments"))
        self.assertSameUnsortedContent(rs, orig)

    def test_env2weightarray(self):
        for env in list(self.nw.environments()) + [None]:
            orig = list(stats.env2weightarray(self.nw, env))
            rs = list(self.execute("env2weightarray", env=env))
            self.assertEqual(orig, rs)

    def test_min(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.min(self.nw, env)
                rs_nw = self.execute("min", env=env)
                orig_arr = stats.min(arr)
                rs_arr = self.execute("min", nw=arr)
                self.assertTrue(
                    orig_nw == rs_nw and rs_nw == orig_arr and
                    orig_arr == rs_arr and rs_arr == orig_nw
                )

    def test_sum(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.sum(self.nw, env)
                rs_nw = self.execute("sum", env=env)
                orig_arr = stats.sum(arr)
                rs_arr = self.execute("sum", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_var(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.var(self.nw, env)
                rs_nw = self.execute("var", env=env)
                orig_arr = stats.var(arr)
                rs_arr = self.execute("var", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_mode(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = list(stats.mode(self.nw, env))
                rs_nw = list(self.execute("mode", env=env))
                orig_arr = list(stats.mode(arr))
                rs_arr = list(self.execute("mode", nw=arr))
                self.assertEqual(orig_nw, rs_nw)
                self.assertEqual(orig_arr, rs_arr)
                self.assertEqual(orig_nw, orig_arr)

    def test_max(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.max(self.nw, env)
                rs_nw = self.execute("max", env=env)
                orig_arr = stats.max(arr)
                rs_arr = self.execute("max", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_variation(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.variation(self.nw, env=env)
                rs_nw = self.execute("variation", env=env)
                orig_arr = stats.variation(arr)
                rs_arr = self.execute("variation", nw=arr)

                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_kurtosis(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.kurtosis(self.nw, env)
                rs_nw = self.execute("kurtosis", env=env)
                orig_arr = stats.kurtosis(arr)
                rs_arr = self.execute("kurtosis", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_amax(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.amax(self.nw, env)
                rs_nw = self.execute("amax", env=env)
                orig_arr = stats.amax(arr)
                rs_arr = self.execute("amax", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_std(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.std(self.nw, env)
                rs_nw = self.execute("std", env=env)
                orig_arr = stats.std(arr)
                rs_arr = self.execute("std", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_amin(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.amin(self.nw, env)
                rs_nw = self.execute("amin", env=env)
                orig_arr = stats.amin(arr)
                rs_arr = self.execute("amin", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_average(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.average(self.nw, env)
                rs_nw = self.execute("average", env=env)
                orig_arr = stats.average(arr)
                rs_arr = self.execute("average", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_median(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.median(self.nw, env)
                rs_nw = self.execute("median", env=env)
                orig_arr = stats.median(arr)
                rs_arr = self.execute("median", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_range(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                orig_nw = stats.range(self.nw, env)
                rs_nw = self.execute("range", env=env)
                orig_arr = stats.range(arr)
                rs_arr = self.execute("range", nw=arr)
                self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_percentile(self):
        for env in list(self.nw.environments()) + [None]:
            arr = stats.env2weightarray(self.nw, env)
            if len(arr):
                for q in range(0, 100):
                    orig_nw = stats.percentile(self.nw, q, env)
                    rs_nw = self.execute("percentile", q=q, env=env)
                    orig_arr = stats.percentile(arr, q)
                    rs_arr = self.execute("percentile", q=q, nw=arr)
                    self.assertAlmostEqual(orig_nw, rs_nw, places=4)
                    self.assertAlmostEqual(orig_arr, rs_arr, places=4)
                    self.assertAlmostEqual(orig_nw, orig_arr, places=4)

    def test_slice(self):
        iterables = [
            list(range(1000)), hashlib.sha512(str(random.random())).hexdigest()
        ]
        for iterable in iterables:
            il = int(len(iterable) - len(iterable) / 3)
            sl = int(len(iterable) - len(iterable) / 4)
            orig = iterable[il:sl]
            rs = self.execute("slice", iterable=iterable, f=il, t=sl)
            self.assertEqual(orig, rs)

            orig = iterable[il:]
            rs = self.execute("slice", iterable=iterable, f=il)
            self.assertEqual(orig, rs)

    def test_size(self):
        iterable = [idx for idx in self.rrange(1, 1000)]
        orig = len(iterable)
        rs = self.execute("size", iterable=iterable)
        self.assertEqual(orig, rs)

    def test_utcnow(self):
        orig = datetime.datetime.utcnow()
        rs = self.execute("utcnow")
        self.assertAproxDatetime(orig, rs)

    def test_utctime(self):
        orig = datetime.datetime.utcnow().time()
        rs = self.execute("utctime")
        self.assertAproxDatetime(orig, rs)

    def test_utctoday(self):
        orig = datetime.datetime.utcnow().date()
        rs = self.execute("utctoday")
        self.assertAproxDatetime(orig, rs)

    def test_today(self):
        orig = datetime.date.today()
        rs = self.execute("today")
        self.assertAproxDatetime(orig, rs)

    def test_now(self):
        orig = datetime.datetime.now()
        rs = self.execute("now")
        self.assertAproxDatetime(orig, rs)

    def test_time(self):
        orig = datetime.datetime.now().time()
        rs = self.execute("time")
        self.assertAproxDatetime(orig, rs)

    def test_minus(self):
        a = random.randint(100, 1000)
        b = random.randint(100, 1000)
        orig = a - b
        rs = self.execute("minus", minuend=a, sust=b)
        self.assertEqual(orig, rs)

    def test_times(self):
        a = random.randint(100, 1000)
        b = random.randint(100, 1000)
        orig = a * b
        rs = self.execute("times", t0=a, t1=b)
        self.assertEqual(orig, rs)

    def test_div(self):
        a = random.randint(100, 1000)
        b = float(random.randint(100, 1000))
        orig = a / b
        rs = self.execute("div", dividend=a, divider=b)
        self.assertAlmostEqual(orig, rs, places=4)

    def test_floor(self):
        a = random.randint(100, 1000)
        b = float(random.randint(100, 1000))
        orig = a % b
        rs = self.execute("floor", dividend=a, divider=b)
        self.assertAlmostEqual(orig, rs, places=4)

    def test_pow(self):
        a = random.randint(100, 1000)
        b = random.randint(100, 1000)
        orig = a ** b
        rs = self.execute("pow", radix=a, exp=b)
        self.assertAlmostEqual(orig, rs, places=4)

    def test_xroot(self):
        rs = self.execute("xroot", radix=8, root=3)
        self.assertAlmostEqual(2, rs, places=4)

    def test_count(self):
        iterable = [idx for idx in self.rrange(1, 100)]
        counter = collections.Counter(iterable)
        for elem, orig in counter.items():
            rs = self.execute("count", iterable=iterable, to_count=elem)
            self.assertEqual(orig, rs)

    def test_sort(self):
        iterable = [idx for idx in self.rrange(1, 100)]
        orig = list(sorted(iterable))
        rs = self.execute("sort", iterable=iterable)
        self.assertEquals(orig, rs)
        orig = list(sorted(iterable, reverse=True))
        rs = self.execute("sort", iterable=iterable, reverse=True)
        self.assertEquals(orig, rs)

        iterable = [
            {"a": random.randint(1, 200)},
            {"a": random.randint(1, 200)}
        ]
        orig = list(sorted(iterable, key=lambda e: e["a"]))
        rs = self.execute("sort", iterable=iterable, key="a")
        self.assertEquals(orig, rs)
        orig = list(sorted(iterable, key=lambda e: e["a"], reverse=True))
        rs = self.execute("sort", iterable=iterable, key="a", reverse=True)
        self.assertEquals(orig, rs)

        dkey = random.randint(1, 300)
        orig = list(sorted(iterable, key=lambda e: dkey))
        rs = self.execute("sort", iterable=iterable, key="b", dkey=dkey)
        self.assertEquals(orig, rs)

        Mock = collections.namedtuple("Mock", ["x"])
        iterable = [
            Mock(x=random.randint(1, 800)), Mock(x=random.randint(1, 800))
        ]
        orig = list(sorted(iterable, key=lambda e: e.x))
        rs = self.execute("sort", iterable=iterable, key="x")
        self.assertEquals(orig, rs)
        orig = list(sorted(iterable, key=lambda e: e.x, reverse=True))
        rs = self.execute("sort", iterable=iterable, key="x", reverse=True)
        self.assertEquals(orig, rs)

        dkey = random.randint(1, 300)
        orig = list(sorted(iterable, key=lambda e: dkey))
        rs = self.execute("sort", iterable=iterable, key="b", dkey=dkey)
        self.assertEquals(orig, rs)

        orig = list(sorted(iterable, key=lambda e: dkey, reverse=True))
        rs = self.execute(
            "sort", iterable=iterable, key="b", dkey=dkey, reverse=True
        )
        self.assertEquals(orig, rs)

    def test_index(self):
        iterable = list(set(idx for idx in self.rrange(100, 200)))
        random.shuffle(iterable)

        orig = len(iterable) / 2
        elem = iterable[orig]

        rs = self.execute("index", iterable=iterable, value=elem)
        self.assertEqual(orig, rs)

        rs = self.execute("index", iterable=iterable, value=elem, start=orig-1)
        self.assertEqual(orig, rs)
        rs = self.execute("index", iterable=iterable, value=elem, start=orig+1)
        self.assertEqual(-1, rs)

        rs = self.execute(
            "index", iterable=iterable, value=elem, start=orig-1, end=orig+1
        )
        self.assertEqual(orig, rs)
        rs = self.execute(
            "index", iterable=iterable, value=elem, start=orig-2, end=orig-1
        )
        self.assertEqual(-1, rs)

    def test_split(self):
        string_s = (
            hashlib.sha512(str(random.random())).hexdigest(),
            hashlib.sha512(str(random.random())).hexdigest(),
            hashlib.sha512(str(random.random())).hexdigest()
        )
        joiners = (
            " ", hashlib.sha512(str(random.random())).hexdigest()
        )
        for joiner in joiners:
            string = joiner.join(string_s)
            orig = string.split(joiner)
            rs = self.execute("split", string=string, s=joiner)
            self.assertEquals(orig, rs)
            orig = string.split(joiner, 1)
            rs = self.execute("split", string=string, s=joiner, maxsplit=1)
            self.assertEquals(orig, rs)

    def test_rsplit(self):
        string_s = (
            hashlib.sha512(str(random.random())).hexdigest(),
            hashlib.sha512(str(random.random())).hexdigest(),
            hashlib.sha512(str(random.random())).hexdigest()
        )
        joiners = (
            " ", hashlib.sha512(str(random.random())).hexdigest()
        )
        for joiner in joiners:
            string = joiner.join(string_s)
            orig = string.rsplit(joiner)
            rs = self.execute("rsplit", string=string, s=joiner)
            self.assertEquals(orig, rs)
            orig = string.rsplit(joiner, 1)
            rs = self.execute("rsplit", string=string, s=joiner, maxsplit=1)
            self.assertEquals(orig, rs)

    def test_strip(self):
        string = " !{}! \n\t".format(
            hashlib.sha512(str(random.random())).hexdigest()
        )
        orig = string.strip()
        rs = self.execute("strip", string=string)
        self.assertEquals(orig, rs)
        self.assertFalse(rs.endswith(string[-1]))
        self.assertFalse(rs.startswith(string[0]))

        tostrip = hashlib.sha512(str(random.random())).hexdigest()
        string = "{} !{}! {}".format(
            tostrip, hashlib.sha512(str(random.random())).hexdigest(), tostrip
        )
        orig = string.strip(tostrip)
        rs = self.execute("strip", string=string, chars=tostrip)
        self.assertEquals(orig, rs)
        self.assertFalse(rs.endswith(string[-1]))
        self.assertFalse(rs.startswith(string[0]))

    def test_lstrip(self):
        string = " !{}! \n\t".format(
            hashlib.sha512(str(random.random())).hexdigest()
        )
        orig = string.lstrip()
        rs = self.execute("lstrip", string=string)
        self.assertEquals(orig, rs)
        self.assertTrue(rs.endswith(string[-1]))
        self.assertFalse(rs.startswith(string[0]))

        tostrip = hashlib.sha512(str(random.random())).hexdigest()
        string = "{} !{}! {}".format(
            tostrip, hashlib.sha512(str(random.random())).hexdigest(), tostrip
        )
        orig = string.lstrip(tostrip)
        rs = self.execute("lstrip", string=string, chars=tostrip)
        self.assertEquals(orig, rs)
        self.assertTrue(rs.endswith(string[-1]))
        self.assertFalse(rs.startswith(string[0]))

    def test_rstrip(self):
        string = " !{}! \n\t".format(
            hashlib.sha512(str(random.random())).hexdigest()
        )
        orig = string.rstrip()
        rs = self.execute("rstrip", string=string)
        self.assertEquals(orig, rs)
        self.assertFalse(rs.endswith(string[-1]))
        self.assertTrue(rs.startswith(string[0]))

        tostrip = hashlib.sha512(str(random.random())).hexdigest()
        string = "{} !{}! {}".format(
            tostrip, hashlib.sha512(str(random.random())).hexdigest(), tostrip
        )
        orig = string.rstrip(tostrip)
        rs = self.execute("rstrip", string=string, chars=tostrip)
        self.assertEquals(orig, rs)
        self.assertFalse(rs.endswith(string[-1]))
        self.assertTrue(rs.startswith(string[0]))

    def test_join(self):
        string_s = (
            hashlib.sha512(str(random.random())).hexdigest(),
            hashlib.sha512(str(random.random())).hexdigest(),
            hashlib.sha512(str(random.random())).hexdigest()
        )
        joiner = hashlib.sha512(str(random.random())).hexdigest()
        orig = joiner.join(string_s)
        rs = self.execute("join", joiner=joiner, to_join=string_s)
        self.assertEqual(orig, rs)

    def test_upper(self):
        string = hashlib.sha512(str(random.random())).hexdigest() + "zzz"
        orig = string.upper()
        rs = self.execute("upper", string=string)
        self.assertEqual(orig, rs)

    def test_lower(self):
        string = hashlib.sha512(str(random.random())).hexdigest() + "QQQ"
        orig = string.lower()
        rs = self.execute("lower", string=string)
        self.assertEqual(orig, rs)

    def test_title(self):
        string = "t" + hashlib.sha512(str(random.random())).hexdigest() + " QQ"
        orig = string.title()
        rs = self.execute("title", string=string)
        self.assertEqual(orig, rs)
        self.assertTrue(rs[0].isupper())
        self.assertTrue(rs[-2].isupper())
        self.assertFalse(rs[-1].isupper())

    def test_capitalize(self):
        string = "t" + hashlib.sha512(str(random.random())).hexdigest() + " QQ"
        orig = string.capitalize()
        rs = self.execute("capitalize", string=string)
        self.assertEqual(orig, rs)
        self.assertTrue(rs[0].isupper())
        self.assertFalse(rs[-2].isupper())
        self.assertFalse(rs[-1].isupper())

    def test_isalnum(self):
        cases = (
            hashlib.sha512(str(random.random())).hexdigest(),
            str(random.randint(100, 1000)), "dhfuoucDSADFDSFsldfnkljsdfb", "!"
        )
        for case in cases:
            orig = case.isalnum()
            rs = self.execute("isalnum", string=case)
            self.assertEqual(orig, rs)

    def test_isalpha(self):
        cases = (
            hashlib.sha512(str(random.random())).hexdigest(),
            str(random.randint(100, 1000)), "dhfuoucDSADFDSFsldfnkljsdfb", "!"
        )
        for case in cases:
            orig = case.isalpha()
            rs = self.execute("isalpha", string=case)
            self.assertEqual(orig, rs)

    def test_isdigit(self):
        cases = (
            hashlib.sha512(str(random.random())).hexdigest(),
            str(random.randint(100, 1000)), "dhfuoucDSADFDSFsldfnkljsdfb", "!"
        )
        for case in cases:
            orig = case.isdigit()
            rs = self.execute("isdigit", string=case)
            self.assertEqual(orig, rs)

    def test_startswith(self):
        one = hashlib.sha512(str(random.random())).hexdigest()
        two = hashlib.sha512(str(random.random())).hexdigest()
        three = hashlib.sha512(str(random.random())).hexdigest()
        four = hashlib.sha512(str(random.random())).hexdigest()
        string = "".join([one, two, three, four])

        rs = self.execute("startswith", string=string, prefix=one)
        self.assertTrue(rs)
        rs = self.execute("startswith", string=string, prefix="ll" + one)
        self.assertFalse(rs)

        offset = len(one)
        rs = self.execute(
            "startswith", string=string, prefix=two, start=offset
        )
        self.assertTrue(rs)
        rs = self.execute(
            "startswith", string=string, prefix=two, start=offset + 1
        )
        self.assertFalse(rs)

        rs = self.execute(
            "startswith", string=string, prefix=two,
            start=offset, end=offset * 2
        )
        self.assertTrue(rs)
        rs = self.execute(
            "startswith", string=string, prefix=two,
            start=offset, end=offset * 2 - 1
        )
        self.assertFalse(rs)

    def test_endswith(self):
        one = hashlib.sha512(str(random.random())).hexdigest()
        two = hashlib.sha512(str(random.random())).hexdigest()
        three = hashlib.sha512(str(random.random())).hexdigest()
        four = hashlib.sha512(str(random.random())).hexdigest()
        string = "".join([one, two, three, four])

        rs = self.execute("endswith", string=string, suffix=four)
        self.assertTrue(rs)
        rs = self.execute("endswith", string=string, suffix=four + "lll")
        self.assertFalse(rs)

        offset = len(one) * 3
        rs = self.execute("endswith", string=string, suffix=four, start=offset)
        self.assertTrue(rs)
        rs = self.execute(
            "endswith", string=string, suffix=four, start=offset + 1
        )
        self.assertFalse(rs)

        offset = len(one) * 2
        rs = self.execute(
            "endswith", string=string, suffix=three,
            start=offset, end=offset + len(one)
        )
        self.assertTrue(rs)
        rs = self.execute(
            "endswith", string=string, suffix=three,
            start=offset, end=offset + len(one) + 1
        )
        self.assertFalse(rs)

    def test_istitle(self):
        string = "a" + hashlib.sha512(str(random.random())).hexdigest() + " a"
        rs = self.execute("istitle", string=string)
        self.assertFalse(rs)
        string = string.title() + " w"
        rs = self.execute("istitle", string=string)
        self.assertFalse(rs)
        string = string.title() + " X"
        rs = self.execute("istitle", string=string)
        self.assertTrue(rs)

    def test_isupper(self):
        string = "a" + hashlib.sha512(str(random.random())).hexdigest() + " a"
        rs = self.execute("isupper", string=string)
        self.assertFalse(rs)
        string = string.upper() + " w"
        rs = self.execute("isupper", string=string)
        self.assertFalse(rs)
        string = string.upper() + " X"
        rs = self.execute("isupper", string=string)
        self.assertTrue(rs)

    def test_isspace(self):
        rs = self.execute("isspace", string=" 1\t\n")
        self.assertFalse(rs)
        rs = self.execute("isspace", string=" \t\n")
        self.assertTrue(rs)

    def test_islower(self):
        string = "a" + hashlib.sha512(str(random.random())).hexdigest() + " a"
        rs = self.execute("islower", string=string)
        self.assertTrue(rs)
        string = string.lower() + " w"
        rs = self.execute("islower", string=string)
        self.assertTrue(rs)
        string = string.lower() + " X"
        rs = self.execute("islower", string=string)
        self.assertFalse(rs)

    def test_swapcase(self):
        string = "aBcDe"
        rs = self.execute("swapcase", string=string)
        self.assertEqual(rs, "AbCdE")

    def test_replace(self):
        string = hashlib.sha512(str(random.random())).hexdigest()
        to_replace = random.choice(string)
        to_count = string.count(to_replace)
        new = "X"

        orig = string.replace(to_replace, new)
        rs = self.execute("replace", string=string, old=to_replace, new=new)
        self.assertEqual(orig, rs)
        self.assertNotIn(to_replace, rs)
        self.assertEqual(rs.count(new), to_count)

        count = to_count - 1
        orig = string.replace(to_replace, new, count)
        rs = self.execute(
            "replace", string=string, old=to_replace, new=new, count=count
        )
        self.assertEqual(orig, rs)
        self.assertEqual(rs.count(new), count)

    def test_find(self):
        one = hashlib.sha512(str(random.random())).hexdigest()
        two = "XXX"
        three = hashlib.sha512(str(random.random())).hexdigest()
        four = "YYY"
        string = "".join([one, two, three, four])

        rs = self.execute("find", string=string, subs=two)
        self.assertEqual(rs, len(one))
        rs = self.execute("find", string=string, subs=four)
        self.assertEqual(rs, len(one) + len(two) + len(three))
        rs = self.execute("find", string=string, subs="WWW")
        self.assertEqual(rs, -1)

        rs = self.execute("find", string=string, subs=two, start=len(one) + 1)
        self.assertEqual(rs, -1)
        rs = self.execute("find", string=string, subs=four, start=len(one) + 1)
        self.assertEqual(rs, len(one) + len(two) + len(three))

        rs = self.execute(
            "find", string=string, subs=two,
            start=len(one), end=len(one) + len(two) + len(three)
        )
        self.assertEqual(rs, len(one))
        rs = self.execute(
            "find", string=string, subs=four,
            start=len(one), end=len(one) + len(two) + len(three)
        )
        self.assertEqual(rs, -1)

    def test_rfind(self):
        one = hashlib.sha512(str(random.random())).hexdigest()
        two = "XXX"
        three = hashlib.sha512(str(random.random())).hexdigest()
        four = "YYY"
        string = "".join([one, two, three, four])

        rs = self.execute("rfind", string=string, subs=two)
        self.assertEqual(rs, len(one))
        rs = self.execute("rfind", string=string, subs=four)
        self.assertEqual(rs, len(one) + len(two) + len(three))
        rs = self.execute("rfind", string=string, subs="WWW")
        self.assertEqual(rs, -1)

        rs = self.execute("rfind", string=string, subs=two, start=len(one) + 1)
        self.assertEqual(rs, -1)
        rs = self.execute(
            "rfind", string=string, subs=four, start=len(one) + 1
        )
        self.assertEqual(rs, len(one) + len(two) + len(three))

        rs = self.execute(
            "rfind", string=string, subs=two,
            start=len(one), end=len(one) + len(two) + len(three)
        )
        self.assertEqual(rs, len(one))
        rs = self.execute(
            "rfind", string=string, subs=four,
            start=len(one), end=len(one) + len(two) + len(three)
        )
        self.assertEqual(rs, -1)

    @unittest.skipUnless(core.MOCK, "require mock")
    def test_kmeans(self):
        envs = tuple(self.nw.environments(["native", "place"]))

        orig = kmeans.kmeans(self.nw, envs=envs, k_or_guess=2)
        rs = self.execute("kmeans", envs=envs, k_or_guess=2)

        self.assertEquals(orig[0], rs[0])
        self.assertEquals(orig[1], rs[1])

        coords = {}

        def coordc(nw, env):
            arr = stats.env2weightarray(nw, env)
            if len(arr):
                coords[env] = [stats.average(arr), stats.std(arr)]
            else:
                coords[env] = [-1, -1]
            return coords[env]

        orig = kmeans.kmeans(
            self.nw, envs=envs, k_or_guess=2, coordc=coordc
        )
        rs = self.execute("kmeans", envs=envs, coords=coords, k_or_guess=2)
        self.assertEquals(orig[0], rs[0])
        self.assertEquals(orig[1], rs[1])


#==============================================================================
# QBJ
#==============================================================================

class QBJEngineTest(core.YatelTestCase):

    def setUp(self):
        super(QBJEngineTest, self).setUp()
        self.qbj = qbj.QBJEngine(self.nw)

    def execute(self, query):
        rs = self.qbj.execute(query, True)
        if rs["error"]:
            full_fail = "".join([rs["error_msg"], rs["stack_trace"]])
            self.fail(full_fail)
        return rs

    def test_describe(self):
        query = {"id": 1, "function": {"name": 'describe'}}

        orig = self.nw.describe()
        orig = typeconv.parse(typeconv.simplifier(orig))
        rs = typeconv.parse(self.execute(query)["result"])
        self.assertEqual(orig, rs)

    def test_change_nw(self):
        query = {"id": 1, "function": {"name": 'average'}}

        orig = stats.average(self.nw)
        orig = typeconv.parse(typeconv.simplifier(orig))
        rs = typeconv.parse(self.execute(query)["result"])
        self.assertAlmostEqual(orig, rs, places=4)

        nw = [random.randint(1, 1000) + r for r in self.rrange(100, 200)]
        query = {
            "id": 1,
            "function": {
                "name": 'average',
                "kwargs": {
                    "nw": {"type": 'literal', "value": nw}
                }
            }
        }
        orig = stats.average(nw)
        orig = typeconv.parse(typeconv.simplifier(orig))
        rs = typeconv.parse(self.execute(query)["result"])
        self.assertAlmostEqual(orig, rs, places=4)

    def test_haplotype_by_id_with_slice(self):
        query = {
            "id": 1545454845,
            "function": {
                "name": 'haplotype_by_id',
                "args": [
                    {
                        "type": 'unicode',
                        "function": {
                            "name": 'slice',
                            "kwargs": {
                                "iterable": {
                                    "type": 'unicode', "value": 'id_01_'
                                },
                                "f": {"type": 'int', "value": '-3'},
                                "t": {"type": 'int', "value": '-1'}
                            }
                        }
                    }
                ]
            }
        }
        orig = self.nw.haplotype_by_id("01")
        orig = typeconv.parse(typeconv.simplifier(orig))
        rs = typeconv.parse(self.execute(query)["result"])
        self.assertEqual(orig, rs)

    def test_haplotype_by_id(self):
        hap_id = random.choice(self.haps_ids)
        query = {
            "id": None,
            "function": {
                "name": 'haplotype_by_id',
                "args": [
                    {
                        "type": 'literal',
                        "value": hap_id
                    }
                ]
            }
        }
        orig = self.nw.haplotype_by_id(hap_id)
        orig = typeconv.parse(typeconv.simplifier(orig))
        rs = typeconv.parse(self.execute(query)["result"])
        self.assertEqual(orig, rs)

    def test_sum(self):
        s0 = random.randint(1, 1000)
        s1 = random.randint(1, 1000)
        query = {
            "id": 'someid',
            "function": {
                "name": 'sum',
                "kwargs": {
                    "nw": {
                        "type": 'list',
                        "value": [
                            {"type": 'literal', "value": s0},
                            {"type": 'int', "value": str(s1)}
                        ]
                    }
                }
            }
        }
        rs = typeconv.parse(self.execute(query)["result"])
        self.assertEqual(s0+s1, rs)

    @unittest.skipUnless(core.MOCK, "require mock")
    def test_kmeans(self):
        envs = tuple(self.nw.environments(["native", "place"]))
        query = {
            "id": 1,
            "function": {
                "name": 'kmeans',
                "args": [
                    {"type": 'literal', "value": envs},
                    {"type": 'literal', "value": 2}
                ]
            }
        }
        orig = kmeans.kmeans(self.nw, envs=envs, k_or_guess=2)
        orig = typeconv.parse(typeconv.simplifier(orig))
        rs = typeconv.parse(self.execute(query)["result"])
        self.assertEquals(orig[0], rs[0])
        self.assertEquals(orig[1], rs[1])

        coords = {}

        def coordc(nw, env):
            arr = stats.env2weightarray(nw, env)
            if len(arr):
                coords[env] = [stats.average(arr), stats.std(arr)]
            else:
                coords[env] = [-1, -1]
            return coords[env]

        query = {
            "id": 1,
            "function": {
                "name": 'kmeans',
                "kwargs": {
                    "envs": {"type": 'literal', "value": envs},
                    "k_or_guess": {"type": 'literal', "value": 2},
                    "coords": {"type": 'literal', "value": coords}
                }
            }
        }

        orig = kmeans.kmeans(self.nw, envs=envs, k_or_guess=2, coordc=coordc)
        orig = typeconv.parse(typeconv.simplifier(orig))
        rs = typeconv.parse(self.execute(query)["result"])
        self.assertEquals(orig[0], rs[0])
        self.assertEquals(orig[1], rs[1])


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
