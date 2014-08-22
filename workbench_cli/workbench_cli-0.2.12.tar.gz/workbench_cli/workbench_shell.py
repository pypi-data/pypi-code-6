"""Workbench Interactive Shell using IPython"""

import os, sys
import hashlib
import zerorpc
import IPython
import lz4
import inspect
import funcsigs
import operator
import matplotlib.pyplot as plt
plt.ion()
from colorama import Fore as F
import pprint

try:
    import pandas as pd
except ImportError:
    print '\n%sNotice: pandas not found...' % F.YELLOW
    print '\t%sWe recommend installing pandas: %s$ pip install pandas%s' % (F.BLUE, F.RED, F.RESET)

try:
    from . import client_helper
    from . import help_content
    from . import version
    from . import file_streamer
    from . import repr_to_str_decorator
    from . import auto_quote_xform

# Okay this happens when you're running in a debugger so having this is
# super handy and we'll keep it even though it hurts coverage score.
except (ImportError,ValueError):
    import client_helper
    import help_content
    import version
    import file_streamer
    import repr_to_str_decorator
    import auto_quote_xform


class WorkbenchShell(object):
    """Workbench CLI using IPython Interactive Shell"""

    def __init__(self):
        ''' Workbench CLI Initialization '''

        # Workbench CLI version
        self.version = version.__version__

        # Workbench CLI Help
        self.help = help_content.WorkbenchShellHelp()

        # Grab server arguments
        self.server_info = client_helper.grab_server_args()

        # Spin up workbench server
        self.workbench = None
        self._connect(self.server_info)

        # Create a user session
        self.session = self.Session()

        # We have a command_set for our Interactive Shell
        self.command_dict = self._generate_command_dict()
        self.command_set = set(self.command_dict.keys())

        # Our Interactive IPython shell
        self.ipshell = None

        # Our File Streamer
        self.streamer = file_streamer.FileStreamer(self.workbench, self._progress_print)

        # Register infomation (for help and other stuff) with Workbench
        self._register_info()

        # Help decorator
        self.help_deco = repr_to_str_decorator.r_to_s(self.workbench.help)

        # What OS/Version do we have?
        self.beer = '\360\237\215\272' if sys.platform == 'darwin' else ' '


    def load_sample(self, file_path, tags=None):
        """Load a sample (or samples) into workbench
            Args:
                file_path: path to a file or directory
                tags (optional): a list of tags for the sample/samples ['bad','aptz13']
            Returns:
                The list of md5s for all samples
        """

        # Recommend a tag
        if not tags:
            print '\n%sRecommended: Add a list of tags when you load samples. \
                   \n\t%sExamples: [\'bad\'], [\'good\'], [\'bad\',\'aptz13\']%s' % (F.YELLOW, F.GREEN, F.RESET)

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
                    print '%sStreaming Sample...%s' % (F.MAGENTA, F.RESET)
                    basename = os.path.basename(path)
                    md5 = self.streamer.stream_to_workbench(raw_bytes, basename, 'unknown', tags)

                print '\n%s  %s%s %sLocked and Loaded...%s\n' % \
                      (self.beer, F.MAGENTA, md5[:6], F.YELLOW, F.RESET)

                # Add tags to the sample
                self.workbench.add_tags(md5, tags)

                # Store information about the sample into the sesssion
                basename = os.path.basename(path)
                self.session.filename = basename
                self.session.md5 = md5
                self.session.short_md5 = md5[:6]
                self.ipshell.push({'md5': self.session.md5})
                self.ipshell.push({'short_md5': self.session.short_md5})

        # Dump out tag information
        self.tag_info()

    def tag_info(self):
        tags = self.workbench.get_all_tags()
        if not tags:
            return
        tag_df = pd.DataFrame(tags)
        tag_df = self.flatten_tags(tag_df)
        del tag_df['md5']
        del tag_df['tags']

        # Give aggregation counts
        tag_freq = tag_df.sum().to_dict()
        tag_freq = sorted(tag_freq.iteritems(), key=operator.itemgetter(1), reverse=True)
        print '\n%sSamples in Database%s' % (F.MAGENTA, F.RESET)
        for (tag, count) in tag_freq[:10]:
            print '  %s%s: %s%s%s' % (F.GREEN, tag, F.BLUE, count, F.RESET)

        # Give label correlations
        topN = 10
        count = 1
        sorted_series = tag_df.corr().unstack().order(ascending=False)
        print '\n%sCorrelated Tags%s' % (F.MAGENTA, F.RESET)
        for (name1, name2), value in sorted_series.iteritems():
            if name1==name2: continue
            if name1=='unknown' or name2=='unknown': continue
            print '  %s%s:%s %s%.1f%s' % (F.GREEN, name1, name2, F.BLUE, value, F.RESET)
            count += 1
            if count > topN: break

    def pull_df(self, md5):
        """Wrapper for the Workbench get_dataframe method
            Args:
                md5: pull the dataframe identified by this md5
            Returns:
                The uncompressed/unserialized dataframe
        """
        try:
            _packed_df = self.workbench.get_dataframe(md5)
            _df = pd.read_msgpack(lz4.loads(_packed_df))
            return _df
        except zerorpc.exceptions.RemoteError as e:
            return repr_to_str_decorator.r_to_s(self._data_not_found)(e)

    def flatten_tags(self, my_df):
        """Flatten(vectorize) the tags column in the dataframe"""
        tags_df = my_df['tags'].str.join(sep='-').str.get_dummies(sep='-')
        my_df['tags'] = [', '.join(tag_list) for tag_list in my_df['tags']]
        return my_df.join(tags_df)

    def search(self, tags=None):
        """Wrapper for the Workbench search method
            Args:
                tags: a single tag 'pcap' or a list of tags to search for ['bad','aptz13']
            Returns:
                A sample_set that contains the md5s for all matching samples
        """
        if isinstance(tags, str):
            tags = [tags]
        return self.workbench.generate_sample_set(tags)

    def versions(self):
        """Announce Versions of CLI and Server
            Args: None
            Returns:
                The running versions of both the CLI and the Workbench Server
        """
        print '%s<<< Workbench CLI Version %s >>>%s' % (F.BLUE, self.version, F.RESET)
        print self.workbench.help('version')

    def run(self):
        ''' Running the workbench CLI '''

        # Announce versions
        self.versions()

        # Sample/Tag info and Help
        self.tag_info()
        print '\n%s' % self.workbench.help('cli')

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
            config=cfg, banner1='', exit_msg='\nWorkbench has SuperCowPowers...')

        # Register our transformer, the shell will use this for 'shortcut' commands
        auto_quoter = auto_quote_xform.AutoQuoteTransformer(self.ipshell, self.ipshell.prefilter_manager)
        auto_quoter.register_command_set(self.command_set)

        # Setting up some Pandas options
        pd.set_option('display.width', 140)
        pd.set_option('max_colwidth', 15)

        # Start up the shell with our set of workbench commands
        self.ipshell(local_ns=self.command_dict)

    def _connect(self, server_info):
        """Connect to the workbench server"""

        # First we do a temp connect with a short heartbeat
        _tmp_connect = zerorpc.Client(timeout=300, heartbeat=2)
        _tmp_connect.connect('tcp://'+server_info['server']+':'+server_info['port'])
        try:
            _tmp_connect._zerorpc_name()
            _tmp_connect.close()
            del _tmp_connect
        except zerorpc.exceptions.LostRemote:
            print '%sError: Could not connect to Workbench Server at %s:%s%s' % \
                  (F.RED, server_info['server'], server_info['port'], F.RESET)
            sys.exit(1)

        # Okay do the real connection
        if self.workbench:
            self.workbench.close()
        self.workbench = zerorpc.Client(timeout=300, heartbeat=60)
        self.workbench.connect('tcp://'+server_info['server']+':'+server_info['port'])
        print '\n%s<<< Connected: %s:%s >>>%s' % (F.GREEN, server_info['server'], server_info['port'], F.RESET)

    def _progress_print(self, sent, total):
        """Progress print show the progress of the current upload with a neat progress bar
           Credits: http://redino.net/blog/2013/07/display-a-progress-bar-in-console-using-python/
        """
        percent = min(int(sent*100.0/total), 100)
        sys.stdout.write('\r{0}[{1}{2}] {3}{4}%{5}'.
                         format(F.GREEN, '#'*(percent/2), ' '*(50-percent/2), F.YELLOW, percent, F.RESET))
        sys.stdout.flush()

    def _work_request(self, worker, md5=None):
        """Wrapper for a work_request to workbench"""

        # I'm sure there's a better way to do this
        if not md5 and not self.session.md5:
            return 'Must call worker with an md5 argument...'
        elif not md5:
            md5 = self.session.md5

        # Is the md5 a sample_set?
        if self.workbench.is_sample_set(md5):
            return self.workbench.set_work_request(worker, md5)

        # Make the work_request with worker and md5 args
        try:
            return self.workbench.work_request(worker, md5)
        except zerorpc.exceptions.RemoteError as e:
            return repr_to_str_decorator.r_to_s(self._data_not_found)(e)

    def _data_not_found(self, e):
        """Message when you get a DataNotFound exception from the server"""
        return '%s%s%s' % (F.RED, e.msg, F.RESET)

    def _generate_command_dict(self):
        """Create a customized namespace for Workbench with a bunch of shortcuts
            and helper/alias functions that will make using the shell MUCH easier.
        """

        # First add all the workers
        commands = {}
        for worker in self.workbench.list_all_workers():
            commands[worker] = lambda md5=None, worker=worker: self._work_request(worker, md5)

        # Next add all the commands
        for command in self.workbench.list_all_commands():
            # Fixme: is there a better way to get the lambda function from ZeroRPC
            commands[command] = self.workbench.__getattr__(command)

        # Now the general commands which are often overloads
        # for some of the workbench commands
        general = {
            'workbench': self.workbench,
            'help': self._help,
            'load_sample': self.load_sample,
            'pull_df': self.pull_df,
            'flatten_tags': self.flatten_tags,
            'tag_info': self.tag_info,
            'search': self.search,
            'reconnect': lambda info=self.server_info: self._connect(info),
            'version': self.versions,
            'versions': self.versions,
            'short_md5': self.session.short_md5
        }
        commands.update(general)

        # Return the list of workbench commands
        return commands

    # Internal Class
    class Session(object):
        """Store information specific to the user session"""
        def __init__(self):
            """Initialization of Session object"""
            self.filename = None
            self.md5 = None
            self.short_md5 = '-'
            self.server = 'localhost'
    
    def _register_info(self):
        """Register local methods in the Workbench Information system"""
        # Stores information on Workbench commands and signatures
        for name, meth in inspect.getmembers(self, predicate=inspect.isroutine):
            if not name.startswith('_') and name != 'run':
                info = {'command': name, 'sig': str(funcsigs.signature(meth)), 'docstring': meth.__doc__}
                self.workbench.store_info(info, name, 'command')

        # Register help information
        self.workbench.store_info({'help': self.help.help_cli()}, 'cli', 'help')
        self.workbench.store_info({'help': self.help.help_cli_basic()}, 'cli_basic', 'help')
        self.workbench.store_info({'help': self.help.help_cli_search()}, 'search', 'help')
        self.workbench.store_info({'help': self.help.help_dataframe()}, 'dataframe', 'help')
        self.workbench.store_info({'help': self.help.help_dataframe_memory()}, 'dataframe_memory', 'help')
        self.workbench.store_info({'help': self.help.help_dataframe_pe()}, 'dataframe_pe', 'help')
 
    def _help(self, topic=None):
        """Help wrapper for Workbench CLI"""
        if not topic:
            topic = 'cli'
        return self.help_deco(topic)

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
