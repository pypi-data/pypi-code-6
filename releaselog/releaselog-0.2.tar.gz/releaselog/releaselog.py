# -*- coding: utf-8 -*-
# Copyright 2014, Red Hat, Inc.
# License: GNU General Public License version 2 or later
# Author: Mike Ruckman <roshi AT fedoraproject.org>

""" Functions for extracting and rendering git log messages into RST. """

import os
import time
import subprocess

import config


def get_range(repo_path):
    """Retreives a range of commits from the last tag to HEAD from the git
    repo. If no tag is present it will pull all parent commits of
    HEAD.
    """

    all_tags = subprocess.check_output(['git', 'tag', '-l'],
                                       cwd=repo_path).split()

    if all_tags == '':
        return 'HEAD'
    else:
        return '%s..HEAD' % all_tags[-1]

    #    # Handle cases of a single release tag, don't pass a range
    #    if len(all_tags) < 2:
    #        return ['%s..HEAD']

    #    curr_tag = all_tags[-2]
    #    prev_tag = all_tags[-1]

    #    return [curr_tag, prev_tag]


def get_logs(repo_path, log_range):
    """Get the raw commit messages between two tags."""

    fmt_string = config.FMT_STRING

    commit_log = subprocess.check_output(['git',
                                          'log',
                                          log_range,
                                          '--pretty=format:%s' % fmt_string,
                                          '--reverse'],
                                         cwd=repo_path)

    return commit_log


def check_duplicate(file_path):
    """Check to see if a fragment already exists. Returns true if file
    already exists."""

    if os.path.isfile(file_path):
        return True
    else:
        return False


def build_release_page(repo_path):
    """Create a reStructured text fragment page for a release. This page will
    be imported as a fragment in the main Release Notes document. Returns the
    filename of the created file.
    """

    day = time.localtime()
    fmt_day = "(%s-%s-%s)" % (day.tm_year, day.tm_mon, day.tm_mday)

    source_path = repo_path + '/docs/source/'
    log_range = get_range(repo_path)
    range_points = log_range.split('..')

    # Write a header for the release fragment
    header = config.FRAGMENT_HEADER % (range_points[0], fmt_day)

    if range_points[0] == 'HEAD':
        file_name = 'first_fragment.rst'
    else:
        file_name = '%s_fragment.rst' % range_points[0]

    if check_duplicate(source_path + file_name):
        print ("Already up to date. Delete old fragment if you need "
               "to regenerate.")
        return 'duplicate'
    else:

        with open(source_path + file_name, 'w') as doc_file:
            doc_file.write(header)
            doc_file.write(get_logs(repo_path, log_range))

            print "Created release notes fragment: %s\n" % file_name
            return file_name


def update_full_release_notes(repo_path, release_notes_file):
    """Create or update a complete Release Notes page."""

    header = config.RELNOTES_HEADER
    rel_notes_path = repo_path + '/docs/source/releasenotes.rst'

    # Write or update based on if the file exists
    if os.path.isfile(rel_notes_path):
        file_access_type = 'a'
    else:
        file_access_type = 'w'

    line_template = ".. include:: %s\n"

    if release_notes_file == 'duplicate':
        return

    else:
        with open(rel_notes_path, file_access_type) as rel_notes:
            if file_access_type == 'w':
                rel_notes.write(header)
            rel_notes.write(line_template % release_notes_file)

        print "Release Notes file has been updated."
