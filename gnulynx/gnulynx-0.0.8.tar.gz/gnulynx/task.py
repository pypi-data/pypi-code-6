#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import argparse
import time 
import logging

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

from cli_util import (
  read_stdin,
  write_stdout,
  write_stderr,
  read_positional_kwargs,
  install_arguments,
  install_default_arguments,
  opts_to_kwargs,
  parse_arg
  )

from serialize import from_yaml, from_json
from exceptions import GnuTaskInitError, GnuTaskIOError

# configure logging.
logging.basicConfig()

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

  stdout = True
  requires_kwargs = True
  log = logging.getLogger("gnulynx")

  # PUBLIC METHODS #

  def configure(self):
    """
    Add objects to self before running `main`.
    """
    pass


  def main(self, **kw):
    """
    Primary nethod to overwrite.
    Use kwargs/opts to run a function
    and yield objects which are 
    json-serializable.

    If the point is to store input, 
    eg self.stdout = False,
    then this function should return
    nothing.
    """
    raise NotImplementedError(
      'You must define `main` to run a GnuTask.'
      )

  def complete(self):
    """
    Perform tasks after completion of `main`.
    """
    pass

  def cli(self):
    try:
      # setup cli 
      self._setup_cli()

      # configure task
      self.configure()
      
      # run main
      self._run()

      # run complete
      self.complete()
    except Exception as e:
      self.log.error('ERROR ERROR ERROR')
      self.log.error(e)

  # INTERNAL METHODS #

  def _setup_cli(self):
    self._load_config()
    self._install_parser()
    self._parse_args()

  def _load_config(self):
    """
    Load yaml config
    """
    # get the scripts directory
    directory = os.path.dirname(os.path.realpath(__name__))

    # generate yml filepath
    path_to_config = os.path.join(directory, sys.argv[0].replace('.py', '.yml'))
    
    # check if it exists
    if os.path.exists(path_to_config):
      self.config = from_yaml(open(path_to_config).read())
    
    # default to empty dict
    else:
      self.config = {}

  def _install_parser(self):
    """ 
    Install a parser based on yaml config
    """
    self.parser = argparse.ArgumentParser()
    install_default_arguments(self.parser)

    if 'arguments' in self.config:
      install_arguments(self.parser, self.config['arguments'])

  def _parse_args(self):
    
    # get obj
    self._opts = self.parser.parse_args()
    
    # set defaults
    self.passthrough = parse_arg(self._opts.passthrough)
    self.queue_size = parse_arg(self._opts.queue_size)
    self.quiet = parse_arg(self._opts.quiet)
    self.add_kwargs = [k.strip() for k in self._opts.add.split(',') if k.strip() != ""]
    self.add = len(self.add_kwargs) > 0

    # get options
    self.opts = opts_to_kwargs(self._opts)

    # set logging level
    self.log.setLevel(logging.WARNING if self.quiet else logging.INFO)

  def _check_kwargs(self, line):
    """
    Check kwargs for presence of required/accepted fields.
    """
    accepts = self.config.get('accepts', None)
    requires = self.config.get('requires', None)
    keys = line.keys()

    # test for unaccepted keys
    if accepts:
      for k in keys:
        if k not in accepts:
            raise GnuTaskInitError(
              'Unregonzized kwarg: ' + k
              )

    # test for requires keys
    if requires:  
      for r in requires:
        if r not in keys:
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
    if self._opts.kwargs is None:
      if self.requires_kwargs:
        for line in read_stdin():
          yield self._process_line(line)
      else:
        # just yield and empty dict
        yield {}

    else:
      for line in read_positional_kwargs(self._opts.kwargs):
        yield self._process_line(line)

  def _add_kwargs(self, in_, out_):
    """
    optionally join input kwargs with output.
    """
    for k,v in in_.items():
      if k in self.add_kwargs:
        out_.update({k:v})
    return out_

  def _read(self):
    """
    Read in kwargs, 
    pass to _process.
    """
    for kw in self._process_kwargs():
      self._tasks.put(kw)


  def _write(self):
    """
    Process kwargs via main.
    optionally write to stdout
    """
    while not self._tasks.empty():
      
      kw = self._tasks.get()

      # if we're writing to stdout...
      if self.stdout:
        l = self.main(**kw)
        for obj in l:

          # optionally add input kwargs
          if self.add:
            obj = self._add_kwargs(kw, obj)
          
          # write to stdout
          write_stdout(obj)

      # otherwise assume we're
      # writing somewhere
      else:
        self.main(**kw)

        # if passthrough, write input to stdout
        if self.passthrough:
          write_stdout(kw)


  def _run(self):
    """
    Spawn read/write queue
    If queue_size == 1,
    run serially.
    """

    if self.queue_size > 1:
      self._tasks = Queue()
      gevent.spawn(self._read).join()
      gevent.joinall([
        gevent.spawn(self._write)
          for w in xrange(self.queue_size)
        ])

    else:
      for kw in self._process_kwargs():
        if self.stdout:
          for obj in self.main(**kw):
            if self.add:
              obj = self._add_kwargs(kw, obj)
            write_stdout(obj)
        else:
          self.main(**kw)

          if self.passthrough:
            write_stdout(kw)

