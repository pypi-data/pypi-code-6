import os
import sys 
import json
import imp

from copy import copy

from importlib import import_module
import inflect

from jinja2 import Environment, PackageLoader
from finny.command import Command

class GenerateEndpoint(Command):

  def __init__(self):
    self.pluralize = inflect.engine()

  def _touch(self, filepath):
    open(filepath, 'a').close()


  def _transform_param_names(self):
    name = self.params.name
    self.params.original_name = name

    names = [ i for i in name.split("_") ]

    plural_names = copy(names)
    plural_names[-1] = self.pluralize.plural(plural_names[-1])

    self.params.name = "".join([ n.capitalize() for n in names])
    self.params.plural_name = "".join([ n.capitalize() for n in plural_names])
    self.params.plural_orig_name = "_".join(plural_names)


  def _read_app_name(self):
    cwd = os.getcwd()

    config = imp.new_module('config')
    config.__file__ = "config"
    # loads the configuration file
    with open(cwd + "/__init__.py") as config_file:
      exec(compile(config_file.read(), "config", 'exec'), config.__dict__)

    self.app_name = config.__APP__

  def run(self, params):
    self.params = params

    cwd = os.getcwd()

    self._read_app_name()
    self._transform_param_names()

    endpoint_path = cwd + "/resources/" + self.params.original_name
    # create folder for endpoint
    os.makedirs(endpoint_path)

    # copy templates over
    self._copy_templates([ "api.py", "model.py"], "endpoint", endpoint_path)

    self.read_default_runner()

  def read_default_runner(self):
    cwd = os.getcwd() + "/resources"

    endpoints = [ name for name in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, name)) ]

    cwd = os.getcwd()

    with open("%s/%s/runners/default.py" % (cwd, self.app_name), "w+") as f:
      f.write("ENDPOINTS = %s" % json.dumps(endpoints))

  def _copy_templates(self, source, src, dst):
    env = Environment(loader=PackageLoader('finny.commands', 'templates/' + src))

    for item in source:
      template = env.get_template("%s.jinja" % item)
      output = template.render(name=self.params.name,
                               plural_name=self.params.plural_name,
                               app_name=self.app_name,
                               original_name=self.params.original_name,
                               plural_orig_name=self.params.plural_orig_name)

      path = dst + "/" + item
      dirname = os.path.dirname(path)

      if not os.path.exists(dirname):
        os.makedirs(dirname)

      self._touch(dirname + "/__init__.py")

      with open(path, "w+") as f:
        f.write(output)
