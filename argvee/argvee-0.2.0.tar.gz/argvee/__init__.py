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

    def cmd(self, name=None):
        ''' Return a decorator which reads func args and kwargs '''
        funcname = name
        def open_func(func):
            if funcname is None:
                name = func.func_name
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
            self.subs[name] = sub
            return func
        return open_func

    def parse_args(self):
        args = self.parser.parse_args()
        if len(self.subs) == 1 and 'main' in self.subs:
            cmd = 'main'
        else:
            cmd = args.cmd
        sub = self.subs[cmd]
        func = sub['func']
        func(
            *[getattr(args, attr) for attr in sub['args']],
            **{
                kwarg: getattr(args, kwarg)
                for kwarg in sub['kwargs']
            }
        )

    def run(self):
        ''' Build parsers and get args '''
        if len(self.subs) == 0:
            return
        # Maps name of command to metadata
        parser_map = {}
        if len(self.subs) == 1 and 'main' in self.subs:
            # add arguments to ArgumentParser for main function
            parser_map['main'] = self.parser
        else:
            subparsers = self.parser.add_subparsers(dest='cmd')
            # create sub parsers
            for sub in self.subs:
                parser_map[sub] = subparsers.add_parser(
                    sub, help=self.subs[sub]['help'])

        # Build subparser arguments
        for sub, parser in parser_map.items():
            sub_d = self.subs[sub]
            for arg in sub_d['args']:
                parser.add_argument(arg)
            shortnames = set()
            for kwarg, default in sub_d['kwargs'].items():
                kwarg_name = '--%s' % kwarg.replace('_', '-')
                short = '-%s' % kwarg[0]
                if short in shortnames:
                    short = short.swapcase()
                if short in shortnames:
                    kwargs = [kwarg_name]
                else:
                    kwargs = [kwarg_name, short]
                    shortnames.add(short)

                if default is True:
                    parser.add_argument(*kwargs, action='store_false')
                elif default is False:
                    parser.add_argument(*kwargs, action='store_true')
                else:
                    parser.add_argument(*kwargs, default=default)
        self.parse_args()

