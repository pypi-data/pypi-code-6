#
# Routines to help input and output DataFrames
#

from pandas import Series, DataFrame
import pandas as pd

def excel_table_pos(path, sheet_name, key):
    """
    Find the start and end rows of a table in an Excel spreadsheet
    based on the first occurence of key text on the sheet, and down
    to the first blank line.

    Returns (col, start_row, end_row, skip_footer)

    where: 
        col is the column number containing the key text
        start_row is the row after this
        end_row is the row number of the next blank line
        skip_footer is how many rows from the end of the sheet this is

    Eg.:
        (col, start, end, skip_footer) = excel_table_pos('data/data.xlsx', 'Sheet1', 'Revenues')
        x = pd.read_excel(path, sheet_name, skiprows=start, skip_footer=skip_footer, header=0)
        x = x.dropna(axis=1, how='all').fillna(method='ffill')
        x.rename(columns=lambda x: x.lower(), inplace=True)
    """
    import xlrd
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_name(sheet_name)
    # find the first occurrence of the key (eg. Number of trees), and the next line break
    (col, start, end) = (-1, -1, sheet.nrows)
    for rownum in xrange(sheet.nrows):
        if col<0: # look for key to start the table off
            try:
                test_col = next(c for c in xrange(sheet.ncols) if sheet.cell(rownum, c).value==key)
            except StopIteration:
                pass
            else:
                col, start = test_col, rownum+1 # row after key text is the start
        else: # test for blank line as end of table
            if not [True for cell in sheet.row(rownum) if cell.value]:
                end = rownum
                break
    skip_footer = sheet.nrows - end
    return (col, start, end, skip_footer)
