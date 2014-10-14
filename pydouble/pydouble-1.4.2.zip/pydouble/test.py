#!/usr/bin/env python
# -*- coding: utf-8 -*-

from job import Duplicate


def test_hash():
    d = Duplicate(source=".", destination="", extension="", typehash="sha1")
    m = "11CB722298C5535ABEA111C650308969A38492BC"
    assert d.hashf("iconapp.png", "sha1") == m
