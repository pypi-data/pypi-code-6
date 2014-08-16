# -*- coding: utf-8 -*-

import operator


class Stack(object):

    def __init__(self):
        self.stack = []

    @classmethod
    def push(cls, item):
        cls.stack.append(item)

    @classmethod
    def pop(cls):
        return cls.stack.pop()

    @classmethod
    def set(cls, stack):
        if not isinstance(stack, list):
            raise Exception('Required list')
        cls.stack = stack

    @classmethod
    def get(cls):
        return cls.stack

    @classmethod
    def isEmpty(cls):
        return False if cls.stack else True

    @classmethod
    def first(cls):
        if cls.isEmpty():
            raise Exception('Stack is empty')
        return cls.stack[0]

    @classmethod
    def last(cls):
        if cls.isEmpty():
            raise Exception('Stack is empty')
        return cls.stack[-1]

    @classmethod
    def clear(cls):
        cls.stack = []

    @classmethod
    def _sort_str(cls, key=None, reverse=False):
        cls.stack = sorted(cls.stack, key=str.lower, reverse=reverse)

    @classmethod
    def _sort_int(cls, key=None, reverse=False):
        cls.stack = sorted(cls.stack, reverse=reverse)

    @classmethod
    def _sort_tuple(cls, key, reverse=False):
        cls.stack = sorted(
            cls.stack, key=lambda item: item[key], reverse=reverse
        )

    @classmethod
    def _sort_dict(cls, key, reverse=False):
        cls.stack = sorted(
            cls.stack, key=operator.itemgetter(key), reverse=reverse
        )

    @classmethod
    def check_data_types(cls):
        items_types = set([type(item) for item in cls.stack])

        if len(items_types) > 1:
            raise Exception('All items must be the same type')

        return items_types.pop()

    @classmethod
    def sort(cls, key=None, reverse=False):
        if cls.isEmpty():
            raise Exception('Stack is empty')

        data_type = cls.check_data_types().__name__

        try:
            sort_by_type = getattr(Stack, '_sort_{}'.format(data_type))
        except AttributeError:
            raise Exception('Unsupported type: {}'.format(data_type))

        sort_by_type(key, reverse)
