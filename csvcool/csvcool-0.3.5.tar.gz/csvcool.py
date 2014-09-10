#!/usr/bin/env python
#-*-coding:utf-8-*-

# "THE WISKEY-WARE LICENSE":
# <jbc.develop@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a WISKEY in return Juan BC


#===============================================================================
# DOC
#===============================================================================

"""Cool way to deal with 'headed' CSV

Rules of the parser
    1 - First row is a list of column names.
    2 - All rows have the same numbers of columns.
    3 - Empty column names are ignored.
    4 - Columns without name are ignored.

Example:

    +-------+-------+----+-------+----+
    | name0 | name1 |    | name3 |    |
    +-------+-------+----+-------+----+
    | v0    |       | v2 | v3    | v4 |
    +-------+-------+----+-------+----+

Equivalent:

    +-------+-------+-------+
    | name0 | name1 | name3 |
    +-------+-------+-------+
    | v0    |       | v2    |
    +-------+-------+-------+

Use:

    >>> import csvcool
    >>> cool = csvcool.read(open("path/to/csv"))
    >>> cool[0]["name0"]
    v0
    >>> cool[0]["name0"] = 1
    >>> cool[0]["name0"]
    1
    >>> csvcool.write(cool, open("path/to/csv", "w"))


"""

#===============================================================================
# META
#===============================================================================

__version__ = "0.3.5"
__license__ = "WISKEY-WARE"
__author__ = "JBC"
__email__ = "jbc dot develop at gmail dot com"
__url__ = "http://bitbucket.org/leliel12/csvcool"
__date__ = "2011-05-22"


#===============================================================================
# IMPORTS
#===============================================================================

import csv


#===============================================================================
# GLOBALS
#===============================================================================

# contains all validator and conversors
_v_and_c = {}


#===============================================================================
# CLASS FROZEN ROW
#===============================================================================

class FrozenRow(object):
    """Esentialy is a "key" fixed dict"""

    def __init__(self, **kwargs):
        """Creates a new instances of a FrozenRow"""
        self._d = kwargs

    def __eq__(self, obj):
        """x.__eq__(obj) <==> x==obj"""
        return isinstance(obj, self.__class__) and self._d == obj._d

    def __ne__(self, obj):
        """x.__ne__(obj) <==> x!=obj"""
        return not self == obj

    def __contains__(self, key):
        """x.__contains__(key) <==> key in x"""
        return key in self._d

    def __getitem__(self, key):
        """x.__getitem__(key) <==> x[key]"""
        return self._d[key]

    def __setitem__(self, key, value):
        """x.__setitem__(key, value) <==> x[key]=y (only if key in D)"""
        if key not in self._d:
            raise KeyError(key)
        self._d[key] = value

    def __len__(self):
        """x.__len__() <==> len(x)"""
        return len(self._d)

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        return iter(self._d)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return "<%s: %s>" % (self.__class__.__name__, repr(self._d))

    def items(self):
        """ D.items() -> list of D's (key, value) pairs, as 2-tuples"""
        return self._d.items()

    def keys(self):
        """D.keys() -> list of D's keys"""
        return self._d.keys()

    def values(self):
        """D.values() -> list of D's values"""
        return self._d.values()

    def get(self, key, default=None):
        """D.get(key[,default]) -> D[key] if key in D, else default.
        default = None."""
        return self._d.get(key, default)


#===============================================================================
# CLASS CSV COOL
#===============================================================================

class CSVCool(object):
    """The CSVCool object is the coolest way to manipulate CSV files."""

    def __init__(self, keys, rows, encoding=None):
        """Creates the new instances of the CSVCool

        @param keys: The first row of the CSV file
        @param rows: All rows of the CSV file except the first one
        """
        self._encoding = encoding
        self._columnnames = keys
        self._rows = []
        for row in rows:
            kdata = zip(keys, row)
            row = FrozenRow(**dict(kdata))
            self._rows.append(row)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return "%s (%i columns x %i rows) at %s" % (self.__class__.__name__,
                                                     len(self.columnnames),
                                                     len(self.rows),
                                                     hex(id(self)))
    def __eq__(self, obj):
        """x.__eq__(obj) <==> x == obj"""
        return isinstance(obj, self.__class__) \
               and self.columnnames == obj.columnnames \
               and self.rows == obj.rows


    def __ne__(self, obj):
        """x.__ne__(obj) <==> x != obj"""
        return not (self == obj)

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        return iter(self._rows)

    def __getitem__(self, idx):
        """x.__getitem__(idx) <==> x[idx]"""
        return self._rows[idx]

    def __len__(self):
        """x.__len__() <==> len(x)"""
        return len(self._rows)

    def __contains__(self, row):
        """x.__contains__(row) <==> row in x

        row can be any iterable with columns order or a frozenrow.

        """
        if not isinstance(row, FrozenRow):
            if len(row) != len(self.columnnames):
                return False
            row = FrozenRow(**dict(zip(self._columnnames, row)))
        return row in self._rows

    def discover_types(self, order=(bool, int, float, type(None), str)):
        """Try to infer the type of columns of a CSVCool instance

        @params order: The order of a register validator types to test

        Example:

            original

                +--------+-------+-------+
                | name0  | name1 | name2 |
                +--------+-------+-------+
                | "True" | "v2"  | "0.0" |
                +--------+-------+-------+

            original.discover_types()
            {"name0": bool, "name1": str, "name2": float}

        """
        types = {}
        for cn in self.columnnames:
            column = self.column(cn)
            for t in order:
                if all(map(_v_and_c[t]["validator"], column)):
                    break
            types[cn] = t
        return types

    def type_corrector(self, column_types):
        """Uses a dictionary with "columnname => type" structure to creates
        a new CSVCool instance with the correct registered type.

        Example:

            original

                +--------+-------+-------+
                | name0  | name1 | name2 |
                +--------+-------+-------+
                | "True" | "v2"  | "0.0" |
                +--------+-------+-------+

            original.discover_types()
            {"name0": bool, "name1": str, "name2": float}

            original.type_corrector(original.discover_types())

                +--------+-------+-------+
                | name0  | name1 | name2 |
                +--------+-------+-------+
                | True   | "v2"  |  0.0  |
                +--------+-------+-------+

        """
        correct = []
        for row in self:
            crow = []
            for cname in self.columnnames:
                ctype = column_types[cname]
                conversor = _v_and_c[ctype]["conversor"]
                crow.append(conversor(row[cname]))
            correct.append(crow)
        return CSVCool(self.columnnames, correct)


    def wrap(self, iterable):
        """Convert an iterable in FrozenRow instance of this CSVCool
        instance.

        """
        return FrozenRow(**dict(zip(self._columnnames, iterable)))

    def cut(self, *columns):
        """Retrieves a new CSVCool instance only with a named columns.

        @params *columns: all columns to be preserved

        Example:

            original

                +-------+-------+-------+
                | name0 | name1 | name2 |
                +-------+-------+-------+
                | v0    |       | v2    |
                +-------+-------+-------+

            cuted = original.cut("name0", "name3")

                +-------+-------+
                | name0 | name2 |
                +-------+-------+
                | v0    | v2    |
                +-------+-------+

        """
        keys = [k for k in self._columnnames if k in columns]
        rows = []
        for r in self._rows:
            rows.append([r[k] for k in keys])
        return CSVCool(keys, rows)

    def filter(self, *conditions):
        """Retrieves a new CSVCool instance only with rows who match all the
        callable conditions passed as parameter.

        @params *conditions: callables to filter rows

        Example:

            original

                +-------+-------+-------+
                | name0 | name1 | name2 |
                +-------+-------+-------+
                | v0    |       | v2    |
                +-------+-------+-------+
                | v0    |   v1  | v2    |
                +-------+-------+-------+

            filtered = original.filter(lambda r: r["name1"] == "v1",
                                       lambda r: r["name0"] == "v0")

                +-------+-------+-------+
                | name0 | name1 | name2 |
                +-------+-------+-------+
                | v0    |   v1  | v2    |
                +-------+-------+-------+

        """
        keys = self._columnnames
        rows = []
        for row in self._rows:
            if all((c(row) for c in conditions)):
                rows.append([row[k] for k in keys])
        return CSVCool(keys, rows)

    def addcolumn(self, name, idx=None, default=None):
        """Append a column.

        @param name: The name of the new column.
        @param idx: The position of the new column (append if None).
        @param default: The vale by default ot the column (None by default).

        Example:

            original

                +-------+-------+-------+
                | name0 | name1 | name2 |
                +-------+-------+-------+
                | v0    |       | v2    |
                +-------+-------+-------+

            >>> original.addcolumn("name1.5", 2, "v1.5")

                +-------+-------+---------+-------+
                | name0 | name1 | name1.5 | name2 |
                +-------+-------+---------+-------+
                | v0    |       |  v1.5   | v2    |
                +-------+-------+---------+-------+

        """
        if name in self._columnnames:
            msg = "name '%s' already exists" % name
            raise KeyError(msg)
        if idx != None:
            self._columnnames.insert(idx, name)
        else:
            self._columnnames.append(name)
        oldrows = self._rows
        self._rows = []
        for row in oldrows:
            row = FrozenRow(**dict(row.items() + [(name, default)]))
            self._rows.append(row)

    def removecolumn(self, name):
        """Remove a column.

        @param name: The name of the column to be removed.

        Example:

            original

                +-------+-------+-------+
                | name0 | name1 | name2 |
                +-------+-------+-------+
                | v0    |       | v2    |
                +-------+-------+-------+

            >>> original.removecolumn("name1")

                +-------+-------+
                | name0 | name2 |
                +-------+-------+
                | v0    | v2    |
                +-------+-------+

        """
        self._columnnames.remove(name)
        for idx, row in enumerate(self):
            nrow = dict((k, v) for k, v in row.items() if k != name)
            self.removerow(row)
            self.addrow(nrow, idx)

    def sort(self, columnname_or_key=None, reverse=False):
        """Sort *IN PLACE*

        @param columnname_or_key: Specify which column or a key use for sorting.
        @param reverse: This is using to flag descending sorts.

        Example:

            original

                +-------+-------+-------+
                | name0 | name1 | name2 |
                +-------+-------+-------+
                | w1    | w2    | None  |
                +-------+-------+-------+
                | v0    |       | v2    |
                +-------+-------+-------+

            >>> original.sort(columnname="name1", reverse=False)

                +-------+-------+-------+
                | name0 | name1 | name2 |
                +-------+-------+-------+
                | v0    |       | v2    |
                +-------+-------+-------+
                | w1    | w2    | None  |
                +-------+-------+-------

        """
        key = None
        if callable(columnname_or_key):
            key = columnname_or_key
        elif columnname_or_key != None:
            key = lambda r: r[columnname_or_key]
        self._rows.sort(key=key, reverse=reverse)

    def addrow(self, row, idx=None):
        """Add a new row, if the values given it's not enough the cells are
        filled with None.

        @param row: Iterable with row values or a compatible FrozenRow instance.
        @param idx: The position of the new row (append if None).

        Example:

            original

                +-------+-------+-------+
                | name0 | name1 | name2 |
                +-------+-------+-------+
                | v0    |       | v2    |
                +-------+-------+-------+

            >>> original.addrow([w1,w2], idx=0)

                +-------+-------+-------+
                | name0 | name1 | name2 |
                +-------+-------+-------+
                | w1    | w2    | None  |
                +-------+-------+-------+
                | v0    |       | v2    |
                +-------+-------+-------+

        """
        if isinstance(row, FrozenRow):

            if sorted(row.keys()) != sorted(self._columnnames):
                raise ValueError("Incompatible FrozenRow instance")
        else:
            row = list(row)
            while len(row) < len(self._columnnames): row.append(None)
            row = self.wrap(row)

        if idx != None:
            self._rows.insert(idx, row)
        else:
            self._rows.append(row)

    def count(self, row):
        if not isinstance(row, FrozenRow):
            row = self.wrap(row)
        return self._rows.count(row)

    def index(self, row, start=None, stop=None):
        """Return first index of row.
        Raises ValueError if the value is not present.

        Example:

            >>> csvcool.index(original.poprow(25))
            25

        """
        start = start if start != None else 0
        stop = stop if stop != None else len(self._rows)
        if not isinstance(row, FrozenRow):
            row = self.wrap(row)
        return self._rows.index(row, start, stop)

    def removerow(self, row):
        """remove first occurrence of value.
        Raises ValueError if the value is not present.

        @param row

        """
        if not isinstance(row, FrozenRow):
            row = self.wrap(row)
        self._rows.remove(row)

    def poprow(self, idx=None):
        """Return a row of a given index.


        @param idx: index of a row

        Example:

            original

                +-------+-------+-------+
                | name0 | name1 | name2 |
                +-------+-------+-------+
                | v0    |       | v2    |
                +-------+-------+-------+

            >>> original.pop(0)
            <FrozenRow: {'name0': 'v0', 'name1': '', 'name2': 'v2'} at 0x0000000>

                +-------+-------+-------+
                | name0 | name1 | name2 |
                +-------+-------+-------+

        """
        return self._rows.pop(idx) if idx != None else self._rows.pop()

    def column(self, columnname):
        """Retrieves al values from a column

        @param columnname: Name of a column

        Example:

            original

                +-------+-------+-------+
                | name0 | name1 | name2 |
                +-------+-------+-------+
                | w1    | w2    | None  |
                +-------+-------+-------+
                | v0    |       | v2    |
                +-------+-------+-------+

            >>> original.column("name2")
            (None, v2)

        """
        c = []
        for r in self:
            c.append(r[columnname])
        return tuple(c)

    @property
    def columnnames(self):
        return tuple(self._columnnames)

    @property
    def rows(self):
        return tuple(self._rows)

    @property
    def encoding(self):
        return self._encoding


#===============================================================================
# FUNCTIONS
#===============================================================================

def register_type(for_type, func_validator, func_conversor):
    """This function register a new type to be used to validate and convert
    string to a a registered type.

    """
    if for_type not in _v_and_c:
        _v_and_c[for_type] = {}
    _v_and_c[for_type]["validator"] = func_validator
    _v_and_c[for_type]["conversor"] = func_conversor

def types():
    """List all registered types"""
    return _v_and_c.keys()


def read(stream, keys=None, encoding=None, sniffsize=1024, **kwargs):
    """Read a CSVCool instance into from file-like stream who contains csv data.

    @param stream: A File like object.
    @param key: list of keys to use, if keys == None the first row is used.
    @param encoding: encoding of the given stream.
    @param sniffsize: the number of byte to be read from stream to determine
        the dialect (not used if the dialect argument is given to **kwargs).
    @param **kwargs: kwargs for csv reader method.


    """

    format = lambda x: x
    if encoding:
        format = lambda x: x.decode(encoding)

    if "dialect" not in kwargs:
        sniff = None
        c = stream.read(sniffsize)
        while c:
            try:
                if sniff:
                    sniff += c
                else:
                    sniff = c
                kwargs["dialect"] = csv.Sniffer().sniff(sniff)
            except:
                c = stream.read(1)
            else:
                break
        del sniff
        stream.seek(0)

    rows = []
    for idx, row in enumerate(csv.reader(stream, **kwargs)):
        if idx == 0 and keys == None:
            keys = [format(k) for k in row if k.strip()]
        else:
            new_row = [format(c) for c in row]
            if new_row:
                rows.append(new_row)
    return CSVCool(keys, rows, encoding)


def write(csvcool, stream, encoding=None, **kwargs):
    """Write a CSVCool instance into file-like stream.

    @param csvcool: CSVCool instance.
    @param stream: A File like object.
    @param **kwargs: kwargs for csv writer method.

    """

    def format(x):
        if encoding:
            if isinstance(x, str):
                return unicode(x, "utf-8").encode(encoding)
            elif isinstance(x, unicode):
                return x.encode(encoding)
        return str(x)

    rows = []
    rows.append([format(cn) for cn in csvcool.columnnames])
    for row in csvcool:
        rows.append([format(row[k]) for k in csvcool.columnnames])
    csv_writer = csv.writer(stream, **kwargs)
    csv_writer.writerows(rows)


#===============================================================================
# ALL THE BUILT-INS VALIDATORS AND CONVERSORS
#===============================================================================

def is_bool(v):
    """Determines if a given string can be converted to bool"""
    return v.strip().lower() in ("true", "false", "0", "1", "")

def to_bool(v):
    """Convert a given string to bool"""
    v = v.strip().lower()
    if v in ("true", "1"):
        return True
    elif v in ("false", "0", ""):
        return False
    msg = "Invalid {type} value: {v}".format(type="bool", v=v)
    raise ValueError(msg)
register_type(bool, is_bool, to_bool)


def is_int(v):
    """Determines if a given string can be converted to int"""
    return v.strip().isdigit() or not v.strip()

def to_int(v):
    """Convert a given string to int"""
    if "." not in v:
        return int(v) if v.strip() else 0
    msg = "Invalid {type} value: {v}".format(type="int", v=v)
    raise ValueError(msg)
register_type(int, is_int, to_int)


def is_float(v):
    """Determines if a given string can be converted to float"""
    return v.strip().replace(".", "0").isdigit() or not v.strip()

def to_float(v):
    """Convert a given string to float"""
    return float(v) if v.strip() else 0.0
register_type(float, is_float, to_float)


def is_str(v):
    """Determines if a given string can be converted to string or unicode"""
    return isinstance(v, basestring)

def to_str(v):
    """Convert a given string to str (return the same thing)"""
    return v
register_type(str, is_str, to_str)


def is_none(v):
    """Determines if a given string can be converted to None"""
    return not v.strip()

def to_none(v):
    """Always return None"""
    return None
register_type(type(None), is_none, to_none)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
