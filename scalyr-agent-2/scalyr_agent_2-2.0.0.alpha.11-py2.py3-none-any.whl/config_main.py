#!/usr/bin/env python
# Copyright 2014, Scalyr, Inc.
#
# The main function for the scalyr-agent-2-config command which can be used to update
# the configuration file.  Currently, this only works on configuration files that have
# not been previously modified by the user.

import getpass
import os
import sys
import inspect
import traceback

from pwd import getpwnam
from optparse import OptionParser

# This is suppose to be a system-independent way of adding the necessary parent directory
# to the python path so that everything executes properly.  We do not rely on __file__ because
# some folks report problems with that when running on some versions of Windows.
# Get the file for this script and make it absolute.
file_path = inspect.stack()[0][1]
if not os.path.isabs(file_path):
    file_path = os.path.abspath(file_path)
file_path = os.path.realpath(file_path)

# We rely on the fact that the agent_main.py file should be in a directory structure that looks like:
# py/scalyr_agent/agent_main.py  .  We wish to add 'py' to the path, so the parent of the parent.
sys.path.append(os.path.dirname(os.path.dirname(file_path)))

from scalyr_agent.configuration import Configuration


def set_api_key(config, config_file_path, new_api_key):
    """Replaces the current api key in the file at 'config_file_path' with the value of 'new_api_key'.

    Params:
        config:  The Configuration object created by reading config_file_path.
        config_file_path:  The full path to the configuration file.  This file will be overwritten.
        new_api_key:  The new value for the api key to write into the file.
    """
    # We essentially search through the current configuration file, looking for the current key's value
    # and rewrite it to be the new_api_key.
    current_key = config.api_key

    tmp_file = None
    original_file = None

    try:
        # Create a temporary file that we will write the new file into.  We will just rename it when we are done
        # to the original file name.
        tmp_file_path = '%s.tmp' % config_file_path
        tmp_file = open(tmp_file_path, 'w')

        # Open up the current file for reading.
        original_file = open(config_file_path)
        found = 0

        for s in original_file:
            # For a sanity check, make sure we only see the current key once in the file.  That guarantees that
            # we are replacing the correct thing.
            found += s.count(current_key)
            if found > 1:
                print >>sys.stderr, 'The existing API key was found in more than one place.  Config file has been'
                print >>sys.stderr, 'modified already.  Cannot safely update modified config file so failing.'
                sys.exit(1)
            s = s.replace(current_key, new_api_key)
            print >>tmp_file, s,

        if found != 1:
            print >>sys.stderr, 'The existing API key could not be found in file, failing'
            sys.exit(1)
        # Determine how to make the file have the same permissions as the original config file.  For now, it
        # does not matter since if this command is only run as part of the install process, the file should
        # be owned by root already.
        os.rename(tmp_file_path, config_file_path)
    except Exception, e:
        print >>sys.stderr, 'Error attempting to update the key: %s' % str(e)
        print >> sys.stderr, traceback.format_exc()
        sys.exit(1)
    finally:
        if tmp_file is not None:
            tmp_file.close()
        if original_file is not None:
            original_file.close()


def update_user_id(file_path, new_uid):
    """Change the owner of file_path to the new_uid.

    Arguments:
        file_path:  The full path to the file.
        new_uid:  The id of the user to set as owner.
    """
    try:
        group_id = os.stat(file_path).st_gid
        os.chown(file_path, new_uid, group_id)
    except Exception, e:
        print >>sys.stderr, 'Error attempting to update permission on file "%s": %s' % (file_path, str(e))
        print >> sys.stderr, traceback.format_exc()
        sys.exit(1)


def update_user_id_recursively(path, new_uid):
    """Change the owner of all files in the directory named 'path' to the new_uid, recursively.

    Arguments:
        file_path:  The full path to the directory.
        new_uid:  The id of the user to set as owner.
    """
    try:
        for f in os.listdir(path):
            full_path = os.path.join(path, f)
            if os.path.isfile(full_path):
                update_user_id(full_path, new_uid)
            elif os.path.isdir(full_path):
                update_user_id_recursively(full_path, new_uid)
    except Exception, e:
        print >>sys.stderr, 'Error attempting to update permissions on files in dir "%s": %s' % (path, str(e))
        print >> sys.stderr, traceback.format_exc()
        sys.exit(1)


def set_executing_user(config, config_file_path, new_executing_user):
    """Update all the configuration files so that the agent can be run as new_executing_user.

    Params:
        config:  The Configuration object created by parsing config_file_path.
        config_file_path:  The full path of the configuration file.
        new_executing_user:  The new user (str) that the agent should be run as.
    """
    try:
        uid = getpwnam(new_executing_user).pw_uid
    except KeyError:
        print >>sys.stderr, 'User "%s" does not exist.  Failing.' % new_executing_user
        sys.exit(1)

    # The agent looks to the owner of the configuration file to determine what user to run as.  So, change that
    # first.
    update_user_id(config_file_path, uid)
    # We have to update all files in the data and log directories to ensure the new user can read them all.
    update_user_id_recursively(config.agent_data_path, uid)
    update_user_id_recursively(config.agent_log_path, uid)


if __name__ == '__main__':
    parser = OptionParser(usage='Usage: scalyr-agent-2-config [options]')
    parser.add_option("-c", "--config-file", dest="config_filename",
                      help="Read configuration from FILE", metavar="FILE")
    parser.add_option("", "--set-key-from-stdin", action="store_true", dest="set_key_from_stdin", default=False,
                      help="Update the configuration file with a new API key read from standard input.  "
                           "The API key is used to authenticate requests to the Scalyr servers for the account.")
    parser.add_option("", "--set-key", dest="api_key",
                      help="Update the configuration file with the new API key."
                           "The API key is used to authenticate requests to the Scalyr servers for the account.")
    parser.add_option("", "--set-user", dest="executing_user",
                      help="Update which user account is used to run the agent.")

    if getpass.getuser() != 'root':
        print >> sys.stderr, 'You must be root to run this command.'
        sys.exit(1)

    (options, args) = parser.parse_args()
    if len(args) > 1:
        print >> sys.stderr, 'Could not parse commandline arguments.'
        parser.print_help(sys.stderr)
        sys.exit(1)

    if options.config_filename is None:
        options.config_filename = Configuration.default_config_file_path()

    if not os.path.isabs(options.config_filename):
        options.config_filename = os.path.abspath(options.config_filename)

    try:
        config_file = Configuration(options.config_filename, None, None)
        config_file.parse()
    except Exception, e:
        print >> sys.stderr, 'Error reading configuration file: %s' % str(e)
        print >> sys.stderr, traceback.format_exc()
        print >> sys.stderr, 'Terminating, please fix the configuration file and restart agent.'
        sys.exit(1)

    if options.set_key_from_stdin:
        api_key = raw_input('Please enter key: ')
        set_api_key(config_file, options.config_filename, api_key)
    elif options.api_key is not None:
        set_api_key(config_file, options.config_filename, options.api_key)

    if options.executing_user is not None:
        set_executing_user(config_file, options.config_filename, options.executing_user)

    sys.exit(0)
