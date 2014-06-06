
from sbdk.commands import check_project_state
from subprocess import Popen
from sys import stdout


def argument_parser(subparsers):
    parser = subparsers.add_parser("pull", help="Fetch docker images from repository")
    parser.set_defaults(func=pull)


def pull(project):
    check_project_state(project)
    pull = Popen(['docker', 'pull', project.repo_name], stdout=stdout)
    pull.wait()
