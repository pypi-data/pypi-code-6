#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import importlib
import sys, re
import os, subprocess
from pipes import quote
from collections import defaultdict

from serialize import (
  from_yaml, from_json,
  to_json, from_jsonlines,
  to_jsonlines
  )
from exceptions import GnuTaskInitError, GnuTaskIOError

from collections import OrderedDict

re_not_int = re.compile(r'[^0-9]+')
re_not_float = re.compile(r'[^0-9\.]+')

RM_ARGS = [
  'kwargs',
  'func'
]

DEFAULT_ARGS = [
  'passthrough',
  'queue_size',
  'subprocess',
  'add',
  'quiet'
]

def read_stdin():
  """
  Read from stdin, parse json, 
  yield objects
  """
  try:
    lines = sys.stdin.readlines()
  except IOError:
    raise GnuTaskIOError(
      'If no arg is prsent, the task assumes input from stdin.'
      )
  else:
    for l in lines:
      if l.strip() != '':
        yield from_json(l)


def write_stdout(obj, lines=True):
  """
  Write jsonlines to stdout
  """
  line = to_json(obj)
  if lines:
    line += "\n"
  sys.stdout.write(line)


def write_stderr(e):
  """
  Write Errors to stderr
  """
  sys.stderr.write(e)


def read_positional_kwargs(kw):
  """
  Read postiional kwargs, 
  parse json, yield objects
  """
  for k in kw.split('\\n'):
    if k.strip() != '':
      yield from_json(k)


def process_kwargs(kw):

  if kw:
    
    # YAML #
    if kw.lower().endswith('.yml') or \
         kw.lower().endswith('.yaml'):
      
      # load and listify
      d = from_yaml(open(kw).read())
      return listify(d)

    # JSON #
    elif kw.lower().endswith('.json'):

      # load and listify
      d = from_json(open(kw).read())
      return listify(d)

    # JSONLINES #
    elif kw.lower().endswith('.jsonlines'):
      
      # load and listify
      return list(from_jsonlines(open(kw).read()))

    # otherwise assume positional kwargs
    else:
      return list(from_jsonlines(kw))

def exec_func(func_path):
  """
  call a python function by it's absolute path
  """
  def _run(kw, args, sub):
    command = ['python', func_path]
    
    # if we passed in json kwargs, append them to 
    # the function call
    if kw:

      kw = to_jsonlines(kw)
      command.append("'{}'".format(kw))
    
    # if we passed in args, add those too.
    if args:
      command.extend(args)

    # run subprocess
    if sub:
      subprocess.Popen(command)

    # run system process
    else:
      os.system(" ".join(command))

  return _run


def slug_path(func_path):
  """
  Prettify a path.
  """
  return func_path.split('.')[0].replace('_', '-').lower().strip()


def parse_task_tree(task_path):
  """
  Parse the task(s) directory for paths, filenames, and yaml-definitions.
  """ 
  
  # tree structure
  tree = defaultdict(lambda : defaultdict())

  # walk through task_path
  for dir_name, dir_list, file_list in os.walk(task_path.encode('utf-8')):

    # copy over files, optionally applying templating
    for filename in file_list:
      
      # Skip DS_Store, .pyc, __init__.py 
      # and any util files for tasks.
      if 'DS_Store' in filename \
          or '.pyc' in filename \
          or filename == "__init__.py" \
          or filename == "util.py":
        continue

      # parse directory / filnename 
      path = os.path.join(dir_name, filename)
      parts = path.split('/')
      group = slug_path(parts[-2])
      task = slug_path(parts[-1])
      cmd = "%s-%s" % (group, task)

      # if it's a yml file, its the cmd's config
      if filename.endswith('.yml'):
        tree[cmd]['config'] = from_yaml(open(path).read())

      # otherwise it's the cmd's path
      else:
        tree[cmd]['path'] = path 

  # order tasks by name.
  return OrderedDict(sorted(tree.items(), key=lambda t: t[0]))


def listify(d):
  """
  Turn dicts to single-element lists
  """
  if isinstance(d, list):
    return d 
  
  elif isinstance(d, dict):
    return [d]


def is_int(arg):
  if re_not_int.search(arg):
    return False
  else:
    return True

def is_float(arg):
  if re_not_float.search(arg):
    return False
  else:
    return True

def parse_arg(arg):
  if isinstance(arg, str): 
    if arg.lower() in ['true','t']:
      return True 
    elif arg.lower() in ['false', 'f']:
      return False
    elif arg.lower() in ["null", "none"]:
      return None
    elif is_int(arg):
      return int(arg)
    elif is_float(arg):
      return float(arg)
  return arg


def opts_to_kwargs(opts):
  exclude = RM_ARGS + DEFAULT_ARGS
  kwargs = {}
  for k,v in opts.__dict__.items():
    if k not in exclude:
      kwargs[k] = parse_arg(v)
  return kwargs  


def opts_to_args(opts):
  args = []
  for k,v in opts.__dict__.items():
    
    if k not in RM_ARGS:
      
      if isinstance(k, list):
        items = " ".join([i for i in v if i != ""])
        arg = "--{}={}".format(k, items)
      
      else:
        arg = "--{}={}".format(k,str(v))  
        
      args.append(arg)

  if len(args) == 0:
    return None 
    
  else:
    return args


def format_usage(cmd, accepts, requires):
  samp_json = "'{\"kw\": \"value\"}'"
  return """
    $ gnulynx {0} {1}
    $ gnulynx {0} path/to/kwargs.json
    $ gnulynx {0} path/to/kwargs.jsonlines  
    $ gnulynx {0} path/to/kwargs.yaml 
    $ echo  {1} | gnulynx {0}
    
    accepted kwargs:
    {2}

    required kwargs:
    {3}
    """.format(
      cmd, 
      samp_json, 
      "\t- " + "\n\t- ".join(accepts),
      "\t- " + "\n\t- ".join(requires)
    )

class AliasedSubParsersAction(argparse._SubParsersAction):
 
  class _AliasedPseudoAction(argparse.Action):
    def __init__(self, name, aliases, help):
      dest = name
      if aliases:
          dest += ' (%s)' % ', '.join(aliases)
      sup = super(AliasedSubParsersAction._AliasedPseudoAction, self)
      sup.__init__(option_strings=[], dest=dest, help=help) 

  def add_parser(self, name, **kwargs):
    if 'aliases' in kwargs:
      aliases = kwargs['aliases']
      del kwargs['aliases']
    else:
      aliases = []

    parser = super(AliasedSubParsersAction, self).add_parser(name, **kwargs)

    # Make the aliases work.
    for alias in aliases:
      self._name_parser_map[alias] = parser

    # Make the help text reflect them, first removing old help entry.
    if 'help' in kwargs:
      help = kwargs.pop('help')
      self._choices_actions.pop()
      pseudo_action = self._AliasedPseudoAction(name, aliases, help)
      self._choices_actions.append(pseudo_action)

    return parser


def install_default_arguments(parser):
  """
  Default arguments for all subcommands
  """
  parser.add_argument(
    'kwargs',
    help="""
    The json kwargs / yaml or json file to pass into the function.
    If not present, read from stdin.
    """, 
    nargs = "?"
  )
  parser.add_argument(
    '--queue_size',
    dest = 'queue_size',
    help = """
    The number of workers to use with gevent. default=2
    """,
    default = 2
  )
  parser.add_argument(
    '--passthrough',
    dest = 'passthrough',
    help = """
    Override a function which doesn't write to stdout by default
    to passthrough all input to stdout while stile performing an operation.
    """,
    default = False
  )
  parser.add_argument(
    '--subprocess',
    dest = 'subprocess',
    help = """
      Whether or not to run the function as a subprocess. 
      Process will hang if stdout is not closed
      by writing to a file or datastore.
      """,
    default = False
  )
  parser.add_argument(
    '--add',
    dest = 'add',
    help = """
      A comma-delimited list of input keywords 
      to add to each row of the output. eg:
      $ echo '{"slug":"members-of-congress": "list_owner":"cspan"}' | 
      $ gnulynx twitter-list --add='slug,list_owner'
    """,
    default = ""
    )
  parser.add_argument(
    "--quiet",
    dest = "quiet",
    help = """
    Silence logging.
    
    """,
    default = True
    )

def install_argument(parser, name, alias, **kw):
  """
  Install an argument for a subcommand based on parameters 
  in the yml file.
  """
  
  if alias:
    parser.add_argument(
      "-" + alias,
      "--" + name, 
      dest=name,
      **kw
    )

  else:
    parser.add_argument(
      "--" + name, 
      dest=name,
      **kw
    )     

def install_arguments(parser, arguments):
  """
  Install all arguments fro a subcommand based on parameters 
  in the yml file. 
  """
  for name, kw in arguments.items():
    alias = kw.get('alias')
    if alias: del kw['alias']
    install_argument(parser, name, alias, **kw)


def install_subparser(subparsers, cmd, meta):
  """
  Create a subparser instance which runs 
  a function.
  """
  
  # parse description / aliases / accepts / requires
  # install arguments from config
  if meta.get('config'):
    description = meta['config'].get('description', '')
    aliases = meta['config'].get('aliases', [])
    accepts = meta['config'].get('accepts', '')
    requires = meta['config'].get('requires', '')
  
  else:
    description = ''
    aliases = []
    accepts = []
    requires = []

  # create subparser
  subparser = subparsers.add_parser(
    cmd, 
    usage = format_usage(cmd, accepts, requires),
    help = description,
    aliases = aliases
  )
  
  # install default arguments 
  install_default_arguments(subparser)

  # install arguments from config
  if meta.get('config'):
    if meta['config'].get('arguments'):
      install_arguments(subparser, meta['config']['arguments'])

  subparser.set_defaults(func=exec_func(meta['path']))


def install_subcommands(tree, subparsers):
  """
  Build a list of subcommands from a tree.
  """
  for cmd, meta in tree.items():
    install_subparser(subparsers, cmd, meta)


