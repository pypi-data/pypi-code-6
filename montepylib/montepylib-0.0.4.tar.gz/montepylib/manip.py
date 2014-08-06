#
# Routines to help manipulate DataFrames
#

from pandas import Series, DataFrame
import pandas as pd


def unpivot_int_cols(df, var_name, value_name):
    """
    Transform integer-named columns into rows.

    Eg. given a dataframe df:
         farm  fruit       variety  2014  2015  2016  2017
    0  Farm A  apple  Granny Smith   200   220   240   250
    1  Farm A  apple      Jonathon   150   175   200   225

    >>> unpivot_int_cols(df, 'year', 'mean')
          farm  fruit       variety  year  mean
    0   Farm A  apple  Granny Smith  2014   200
    1   Farm A  apple      Jonathon  2014   150
    2   Farm A  apple  Granny Smith  2015   220
    3   Farm A  apple      Jonathon  2015   175
    ...
    """
    from .utils import is_string_int
    id_vars = [field for field in df.columns if not is_string_int(field)]
    return pd.melt(df, id_vars=id_vars, var_name=var_name, value_name=value_name)


def cross_merge(df1, df2):
    """
    As of pandas 0.13 there is no quick way to merge two dataframes with no common columns,
    eg. df1.merge(df2, how='outer')
    This may be coming in a future version of pandas, perhaps with how='cross'.
    Instead use this function, which uses a workaround - 
        obliterate the indices and join, then reconstruct indices.
    """
    df1 = df1.set_index([[0]*len(df1)])
    df2 = df2.set_index([[0]*len(df2)])
    result = df2.join(df1, how='outer')
    result.set_index([range(len(result))])
    return result
