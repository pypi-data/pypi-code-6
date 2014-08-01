#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Workbench Interactive Shell using IPython"""
import os, sys
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

        # Capture the original line
        orig_line = line

        # Very conservative logic (but possibly flawed)
        # 1) Lines with any of these symbols ; , ' " ( ) aren't touched
        # 2) Need to have more than one token
        # 3) First token in line must be in the workbench command set
        # 4) If first token is 'help' than all other tokens are quoted
        # 5) Otherwise only tokens that are not in any of the namespace are quoted


        # 1) Lines with any of these symbols ; , ' " ( ) aren't touched
        skip_symbols = [';',',','\'','"','(',')']
        if any([sym in line for sym in skip_symbols]):
            return line

        # Build up token set and info
        token_list = re.split(' |;|,|(|)|\'|"', line)
        num_tokens = len(token_list)
        first_token = token_list[0]
        token_set = set(token_list)
        if None in token_set: # In some cases None creeps in
            token_set.remove(None)

        # 2) Need to have more than one token
        # 3) First token in line must be in the workbench command set
        if num_tokens > 1 and first_token in self.command_set:

            # 4) If first token is 'help' than all other tokens are quoted
            if first_token == 'help':
                token_set.remove('help')
                for token in token_set:
                    line = line.replace(token, '"'+token+'"')

            # 5) Otherwise only tokens that are not in any of the namespace are quoted
            else: # Not help
                ns_token_set = set([token for nspace in self.shell.all_ns_refs for token in nspace])
                for token in token_set:
                    if token not in ns_token_set:
                        line = line.replace(token, '"'+token+'"')

        # Push out the processed line and return it
        if orig_line != line:
            self.shell.auto_rewrite_input(line)
        return line

class WorkbenchShell(object):
    """Workbench CLI using IPython Interactive Shell"""

    def __init__(self):
        ''' Workbench CLI Initialization '''

        # Grab server arguments
        self.server_info = client_helper.grab_server_args()

        # Spin up workbench server
        self.connect(self.server_info)

        # Create a user session
        self.session = self.Session()

        # We have a command_set for our Interactive Shell
        self.command_dict = self._generate_command_dict()
        self.command_set = set(self.command_dict.keys())

        # Our Interactive IPython shell
        self.ipshell = None

        # What OS/Version do we have?
        self.beer = '\360\237\215\272' if sys.platform == 'darwin' else ' '

    # Internal Classes
    class Session(object):
        """Store information specific to the user session"""
        def __init__(self):
            """Initialization of Session object"""
            self.filename = None
            self.md5 = None
            self.short_md5 = '-'
            self.server = 'localhost'

    # Helper Methods
    def connect(self, server_info):

        # First we do a temp connect with a short heartbeat
        _tmp_connect = zerorpc.Client(timeout=300, heartbeat=2)
        _tmp_connect.connect('tcp://'+server_info['server']+':'+server_info['port'])
        try:
            _tmp_connect._zerorpc_name()
            _tmp_connect.close()
        except zerorpc.exceptions.LostRemote:
            print '%sError: Could not connect to Workbench Server at %s:%s%s' % \
                  (Fore.RED, server_info['server'], server_info['port'], Fore.RESET)
            exit(1)

        # Okay do the real connection
        self.workbench = zerorpc.Client(timeout=300, heartbeat=60)
        self.workbench.connect('tcp://'+server_info['server']+':'+server_info['port'])
        print '\t%s- Connected to Server: (%s:%s)%s' % (Fore.GREEN, server_info['server'], server_info['port'], Fore.RESET)

    def progress_print(self, sent, total):
        """Progress print show the progress of the current upload with a neat progress bar
           Credits: http://redino.net/blog/2013/07/display-a-progress-bar-in-console-using-python/
        """
        percent = min(int(sent*100.0/total),100)
        sys.stdout.write('\r{0}[{1}{2}] {3}{4}%{5}'.format(Fore.GREEN, '#'*(percent/2),
            ' '*(50-percent/2), Fore.YELLOW, percent, Fore.RESET))
        sys.stdout.flush()

    @staticmethod
    def chunks(data, chunk_size):
        """ Yield chunk_size chunks from data."""
        for i in xrange(0, len(data), chunk_size):
            yield data[i:i+chunk_size]

    def file_chunker(self, filename, raw_bytes, type_tag):
        """Split up a large file into chunks and send to Workbench"""
        md5_list = []
        sent_bytes = 0
        mb = 1024*1024
        chunk_size = 1*mb # 1 MB
        total_bytes = len(raw_bytes)
        for chunk in self.chunks(raw_bytes, chunk_size):
            md5_list.append(self.workbench.store_sample(filename, chunk, type_tag))
            sent_bytes += chunk_size
            self.progress_print(sent_bytes, total_bytes)
            # print '\t%s- Sending %.1f MB (%.1f MB)...%s' % (Fore.YELLOW, sent_bytes/mb, total_bytes/mb, Fore.RESET)

        # Now we just ask Workbench to combine these
        return self.workbench.combine_samples(md5_list, filename, type_tag)

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
                    print '%sStreaming Sample...%s' % (Fore.MAGENTA, Fore.RESET)
                    basename = os.path.basename(path)
                    md5 = self.file_chunker(basename, raw_bytes, 'unknown')

                print '\n%s  %s%s %sLocked and Loaded...%s\n' % \
                      (self.beer, Fore.MAGENTA, md5[:6], Fore.YELLOW, Fore.RESET)

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
            'reconnect': lambda info=self.server_info: self.connect(info),
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
