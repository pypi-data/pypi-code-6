#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from cli_util import (
  install_subcommands, parse_task_tree, 
  process_kwargs, opts_to_args,
  AliasedSubParsersAction,
  parse_arg
)
from settings import DEFAULT_TREE

def main(task_path=None):
  """
  recursively paginate through tasks directory
  and construct a command line interface of the following
  structure:
  `gnulynx {group}-{task}`
  """

  # parse tree
  if task_path:
    tree = parse_task_tree(task_path)

  else:
    tree = DEFAULT_TREE

  # create parser instance
  parser = argparse.ArgumentParser(prog='gnulynx / lx')

  # allow for aliases
  parser.register('action', 'parsers', AliasedSubParsersAction)

  # add the subparser "container"
  subparsers = parser.add_subparsers()

  # install subcommands
  install_subcommands(tree, subparsers)
    
  # parse the arguments
  opts = parser.parse_args()

  # turn kwargs into json
  kwargs = process_kwargs(opts.kwargs)

  # parse flags 
  args = opts_to_args(opts)

  # subprocess 
  sub = parse_arg(opts.subprocess)

  # run the sub command with optional args + kwargs
  opts.func(kwargs, args, sub)

if __name__ == '__main__':
    main()

