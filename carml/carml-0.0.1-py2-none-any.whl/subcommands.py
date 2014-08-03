import interface


registry = {}

def register(command_name, subcommand):
    """
    :param subcommand: implements ISubCommand
    """

    registry[command_name] = interface.ISubCommand(subcommand)
