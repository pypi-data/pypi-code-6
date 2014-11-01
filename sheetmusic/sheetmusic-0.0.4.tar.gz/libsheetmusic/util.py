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

def parse_range_ref(Gnumeric, range_ref):
    workbook_index = 0 # Let's just hope that's always the case
    workbook = Gnumeric.workbooks()[workbook_index]
    sheet_index = int(Gnumeric.functions['sheet'](range_ref)) - 1
    sheet = workbook.sheets()[sheet_index]
    
    rows_list_or_float = Gnumeric.functions['row'](range_ref)
    if type(rows_list_or_float) == list:
        top = int(min(rows_list_or_float[0]))
        bottom = int(max(rows_list_or_float[0]))
    elif type(rows_list_or_float) == float:
        top = bottom = int(rows_list_or_float)
    
    columns_list_or_float = Gnumeric.functions['column'](range_ref)
    if type(columns_list_or_float) == list:
        left = int(min(x[0] for x in columns_list_or_float))
        right = int(max(x[0] for x in columns_list_or_float))
    elif type(columns_list_or_float) == float:
        left = right = int(columns_list_or_float)

    return left - 1, top - 1, right - 1, bottom - 1

def transpose(matrix):
    return zip(*matrix)

def cell_string_to_pos(cell_string):
    column = string.ascii_uppercase.index(re.match('^([A-Z]).*', cell_string, flags = re.IGNORECASE).group(1).upper())
    row = int(re.match(r'^[A-Z]+([0-9]+)$', cell_string, flags = re.IGNORECASE).group(1)) - 1
    return column, row

def parse_range_string(range_string):
    (left, top), (right, bottom) = map(cell_string_to_pos, range_string.split(':'))
    return left, top, right, bottom

def cell_positions(left, top, right, bottom):
    return [[(x,y) for y in range(top, bottom + 1)] for x in range(left, right + 1)]

def rendered_text(Gnumeric, x, y, workbook = 0, sheet = 1.0):
    sheet = Gnumeric.workbooks()[workbook].sheets()[int(sheet) - 1]
    return sheet.cell_fetch(x,y).get_rendered_text()

def italic(Gnumeric, x, y, workbook = 0, sheet = 1.0):
    sheet = Gnumeric.workbooks()[workbook].sheets()[int(sheet) - 1]
    result = sheet.cell_fetch(x,y).get_style().get_font_italic()
    return {0:False,1:True}[result]

def range_rendered_text(Gnumeric, left, top, right, bottom, workbook = 0, sheet = 1.0):
    columns = cell_positions(left, top, right, bottom)
    return [[rendered_text(Gnumeric, x,y) for x, y in column] for column in columns]

def range_rendered_text_and_italic(Gnumeric, left, top, right, bottom, workbook = 0, sheet = 1.0):
    columns = cell_positions(left, top, right, bottom)
    return [[(rendered_text(Gnumeric, x,y), italic(Gnumeric, x, y)) for x, y in column] for column in columns]

def iterate(func):
    'Decorate a function with this so I can pretend that I\'m using generators.'
    TIMES = 100
    def wrapper(*args, **kwargs):
        out = []
        iterable = iter(func(*args, **kwargs))
        for _ in range(TIMES):
            try:
                out.append(next(iterable))
            except StopIteration:
                break
        return out
    return wrapper

def repeat(func):
    TIMES = 30
    def wrapper(*args, **kwargs):
        result = list(func(*args, **kwargs))
        out = []
        for column in result:
            out.append(column * TIMES)
        return out
    return wrapper
