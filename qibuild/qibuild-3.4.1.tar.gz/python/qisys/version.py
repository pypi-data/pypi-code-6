## Copyright (c) 2012-2014 Aldebaran Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.
""" Set of tools relate to version numbers

"""

def compare(a_str, b_str):
    """ Compare two versions

    >>> compare("1.2.3", "1.2.3")
    0
    >>> compare("1.2.3", "1.2.3-rc1")
    -1
    >>> compare("1.20", "1.3")
    1
    >>> compare("1.20", "1.3-rc2")
    1

    """
    v_a = explode_version(a_str)
    v_b = explode_version(b_str)

    res = 0
    a_sep = 0
    b_sep = 0
    c_a = ""
    c_b = ""
    while True:
        if not v_a:
            c_a = ""
        else:
            c_a = v_a.pop(0)
        if not v_b:
            c_b = ""
        else:
            c_b = v_b.pop(0)
        if (not c_a) and (not c_b):
            return 0
        if not c_a:
            return -1
        if not c_b:
            return 1
        if not c_a[0].isdigit():
            a_sep = (c_a == "." or c_a == "-")
        if not c_b[0].isdigit():
            b_sep = (c_b == "." or c_b == "-")
        if a_sep and not b_sep:
            return -1
        if not a_sep and b_sep:
            return 1
        res = compare_substring(c_a, c_b)
        if res:
            return res
    return 0

def eat_number(str, index):
    """ Helper for explode_version """
    first = index
    while index < len(str):
        if not str[index].isdigit():
            break
        index += 1
    return (str[first:index], index)

def eat_alpha(str, index):
    """ Helper for explode_version """
    first = index
    while index < len(str):
        if not str[index].isalpha():
            break
        index += 1
    return (str[first:index], index)


def explode_version(str):
    """ Explode a version string into a list
    made of either numbers, or alphabetic chars,
    or separators

    >>> explode_version('1.2.3')
    ['1', '.', '2', '.', '3']

    >>> explode_version('1.2.3-rc1')
    ['1', '.', '2', '.', '3', '-', 'rc', '1']

    """
    res = list()
    index = 0
    while index < len(str):
        if str[index].isdigit():
            (to_append, index) = eat_number(str, index)
            res.append(to_append)
        elif str[index].isalpha():
            (to_append, index) = eat_alpha(str, index)
            res.append(to_append)
        else:
            # append a string with just one char
            res.append("%s" % str[index])
            index += 1
    return res

def compare_substring(a_str, b_str):
    """ Helper for compare """
    a_digit = a_str[0].isdigit()
    b_digit = b_str[0].isdigit()
    # string > int
    if a_digit and not b_digit:
        return -1
    if not a_digit and b_digit:
        return 1
    if a_digit and b_digit:
        # compare to digits
        a_int = int(a_str)
        b_int = int(b_str)
        if a_int > b_int:
            return 1
        if a_int < b_int:
            return -1
    else:
        # compare two strings
        if a_str > b_str:
            return 1
        if a_str > b_str:
            return -1
    return 0

if __name__ == "__main__":
    import doctest
    doctest.testmod()
