import os
import imp

def read_env_variable(variable_name):

  if variable_name in os.environ:
    return os.environ[variable_name]
  else:
    current_path = os.getcwd()

    config = imp.new_module('config')
    config.__file__ = "config"

    if os.path.exists(current_path + "/.env"):
      # loads the configuration file
      with open(current_path + "/.env") as config_file:
        exec(compile(config_file.read(), "config", 'exec'), config.__dict__)

      if hasattr(config, variable_name):
        return getattr(config, variable_name)

    raise AttributeError("Could not find %s as an ENV variable or in the .env file")
