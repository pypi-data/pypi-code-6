import functools
from itertools import izip
from Queue import Queue
from threading import Thread

import mingus.containers as c
import mingus.extra.LilyPond as LilyPond
from mingus.midi import fluidsynth, MidiFileOut

import libsheetmusic.util as u

class Sub:
    def __init__(self, function):
        self.queue = Queue()
        def worker(queue):
            while queue.empty():
                function()
        self.thread = Thread(None, target = worker, args = (self.queue,))
        self.thread.start()
    def stop(self):
        self.queue.put(9839232)

def to_track(range_values, key, upper, lower):
    '''
    Convert the cells to sheet music.
    >>> to_track([['C3', 'C3'], ['E3', 'E3'], ['G3', 'G3'], ['C4', 'G4']], 'C', 2, 4)
    '''
    cells = u.transpose(u.range_apply(u.maybe_from_scientific, range_values))
    meter = (int(upper), int(lower))

    t = c.Track()
    b = c.Bar(key = key, meter = meter)
    for row in cells:
        nc = c.NoteContainer()
        for note in row:
            if note != None:
                nc.add_note(note)
        b.place_notes(nc, lower)
        if b.is_full():
            t.add_bar(b)
            b = c.Bar(key = key, meter = meter)
    while b.current_beat != 0.0 and (not b.is_full()):
        b.place_rest(lower)
    t.add_bar(b)
    return t

def sheetmusic(Gnumeric, range_ref, key = "C", upper = 4, lower = 4):
    '''
    Convert the cells to sheet music.
    '''
    t = to_track(u.from_range_ref(Gnumeric, range_ref), key, upper, lower)
    lp = LilyPond.from_Track(t)
    return LilyPond.to_png(lp, '/tmp/track')

def midi(Gnumeric, fn, range_string):
    'Convert the cells to MIDI.'
    top, left, bottom, right = u.from_range_string(Gnumeric, range_string)
    MidiFileOut.write_Track(fn, to_track(u.rendered_text(Gnumeric, top, left, bottom, right)))

def play(Gnumeric, range_string, key = "C", upper = 4, lower = 4, bpm = 120):
    'Play the music in some cells.'
    top, left, bottom, right = u.from_range_string(Gnumeric, range_string)
    track = to_track(u.rendered_text(Gnumeric, top_left_bottom_right), key, upper, lower)
    fluidsynth.play_Track(track, bpm = bpm)

def loop(Gnumeric, range_string, bpm = 120):
    'Loop the music in some cells.'
    raise NotImplementedError
    return Sub(functools.partial(play, Gnumeric, range_string, bpm))

def init():
    sf = '/usr/share/soundfonts/Unison.sf2'
    fluidsynth.init(sf, 'alsa')

def bold(Gnumeric, range_string, workbook = 0, sheet = 0):
    top, left, bottom, right = u.from_range_string(range_string)
    sheet = Gnumeric.workbooks()[workbook].sheets()[sheet]
    range = Gnumeric.Range(top, left, bottom, right)
    style = Gnumeric.GnmStyle()
    style.set_font_bold(1)
    sheet.style_apply_range(range, style)
