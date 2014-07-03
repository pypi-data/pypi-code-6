import sys 
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
  read_positional_kwargs
  )

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

  def configure(self):
    """
    Add objects to self for exection in 
    `self.main`
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

  def run(self):
    # configure task
    self.configure()
    
    if not self.concurrent:
      self._run_non_concurrent()

    else:
      self._run_concurrent()

  # INTERNAL METHODS #

  def _process_kwargs(self):
    """
    Process kwargs from various sources
    """
    try:
      kw = sys.argv[1]
    except IndexError:
      kw = None

    # if no positional kwargs, read fron stdin
    if kw is None:
      return read_stdin()

    else:
      return read_positional_kwargs(kw)

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
      
      if self.stdout:
        for obj in self.main(**kw):
        # if we're writing to stdout...
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

