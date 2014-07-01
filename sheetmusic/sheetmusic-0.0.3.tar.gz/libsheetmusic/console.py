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
    def note_and_italic(cell):
        maybe_note, italic = cell
        return u.maybe_from_scientific(maybe_note), italic
    cells = u.transpose(u.range_apply(note_and_italic, range_values))
    meter = (int(upper), int(lower))

    ncs = []
    for row in cells:
        nc = c.NoteContainer()
        for note, _ in row:
            if note != None:
                nc.add_note(note)
        allitalic = all(note_italic[1] for note_italic in row)
        ncs.append((nc, allitalic))

    t = c.Track()
    while len(ncs) > 0:
        nc, allitalic = ncs.pop(0)
        duration = 0.25
        while allitalic and len(ncs) > 0 and ncs[0][0] == nc:
            duration += 0.25
            _, allitalic = ncs.pop(0)
        if not t.add_notes(nc, duration = int(1/duration)):
            raise AssertionError('I failed to add a note container.')
    return t

def sheetmusic(Gnumeric, range_ref, key = "C", upper = 4, lower = 4):
    '''
    Convert the cells to sheet music.
    '''
    left, top, right, bottom = u.parse_range_ref(Gnumeric, range_ref)
    values = u.range_rendered_text(Gnumeric, left, top, right, bottom,
        sheet = 1) #Gnumeric.functions['sheet'](range_ref))
    t = to_track(values, key, upper, lower)
    lp = LilyPond.from_Track(t)
    return LilyPond.to_png(lp, '/tmp/track')

def midi(Gnumeric, fn, range_string, key = "C", upper = 4, lower = 4, bpm = 120):
    'Convert the cells to MIDI.'
    top, left, bottom, right = u.parse_range_string(range_string)
    MidiFileOut.write_Track(fn, to_track(u.rendered_text(Gnumeric, top, left, bottom, right), key, upper, lower), bpm = bpm)

def play(Gnumeric, range_string, key = "C", upper = 4, lower = 4, bpm = 120):
    'Play the music in some cells.'
    def track(range_string):
        top, left, bottom, right = u.parse_range_string(range_string)
        stuff = u.range_rendered_text_and_italic(Gnumeric, top, left, bottom, right)
        return to_track(stuff, key, upper, lower)
    fluidsynth.play_Track(track(range_string), bpm = bpm)

def loop(Gnumeric, range_string, key = "C", upper = 4, lower = 4, bpm = 120):
    'Loop the music in some cells.'
    return Sub(functools.partial(play, Gnumeric, range_string, key, upper, lower, bpm))

def init():
    sf = '/usr/share/soundfonts/Unison.sf2'
    fluidsynth.init(sf, 'alsa')
    fluidsynth.play_Note(c.Note('A'))

'''
def show_track(Gnumeric, range_string, key = "C", upper = 4, lower = 4, bpm = 120):
    'Play the music in some cells.'
    top, left, bottom, right = u.parse_range_string(range_string)
    track = to_track(u.rendered_text(Gnumeric, top, left, bottom, right), key, upper, lower)
    return track

def show_rendered_text(Gnumeric, range_string, key = "C", upper = 4, lower = 4, bpm = 120):
    'Play the music in some cells.'
    top, left, bottom, right = u.parse_range_string(range_string)
    return u.rendered_text(Gnumeric, top, left, bottom, right)
'''
