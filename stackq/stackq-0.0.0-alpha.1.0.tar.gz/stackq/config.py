import json
import os
from . import io


HOME = os.path.expanduser("~")
CONFIG_FILE = os.path.join(HOME, ".stackqrc")


def read(filepath=CONFIG_FILE):
  '''Reads configuration values from a config. file.
  The default config. file is read if no filepath
  is not passed.
  @param {str} filepath - path to config. file
  @return {dict} config. dictionary'''
  config = {}
  try:
    with open(filepath) as config_file:
      content = config_file.read()
      try:
        config = json.loads(content)
      except ValueError as e:
        io.log("configuration loading").error(err=e)
  except IOError as e:
    io.log("configuration file '{0}' not found".format(filepath)).warning()
  return config


def write(key, value, filepath=CONFIG_FILE):
  '''Writes configuration values to the config file
  pointed to by the filepath.The default config. file
  is written to.
  @param {str} filepath
  @return {dict or None} (success or error)'''
  try:
    with open(filepath, "r+") as config_file:
      content = config_file.read()
      try:
        config = json.loads(content)
        config.update({key: value})
        content = json.dumps(config)
        config_file.truncate(0)
        config_file.write(content)
        return config
      except Exception as e:
        io.log("configuration writing").error(err=e)
  except Exception as e:
    io.log("configuration file opening").error(err=e)
  return None
