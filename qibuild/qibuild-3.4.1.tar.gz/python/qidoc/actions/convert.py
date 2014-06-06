""" Fix a qidoc2 worktree.

It will be usable both with qidoc2 and qidoc3 by default

"""

from qisys import ui
import qisys.parsers

import qidoc.convert

def configure_parser(parser):
    qisys.parsers.worktree_parser(parser)
    qisys.parsers.project_parser(parser)


def do(args):
    worktree = qisys.parsers.get_worktree(args)
    projects = qisys.parsers.get_projects(worktree, args)
    for project in projects:
        qidoc.convert.convert_project(project)
