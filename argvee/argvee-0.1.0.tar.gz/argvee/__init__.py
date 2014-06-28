#!/usr/bin/env python
import argparse
import inspect

class Application(object):
    ''' Contains all registered functions '''

    def __init__(self):
        ''' Create initial application empty state '''
        self.subs = {}
        self.funcs = {}
        self.parser = argparse.ArgumentParser()

    def cmd(self):
        ''' Return a decorator which reads func args and kwargs '''
        def open_func(func):
            sub = {}
            sub['help'] = inspect.getdoc(func)
            argspec = inspect.getargspec(func)
            len_args = 0 if argspec.args is None else len(argspec.args)
            len_kwargs = 0 if argspec.defaults is None else len(argspec.defaults)
            split = len_args - len_kwargs
            sub['args'] = argspec.args[:split]
            sub['kwargs'] = {}
            kwargs = argspec.args[split:]
            for i, arg in enumerate(kwargs):
                sub['kwargs'][arg] = argspec.defaults[i]
            sub['func'] = func
            self.subs[func.func_name] = sub
            return func
        return open_func

    def run(self):
        subparsers = self.parser.add_subparsers(dest='cmd')
        parser_map = {}
        for sub in self.subs:
            parser_map[sub] = subparsers.add_parser(
                sub, help=self.subs[sub]['help'])
        for sub, parser in parser_map.items():
            sub_d = self.subs[sub]
            for arg in sub_d['args']:
                parser.add_argument(arg)
            for kwarg, default in sub_d['kwargs'].items():
                kwarg_name = '--%s' % kwarg.replace('_', '-')
                if default is True:
                    parser.add_argument(kwarg_name, action='store_false')
                elif default is False:
                    parser.add_argument(kwarg_name, action='store_true')
                else:
                    parser.add_argument(kwarg_name, default=default)
        args = self.parser.parse_args()
        sub = self.subs[args.cmd]
        func = sub['func']
        func(
            *[getattr(args, attr) for attr in sub['args']],
            **{
                kwarg: getattr(args, kwarg)
                for kwarg in sub['kwargs']
            }
        )

