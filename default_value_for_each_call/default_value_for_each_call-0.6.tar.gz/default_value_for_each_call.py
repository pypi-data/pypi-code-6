#!/usr/bin/env python
# coding=utf-8
__author__ = 'chenfengyuan'

import inspect
import ast
import re


def compute_default_value_for_each_call(func):
    """Return a function whose default values will be computed for each call,
    instead of evaluating the default values when function definition is executed.

    make sure this function is the last(closest to the function) decorator
    Usage:
    @default_value_for_each_call.compute_default_value_for_each_call
    def foo(a=([])):
        a.append(3)
        print a

    foo()
    foo()

    Output:
    [3]
    [3]"""
    source = inspect.getsource(func)
    m = re.search(r'^\s+', source)
    if m:
        m.group(0)
        n = len(m.group(0))
        lines = [line[n:] for line in str.splitlines(source)]
        source = '\n'.join(lines)
    root = ast.parse(source)
    arg_names = [arg.id for arg in root.body[0].args.args]
    default_nodes = root.body[0].args.defaults
    arg_names = arg_names[len(arg_names) - len(default_nodes):]
    body = root.body[0].body
    n = len(arg_names)
    for i in reversed(range(n)):
        arg_name = arg_names[i]
        default_node = default_nodes[i]
        lineno = default_node.lineno
        col_offset = default_node.col_offset
        body.insert(0, ast.Assign(targets=[ast.Name(id=arg_name, ctx=ast.Store(),
                                                    lineno=lineno, col_offset=col_offset)],
                                  value=ast.BoolOp(op=ast.Or(), lineno=lineno, col_offset=col_offset,
                                                   values=[ast.Name(id=arg_name, ctx=ast.Load(), lineno=lineno,
                                                                    col_offset=col_offset),
                                                           default_node]),
                                  lineno=lineno, col_offset=col_offset))
    root.body[0].args.defaults = [ast.Name(id='None', ctx=ast.Load(), lineno=old.lineno, col_offset=old.col_offset)
                                  for old in default_nodes]
    root.body[0].body = body
    root.body[0].decorator_list.pop()
    l = {}
    exec compile(root, '<string>', mode='exec') in globals(), l
    func = l[func.__name__]
    return func
