import argparse
import os
from inspect import getargspec

from kaiju.arguments import Var


class KaijuCLI(object):
    """KaijuCLI simplifies the creation of a command line interface.

    When instantiating a new KaijuCLI, youa provide a list of operations and a
    description. A subparser is automatically created for each operation,
    giving you a basic interface (including a useful --help option) with no
    cost.
    """

    SPECIAL_ARG_NAMES = ["operation", "database_uri", "no_memo", "no_store", "enable_print"]

    def __init__(self, operations, description):
        self.operations = operations

        self.parser = argparse.ArgumentParser(
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.parser.add_argument(
            "--database-uri",
            default=os.environ.get("TRILOBITE_DATABASE_URI", None)
        )
        self.parser.add_argument("--no-memo", default=False, action="store_true")
        self.parser.add_argument("--no-store", default=False, action="store_true")
        self.parser.add_argument("--enable-print", default=False, action="store_true")

        self.subparsers = self.parser.add_subparsers(title="operations", dest="operation")

        for op_name, op in self.operations.items():
            self.configure_parser_from_function(op)

    def configure_parser_from_function(self, op):
        """Map arguments from `op` to parser entries.

        Analyze args from `op` and create corresponding entries on the parser.
        """

        brief_description = op.__doc__.splitlines() if op.__doc__ else [""]
        sp = self.subparsers.add_parser(op.__name__, help=brief_description[0])
        args, _, _, defaults = getargspec(op.__original__)
        if defaults is None:
            defaults = []

        cut = len(args) - len(defaults)
        non_optional_arguments = args[:cut]
        optional_arguments = args[cut:]

        kaiju_arguments = op.__kaiju__

        for argument in non_optional_arguments:
            arg_handler = kaiju_arguments.get(argument, Var())
            sp.add_argument(argument, **arg_handler.config)

        for argument, default_value in zip(optional_arguments, defaults):
            arg_handler = kaiju_arguments.get(argument, Var())
            sp.add_argument("--" + argument,
                            default=default_value,
                            **arg_handler.config)

    def parse_args(self, args=None):
        """Run ArgumentParser and filter out special arguments.

        There are some arguments considered "special" (see the SPECIAL_ARG_NAMES
        constant) and they aren't passed as parameters when the operation is
        run.

        """

        args_namespace = self.parser.parse_args(args)

        global_args = {
            k: v
            for k, v in vars(args_namespace).items()
            if k in self.SPECIAL_ARG_NAMES
        }

        operation_args = {
            k: v
            for k, v in vars(args_namespace).items()
            if k not in self.SPECIAL_ARG_NAMES
        }

        return global_args, operation_args
