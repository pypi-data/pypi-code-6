#!/usr/bin/env python
# encoding: utf-8

import errno
import os
import os.path

from fabric.api import local, warn_only
import begin


def get_top_dir(path):
    if not os.path.dirname(path):
        return path, os.sep
    else:
        top_dir, rest = get_top_dir(os.path.dirname(path))
        return top_dir, os.path.join(rest, os.path.basename(path))


@begin.subcommand
def add(local_filename):
    """Adds LOCAL_FILENAME from the remote system.

    LOCAL_FILENAME has the format: remote.hostname/path/to/remote/file

    This will pull /path/to/remote/file from the host named remoted.hostname
    and place it in remote.hostname/path/to/remote/file under $PWD

    The file is then added to git and committed.

    LOCAL_FILENAME must not yet exist."""

    if os.path.exists(local_filename):
        raise OSError(errno.EEXIST, "%s already exists" % local_filename)
    if not os.path.exists(os.path.dirname(local_filename)):
        os.makedirs(os.path.dirname(local_filename))
    hostname, remote_path = get_top_dir(local_filename)
    local("scp %s:%s %s" % (hostname, remote_path, local_filename))
    with warn_only():
        local("git add -f %s" % local_filename)
        local("git commit -m 'Added %s from %s' %s" % (
              remote_path, hostname, local_filename))


@begin.subcommand
def pull(local_filename):
    """Pulls the remote copy of LOCAL_FILENAME"""
    if not os.path.exists(local_filename):
        raise OSError(errno.ENOENT, "%s does not exist" % local_filename)
    hostname, remote_path = get_top_dir(local_filename)
    local("git stash")
    local("scp %s:%s %s" % (hostname, remote_path, local_filename))
    with warn_only():
        local("git commit -m 'Pull %s from %s' %s" % (
              remote_path, hostname, local_filename))
        local("git stash pop")


@begin.subcommand
def vimdiff(local_filename):
    """Opens vimdiff on LOCAL_FILENAME and its remote counterpart"""
    hostname, remote_path = get_top_dir(local_filename)
    local("vimdiff %s scp://%s/%s" % (local_filename, hostname, remote_path))


@begin.start
def run():
    """Fuggit: for when you want to put that file in git, but you can't be...

    You know the feeling. You're making a quick dirty hack to a file on a
    remote machine that. The file isn't under version control. You want to
    have the convenience of editing the file locally, *and* you want the
    ability to roll back your changes. Putting the remote file under version
    control is just too hard, so what do you say? fuggit.
    
    Specifcally:
        
    fuggit add remote.hostname/etc/file.name
    
    this will grab /etc/file.name from the machine remote.hostname; save it
    as remote.hostname/etc/file.name under $PWD. The file will be added and
    committed to git.
    
    fuggit pull remote.hostname/etc/file.name
    
    can be used to refresh your local copy of the file. Any local changes
    will be preserved; any remote changes will result in a new commit.
    
    fuggit vimdiff remote.hostname/etc/file.name
    
    will open a vimdiff window showing your local copy of the file and the
    remote copy. Thanks to the magic of vim, any changes you make to the
    remote file will be pushed to the servce once you close the file."""
    pass
