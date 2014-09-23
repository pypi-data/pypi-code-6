#!/usr/bin/env python

# Copyright 2014 Larry Fenske

# This file is part of ListDict.

# ListDict is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# ListDict is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.


class ListDict(object):
    """
    This is a container class that acts like a list and a dictionary
    and a structure.

    So far, "append" is the only list method supported.

    The "append" method adds items to the list. If there's a second
    parameter, it is a label that can subsequently be used as an
    index, but that also is stored in the main dictionary. This means
    that an element could be read or written as, for example, ld[1],
    ld["somelabel"], and ld.somelabel.

    A ListDict can optionally be initialized with a starting list value.
    """

    """
    __l is a list of lists of [value,label]
    __d is a set of labels

    If an item has a label, then the definitive value is in the
    structure, i.e. in self.__dict__. This is necessary so that
    ld.somelabel=value works.
    """

    def __init__(self, initial_list=None):
        if initial_list:
            # Initialize the list with the given values and no labels.
            self.__l = [[i,None] for i in initial_list]
        else:
            self.__l = []
        # Initialize the set of labels.
        self.__d = set()

    def append(self, val, label=None):
        v = [val,label]
        if label:
            # If there's a label, save it.
            self.__d.add(label)
            # And create a structure element.
            self.__dict__[label] = val
        self.__l.append(v)

    def __str__(self):
        # The __str__ is simply the str of the list part.
        return str(list(self))

    def __len__(self):
        return len(self.__l)

    def __getitem__(self, ix):
        if isinstance(ix, slice):
            # A slice was requested. Return that slice of the list of values.
            return [val for val,label in self.__l][ix]
        elif ix in self.__d:
            # The index is a label; return the value from the structure.
            return self.__dict__[ix]
        elif self.__l[ix][1]:
            # The index must be an integer, and this item has a label;
            # return the value from the structure.
            return self.__dict__[self.__l[ix][1]]
        else:
            # The index must be an integer, and this item has no label;
            # return the value from the list.
            return self.__l[ix][0]

    def __setitem__(self, ix, val):
        if ix in self.__d:
            # The index is a label; set the value in the structure.
            self.__dict__[ix] = val
        elif self.__l[ix][1]:
            # The index must be an integer, and this item has a label;
            # set the value in the structure.
            self.__dict__[self.__l[ix][1]] = val
        else:
            # The index must be an integer, and this item has no label;
            # set the value in the list.
            self.__l[ix][0] = val

    def __iadd__(self, other):
        # Append all items in other to self.
        for val,label in other.__l:
            self.append(val, label)
        return self

    def __add__(self, other):
        # Create a new empty ListDict, then append self and other to it.
        retval = ListDict()
        retval += self
        retval += other
        return retval


if __name__ == "__main__":
    # For these tests, __d cannot start with two underscores.
    # It should have two underscores for production.
    ld = ListDict()
    ld.append(3, 'y')
    ld.append(4, 'z')
    ld.append(2)
    assert ld[0] == 3
    assert ld.y == 3
    assert ld["y"] == 3
    assert ld[1] == 4
    assert ld.z == 4
    assert ld["z"] == 4
    assert ld[2] == 2
    assert str(ld) == "[3, 4, 2]"
    assert len(ld) == 3
    ld["y"] = 5
    assert ld["y"] == 5
    assert ld[0] == 5
    assert ld.y == 5
    ld[0] = 6
    assert ld["y"] == 6
    assert ld[0] == 6
    assert ld.y == 6
    ld.y = 7
    assert ld["y"] == 7
    assert ld[0] == 7
    assert ld.y == 7
    ld[2] = 1
    assert ld[2] == 1
    print ld
    print ld.__d

    le = ListDict()
    print "new le =", le
    le.append(10)
    assert le[0] == 10
    le.append(11, "x")
    assert le["x"] == 11
    assert le[1] == 11
    assert le.x == 11
    print "le =", le
    print le.__d

    lf = ListDict([20,21,22])
    assert lf[0] == 20
    lf[0] = 23
    assert lf[0] == 23
    print "lf =", lf
    print lf.__d

    ld += le
    assert ld[1] == 4
    assert ld.z == 4
    assert ld["z"] == 4
    assert str(ld) == "[7, 4, 1, 10, 11]"
    assert len(ld) == 5
    assert ld["y"] == 7
    assert ld[0] == 7
    assert ld.y == 7
    assert ld[2] == 1

    assert ld[3] == 10
    assert ld["x"] == 11
    assert ld[4] == 11
    assert ld.x == 11
    print "ld =", ld
    print ld.__d

    lg = le + lf
    assert len(lg) == 5
    assert str(lg) == "[10, 11, 23, 21, 22]"
    assert lg[0] == 10
    assert lg["x"] == 11
    assert lg[1] == 11
    assert lg.x == 11
    assert lg[2] == 23
    print "lg =", lg
    print lg.__d

