#!/usr/bin/env python3
"""SHAPICLI Client Utility

This command line utility accesses the REST interface and is suitable
for embedding in shell scripts or other devops utilities.

Usage:
    shapi help         [<command> [--examples] ] [--nobold]
    shapi config
    shapi ping         [--config=<path>]
    shapi hal          [--config=<path>] [<relativeuri>] [--props | --post=<path>]
    shapi shell        [--config=<path>]
    shapi login        [--config=<path>] 
    
Options:
  --help              Show this screen.
  --config=<path>     Path to config file
  --examples          Display usage examples [default: False]
  --nobold            When true, no terminal output will be bolded, useful for piping [default: False]
"""

from docopt import docopt
from hyperdns.hapi.sysmgr.cli import SHAPICLI
import hyperdns.hal.navigator
import urllib.error

arguments=docopt(__doc__, version='SHAPICLI Client 1.0')

# load all the commands that are documented in the help above
base='hyperdns.hapi.sysmgr.cli'
for _cmd in arguments.keys():
    if not (_cmd.startswith("-") or _cmd.startswith("<")):
        mod='%s.cli_%s' % (base,_cmd)
        __import__(mod, fromlist=[base])
        
# now run the SHAPICLI given the command line
try:
    SHAPICLI(arguments,docopt_doc=__doc__)
except urllib.error.URLError as E:
    print("Sorry, I can not connect to the configured server")
except SHAPICLI.BadCall as E:
    code=E.response.status_code
    reason=E.response.reason
    print("Sorry, I could do not that - (code %s) - %s" % (code,reason))