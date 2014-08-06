#
# extend the DataFrame with some new functions
#     any sort of import montepylib.extend will execute this code, 
#     and add eg. the DataFrame.command() method to all dataframes
#

from types import MethodType
from pandas import DataFrame, MultiIndex


def _del_columns(df, cols):
    """
    Delete the specified columns (passed as a list/iterable) if present.
    >>> print x
         farm  fruit       variety  num trees  min  mode  max
    0  Farm A  apple  Granny Smith        100    4     6    7
    1  Farm A  apple      Jonathon        200    4     7    9
    2  Farm A   pear         Nashi         50    2     6   10
    >>> del_columns(x, ['min', 'mode', 'max'])
    >>> print x
         farm  fruit       variety  num trees
    0  Farm A  apple  Granny Smith        100
    1  Farm A  apple      Jonathon        200
    2  Farm A   pear         Nashi         50
    """
    for col in cols:
        try:
            del df[col]
        except KeyError:
            pass

DataFrame.del_columns = MethodType(_del_columns, None, DataFrame)


def _gencmd(df, pandas_as='pd'):
    """
    With this addition to DataFrame's methods, you can use:
        df.command()
    to get the command required to regenerate the dataframe df.
    """
    if pandas_as:
        pandas_as += '.'
    index_cmd = df.index.__class__.__name__
    if type(df.index)==MultiIndex:
        index_cmd += '.from_tuples({0}, names={1})'.format([i for i in df.index], df.index.names)
    else:
        index_cmd += "({0}, name='{1}')".format([i for i in df.index], df.index.name)
    return 'DataFrame({0}, index={1}{2}, columns={3})'.format([[xx for xx in x] for x in df.values],
                                                                pandas_as,
                                                                index_cmd,
                                                                [c for c in df.columns])

DataFrame.command = MethodType(_gencmd, None, DataFrame)
