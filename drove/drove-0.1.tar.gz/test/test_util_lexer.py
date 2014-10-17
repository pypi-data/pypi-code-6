#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from drove.util.lexer import Lexer


def test_lexer():
    """Testing util.lexer.Lexer: basic behaviour"""
    x = Lexer()
    items = [i for i in x.parse("item1 arg1, item2 arg2.")]
    for item in items:
        assert item.__class__.__name__ == "LexerItem"

    assert [y.item for y in items] == ["arg1", "arg2"]


def test_lexer_without_term():
    """Testing util.lexer.Lexer: without terminator"""
    x = Lexer()
    items = [i for i in x.parse("item1 arg1, item2 arg2")]
    for item in items:
        assert item.__class__.__name__ == "LexerItem"

    assert [y.item for y in items] == ["arg1", "arg2"]


class ExampleItem(object):
    def __init__(self, arg):
        self.item = "example"
        pass


def test_lexer_add_parser():
    """Testing util.lexer.Lexer: addItemParser()"""
    x = Lexer()
    x.addItemParser("item1", ExampleItem)

    items = [i for i in x.parse("item1 arg1, item2 arg2")]
    assert [y.__class__.__name__ for y in items] == \
        ["ExampleItem", "LexerItem"]

    assert [y.item for y in items] == ["example", "arg2"]


def test_lexer_ignore_words():
    """Testing util.lexer.Lexer: addItemParser() with ignore_words"""
    x = Lexer()
    x.addItemParser("item1", ExampleItem, ignore_words=["ignore"])

    items = [i for i in x.parse("item1 ignore arg1.")]
    assert [y.__class__.__name__ for y in items] == ["ExampleItem"]

    items = [i for i in x.parse("item1 arg1 ignore.")]
    assert [y.__class__.__name__ for y in items] == ["ExampleItem"]
