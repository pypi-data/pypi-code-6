"""
functions having to do with tables
"""

import csv
from .decorator import lines
from StringIO import StringIO

@lines
def make_csv(text):
    """make space-separated text into comma-separated"""
    return [','.join(line.strip().split()) for line in text]

def format_cols(rows, header=None, right_align=()):
    if header:
        raise NotImplementedError('TODO') # -> record TODO items
    if not rows:
        return # XXX header
    assert len(set([len(row) for row in rows])) == 1
    rows = [[str(col) for col in row]
            for row in rows]
    lengths = [max([len(row[i]) for row in rows])
               for i in range(len(rows[0]))]
    rows = [[col + ' '*(length-len(col)) for col, length in zip(row, lengths)]
            for row in rows]
    return rows


def tablify(table_lines, header=True):
    """=> HTML table"""
    table = '<table>\n'
    if header:
        tag, invtag = '<th> ', ' </th>'
    else:
        tag, invtag = '<td> ', ' </td>'
    if not hasattr(table_lines, '__iter__'):
        table_lines = ( table_lines, )
    for i in table_lines:
        table += '<tr>'
        if not hasattr(i, '__iter__'):
            i = (i,)
        for j in i:
            table += tag + str(j) + invtag
        table += '</tr>\n'
        tag = '<td> '
        invtag = ' </td>'
    table += '</table>'
    return table
