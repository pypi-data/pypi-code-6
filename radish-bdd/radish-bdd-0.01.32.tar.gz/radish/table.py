# -*- coding: utf-8 -*-

import traceback
import inspect
import sys
import re

from radish.timetracker import Timetracker
from radish.config import Config
from radish.utilregistry import UtilRegistry
from radish.exceptions import ValidationError, RadishError

class Property:
    pass

class Table:
    def __init__(self):
        self._table = [] 

    def create_instance(self):
        ret = Property()
        for row in self._table:
            assert len(row) > 1
            setattr(ret, row[0].strip(), row[1].strip())
        return ret

    def create_set(self):
        ret = []
        column_names = self._table[0]
        for row in self._table[1:]:
            pp = Property()
            for ii in range(len(column_names)):
                setattr(pp, column_names[ii].strip(), row[ii].strip())
                pass
            ret.append(pp)
        return ret

    def append(self, columns):
        self._table.append(columns)

    def length(self):
        return len(self._table)
