#!/usr/bin/env/python
# coding=utf-8
#

import cStringIO
import csv

def master(rows, *args):
    """
    csvlib.master
    ------------------------------------------------
    Create master set of keys for a number of dictionaries.
    Each argument should be (list) or generate a number of
    dictionaries when iterated. Each dictionary
    represents a row in an eventual csv file.
    ------------------------------------------------
    @param  args (list / generator / iterator, ..)
    @return       set
    """
    #if not args:
    #    error_message = 'Must provide at least one (optionally empty) set of rows as an argument. args=%s.'
    #    raise ValueError(error_message % args)
    master = set()
    for rows in (rows,) + args:
        for row in rows:
            master |= set(row.keys())
            pass
        pass
    return master

def dialect(name=None, **kwargs):
    """
    csvlib.dialect
    ------------------------------------------------
    Create a new csv dialect for use with the native
    python csv module or with csvlib.
    ------------------------------------------------
    @param  name   str
    @param  kwargs dict
            strict boolean
            ..
    @return        csv.Dialect subclass
    """
    if not name:
        if not kwargs:
            name = 'CLStandardDialect'
            pass
        else:
            name = 'CLCustomDialect'
            pass
        pass

    defaults = {'strict': True,
                'delimiter': ',',
                'quotechar': '"',
                'escapechar': '\\',
                'doublequote': False,
                'lineterminator': '\r\n',
                'quoting': csv.QUOTE_ALL,
                'skipinitialspace': False
               }
    defaults.update(kwargs)
    csv.register_dialect(name, **defaults)
    return name

def prepare(master, dialect_name, **kwargs):
    """
    csvlib.prepare
    ------------------------------------------------
    Create a cStringIO object to hold the eventual
    csv string and return this in a tuple along with
    an instance of csv.DictWriter for the given master
    list of keys and csv.Dialect subclass.

    Order for the master set can be optionally
    specified using kwargs forwarded then to python
    sorted() built-in function.

    @see csvlib.master
    @see csvlib.dialect
    ------------------------------------------------
    @param  master   list
    @param  dialect  csv.Dialect subclass
    @param  kwargs   dict
            cmp      function
            key      function
            reverse  boolean
    @return         (StringIO instance, csv.DictWriter instance)
    """
    csvout = cStringIO.StringIO()
    return (csvout, csv.DictWriter(csvout, sorted(list(master), **kwargs), dialect=dialect_name))

def label(writer, master):
    """
    csvlib.label
    ------------------------------------------------
    Write a row of labels from a given set.
    Labels are written in order specified by csvlib.prepare.

    @see csvlib.master
    @see csvlib.prepare
    ------------------------------------------------
    @param  writer csv.DictWriter instance
    @param  master set
    @return None
    """
    writer.writerow({label: label for label in list(master)})
    pass

def write(writer, *args):
    """
    csvlib.write
    ------------------------------------------------
    Write a number of dictionaries to the csv file used
    by the supplied DictWriter instance.
    If using csvlib.prepare this is a StringIO instance
    and the first item in the returned tuple.

    Write all dictionaries that exist in rows (an
    iterable data structure) to csvout (implicitly
    used) using the provided csv.DictWriter from
    the writer parameter.

    @see csvlib.prepare
    @see csvlib.master
    @see csvlib.label
    ------------------------------------------------
    @param  writer      csv.DictWriter
    @param  **kwargs
    @param  rows        iterable
    @param  [label_row] list
    @return             None
    """
    for rows in args:
        for row in rows:
            if any(row):
                writer.writerow({label: value for label, value in row.iteritems()})
                pass
            pass
        pass
    pass

def stringify(label_columns, *args, **kwargs):
    """
    csvlib.stringify
    ------------------------------------------------
    Easy interface for building csv strings from a
    number of dictionaries.

    Combines the other csvlib functions in a straight-
    forward manner which will suit many common use-
    cases.
    ------------------------------------------------
    @param  label  boolean
    @param  args   @see csvlib.master
    @param  kwargs @see csvlib.dialect
    @return        string
    """
    _master = master(*args)
    _dialect = dialect(**kwargs)

    csvout, writer = prepare(_master, _dialect)
    if label_columns:
        label(writer, _master)
    write(writer, *args)

    output = csvout.getvalue()
    csvout.close()
    return output
