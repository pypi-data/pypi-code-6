import importlib
import sys
import os, subprocess
from collections import defaultdict
from serialize import (
  yaml_from_string, json_from_string,
  json_to_string
  )

def exec_func(func_path):
  """
  call a python function by it's absolute path
  """
  def _run(kw):
    args = ['python', func_path]
    
    # if we passed in json kwargs, append them to 
    # the function call
    if kw:
      args.append(json_to_string(kw))

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

def process_kwargs(kw):

  if kw:
    if kw.lower().endswith('.yml') or \
         kw.lower().endswith('.yaml'):
      return yaml_from_stringl(open(kw).read())

    elif kw.lower().endswith('.json'):
      return json_from_string(open(kw).read())

    # Otherwise assume a single json string as the kwargs
    else:
      return json_from_string(kw)

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
