import sys 
import fileinput
import argparse

from exceptions import GnuTaskIOError
from serialize import (
  json_from_string,
  yaml_from_string,
  json_to_string
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
  """

  def _process_kwargs(self):
    """
    Process kwargs from various sources
    """
    try:
      kw = sys.argv[1]
    except IndexError:
      kw = None

    # if no args, read fron stdin
    if kw is None:
      kwargs = []
      try:
        lines = sys.stdin.readlines()
      except IOError:
        raise GnuTaskIOError(
          'If no arg is prsent, the task assumes input from stdin.'
          )
      else:
        for l in lines:
          if l.strip() != '':
            yield json_from_string(l)

    else:
      yield json_from_string(kw)

  def main(self, **kw):
    """
    Method to overwrite.
    Use kwargs to run a function
    that yields objects
    which are json-serializable.
    """
    for i in range(0,1):
      yield kw

  def run(self):
    """
    Run and stream line-separated json
    """
    kw = self._process_kwargs()

    for k in kw:
      # pass to main
      for obj in self.main(**k):

        # format line-separated json
        line = json_to_string(obj) + "\n"
        
        # write to stdout
        sys.stdout.write(line)


