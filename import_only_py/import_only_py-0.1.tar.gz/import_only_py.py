"""Module to restrict imports from specific directories to .py files only.

This is free software, Apache License 2.0. There is NO WARRANTY. Use at your
own risk.

This module is compatible with Python 2.4, 2.5, 2.6 and 2.7 (but not 3.x).

More info about find_module and load_module:
http://legacy.python.org/dev/peps/pep-0302/
"""

import os
import os.path
import sys

__author__ = 'pts@fazekas.hu (Peter Szabo)'


def import_only_py_sources(basedir):
  """Sets up that only .py files can be imported from basedir (recursively).

  Also makes sure that .pyc files are not used or generated for such imports.
  """
  if not isinstance(basedir, str):
    raise TypeError
  if not os.path.isabs(basedir):
    basedir = os.path.abspath(basedir)
  else:
    items = basedir.split(os.sep)
    if '.' in items or '..' in items:
      basedir = os.path.abspath(basedir)

  def finder(path_entry):
    is_in = (path_entry.startswith(basedir) and
        '/'.startswith(path_entry[len(basedir) : len(basedir) + 1]))
    if not is_in:
      raise ImportError  # Try another Finder.
    return _OnlyPyFinder(path_entry)

  sys.path_importer_cache.pop(basedir, None)
  finder.basedir = basedir
  for finder0 in sys.path_hooks:
    if (getattr(finder0, 'func_code', None) is finder.func_code and
        finder0.basedir == basedir):
      break  # Already registered.
  else:
    sys.path_hooks.append(finder)
  

class _OnlyPyFinder(object):
  """Helper class for finding .py source files."""

  def __init__(self, path_entry):
    self.path_entry = path_entry

  def find_module(self, fullname):  # Called by Python.
    filename = fullname[fullname.rfind('.') + 1:].replace('.', os.path.sep)
    filename_dir = os.path.join(filename, '__init__.py')
    filename_file = filename + '.py'
    has_file = os.path.isfile(os.path.join(self.path_entry, filename_file))
    has_dir = os.path.isdir(os.path.join(self.path_entry, filename))
    if has_dir:
      pathname = os.path.join(self.path_entry, filename_dir)
    elif has_file:
      pathname = os.path.join(self.path_entry, filename_file)
    else:
      return  # Not found, will be looked at next entry in sys.path.
    return _OnlyPyLoader(fullname, pathname, has_file, has_dir)


class _OnlyPyLoader(object):
  """Helper class for loading .py source files without creating .py files."""

  def __init__(self, fullname, pathname, has_file, has_dir):
    self.fullname = fullname
    self.pathname = pathname
    self.has_file = has_file
    self.has_dir = has_dir

  def load_module(self, fullname):  # Called by Python.
    assert fullname == self.fullname, (fullname, self.fullname)
    if fullname in sys.modules:
      # TODO(pts): What to do with reload(...)?
      raise ImportError('Module already imported: ' + fullname)
    if self.has_file and self.has_dir:
      raise ImportError('Ambiguous import of %s: dir vs file: %s' %
                        (fullname, self.pathname))
    # True but we'd need `import imp': assert imp.lock_held()
    # TODO(pts): Add support for .so (.dll) files (but not .pyc).
    if not os.path.isfile(self.pathname):
      # Mostly for a missing __init__.py.
      raise ImportError('Source file not found: ' + self.pathname)
    f = open(os.path.join(self.pathname), 'U')
    try:
      mod = type(sys)(fullname)  # Create new module.
      sys.modules[fullname] = mod
      mod.__file__ = self.pathname
      if self.has_dir:
        mod.__path__ = [os.path.dirname(self.pathname)]
      # Why we don't use imp.load_module: it generates .pyc files, and it can't
      # load __init__.py with the proper .__path__ correctly.
      exec f in mod.__dict__  # Respects `coding:' etc.
    finally:
      f.close()
    return mod
