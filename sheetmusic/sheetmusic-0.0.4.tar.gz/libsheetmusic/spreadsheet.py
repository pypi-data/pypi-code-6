from itertools import repeat

import libsheetmusic.music as m
import libsheetmusic.util as u

@u.iterate
def scale(func_name, string_note):
    note_in = u.from_scientific(string_note)
    notes_out = m.scale(func_name, note_in)
    return u.range_apply(u.to_scientific, notes_out)

@u.iterate
def chord(func_name, string_note, *args, **kwargs):
    return u.range_apply(u.to_scientific, m.chord(func_name, u.from_scientific(string_note), *args, **kwargs))

@u.iterate
def arpeggio(func_name, string_note, *args, **kwargs):
    return u.range_apply(u.to_scientific, m.arpeggio(func_name, u.from_scientific(string_note), *args, **kwargs))

@u.repeat
def progression(Gnumeric, progression_range_ref, string_root_note):
    if 'RangeRef' in str(type(progression_range_ref)):
        left, top, right, bottom = u.parse_range_ref(Gnumeric, progression_range_ref)
        # the_progression = u.range_rendered_text(Gnumeric, progression_range_ref)
        raise NotImplementedError
    else:
        the_progression = progression_range_ref
    root_note = u.from_scientific(string_root_note)
    return u.range_apply(u.to_scientific, m.progression(the_progression, root_note))

def keyed_interval(func_name, string_note, key):
    key = str(key)[0]
    return u.to_scientific(m.keyed_interval(func_name, u.from_scientific(string_note), key))

def nonkeyed_interval(func_name, string_note):
    return u.to_scientific(m.nonkeyed_interval(func_name, u.from_scientific(string_note)))

def note_method(method_name, string_note):
    note = u.from_scientific(string_note)
    getattr(note, method_name)()
    return u.to_scientific(note)

@u.repeat
def rep(Gnumeric, range_ref, times):
    left, top, right, bottom = u.parse_range_ref(Gnumeric, range_ref)
    values = u.range_rendered_text(Gnumeric, left, top, right, bottom,
        sheet = 1) # Gnumeric.functions['sheet'](range_ref))
    for column in values:
        newcolumn = []
        for cell in column:
            newcolumn.extend([cell] * int(times))
        yield newcolumn
