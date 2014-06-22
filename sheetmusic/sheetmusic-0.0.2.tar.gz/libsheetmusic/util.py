import re
import string

import mingus.containers as containers

def merge(a, b):
    '''
    (dict,dict) -> dict
    Combine two dictionaries without side-effects.
    '''
    result = dict(a)
    result.update(b)
    return result

def range_apply(func, list_list):
    return [[func(cell) for cell in column] for column in list_list]

def to_integer(scientific_note):
    '''
    :param scientific_note: Scientific representation of the note, like A4

    Returns an integer so you can feed this into spreadsheet functions
    '''
    return int(scientific_note)

def from_integer(integral_note):
    '''
    :param integral_note: Integral representation of a note, like 42

    Returns the note in scientific notation so you can feed this into
    other sheetmusic functions
    '''
    return containers.Note(integral_note)

def from_scientific(scientific_note):
    m = re.match(r'^([^0-9]+)([0-9]+)$', str(scientific_note))
    if not m:
        raise ValueError('%s is not in scientific notation' % scientific_note)
    note_within_octave = m.group(1)
    octave = int(m.group(2))
    return containers.Note(note_within_octave, octave)

def maybe_from_scientific(scientific_note):
    try:
        return from_scientific(scientific_note)
    except ValueError:
        return None

def to_scientific(integral_note):
    note = containers.Note(int(integral_note))
    return note.name + str(note.octave)

def from_range_ref(Gnumeric, range_ref):
    workbook_index = 0 # Let's just hope that's always the case
    workbook = Gnumeric.workbooks()[workbook_index]
    sheet_index = int(Gnumeric.functions['sheet'](range_ref)) - 1
    sheet = workbook.sheets()[sheet_index]
    
    rows_list_or_float = Gnumeric.functions['row'](range_ref)
    if type(rows_list_or_float) == list:
        rows = [int(x) for x in rows_list_or_float[0]]
    elif type(rows_list_or_float) == float:
        rows = [int(rows_list_or_float)]
    
    columns_list_or_float = Gnumeric.functions['column'](range_ref)
    if type(columns_list_or_float) == list:
        columns = [int(x[0]) for x in columns_list_or_float]
    elif type(columns_list_or_float) == float:
        columns = [int(columns_list_or_float)]

    return [[sheet.cell_fetch(int(column-1), int(row-1)).get_rendered_text() for row in rows] for column in columns]

def transpose(matrix):
    return zip(*matrix)

def from_range_string(range_string):
    def cell_string_to_pos(cell_string):
        column = string.ascii_uppercase.index(re.match('^([A-Z]).*', cell_string, flags = re.IGNORECASE).group(1).upper())
        row = int(re.match(r'^[A-Z]+([0-9]+)$', cell_string, flags = re.IGNORECASE).group(1))
        return column, row
    (top, left), (bottom, right) = map(cell_string_to_pos, range_string.split(':'))
    return top, left, bottom, right

def rendered_text(Gnumeric, top, left, bottom, right, workbook = 0, sheet = 1.0):
    sheet = Gnumeric.workbooks()[workbook].sheets()[int(sheet) - 1]
    columns = range(left, right + 1)
    rows = range(top, bottom + 1)
    return [[sheet.cell_fetch(column - 1, row - 1).get_rendered_text() for row in rows] for column in columns]
