#!/usr/bin/env python
import cmd
import csv
import json
from StringIO import StringIO
from inspect import isfunction, getdoc, getargspec

class ShellError(ValueError):
    pass

def inspect_func(func):
    ''' Return info about all arguments '''
    argspec = getargspec(func)
    len_args = 0 if argspec.args is None else len(argspec.args)
    len_kwargs = 0 if argspec.defaults is None else len(argspec.defaults)
    split = len_args - len_kwargs
    f_args = argspec.args[:split]
    f_kwargs_ids = argspec.args[split:]
    f_varargs = argspec.varargs
    f_kwargs = {}
    for i, arg in enumerate(f_kwargs_ids):
        f_kwargs[arg] = argspec.defaults[i]
    return f_args, f_kwargs, f_varargs

def hungarian_value(name, value):
    ''' Convert value to a type if name is hungarian notation '''
    if name.endswith('_i') or name.endswith('_n'):
        return int(value)
    elif name.endswith('_f'):
        return float(value)
    elif name.endswith('_b'):
        if value.lower().strip() in [
            'false', '0', 'none', 'null', 'nil', 'no'
        ]:
            return False
        else:
            return True
    else:
        return value

def exec_csv_command(func, cargs):
    ''' Execute function with csv styled list `cargs` '''
    f_args, f_kwargs, f_varargs = inspect_func(func)
    if len(cargs) < len(f_args):
        raise ShellError('Requires more arguments: %s %s' % (
            func.func_name,
                ','.join(f_args),
            )
        )
    if not cargs:
        return func(**f_kwargs)
    args = []
    kwargs = f_kwargs.copy()
    queue = cargs[:]
    for name in f_args:
        try:
            args += [hungarian_value(name, queue[0])]
        except ValueError:
            raise ShellError('Arguments with _i,_n,_f are typed: %s %s' % (
                func.func_name,
                    ','.join(f_args),
                )
            )
            return
        queue = queue[1:]
    for kwarg in queue:
        spl = kwarg.split('=')
        if len(spl) != 2:
            raise ShellError(
                'please specify remaining arguments with key=value')
        name, val = spl
        try:
            kwargs[name] = hungarian_value(name, val)
        except ValueError:
            raise ShellError('Arguments with _i,_n,_f are typed: %s %s' % (
                func.func_name,
                    ','.join(f_args),
                )
            )
            return
    return func(*args, **kwargs)

def exec_json_command(func, jargs):
    ''' Execute function with json style args args*,{} in `jargs` '''
    f_args, f_kwargs, f_varargs = inspect_func(func)
    if not jargs:
        return func(**f_kwargs)
    if f_kwargs and isinstance(jargs[-1], dict):
        kwargs = jargs[-1]
        args = jargs[:-1]
    else:
        kwargs = {}
        args = jargs
    return func(*args, **kwargs)

def generate_command(func, delimiter=',', quotechar='"', json_type=False):
    ''' Generate a function which can call the original with the correct args
    '''
    json_cmd = json_type
    delim = delimiter
    qchar = quotechar
    def command_func(self, arg):
        if json_cmd:
            try:
                jargs = json.loads('[' + arg + ']')
            except ValueError as e:
                print(str(e))
                print('Please specify arguments as: '
                    'func $arg1, $arg2, {"kwarg1": value1, ...}'
                )
                return
            try:
                exec_json_command(func, jargs)
            except ShellError as e:
                print(str(e))
            except TypeError as e:
                print(str(e))
        else:
            arg_parser = csv.reader(StringIO(arg),
                delimiter=delim, quotechar=qchar
            )
            try:
                cargs = arg_parser.next()
            except StopIteration:
                cargs = []
            try:
                exec_csv_command(func, cargs)
            except ShellError as e:
                print(str(e))
            except TypeError as e:
                print(str(e))
    command_func.__doc__ = getdoc(func)
    return command_func

def generate_shell(mod_name, version, funcs):
    ''' Generate the shell class to run '''
    attrs = {
        'prompt': '> ',
        'intro': '%s v%s' % (mod_name, version),
    }
    for func_name, cmd_func in funcs.items():
        attrs['do_%s' % func_name] = cmd_func
    return type(
        'GeneratedShell',
        (cmd.Cmd, object),
        attrs,
    )

class Shell(object):
    ''' Generate a shell from functions '''
    
    def __init__(self, name='Shell', version='1'):
        self.name = name
        self.version = version
        self.funcs = {}
        self.shell_class = None
        self.shell = None

    def cmd(self, *args, **kwargs):
        ''' Save shell command to self.funcs
        The shell command takes (self, arg), but arg will be split up
        appropriately.
        '''
        if args and isfunction(args[0]):        
            return self.cmd(name=args[0].func_name)(args[0])                    
        elif args and isinstance(args[0], basestring):                          
            funcname = args[0]                                                  
        else:                                                                   
            funcname = kwargs.get('name')
        delimiter = kwargs.get('delimiter', ',')
        quotechar = kwargs.get('quotechar', '"')
        json_type = kwargs.get('json', False)
        def cmd_func(func):
            name = funcname or func.func_name
            self.funcs[name] = generate_command(
                func, 
                delimiter=delimiter, 
                quotechar=quotechar,
                json_type=json_type,
            )
            return func
        return cmd_func

    def json(self, *args, **kwargs):
        ''' Save shell command to self.funcs
        The shell command takes (self, arg), but arg will be split up
        appropriately.
        '''
        if args and isfunction(args[0]):        
            return self.json(name=args[0].func_name)(args[0])                    
        elif args and isinstance(args[0], basestring):                          
            funcname = args[0]                                                  
        else:                                                                   
            funcname = kwargs.get('name')
        json_type=True
        def cmd_func(func):
            name = funcname or func.func_name
            self.funcs[name] = generate_command(
                func, 
                json_type=json_type,
            )
            return func
        return cmd_func

    def run(self):
        ''' Build and run shell '''
        self.shell_class = generate_shell(self.name, self.version, self.funcs)
        self.shell = self.shell_class()
        self.shell.cmdloop()

