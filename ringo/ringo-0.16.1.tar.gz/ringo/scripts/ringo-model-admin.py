"""Admin command to do various administration tasks on the ringo model
application"""

import argparse
import logging
from paste.deploy import appconfig
from sqlalchemy import engine_from_config
from ringo.lib.sql import DBSession
from ringo.model import Base
from ringo.lib.helpers import dynamic_import

def export(args):
    out = []
    init_model(args.c)
    for modul in args.modul:
        clazz = dynamic_import(modul)
        for x in DBSession.query(clazz).all():
            print x

log = logging.getLogger(__name__)
parser = argparse.ArgumentParser(description='Adminitrational command for the model of ringo applications',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# Global arguments
gop = argparse.ArgumentParser(add_help=False)
gop.add_argument('-c', help='Configuration file of the application', 
                    metavar="CONF", default="development.ini")

# Add subcommands
cmdparsers = parser.add_subparsers()
export_cmd_description = """
Will export the given modules.
"""
export_cmd = cmdparsers.add_parser('export',
                                   help='Export the given models',
                                   description=export_cmd_description, 
                                   parents=[gop])
export_cmd.add_argument('modul', help='modul to export', 
                        metavar="MODUL", nargs="*")
export_cmd.set_defaults(func=export)

def init_model(config):
    # Load Application Configuration and Return as Dictionary
    settings = appconfig('config:' + config,
                         relative_to=".",
                         name="main")
    # Bind Engine Based on Config
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

def main():
    args.func(args)

if __name__ == "__main__":
    args = parser.parse_args()
    main()
