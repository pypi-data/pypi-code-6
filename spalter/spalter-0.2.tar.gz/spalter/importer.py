import os
import pandas as pd


def _import_csv(filename, split_column, *args, **kwargs):
    if not os.path.isfile(filename):
        raise IOError("File '{}' does not exist.".format(filename))
    df = pd.read_csv(filename, *args, **kwargs)
    return _parse_dataframe(df, split_column)


def _parse_dataframe(df, split_column):
    if split_column not in df.columns:
        raise KeyError("'{}' not in DataFrame.".format(split_column))
    variants = df[split_column].unique()
    observations = df.columns.drop(split_column)
    result = {}
    for observation in observations:
        result[observation] = {}
        for variant in variants:
            tmp = df[[split_column, observation]]
            values = tmp[tmp[split_column] == variant][observation].tolist()
            result[observation][variant] = values
    return result
