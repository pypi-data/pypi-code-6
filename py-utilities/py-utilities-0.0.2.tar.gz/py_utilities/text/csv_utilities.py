#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import csv
import string


def csv_to_list(file_path, has_headers=None, delimiters=[',', ';']):
    return _csv_to_headers_rows_tuple(file_path, has_headers, delimiters)[1]


def csv_to_headers(file_path, has_headers=None, delimiters=[',', ';']):
    return _csv_to_headers_rows_tuple(file_path, has_headers, delimiters)[0]


def csv_to_html(file_path, has_headers=None, delimiters=[',', ';']):
    """
    Writes csv instream as html outstream
    """
    headers, rows = _csv_to_headers_rows_tuple(file_path,
                                               has_headers,
                                               delimiters)
    table_string = ""
    if headers:
        table_string += "<thead><tr><th>" + \
                        string.join(headers, "</th><th>") + \
                        "</th></tr></thead>"

    for row in rows:
        table_string += "<tbody><tr><td>" + \
                        string.join(row, "</td><td>") + \
                        "</td></tr></tbody>"

    return '<table>' + table_string + '</table>'


def list_to_csv(file_path, data_as_list, delimiter=',', quoting=csv.QUOTE_ALL):
    """
    Writes data_as_list into a csv file at file_path
    """
    with open(file_path, 'wb') as f:
        writer = csv.writer(f, delimiter=delimiter, quoting=quoting)
        writer.writerows(data_as_list)


def _csv_to_headers_rows_tuple(file_path,
                               has_headers=None,
                               delimiters=[',', ';']):
    """
    Reads csv file at file_path into a tuple that contains a list of headers
    and a list of data
    """
    with open(file_path, 'rb') as f:
        sniffer = csv.Sniffer()
        has_headers = sniffer.has_header(f.readline()) \
            if has_headers is None else has_headers
        dialect = sniffer.sniff(f.read(1024), delimiters)
        f.seek(0)
        csv_data = list(csv.reader(f, dialect))
        return (csv_data[0], csv_data[1:]) if has_headers else ([], csv_data)

# vim: filetype=python
