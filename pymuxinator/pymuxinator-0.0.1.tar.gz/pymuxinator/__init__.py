import argparse
from pymuxinator.cli import CLI


def main():
    parser = argparse.ArgumentParser(description='Pymuxinator')
    parser.add_argument('project', help='pymuxinator project to start')
    parser.add_argument('--preview', dest='preview',
        action='store_true', help='preview tmux commands')

    args = parser.parse_args()

    cli = CLI()
    cli.start(args)
