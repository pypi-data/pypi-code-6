def is_string_int(s):
    """
    Returns True if the argument is a string and can be converted to an integer with int().
    eg. is_string_int("7.5") returns None.
        is_string_int(7.5) raises an error.
        is_string_int("2010") returns True.
    """
    assert type(s)==str, 'is_string_int expects a string, received {0} {1}'.format(s, type(s))
    try:
        int(s)
    except ValueError:
        return None
    else:
        return True


from pandas.util.testing import assert_frame_equal

def assert_data_equal(df1, df2, index=None, **kwargs):
    """
    Compares two dataframes, ignoring the order of rows and columns.
    As a shortcut, you can pass `index` to set a common index on the two dataframes.
    If you use the default integer index, it may not know what row order is meaningful.
    You can also pass arguments to the underlying assert_frame_equal function,
    such as check_dtype=False.
    Eg.
    >>> df1 = DataFrame(index = [1,3,2,4])
    >>> df2 = DataFrame(index = [1,2,3,4])
    >>> df1['A'] = [1,3,2,4]
    >>> df1['B'] = [2,4,3,5]
    >>> df2['B'] = [2,3,4,5]
    >>> df2['A'] = [1,2,3,4]
    >>> assert_data_equal(df1, df2)
    """
    if not 'check_names' in kwargs:
        kwargs['check_names'] = True
    if index:
        df1 = df1.set_index(index)
        df2 = df2.set_index(index)
    return assert_frame_equal(df1.sort().sort(axis=1), df2.sort().sort(axis=1), **kwargs)
