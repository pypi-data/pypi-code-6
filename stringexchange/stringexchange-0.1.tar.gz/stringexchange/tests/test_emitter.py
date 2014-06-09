# -*- coding:utf-8 -*-
def _getTarget():
    from stringexchange import make_exchange
    return make_exchange


def _makeOne(*args, **kwargs):
    return _getTarget()(*args, **kwargs)


def test_it():
    from stringexchange import join_emitter

    target = _makeOne(join_emitter)
    xs = [target.subscribe("xxx"), "hello", "this is", target.subscribe("xxx"), "www"]

    publisher = target.publisher("xxx")
    publisher.publish("@.@")
    content = "".join(xs)

    result = target.emit(content)
    assert result == "@.@hellothis is@.@www"


def test_funcall():
    from stringexchange import function_call_emitter, stripped_iterator

    target = _makeOne(function_call_emitter, stripped_iterator)
    fmt = """f(x, {}, y, z)""".format(target.subscribe("args"))

    publisher = target.publisher("args")
    publisher.publish("a")
    publisher.publish("b\n")
    publisher.publish("c\n")

    result = target.emit(fmt)

    assert result == "f(x, a, b, c, y, z)"

