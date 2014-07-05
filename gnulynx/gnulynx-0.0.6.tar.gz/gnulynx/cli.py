import argparse
from util import (
install_subcommands, parse_task_tree, 
process_kwargs, opts_to_args
)
from settings import DEFAULT_TREE


def main(task_path=None):
    """
    recursively paginate through tasks directory
    and construct a command line interface of the following
    structure:
    `gnulynx {group}-{task}`

    since each task will have its only cli handler,
    we'll just simply create a tree of sub-commands 
    based on the directory structure.
    """

    # parse tree
    if task_path:
      tree = parse_task_tree(task_path)

    else:
      tree = DEFAULT_TREE

    # create parser instance
    parser = argparse.ArgumentParser(prog='gnulynx')

    # add the subparser "container"
    subparser = parser.add_subparsers(help='sub-commands', dest='subcommand')

    # install subcommands
    subcommands = install_subcommands(tree, subparser)
      
    # parse the arguments
    opts = parser.parse_args()

    # turn kwargs into json
    kw = process_kwargs(opts.kw)

    # parse flags 
    args = opts_to_args(opts)

    # check for unlisted commands
    if opts.subcommand not in subcommands:
      raise RuntimeError, "No such subcommand."

    # run the sub command with optional kwargs
    subcommands[opts.subcommand](kw, args)

if __name__ == '__main__':
    main()

