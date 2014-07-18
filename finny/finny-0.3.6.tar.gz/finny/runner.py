import os
import sys
import argparse

import imp

from finny.commands import CommandFactory

STRUCTURE_REPRESENTATIVES = [ "manage.py", "__init__.py" ]

class CLI(object):

  def __init__(self):
    self.parser = argparse.ArgumentParser(description='Finny.')
    self.subparsers = self.parser.add_subparsers(help='sub-command help')

  def add_subparsers(self, *args, **kwargs):
    return self.parser.add_subparsers(*args, **kwargs)

  def add_param(self, *args, **kwargs):
    return self.parser.add_argument(*args, **kwargs)

  def add_argument(self, *args, **kwargs):
    return self.parser.add_argument(*args, **kwargs)

  def run(self):
    self.params = self.parser.parse_args()
    self.main()

class Finny(CLI):
  """
  Finny entry point
  """
  def __init__(self, is_structure):
    super(Finny, self).__init__()

    self.is_structure = is_structure

    self.parser = argparse.ArgumentParser(description='Process some integers.')

  def run_command(self):
    command = CommandFactory.get(command=self.params.command,
                                 command_type=self.params.command_type)
    command.run(self.params)

  def generate_structure(self):
    path = self.params.path

    if path[0] != "/":
      path = os.path.abspath(os.getcwd() + "/" + self.params.path)

    name = path.split("/")[-1]

    if os.path.exists(path):
      raise AttributeError("Path %s is already present." % path)

    CommandFactory.get(command="GenerateStructure").run(name, path)

  def main(self):
    if self.is_structure:
      self.run_command()
    else:
      self.generate_structure()

def detect_current_structure():
  current_path = os.getcwd()

  reprensentatives = [ os.path.exists(current_path + "/" + item)
                      for item in STRUCTURE_REPRESENTATIVES ]

  if all(reprensentatives):
    config = imp.new_module('config')
    config.__file__ = "config"
    # loads the configuration file
    with open(current_path + "/__init__.py") as config_file:
      exec(compile(config_file.read(), "config", 'exec'), config.__dict__)

    finny_app = config.__APP__

    if os.path.exists(current_path + "/" + finny_app):
      return True

  return False

def execute_from_cli():
  current_path = os.getcwd()
  is_structure = detect_current_structure()

  f = Finny(is_structure)

  if is_structure:
    subparsers = f.add_subparsers(dest="command",
                                  help='Commands for a present finny app')

    parser_generate = subparsers.add_parser('generate',
                                        help='Generate a number of constructs')

    subparser_gen = parser_generate.add_subparsers(dest="command_type",
                                        help='Generate a number of constructs')

    parser_runner = subparser_gen.add_parser('runner',
                                             help='Generate new runner')

    parser_endpoint = subparser_gen.add_parser('endpoint',
                                               help='Generate new endpoint')

    parser_default_runner  = subparser_gen.add_parser('default-runner',
                                                    help='Generate new runner')

    parser_runner.add_argument("name", help="Name of the runner")
    parser_endpoint.add_argument("name", help="Name of the endpoint")

  else:
    subparsers = f.add_subparsers(help='sub-command help')
    parser_new = subparsers.add_parser('new', help='new help')
    parser_new.add_argument("path", help="Path or name of the finny app",
                             default=False)

  f.run()
