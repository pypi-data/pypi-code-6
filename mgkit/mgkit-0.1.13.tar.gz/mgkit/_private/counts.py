"""
This module deals with count data, from loading HTSeq-count output to
manipulation and testing.
"""

from __future__ import division

import logging
import itertools
import pandas

LOG = logging.getLogger(__name__)


def group_dataframe_by_category(counts, mapping):
    """
    Takes a DataFrame instance in the form (IDxTAXA) and a mapping dictionary
    for the categories. All elements of counts will be mapped to the mapping
    values, summing values belonging to the same (MAPID, TAXON) element.

    * counts: a DataFrame instance with counts in the form (IDxTAXA)
    * mapping: a dictionary whose keys are the same, or a subset of counts
      rows, and the values are iterables of ids to which the key belong to.

    returns a DataFrame instance with the same number of rows as mapping
    values and the same number of rows as *counts*
    """

    mapped_categories = set(itertools.chain(*mapping.values()))

    mapped = pandas.DataFrame(index=sorted(mapped_categories),
                              columns=counts.columns)
    mapped.fillna(0, inplace=True)

    for column, series in counts.iterkv():
        #no reason to do a lookup over genes with no counts
        for idx, value in series[series > 0].iterkv():
            try:
                mappings = mapping[idx]
            except KeyError:
                continue
            for mapped_id in mappings:
                # print mapped.ix[mapped_id, column]
                mapped.ix[mapped_id, column] += value
                # print value
                # print mapped.ix[mapped_id, column]

    return mapped


def scale_by_min_value(data):
    """
    Scale by the minimun sample sum.

    data / (data.sum(axis=0).min() / data.sum(axis=0).sum())
    """

    return data / (data.sum(axis=0).min() / data.sum(axis=0).sum())


def scale_fpkm_data_frame(data, data_tot, gene_len, data_mean=None, scale=True):
    """
    Scale DataFrame using FPKM (formula from cufflink)
    counts are first scaled to make them comparable

    data: DataFrame
    data_tot: sum of all counts in the data sets
    gene_len: DataFrame containing gene lengths (same columns and rows as data)
    data_mean: mean of all data sets sums
    scale: if the the data needs to be scaled with scale_data_frame first
    """
    if scale and data_mean:
        data = scale_data_frame(data, data_mean)

    data_sum = data.sum().sum()

    const = 10**9

    data = const * data / (gene_len * data_tot)

    return data.fillna(0)


def scale_fpkm_data_frames(data1, data2, gene_len, scale_first=True):
    """
    Scale DataFrames using FPKM (formula from cufflink)
    counts are first scaled to make them comparable
    """
    if scale_first:
        data1, data2 = scale_data_frames(data1, data2)
    data1_sum = data1.sum().sum()
    data2_sum = data2.sum().sum()
    total_sum = data1_sum + data2_sum

    const = 10**9

    data1 = const * data1 / (gene_len * total_sum)
    data2 = const * data2 / (gene_len * total_sum)
    data1.fillna(0, inplace=True)
    data2.fillna(0, inplace=True)

    return data1, data2


def batch_scale_fpkm(data, gene_len):
    """
    gene_len is a Series instance that is the result of combine_dicts run on
    a ko_idx->name (profile name) and batch_load_gene_length
    """

    gene_len = gene_len[data.index]

    const = 10**9

    data = (const * data).div(gene_len * data.sum().sum(), axis=0)

    return data.fillna(0)

