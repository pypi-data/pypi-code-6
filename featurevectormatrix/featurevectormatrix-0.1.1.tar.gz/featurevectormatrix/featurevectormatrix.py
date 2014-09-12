# -*- coding: utf-8 -*-

import numpy as np


class FeatureVectorMatrix(object):
    """ A class to abstract away the differences in internal representation between dictionaries and lists that can matter for very large datasets
     of vectors and allow them to work seamlessly with each other
    """

    def __init__(self, default_value=0, default_to_hashed_rows=False, rows=None):
        """ Initialization

        :param default_value: the default value for the vector
        :param default_to_hashed_rows: whether to default to returning dict rows
        """

        self._column_name_list = []
        self._column_name_idx = {}

        self._row_name_list = []
        self._row_name_idx = {}

        self._rows = []
        self._default_value = default_value
        self._default_to_hashed_rows = default_to_hashed_rows

        self._row_memo = {}

        if rows is not None:
            self.extend_rows(rows)

    def default_to_hashed_rows(self, default=None):
        if default is not None:
            self._default_to_hashed_rows = (default is True)

        return self._default_to_hashed_rows

    def _update_internal_column_state(self, column_names):
        """ Update the internal state with some (possibly) new columns

        :param column_names: an iterable which contains new column names
        """
        for k in column_names:
            if k not in self._column_name_idx:
                self._column_name_idx[k] = len(self._column_name_list)
                self._column_name_list.append(k)

    def _add_dict_row(self, feature_dict, key=None):
        """ Add a dict row to the matrix

        :param str key: key used when rows is a dict rather than an array
        :param dict feature_dict: a dictionary of features and weights
        """
        self._update_internal_column_state(set(feature_dict.keys()))

        # reset the row memoization
        self._row_memo = {}

        if key is not None:
            if key in self._row_name_idx:
                self._rows[self._row_name_idx[key]] = feature_dict
                return
            else:
                self._row_name_idx[key] = len(self._rows)
                self._row_name_list.append(key)

        self._rows.append(feature_dict)

    def _add_list_row(self, feature_list, key=None):
        """ Add a list row to the matrix

        :param str key: key used when rows is a dict rather than an array
        :param feature_list: a list of features in the same order as column_names

        :raise IndexError: if the list doesnt match the expected number of columns
        """
        if len(feature_list) > len(self._column_name_list):
            raise IndexError("Input list must have %s columns or less" % len(self._column_name_list))

        # reset the row memoization
        self._row_memo = {}

        if key is not None:
            if key in self._row_name_idx:
                self._rows[self._row_name_idx[key]] = feature_list
                return
            else:
                self._row_name_idx[key] = len(self._rows)
                self._row_name_list.append(key)

        self._rows.append(feature_list)

    def set_column_names(self, column_names):
        """ Setup the feature vector with some column names
        :param column_names: the column names we want
        :return:
        """
        if len(self._rows):
            raise NotImplementedError("You can't manually set columns once data has been added")

        self._update_internal_column_state(column_names)

    def set_row_names(self, row_names):
        """ Setup the feature vector with some column names
        :param row_names: the column names we want
        :return:
        """
        if self.row_count() != len(row_names) or len(self._row_name_list) > 0 or len(self._row_name_idx) > 0:
            raise NotImplementedError("You can only manually set names once data has been added")

        for idx, k in enumerate(row_names):
            self._row_name_idx[k] = idx

        self._row_name_list = row_names

    def column_names(self):
        """ get the column names

        :return: The ordered list of column names
        """
        return self._column_name_list

    def row_names(self):
        """ get the column names

        :return: The ordered list of column names
        """
        return self._row_name_list

    def add_row(self, list_or_dict, key=None):
        """ Dispatches to the correct add_*_row function

        :param str key: key used when rows is a dict rather than an array
        :param list_or_dict: a feature list or dict
        """
        if isinstance(list_or_dict, list):
            self._add_list_row(list_or_dict, key)
        else:
            self._add_dict_row(list_or_dict, key)

    def extend_rows(self, list_or_dict):
        """ Add multiple rows at once

        :param list_or_dict: a 2 minensional structure for adding multiple rows at once
        :return:
        """
        if isinstance(list_or_dict, list):
            for r in list_or_dict:
                self.add_row(r)
        else:
            for k,r in list_or_dict.iteritems():
                self.add_row(r, k)

    def row_count(self):
        """ The current number of rows

        :return: the count
        """
        return len(self._rows)

    def __len__(self):
        return self.row_count()

    def column_count(self):
        """ Get the current number of columns

        :return: the count
        """
        return len(self._column_name_list)

    def get_row_list(self, row_idx):
        """ get a feature vector for the nth row

        :param row_idx: which row
        :return: a list of feature values, ordered by column_names
        """

        try:
            row = self._rows[row_idx]
        except TypeError:
            row = self._rows[self._row_name_idx[row_idx]]

        if isinstance(row, list):
            extra = [ self._default_value ] * (len(self._column_name_list) - len(row))
            return row + extra

        else:
            if row_idx not in self._row_memo:
                self._row_memo[row_idx] = [ row[k] if k in row else self._default_value for k in self._column_name_list ]

            return self._row_memo[row_idx]

    def get_row_dict(self, row_idx):
        """ Return a dictionary representation for a matrix row

        :param row_idx: which row
        :return: a dict of feature keys/values, not including ones which are the default value
        """

        try:
            row = self._rows[row_idx]
        except TypeError:
            row = self._rows[self._row_name_idx[row_idx]]

        if isinstance(row, dict):
            return row

        else:
            if row_idx not in self._row_memo:
                self._row_memo[row_idx] = dict((self._column_name_list[idx], v) for idx, v in enumerate(row) if v != self._default_value)

            return self._row_memo[row_idx]

    def get_matrix(self):
        """  Use numpy to create a real matrix object from the data

        :return: the matrix representation of the fvm
        """
        return np.array([ self.get_row_list(i) for i in range(self.row_count()) ])

    def transpose(self):
        """ Create a matrix, transpose it, and then create a new FVM

        :raise NotImplementedError: if all rows aren't keyed
        :return: a new FVM rotated from self
        """
        if len(self._row_name_list) != len(self._rows):
            raise NotImplementedError("You can't rotate a FVM that doesn't have all rows keyed")

        fvm = FeatureVectorMatrix(default_value=self._default_value, default_to_hashed_rows=self._default_to_hashed_rows)
        fvm._update_internal_column_state(self._row_name_list)
        for idx, r in enumerate(self.get_matrix().transpose()):
            fvm.add_row(r.tolist(), self._column_name_list[idx])

        return fvm

    def keys(self):
        """ Returns all row keys

        :raise NotImplementedError: if all rows aren't keyed
        :return: all row keys
        """
        if len(self._row_name_list) != len(self._rows):
            raise NotImplementedError("You can't get row keys for a FVM that doesn't have all rows keyed")

        return self.row_names()

    def __getitem__(self, idx):
        """ Allow for standard array/dict access syntax

        :param idx: index of desired item
        :return: return row in list or dict format
        """
        if self._default_to_hashed_rows:
            return self.get_row_dict(idx)
        else:
            return self.get_row_list(idx)

    def __iter__(self):
        """ A generator for iterating over the rows. It should behave as expected - if the top level data structure has all keyed rows,
        return keys rather than the rows themselves

        :return: a generator for iterating over the rows
        """
        if self.row_count() == len(self.row_names()):
            for k in self.row_names():
                yield k
        else:
            for row in self._rows:
                yield row