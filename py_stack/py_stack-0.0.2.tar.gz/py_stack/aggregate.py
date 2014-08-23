# -*- coding: utf-8 -*-

import itertools

from py_stack.stack import Stack


class Aggregate(Stack):

    @classmethod
    def _replace(cls, field, item, stack_item, replace_field=None):
        if not replace_field and not field in item.keys() or not item[field]:
            item[field] = stack_item[field]
        elif replace_field in item.keys():
            item[field] = stack_item[field]
        elif type(item.get(field)).__name__ == 'dict':
            old_value = item[field].copy()
            for key, value in stack_item[field].items():
                if not key in old_value.keys():
                    old_value[key] = value
            item[field] = old_value
        elif type(item.get(field)).__name__ == 'list':
            item[field] = list(
                set(itertools.chain(item[field], stack_item[field]))
            )
        return item

    @classmethod
    def _update_item(cls, key, merged_data, stack_item):
        for item in merged_data:
            if item.get(key) != stack_item.get(key):
                continue
            fields_list = itertools.chain(item.keys(), stack_item.keys())
            for field in fields_list:
                cls._replace(field, item, stack_item)
            break
        return item

    @classmethod
    def _add_or_update(cls, key, merged_data, stack_item):
        merged_data_key_values = [item.get(key) for item in merged_data]

        if stack_item.get(key) in merged_data_key_values:
            cls._update_item(key, merged_data, stack_item)
        else:
            merged_data.append(stack_item)
        return merged_data

    @classmethod
    def merge(cls, key, replace_field=None):
        if not isinstance(cls.first(), dict):
            raise Exception('Required list of dicts')
        merged_data = []

        while cls.stack:
            stack_item = cls.stack.pop()
            merged_data = cls._add_or_update(key, merged_data, stack_item)
        Stack.set(merged_data)
        Stack.sort(key='id')
        return Stack.get()
