from decimal import Decimal

from django import template

register = template.Library()


def number(value):
    """
    Convert different values to their numbers.
    :param value: a single value.
    :return: single value converted to number.
    :rtype: int or long or float.
    :raises: py:class:`ValueError`
    """
    if isinstance(value, (int, long, float, Decimal)):
        return value
    try:
        return int(value)
    except ValueError:
        return float(value)


def make_sure(func):
    """
    Returns an empty string in any error is raised.
    :param func: a function
    :return: If no exception is raised, `func` result. Otherwise, an empty string.
    """

    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return ''

    return func_wrapper


@make_sure
def absolute_value(obj):
    """
    Return the absolute value of `obj`.
    :param obj: first argument.
    :return: the absolute value of `obj`.
    """
    from __builtin__ import abs

    return abs(number(obj))


@register.filter(name='abs')
def abs(obj):
    return absolute_value(obj)


@make_sure
def division(a, b):
    """
    Return `a / b`, for `a` and `b` numbers.
    :param a: first argument.
    :param b: second argument.
    :return: `a / b`
    """
    return number(a) / number(b)


@register.filter(name='div')
def div(a, b):
    return division(a, b)


@make_sure
def exponentiation(a, b):
    """
    Return `a` raised to the power `b`.
    :param a: first argument.
    :param b: second argument.
    :return: `pow(a, b)`
    """
    from __builtin__ import pow

    return pow(number(a), number(b))


@register.filter(name='pow')
def pow(a, b):
    return exponentiation(a, b)


@make_sure
def floor_division(a, b):
    """
    Return `a // b`, for `a` and `b` numbers.
    :param a: first argument.
    :param b: second argument.
    :return: `a // b`
    """
    return number(a) // number(b)


@register.filter(name='floordiv')
def floordiv(a, b):
    return floor_division(a, b)


@make_sure
def modulo(a, b):
    """
    Return `a % b`, for `a` and `b` numbers.
    :param a: first argument.
    :param b: second argument.
    :return: `a % b`
    """
    return number(a) % number(b)


@register.filter(name='mod')
def mod(a, b):
    return modulo(a, b)


@make_sure
def multiplication(a, b):
    """
    Return `a * b`, for `a` and `b` numbers.
    :param a: first argument.
    :param b: second argument.
    :return: `a * b`
    """
    return number(a) * number(b)


@register.filter(name='mul')
def mul(a, b):
    return multiplication(a, b)


@make_sure
def square_root(a):
    """
    Return the square root of `a`.
    :param a: first argument.
    :return: `sqrt(a)`
    """
    from math import sqrt

    return sqrt(number(a))


@register.filter(name='sqrt')
def sqrt(a):
    return square_root(a)


@make_sure
def subtraction(a, b):
    """
    Return `a - b`, for `a` and `b` numbers.
    :param a: first argument.
    :param b: second argument.
    :return: `a - b`
    """
    return number(a) - number(b)


@register.filter(name='sub')
def sub(a, b):
    return subtraction(a, b)