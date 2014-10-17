#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""The data module contains definitions of data used in drove
client-server communication
"""

import os
from ..importer import Importer


class Daemon(object):
    @classmethod
    def create(cls, handler, exit_handler=None):
        importer = Importer("drove.daemon", class_suffix="Daemon")
        if os.name == "posix":
            return importer(os.name, handler, exit_handler)
        else:
            raise NotImplementedError("The platform '%s' " % (os.name,) +
                                      "is not supported yet. Please drop us " +
                                      "a line if you are interesting in " +
                                      "porting drove to this platform.")
