DEFAULT_CONFIG = """\
# Aliases let you define shortcuts for commonly used recipients.
# Each line contains a whitespace separated ALIAS EXPANSION pair.

bob 123-456-7890"""

from babel.bin.base import *

import os.path

check_for_config_dir()

# Create alias file if it doesn't already exist
if not os.path.isfile(BABEL_DIR+'/aliases.txt'):
    open(BABEL_DIR+'/aliases.txt', 'w').write(DEFAULT_CONFIG)

# Load alias file
aliases = {}
line_number = 0
for line in open(BABEL_DIR+'/aliases.txt'):
    line_number += 1
    if line.find('#') != -1: line = line[:line.find('#')]
    line = line.split()
    if len(line) == 0: continue
    if len(line) != 2:
        fail("Invalid alias on %s/aliases.txt line %s" % (BABEL_DIR, line_number),
             "You may need to edit %s/sms.toml."%BABEL_DIR)
    aliases[line[0]] = line[1]

# Replace args.TO
if args.TO in aliases: args.TO = aliases[args.TO]