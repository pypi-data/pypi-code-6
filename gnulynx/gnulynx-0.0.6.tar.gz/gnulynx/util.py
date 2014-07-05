import importlib
import sys, re
import os, subprocess
from collections import defaultdict
from serialize import (
  from_yaml, from_json,
  to_json, from_jsonlines,
  to_jsonlines
  )

re_not_int = re.compile(r'[^0-9]+')
re_not_float = re.compile(r'[^0-9\.]+')

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


def read_positional_kwargs(kw):
  """
  Read postiional kwargs, 
  parse json, yield objects
  """
  for k in kw.split('\n'):
    if k.strip() != '':
      yield from_json(k)


def write_stdout(obj):
  """
  Write jsonlines to stdout
  """
  line = to_json(obj) + "\n"
  sys.stdout.write(line)


def exec_func(func_path):
  """
  call a python function by it's absolute path
  """
  def _run(kw, args=None):
    command = ['python', func_path]
    
    # if we passed in json kwargs, append them to 
    # the function call
    if kw:
      command.append(to_jsonlines(kw))
    
    if args:
      command.extend(args)

    subprocess.Popen(command)

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
  
  tree = defaultdict(lambda : defaultdict())

  for dir_name, dir_list, file_list in os.walk(task_path.encode('utf-8')):

    # copy over files, optionally applying templating
    for filename in file_list:
      
      # if somehow a DS_Store or pyc gets in here during dev, skip it
      if 'DS_Store' in filename \
          or '.pyc' in filename \
          or filename == "__init__.py":
        continue

      # parse directory / filnename 
      path = os.path.join(dir_name, filename)
      parts = path.split('/')
      group = slug_path(parts[-2])
      task = slug_path(parts[-1])
      cmd = "%s-%s" % (group, task)

      # if its a yml file, its the cmd's config
      if filename.endswith('.yml'):
        tree[cmd]['config'] = from_yaml(open(path).read())

      # otherwise it's the cmd's path
      else:
        tree[cmd]['path'] = path 

  return tree


def listify(d):
  """
  Turn dicts to single-element lists
  """
  # listify
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
    elif arg.lower() == "null":
      return None
    elif is_int(arg):
      return int(arg)
    elif is_float(arg):
      return float(arg)
  return arg


def opts_to_kwargs(opts, exclude=["kw", "subcommand"]):
  kwargs = {}
  for k,v in opts.__dict__.items():
    if k not in exclude:
      kwargs[k] = parse_arg(v)
  return kwargs  


def opts_to_args(opts, exclude=["kw", "subcommand"]):
  args = []
  for k,v in opts.__dict__.items():
    
    if k not in exclude:
      
      if isinstance(k, list):
        arg = "--{}={}".format(k, " ".join([i for i in v if i != ""))
      
      else:
        arg = "--{}={}".format(k,str(v))  
      args.append(arg)

  if len(args) == 0:
    return None 
    
  else:
    return args


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
      lines = open(kw).read().split('\n')
      return list(from_jsonlines(lines))

    # otherwise assume positional kwargs
    else:

      # load and listify
      return listify(from_json(kw))


def format_usage(cmd):
  samp_json = "'{\"kw\": \"value\"}'"
  return """
    $ gnulynx {0} {1}
    $ gnulynx {0} path/to/kw.json 
    $ gnulynx {0} path/to/kw.yaml 
    $ echo  {1} | gnulynx {0}
    """.format(cmd, samp_json)


def install_arguments(parser, arguments):
  for name, kw in arguments.items():
    parser.add_argument(
      "--" + name, 
      dest=name,
      **kw
    )


def install_subparser(parser, cmd, meta):
  """
  Create a subparser instance which runs 
  a function.
  """
  # create subparser
  sub_parser = parser.add_parser(cmd, usage=format_usage(cmd))
  sub_parser.add_argument(
    'kw',
    help="The json kwargs / yaml or json file to pass into the function.\nIf not present, read from stdin.", 
    nargs = "?"
    )

  # install arguments from config
  if 'config' in meta:
    if 'arguments' in meta['config']:
      install_arguments(sub_parser, meta['config']['arguments'])

  # return the function
  return exec_func(meta['path'])


def install_subcommands(tree, subparser):
  subcommands = {}
  for cmd, meta in tree.items():
    subcommands[cmd] = install_subparser(subparser, cmd, meta)
  return subcommands


