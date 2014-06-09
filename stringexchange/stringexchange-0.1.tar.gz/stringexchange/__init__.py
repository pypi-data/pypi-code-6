# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from zope.interface import provider
import hashlib
from collections import defaultdict

from .compat import text_
from .interfaces import (
    IEmitter,
    IContentsIterator
)


class Gensym(object):
    def __init__(self, i=0):
        self.i = i

    def __call__(self):
        v = "g!{}".format(hashlib.sha1(bytes(self.i)).hexdigest())
        self. i += 1
        return v


@provider(IEmitter)
def join_emitter(hashval, xs, string):
    return string.replace(hashval, "".join(xs))


@provider(IEmitter)
def function_call_emitter(hashval, xs, string):
    return string.replace(hashval, ", ".join(xs))


@provider(IEmitter)
def newline_join_emitter(hashval, xs, string):
    return string.replace(hashval, "\n".join(xs))


@provider(IContentsIterator)
def identity_iterator(xs):
    return xs


@provider(IContentsIterator)
def stripped_iterator(xs):
    return (x.strip() for x in xs)


@provider(IContentsIterator)
def remove_duplicate_iterator(xs):
    D = {}
    for x in stripped_iterator(xs):
        if x in D:
            continue
        D[x] = 1
        yield x


class EmitterFactory(object):
    def __init__(self, request):
        self.request = request

    def __call__(self, name):
        q = self.request.registry.getUtility
        return q(IEmitter, name=name)


class ContentsIteratorFactory(object):
    def __init__(self, request):
        self.request = request

    def __call__(self, name):
        q = self.request.registry.getUtility
        return q(IContentsIterator, name=name)


def default_emiter_factory(name):
    return join_emitter


def default_iterator_factory(name):
    return identity_iterator


def make_exchange(emitter, iterator=identity_iterator):
    return StringExchange(lambda name: emitter, lambda name: iterator)


class StringExchange(object):
    def __init__(self,
                 emitter_factory=default_emiter_factory,
                 iterator_factory=default_iterator_factory):
        self.emitter_factory = emitter_factory
        self.iterator_factory = iterator_factory
        self.hash_map = {}
        self.contents_map = defaultdict(list)
        self.gensym = Gensym()
        self.publishers = {}
        self.emit_name_map = {}
        self.iterator_name_map = {}

    def subscribe(self, k, emit="", iterator=""):
        try:
            return self.hash_map[k]
        except KeyError:
            v = self.hash_map[k] = self.gensym()
            setattr(self, k, v)
            self.emit_name_map[k] = emit
            self.iterator_name_map[k] = iterator
            return v

    def emit(self, string):
        for k in self.hash_map:
            hash_val = self.hash_map[k]
            contents = self.contents_map[k]
            emitter = self.emitter_factory(self.emit_name_map[k])
            iterator = self.iterator_factory(self.iterator_name_map[k])
            string = emitter(hash_val, iterator(contents), string)
        return string

    def publisher(self, k):
        try:
            return self.publishers[k]
        except KeyError:
            p = self.publishers[k] = Publisher(self.contents_map, k)
            return p

    def talk(self, k, message):
        self.contents_map[k].append(message)


class Publisher(object):
    def __init__(self, strings, k):
        self.buf = strings[k]
        self.k = k

    def publish(self, message):
        return self.buf.append(message)


empty = text_("")


class StringExchangeTweenFactory(object):
    def __init__(self, handler, setting):
        self.handler = handler

    def __call__(self, request):
        response = self.handler(request)
        if response.status_int != 200:
            return response

        if not (response.content_type and
                response.content_type.lower() in ['text/html', 'text/xml']):
            return response

        response_text = response.text
        response.text = empty
        response.write(request.string_exchange.emit(response_text))
        return response


def get_string_exchange(request):
    return StringExchange(EmitterFactory(request), ContentsIteratorFactory(request))


def add_emitter(config, emitter, name=""):
    config.registry.registerUtility(emitter, IEmitter, name=name)


def add_contents_iterator(config, contents_iterator, name=""):
    config.registry.registerUtility(contents_iterator, IContentsIterator, name=name)


def includeme(config):
    config.add_tween("stringexchange.StringExchangeTweenFactory")
    config.add_request_method(get_string_exchange, "string_exchange", reify=True)
    config.add_directive("add_emitter", add_emitter)
    config.add_directive("add_contents_iterator", add_contents_iterator)

    config.add_emitter(join_emitter)
    config.add_emitter(function_call_emitter, "call")
    config.add_emitter(newline_join_emitter, "newline")

    config.add_contents_iterator(identity_iterator)
    config.add_contents_iterator(stripped_iterator, "stripped")
    config.add_contents_iterator(remove_duplicate_iterator, "unique")
