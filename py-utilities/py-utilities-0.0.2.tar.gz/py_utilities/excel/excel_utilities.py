#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier
    from ordereddict import OrderedDict
import json
import xlrd


def excel_to_json(excel_path, worksheet_num=0, header_row=0):
    workbook = xlrd.open_workbook(excel_path)
    worksheet = workbook.sheet_by_index(worksheet_num)
    rows = []
    keys = [worksheet.cell_value(header_row, i)
            for i in xrange(worksheet.ncols)]

    for row_num in range(header_row + 1, worksheet.nrows):
        row = OrderedDict()
        vals = worksheet.row_values(row_num)

        num_col = 0
        while num_col < worksheet.ncols:
            row[keys[num_col]] = vals[num_col]
        rows.append(row)

    return json.dumps(rows)

# vim: filetype=python
