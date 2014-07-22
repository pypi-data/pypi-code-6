#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""
Simple fixed-format data reader that guesses offsets.

Python 2.x only.

Does not attempt to do any data transformation other than striping separators
(normally whitespace).

Input can be any iterable of string (str or unicode), including files. The
data is returned as dictionaries of strings. This is not efficient for
large datasets, but is quite convenient for configuration files and small
sets.

For usage examples, first consider some fixed-format data:

>>> data = ["Column1 Column2    Column3     \n",
...         "simple1 la lala la 123         \n",
...         "simple2 lalala  la 123*321     \n"]
...
>>> records = list(reader(data))

Then, it is faily easy to get the data out:

>>> for record in records:
...     sorted(record.iteritems())
...
[('Column1', 'simple1'), ('Column2', 'la lala la'), ('Column3', '123')]
[('Column1', 'simple2'), ('Column2', 'lalala  la'), ('Column3', '123*321')]
"""

import re


def reader(list, separator=" "):
    return SimpleReader(list, separator)


class SimpleReader(object):
    ur"""
    Simple reader.

    Usage and testing:

    >>> from __future__ import print_function
    >>> data = ["Test        Value1    Value2\n",
    ...        u"unicode     çáóí      Πύλη  \n",
    ...         "missing sep xyz       xyz\n"]
    >>> reader = SimpleReader(data)
    >>> res = list(reader)
    >>> print(res[0]["Value1"])
    çáóí
    >>> print(res[0]["Value2"])
    Πύλη
    >>> print(res[1]["Value2"])
    xyz
    """

    def __init__(self, lines, separator=" "):
        self.lines = lines.__iter__()  # iterator (has next() method)
        self.sep = separator
        self.strip = separator + "\n"
        self.header = None  # a list of tuples (name, start, end)

    def next(self):
        if not self.header:
            self.header = self._parse_header(self.lines.next())
        return self._parse_line(self.lines.next())

    def _parse_header(self, line):
        name = re.compile(r"[^{0}\n]+[{0}]*".format(self.sep))
        return [(col.group().strip(self.sep), col.start(), col.end())
                for col in name.finditer(line)]

    def _parse_line(self, line):
        output = dict()
        for name, start, end in self.header:
            output[name] = line[start:end].strip(self.strip)
        return output

    def __iter__(self):
        return self


if __name__ == "__main__":
    import doctest
    doctest.testmod()
