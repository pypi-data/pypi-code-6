#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def piped(input=sys.stdin):
    """
    Returns input if input is not connected to a tty(-like) device
    """
    return input if not input.isatty() else None


def prompt_yes_no(prompt_msg, default=None, num_retries=5, input=raw_input):
    """
    Yes/no prompts a user with `prompt_msg`. Default can be `yes`, `no`, or
    None. If user answer is not valid, he/she has `num_retries` to provide a
    valid yes/no prompt.
    """
    def _get_prompt_defaults(default):
        if default is None:
            return "[y/n]"
        elif default == "yes":
            return "[Y/n]"
        elif default == "no":
            return "[y/N]"
        else:
            raise ValueError("Invalid default value: '%s'" % default)

    prompt_msg = "{0} {1} ".format(prompt_msg, _get_prompt_defaults(default))

    while True:
        choice = input(prompt_msg).lower()

        if default is not None and choice == '':
            choice = default
        if choice in ('y', 'ye', 'yes', '1'):
            return True
        if choice in ('n', 'no', '0'):
            return False

        num_retries = num_retries - 1
        if num_retries < 0:
            raise IOError

        sys.stdout.write("Please respond with a valid 'yes' or 'no'\n")

# vim: filetype=python
