import gspread
import numpy as np
import pandas as pd
import time

from pandas import DataFrame
from gspread.exceptions import WorksheetNotFound


def data_frame_to_gs(gc, sp_key, worksheet, df, reset=True, headers=True):
    """
    Store a data frame into a google spreadsheet
    Max number of rows 1000, max columns 26 by default, overwritten if df dimensions exceeds it.
    :param gc: Google spreasheet session gc = gspread.login('user', 'password')
    :param sp_key: Spreadsheet key
    :param worksheet: Name of worksheet
    :param df: Pandas Data frame
    :param reset: True to delete original worksheet and create a new one.
    :param headers: True to include headers in worksheet
    :return: None
    """
    data_frame = df.reset_index().fillna('')
    sps = gc.open_by_key(sp_key)

    try:
        wks = sps.worksheet(worksheet)
    except WorksheetNotFound:
        wks = sps.add_worksheet(title=worksheet, rows="1000", cols="26")
        reset = False
    rows = 1000
    cols = 26
    if reset:
        if data_frame.shape[0] > rows or data_frame.shape[1] > cols:
            rows = data_frame.shape[0]
            cols = data_frame.shape[1]
        sps.del_worksheet(wks)
        #This line is to overcome a bug in gspread
        sps.client.session.connections['httpsspreadsheets.google.com'].close()
        wks = sps.add_worksheet(title=worksheet, rows=str(rows), cols=str(cols))

    size = data_frame.shape
    offset = 0

    #Insert worksheet headers
    if headers:
        offset = 1
        cols = data_frame.columns
        last_head = wks.get_addr_int(1, len(cols))
        cells = wks.range('%s:%s' % ('A1', last_head))
        for cell in cells:
            cell.value = cols[cell.col-1]
        wks.update_cells(cells)

    first_cell = wks.get_addr_int(offset + 1, 1)
    last_cell = wks.get_addr_int(size[0] + offset, size[1])
    cells = wks.range('%s:%s' % (first_cell, last_cell))
    for cell in cells:
        cell.value = data_frame.ix[cell.row-1-offset, cell.col-1]

    wks.update_cells(cells)


