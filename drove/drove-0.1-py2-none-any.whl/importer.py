#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""This module contains classes and methods to import dynamically modules
from specified paths."""

import sys


class Importer(object):
    def __init__(self,
                 parent_module=None,
                 class_prefix='',
                 class_suffix='',
                 path=[]):
        """Load a class from module in specified directory.

        For example if you have a module ``example`` with a ``myclass.py``
        inside, which contains the class ``Myclass`` then you can use:

        >>> x = ModuleImporter('example')
        >>> x('myclass')

        When calling the object you can also pass a number of variable
        arguments which will be used as parameters for the ``__init__``
        of the object.

        :type parent_module: str
        :param parent_module: the parent module where other submodules
                              and classes lives.
        :type class_prefix: str
        :param class_prefix: the prefix for classes to load.
        :type class_suffix: str
        :param class_suffix: the suffix for classes to load.
        :type path: str
        :param path: a path to find the module if it's not present
            in default library.
        """
        self.path = path
        self.parent_module = parent_module
        self.class_prefix = class_prefix
        self.class_suffix = class_suffix

        if not self.path and self.parent_module is None:
            raise ImportError("path or parent_module is required for Importer")

    def __call__(self, name, *args, **kwargs):
        if self.path:
            sys.path.extend(self.path)
            full_path = name
        else:
            full_path = "%s.%s" % (self.parent_module, name,)

        try:
            mod = __import__("%s" % (full_path,),
                             globals(),
                             locals(),
                             ["%s%s%s" % (self.class_prefix,
                                          name.title(),
                                          self.class_suffix)])
        finally:
            for p in self.path:
                if p in sys.path:
                    sys.path.remove(p)

        kls = getattr(mod, "%s%s%s" % (self.class_prefix,
                                       name.title(),
                                       self.class_suffix))

        obj = kls(*args, **kwargs)
        obj.importer_name = name
        return obj
