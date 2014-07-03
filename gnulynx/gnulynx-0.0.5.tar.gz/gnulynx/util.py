import importlib
import sys
import os, subprocess
from collections import defaultdict
from serialize import (
  yaml_from_string, json_from_string,
  json_to_string, json_from_lines,
  json_to_lines
  )

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
        yield json_from_string(l)

def read_positional_kwargs(kw):
  """
  Read postiional kwargs, 
  parse json, yield objects
  """
  for k in kw.split('\n'):
    if k.strip() != '':
      yield json_from_string(k)

def write_stdout(obj):
  """
  Write jsonlines to stdout
  """
  line = json_to_string(obj) + "\n"
  sys.stdout.write(line)

def exec_func(func_path):
  """
  call a python function by it's absolute path
  """
  def _run(kw):
    args = ['python', func_path]
    
    # if we passed in json kwargs, append them to 
    # the function call
    if kw:
      args.append(json_to_lines(kw))

    subprocess.Popen(args)

  return _run

def slug_path(func_path):
  """
  Prettify a path.
  """
  return func_path.split('.')[0].replace('_', '-').lower().strip()

# parse a directory for functions and yaml files and return
# a tree of commands
def parse_task_tree(task_path):
  """
  Parse the task(s) directory for paths, filenames, and yaml-definitions.
  """ 
  
  tree = defaultdict()

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

      # build tree
      tree[cmd] = path 

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

def process_kwargs(kw):

  if kw:
    
    # YAML #
    if kw.lower().endswith('.yml') or \
         kw.lower().endswith('.yaml'):
      
      # load and listify
      d = yaml_from_string(open(kw).read())
      return listify(d)

    # JSON #
    elif kw.lower().endswith('.json'):

      # load and listify
      d = json_from_string(open(kw).read())
      return listify(d)

    # JSONLINES #
    elif kw.lower().endswith('.jsonlines'):
      
      # load and listify
      lines = open(kw).read().split('\n')
      return json_from_lines(lines)

    # otherwise assume positional kwargs
    else:
      # load and listify
      d = json_from_string(kw)
      return listify(d)

def format_usage(cmd):
  samp_json = "'{\"kw\": \"value\"}'"
  return """
    $ gnulynx {0} {1}
    $ gnulynx {0} path/to/kw.json 
    $ gnulynx {0} path/to/kw.yaml 
    $ echo  {1} | gnulynx {0}""".format(cmd, samp_json)

def install_subparser(parser, cmd, path):
  """
  Create a subparser instance which runs 
  a function.
  """
  # create subparser
  sub_parser = parser.add_parser(cmd, usage=format_usage(cmd))
  sub_parser.add_argument(
    'kw',
    help="The json kwargs/ yaml or json file to pass into the function.\nIf not present, read from stdin.", 
    nargs = "?"
    )
  # return the function
  return exec_func(path)

def install_subcommands(tree, subparser):
  subcommands = {}
  for cmd, path in tree.items():
    subcommands[cmd] = install_subparser(subparser, cmd, path)
  return subcommands


