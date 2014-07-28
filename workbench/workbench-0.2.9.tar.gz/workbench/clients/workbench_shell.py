#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Workbench Interactive Shell using IPython"""
import os
import hashlib
import zerorpc
import IPython
import functools
from colorama import Fore
import re
try:
    import pandas as pd
except ImportError:
    print '\n%sNotice: pandas not found...' % Fore.YELLOW
    print '\t%sWe recommend installing pandas: %s$ pip install pandas%s' % (Fore.BLUE, Fore.RED, Fore.RESET)

try:
    from . import client_helper

# Okay this happens when you're running in a debugger so having this is
# super handy and we'll keep it even though it hurts coverage score.
except ValueError:
    import client_helper

# These little helpers get around IPython wanting to take the
# __repr__ of string output instead of __str__.
def repr_to_str_decorator(func):
    """Decorator method for Workbench methods returning a str"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Decorator method for Workbench methods returning a str"""

        class ReprToStr(str):
            """Replaces a class __repr__ with it's string representation"""
            def __repr__(self):
                return str(self)
        return ReprToStr(func(*args, **kwargs))
    return wrapper

# Helper Classes
class AutoQuoteTransformer(IPython.core.prefilter.PrefilterTransformer):
    """IPython Transformer for commands to use 'auto-quotes'"""

    def register_command_set(self, command_set):
        """Register all the Workbench commands"""
        self.command_set = command_set

    def transform(self, line, _continue_prompt):
        """IPython Transformer for commands to use 'auto-quotes'"""

        # Very conservative logic here
        # - Need to have more than one token
        # - First token in line must be in the workbench command set
        # - No other otkens can be in any of the shell namespaces
        token_list = re.split(' |;|,|(|)|\'|"', line)
        num_tokens = len(token_list)
        first_token = token_list[0]
        token_set = set(token_list)
        if num_tokens > 1 and first_token in self.command_set:
            ns_token_set = set([token for nspace in self.shell.all_ns_refs for token in nspace])
            if len(token_set.intersection(ns_token_set))==1:
                return ','+line

        # Doesn't match criteria so don't try to auto-quote it
        return line

class WorkbenchShell(object):
    """Workbench CLI using IPython Interactive Shell"""

    def __init__(self):
        ''' Workbench CLI Initialization '''

        # Grab server arguments
        server_info = client_helper.grab_server_args()

        # Spin up workbench server
        self.workbench = zerorpc.Client(timeout=300, heartbeat=60)
        self.workbench.connect('tcp://'+server_info['server']+':'+server_info['port'])

        # Create a user session
        self.session = self.Session()

        # We have a command_set for our Interactive Shell
        self.command_dict = self._generate_command_dict()
        self.command_set = set(self.command_dict.keys())

        # Our Interactive IPython shell
        self.ipshell = None

    # Internal Classes
    class Session(object):
        """Store information specific to the user session"""
        def __init__(self):
            """Initialization of Session object"""
            self.filename = None
            self.md5 = None
            self.short_md5 = '-'
            self.server = 'localhost'

    def load_sample(self, file_path):
        """Load a sample (or samples) into workbench
           load_sample </path/to/file_or_dir> """

        # Do they want everything under a directory?
        if os.path.isdir(file_path):
            file_list = [os.path.join(file_path, child) for child in os.listdir(file_path)]
        else:
            file_list = [file_path]

        # Upload the files into workbench
        for path in file_list:
            with open(path, 'rb') as my_file:
                raw_bytes = my_file.read()
                md5 = hashlib.md5(raw_bytes).hexdigest()
                if not self.workbench.has_sample(md5):
                    print 'Storing Sample...'
                    basename = os.path.basename(path)
                    md5 = self.workbench.store_sample(basename, raw_bytes, 'unknown')
                else:
                    print 'Sample already in Workbench...'

                # Store information about the sample into the sesssion
                basename = os.path.basename(path)
                self.session.filename = basename
                self.session.md5 = md5
                self.session.short_md5 = md5[:6]
                self.ipshell.push({'md5': self.session.md5})
                self.ipshell.push({'short_md5': self.session.short_md5})

    def work_request(self, worker, md5=None):
        """Wrapper for a work_request to workbench"""

        # I'm sure there's a better way to do this
        if not md5 and not self.session.md5:
            return 'Must call worker with an md5 argument...'
        elif not md5:
            md5 = self.session.md5

        # Make the work_request with worker and md5 args
        try:
            return self.workbench.work_request(worker, md5)
        except zerorpc.exceptions.RemoteError as e:
            return repr_to_str_decorator(self._data_not_found)(e)

    def workbench_command(self, command, *args):
        """Wrapper for a command to workbench"""

        # Temp debug
        print 'Executing %s %s' % (command, args)

        # Run the workbench command with args
        try:
            return self.workbench[command](*args)
        except zerorpc.exceptions.RemoteError as e:
            return repr_to_str_decorator(self._data_not_found)(e)

    def _data_not_found(self, e):
        """Message when you get a DataNotFound exception from the server"""
        return '%s%s%s' % (Fore.RED, e.msg, Fore.RESET)

    def _generate_command_dict(self):
        """Create a customized namespace for Workbench with a bunch of shortcuts
            and helper/alias functions that will make using the shell MUCH easier.
        """

        # First add all the workers
        commands = {}
        for worker in self.workbench.list_all_workers():
            commands[worker] = lambda md5=None, worker=worker: self.work_request(worker, md5)

        # Next add all the commands
        for command in self.workbench.list_all_commands():
            # Fixme: is there a better way to get the lambda function from ZeroRPC
            commands[command] = self.workbench.__getattr__(command)

        # Now the general commands which are often overloads
        # for some of the workbench commands
        general = {
            'workbench': self.workbench,
            'help': repr_to_str_decorator(self.workbench.help),
            'load_sample': self.load_sample,
            'short_md5': self.session.short_md5
        }
        commands.update(general)

        # Return the list of workbench commands
        return commands

    def run(self):
        ''' Running the workbench CLI '''

        # Announce Version
        print self.workbench.help('version')

        # Now that we have the Workbench connection spun up, we register some stuff
        # with the embedded IPython interpreter and than spin it up
        cfg = IPython.config.loader.Config()
        cfg.InteractiveShellEmbed.autocall = 2
        cfg.InteractiveShellEmbed.colors = 'Linux'
        cfg.InteractiveShellEmbed.color_info = True
        cfg.InteractiveShellEmbed.autoindent = True
        cfg.InteractiveShellEmbed.deep_reload = True
        cfg.PromptManager.in_template = (
            r'{color.Purple}'
            r'{short_md5}'
            r'{color.Blue} Workbench{color.Green}[\#]> ')
        # cfg.PromptManager.out_template = ''

        # Create the IPython shell
        self.ipshell = IPython.terminal.embed.InteractiveShellEmbed(
            config=cfg, banner1=self.workbench.help('workbench'), exit_msg='\nWorkbench has SuperCowPowers...')

        # Register our transformer
        auto_quoter = AutoQuoteTransformer(self.ipshell, self.ipshell.prefilter_manager)
        auto_quoter.register_command_set(self.command_set)

        # Start up the shell with our set of workbench commands
        self.ipshell(local_ns = self.command_dict)

import pytest
@pytest.mark.exclude
def test():
    """Test the Workbench Interactive Shell"""
    work_shell = WorkbenchShell()
    try:
        work_shell.run()
    except AttributeError: # IPython can get pissed off when run in a test harness
        print 'Expected Fail... have a nice day...'

if __name__ == '__main__':
    test()
