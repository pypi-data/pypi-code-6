from .generate_structure import GenerateStructure
from .generate_runner import GenerateRunner
from .generate_endpoint import GenerateEndpoint 

class CommandFactory(object):

  @staticmethod
  def get(command, command_type=None):
    if command == "GenerateStructure":
      return GenerateStructure()

    if command == "generate":
      if command_type == "runner":
        return GenerateRunner()

      if command_type == "endpoint":
        return GenerateEndpoint()

    raise NotImplementedError("The command with command=%s and command_type=%s" \
                              % (command, command_type))
