import os
import imp
from importlib import import_module

from flask.ext.testing import TestCase

from alembic import command
from alembic.config import Config as AlembicConfig

class Config(AlembicConfig):
  def get_template_directory(self):
    package_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(package_dir, 'templates')

class ResourceTest(TestCase):

  finny_app = None

  def setUp(self):
    command.upgrade(self.config, "head")

  def tearDown(self):
    self.db.session.remove()
    self.db.drop_all()

    self.db.engine.execute("drop schema public cascade; create schema public;")

  def _get_config(self, current_app):
    directory = current_app.extensions['migrate'].directory

    config = Config(os.path.join(directory, 'alembic.ini'))
    config.set_main_option('script_location', directory)
    return config

  def create_app(self):
    if ResourceTest.finny_app:
      return ResourceTest.finny_app

    current_path = os.getcwd()

    config = imp.new_module('config')
    config.__file__ = "config"
    # loads the configuration file
    with open(current_path + "/__init__.py") as config_file:
      exec(compile(config_file.read(), "config", 'exec'), config.__dict__)

    finny_app = config.__APP__

    boot_module = import_module("%s.boot" % finny_app)

    create_app = boot_module.create_app
    ResourceTest.db = boot_module.db

    current_app = create_app("andromeda_api", "test", "default")

    ResourceTest.config = self._get_config(current_app)
    ResourceTest.finny_app = current_app

    return current_app
