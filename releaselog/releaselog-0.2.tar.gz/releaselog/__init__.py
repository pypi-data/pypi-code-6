import os
import argparse

from . import releaselog

__version__ = "0.2"


def main():
    """Run standalone."""

    args = get_args()

    if args['git_path'] is None:
        cwd = os.path.abspath(os.pardir)
    else:
        cwd = os.path.abspath(args['git_path'])
    latest_file = releaselog.build_release_page(cwd)

    releaselog.update_full_release_notes(cwd, latest_file)


def get_args():
    parser = argparse.ArgumentParser(description="Generate release notes "
                                     "from git logs for sphinx.")

    parser.add_argument('git_path',
                        nargs='?',
                        default='..',
                        help='Pass in a path to where the git repo lives. \
                        \n Default is "..".')

    args = parser.parse_args()

    return vars(args)
