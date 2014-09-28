# -*- coding: utf-8 -*-
from yxpy import yamlfile

def test_include_document():
    d = yamlfile.load('test/data/yamlfile/main.yaml')
    assert d['name'] == 'main'
    assert d['a']['name'] == 'a'
    assert d['a']['aa']['name'] == 'aa'

def test_include_node():
    d = yamlfile.load('test/data/yamlfile/main.yaml')
    assert d['aa_name'] == 'aa'
    print(d)
