#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# (c) 2011 Mouad Benchchaoui
# Licensed under the BSD license:
# http://www.opensource.org/licenses/bsd-license.php
"""Locate a python object (package, module, function, class ...) source file.

Usage:
   pywhereis [OPTIONS] dotted_name...

Options:
   -h, --help: print the help message and exit.
   -v, --verbose: Enable the verbose mode.
   -s, --site-packages: Search in site-packages before current directory.

"""


import os
import sys
import getopt
import pkgutil
import inspect
import warnings
import zipimport


def _normalize_path(filepath):
    "Normalize file path."""
    return os.path.normcase(os.path.realpath(filepath))


class LocateError(Exception):
    "Error raised when locating an object fail."


def _safe_import(name, **kws):
    """Importer that always raise ImportError when the import fail.

    Arguments:
       - name: A dotted-name in the same syntax for importing.
       - kws: Extra keywords argument, the same one accepted by ``__import__``
              function.
    Return:
       The imported object representing ``name``.
    Raise:
       ImportError: If in any case the import fail.

    """
    try:
        return __import__(name, **kws)
    except ValueError:
        raise ImportError('Empty module name.')
    except:
        # Broken modules end up here.
        ex = sys.exc_info()[1]
        raise ImportError(str(ex))


def resolve(name):
    """Resolve an object by dotted path/name.

    Arguments
       name: A dotted-name in the same syntax used for importing.
    Return:
       The object representing the dotted_name.
    Raise:
       ImportError: If the import fail.

    """
    path = name.split('.')
    current = path[0]
    found = _safe_import(current)
    for part in path[1:]:
        current += '.' + part
        try:
            found = getattr(found, part)
        except AttributeError:
            found = _safe_import(current, fromlist=part)
    return found


def _get_filename(loader, name):
    "get the method ``get_filename`` from ``pkgutil.ImpLoader`` class."
    # In Python 2.6 ``zipimport.zipimporter`` don't have a ``get_filename``
    # method  but the PEP 302 feature was implemented under ``_get_filename``
    # b/c of backward compatibility.
    try:
        return loader.get_filename(name)
    except AttributeError:
        try:
            return loader._get_filename(name)
        except AttributeError:
            pass


def _locate_without_import(name):
    """locate ``name`` source file or directory w/o trying to import it.

    To overcome places where the import will fail e.g. broken module .., this
    function use ``pkgutil.get_loader`` instead, which will work fine for
    module and packages but not for function, class ... .

    """
    # Don't try to locate empty string b/c when an empty string is passed to
    # ``pkgutil.get_loader`` this latest return the first module found in
    # python2.
    if not name:
        raise LocateError('Invalid object %r' % name)

    try:
        loader = pkgutil.get_loader(name)
        if not loader:
            return
    except (ImportError, AttributeError):  # http://bugs.python.org/issue14710
        # If ``pkgutil.get_loader`` fail we can still try using import.
        return
    except Exception:
        # Raised when name is a broken module and ``pkgutil.get_loader`` try to
        # import it to accept the module member e.g. broken_module.whatever.
        raise LocateError(str(sys.exc_info()[1]))

    filename = None
    # In case loader is wrapped in a zipimporter i.e. eggs, zip, the method
    # ``get_filename`` accept the name of the module to check for.
    if isinstance(loader, zipimport.zipimporter):
        filename = _get_filename(loader, name)
    else:
        # Python 3.2 and below
        try:
            filename = loader.get_filename()
        except AttributeError:
            try:
                # XXX: Only importlib.machinery.SourceFileLoader is supported.
                filename = loader.path
            except AttributeError:
                pass
    return filename


def locate(name):
    """locate ``name`` source file or directory.

    Arguments:
       - name: A dotted-name in the same syntax used for importing.
    Return:
       A string representing the path of the ``name`` object if this latest was
       found.
    Raise:
       LocateError: When locating ``name`` fail.

    """
    # First try locating an object w/o importing it.
    result = _locate_without_import(name)
    if result:
        return _normalize_path(result)

    try:
        obj = resolve(name)
    except ImportError:
        raise LocateError('object %r not found.' % name)

    try:
        sourcefile = inspect.getsourcefile(obj)
        # Looking at getsourcefile code, we see that this later can return
        # None instead of raising TypeError, so we do it in her place.
        if not sourcefile:
            raise TypeError
    except TypeError:
        raise LocateError('%r is not pure python.' % obj)

    output = _normalize_path(sourcefile)
    # Print also the line number of the object if it's not a module.
    if not inspect.ismodule(obj):
        line = inspect.getsourcelines(obj)[1]
        output += ' %d' % line
    return output


def usage(err_msg=None):
    """Print error message and usage string."""
    if err_msg:
        sys.stderr.write('Error: %s' % err_msg)
        sys.stderr.write('\n\n')
    sys.stderr.write(__doc__)


def main(argv=sys.argv[1:]):
    """Main function."""
    try:
        opts, args = getopt.getopt(
            argv, 'hvs', ('help', 'verbose', 'site-packages'))
    except getopt.GetoptError:
        usage(sys.exc_info()[1])
        return 1

    verbose = 0
    # Set to true to start searching in site_packages first or false to search
    # in current directory first.
    site_packages = False
    for opt, _ in opts:
        if opt in ('-h', '--help'):
            return usage()
        elif opt in ('-v', '--verbose'):
            verbose = 1
        elif opt in ('-s', '--site-packages'):
            if sys.version_info >= (3, 3):
                warnings.warn(
                    'Python 3.3 and above use absolute import by default !')
            site_packages = True

    if not args:
        usage('No name was given.')
        return 1

    # Save the current sys.path to recover it in the end of the function.
    original_sys_path = sys.path[:]
    if site_packages:
        sys.path.append('.')  # Add current directory to the last.
    else:
        # Add the current directory in the first.
        sys.path.insert(0, '.')

    try:
        for dotted_name in args:
            res = ''
            try:
                res = locate(dotted_name)
            except LocateError:
                if verbose:
                    res = 'Error: %s' % sys.exc_info()[1]
            print('%s: %s' % (dotted_name, res))
    finally:
        sys.path = original_sys_path


if __name__ == '__main__':
    sys.exit(main())
