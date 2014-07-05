import sys, os
import argparse

import gevent
from gevent.queue import Queue

# patch everything except for thread.
import gevent.monkey
gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()
gevent.monkey.patch_os()
gevent.monkey.patch_time()
gevent.monkey.patch_select()
gevent.monkey.patch_subprocess()

from util import (
  read_stdin,
  write_stdout,
  read_positional_kwargs,
  install_arguments,
  opts_to_kwargs
  )

from serialize import from_yaml
from exceptions import GnuTaskInitError, GnuTaskIOError

class GnuTask:
  """
  A GnuTask does three things:
  
  1. process json strings, 
     json / yml filepaths,
     or json from stdin
     which represent a single dictionary
     or input kwargs.
  2. given the kwargs, performs a user-specified task.
  3. streams json to stdout.
  TODO: ADD CLI ARGUMENT INTEGRATION
  """

  # DEFAULTS #

  concurrent = True
  num_workers = 10
  stdout =  True


  # PUBLIC METHODS #

  def configure(self, **opts):
    """
    Add objects to self for exection in 
    `main` from cli flags.
    """
    pass


  def main(self, **kw):
    """
    Method to overwrite.
    Use kwargs to run a function
    and returns objects which are 
    json-serializable.

    If the point is to store input, 
    eg self.stdout = False,
    then this function should return
    nothing.
    """
    raise NotImplementedError(
      'You must define `main` to run a GnuTask.'
      )

  def cli(self):
    
    # setup cli 
    self._setup_cli()

    # configure task
    self.configure(**self.opts)
    
    if not self.concurrent:
      self._run_non_concurrent()

    else:
      self._run_concurrent()


  # INTERNAL METHODS #
  def _load_config(self):
    """
    Load yaml config
    """
    directory = os.path.dirname(os.path.realpath(__name__))
    path_to_config = os.path.join(directory, sys.argv[0]).replace('.py', '.yml')
    if os.path.exists(path_to_config):
      self.config = from_yaml(open(path_to_config).read())
    
    else:
      self.config = {}

  def _install_parser(self):
    """
    Install a parser based on yaml config
    """
    self.parser = argparse.ArgumentParser()
    self.parser.add_argument(
      'kw',
      help="The json kwargs / yaml or json file to pass into the function.\nIf not present, read from stdin.", 
      nargs = "?"
    )
    if 'arguments' in self.config:
      install_arguments(self.parser, self.config['arguments'])

  def _parse_args(self):
    self.cli_opts = self.parser.parse_args()
    self.opts = opts_to_kwargs(self.cli_opts)

  def _setup_cli(self):
    self._load_config()
    self._install_parser()
    self._parse_args()

  def _check_kwargs(self, line):
    """
    Check kwargs for presence of required fields.
    """
    if self.config.has_key('requires'):
      for r in self.config['requires']:
        if r not in line.keys():
          raise GnuTaskInitError(
            'Function missing required kwarg: ' + r
            ) 

  def _process_line(self, line):
    """
    Take a line of input and combine it with options.
    """
    self._check_kwargs(line)
    return line

  def _process_kwargs(self):
    """
    Process kwargs from various sources
    """

    # if no positional kwargs, read fron stdin
    if self.cli_opts.kw is None:
      for line in read_stdin():
        yield self._process_line(line)

    else:
      for line in read_positional_kwargs(kw):
        yield self._process_line(line)


  def _read(self):
    """
    Read in kwargs, 
    pass to _process.
    """
    for kw in self._process_kwargs():
      self._tasks.put(kw)


  def _process(self):
    """
    Process kwargs via main, 
    pass to _write.
    """
    while not self._tasks.empty():
      kw = self._tasks.get()
      
      # if we're writing to stdout...
      if self.stdout:
        for obj in self.main(**kw):
          write_stdout(obj)

      # otherwise assume we're
      # writing somewhere
      else:
        self.main(**kw)


  def _run_concurrent(self):
    self._tasks = Queue(self.num_workers)
    gevent.spawn(self._read)
    gevent.joinall([
      gevent.spawn(self._process)
        for w in xrange(self.num_workers)
      ])


  def _run_non_concurrent(self):
    # iterate through kwargs and run task(s).    
    for kw in self._process_kwargs():
      for obj in self.main(**kw):
        
        # if we're writing to stdout:
        if self.stdout:
          write_stdout(obj)

        # otherwise pass
        else:
          pass

