from bigpanda_splunk import \
        SPLUNK_HOME, \
        SCRIPT_NAME, \
        LOG, write_config, setup_logging, get_path
from bigpanda_splunk.runner import send_test_alert

import glob
import grp
import os
import pwd
import sys

SPLUNK_USER_NAME = "splunk"
PRINT_PREFIX = "BigPanda Splunk"


def configure(runner_path, args):
    """
    Configure BigPanda Splunk Provider
    """
    error = validate_args(runner_path, args)
    if error:
        return sys.exit(error)
    token, app_key = args[1], args[2]
    try:
        write_shell_file(runner_path)
        write_config(token, app_key)
        verify_logging_permissions()
        chown_bigpanda_files()
    except Exception as error:
        return sys.exit(
            "BigPanda Splunk: Invalid permissions detected: %s" % str(error))

    error = send_test_alert()
    if error:
        sys.exit(error)
    print 'BigPanda Splunk Integration Configured.\n\
Your should see a test alert at your BigPanda dashboard...'

def write_shell_file(runner_path):
    bp_shell_path = get_path(SCRIPT_NAME)
    if os.path.exists(bp_shell_path):
        os.unlink(bp_shell_path)
    bp_shell_content = """#!/bin/bash
PYTHONPATH= LD_LIBRARY_PATH= %s %s "$@"
""" % (sys.executable, os.path.join(os.path.dirname(runner_path), SCRIPT_NAME))
    with open(bp_shell_path, "w") as shell_file:
        shell_file.write(bp_shell_content)


def verify_logging_permissions():
    setup_logging()
    LOG.info("Testing permissions")


def chown_bigpanda_files():
    try:
        GID = grp.getgrnam(SPLUNK_USER_NAME).gr_gid
        UID = pwd.getpwnam(SPLUNK_USER_NAME).pw_uid
    except:
        pass
    if GID and UID:
        for bp_file in glob.glob(get_path('') + "/bigpanda*"):
            os.chown(bp_file, UID, GID)


def validate_args(runner_path, args):
    if not args or len(args) != 3:
        return "%s\nUsage: %s TOKEN APP_KEY" % (
            PRINT_PREFIX,
            os.path.basename(runner_path)
            )
                
    if not os.path.exists(SPLUNK_HOME):
        return "%s: Splunk installation not found!" % PRINT_PREFIX
