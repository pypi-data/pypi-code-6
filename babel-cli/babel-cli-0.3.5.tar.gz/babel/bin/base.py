BABEL_DIR    = "~/.babel"

TO_HELP      = "the recipient address"
MESSAGE_HELP = "the message data"
REPLY_HELP   = "wait for and print reply"

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser('babel')
parser.add_argument('TO', help=TO_HELP)
parser.add_argument('MESSAGE', nargs='?', help=MESSAGE_HELP)
parser.add_argument('-r', '--reply', action='store_true', help=REPLY_HELP)
args = parser.parse_args()

# Properly qualify BABEL_DIR
import os.path
BABEL_DIR = os.path.expanduser(BABEL_DIR)

# Print error message and exit
def fail(message, suggestion=None):
    print("Error:", message)
    if suggestion: print("Note:", suggestion)
    exit(1)

# Look for and create the Babel directory if it doesn't already exist
def check_for_config_dir():
    if not os.path.isdir(BABEL_DIR):
        os.makedirs(BABEL_DIR)