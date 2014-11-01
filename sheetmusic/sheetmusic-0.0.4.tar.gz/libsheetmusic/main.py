import functools
import itertools

import libsheetmusic.spreadsheet as s
import libsheetmusic.util as u

def note_functions():
    method_names = ['octave_up', 'octave_down']
    template = 'lambda root: s.note_method("%s", root)'
    return {method_name: eval(template % method_name) for method_name in method_names}

def interval_functions():
    special = 'from_shorthand',
    maybe_useful = ['get_interval', 'measure', 'invert',]
    questions = ['is_consonant', 'is_dissonant', 'is_imperfect_consonant', 'is_perfect_consonant',]

    keyed = ['second', 'third', 'fourth','fifth', 'sixth', 'seventh', 'unison']
    not_keyed = [
        'augmented_unison',
        'major_fifth', 'major_fourth', 'major_second', 'major_seventh', 'major_sixth', 'major_third', 'major_unison',
        'minor_fifth', 'minor_fourth', 'minor_second', 'minor_seventh', 'minor_sixth', 'minor_third', 'minor_unison',
        'perfect_fifth', 'perfect_fourth', 'unison'
    ]
    keyed_template = 'lambda root, key: s.keyed_interval("%s", root, key)'
    nonkeyed_interval = 'lambda root: s.nonkeyed_interval("%s", root)'
    keyed_functions = {name + '_interval': eval(keyed_template % name) for name in keyed}
    nonkeyed_functions = {name + '_interval': eval(nonkeyed_interval % name) for name in not_keyed}
    named = u.merge(keyed_functions, nonkeyed_functions)
    fancy = {'interval': _interval}
    return u.merge(named, fancy)

def _interval(majorminor, number, root):
    words = { 1: 'unison', 2: 'second', 3: 'third', 4: 'fourth',
              5: 'fifth',  6: 'sixth',  7: 'seventh' }
    if number in words:
        return s.nonkeyed_interval('%s_%s' % (majorminor, words[number]), root)

def scale_functions():
    scale_names = [
        'aeolian',
        'chromatic',
        'diatonic',
        'diminished',
        'dorian',
        'harmonic_minor',
        'ionian',
        'locrian',
        'lydian',
        'melodic_minor',
        'mixolydian',
        'natural_minor',
        'phrygian',
        'whole_note'
    ]
    template = 'lambda base: s.scale("%s", base)'
    return {name + '_scale':  eval(template % name) for name in scale_names}

def chord_functions():
    chord_names = [
        'I', 'I7', 'II', 'II7', 'III', 'III7', 'IV', 'IV7', 'V', 'V7', 'VI', 'VI7', 'VII', 'VII7',
        'augmented_major_seventh', 'augmented_minor_seventh', 'augmented_triad',
        'diminished_seventh', 'diminished_triad',
        'dominant', 'dominant7', 'dominant_flat_five', 'dominant_flat_ninth', 'dominant_ninth',
        'dominant_seventh', 'dominant_sharp_ninth', 'dominant_sixth','dominant_thirteenth',
        'eleventh', 'first_inversion',
        'half_diminished_seventh', 'hendrix_chord',
    #   'ii', 'ii7', 'iii', 'iii7', 'vi', 'vi7', 'vii', 'vii7',
        'invert', 'lydian_dominant_seventh',
        'major_ninth', 'major_seventh', 'major_sixth', 'major_thirteenth', 'major_triad',
        'mediant', 'mediant7', 'minor_eleventh', 'minor_major_seventh', 'minor_ninth',
        'minor_seventh', 'minor_seventh_flat_five', 'minor_sixth', 'minor_thirteenth',
        'minor_triad', 'second_inversion', 'seventh', 'sixth_ninth',
        'subdominant', 'subdominant7', 'submediant', 'submediant7', 'subtonic', 'subtonic7',
        'supertonic', 'supertonic7',
        'suspended_fourth_ninth', 'suspended_fourth_triad', 'suspended_second_triad',
        'suspended_seventh', 'suspended_triad', 'third_inversion',
        'tonic', 'tonic7', 'triad',
    ]
    chord_template = 'lambda base: s.chord("%s", base)'
    arpeggio_template = 'lambda base: s.arpeggio("%s", base)'

    chord = {name + '_chord': eval(chord_template % name) for name in chord_names}
    arpeggio = {name + '_arpeggio': eval(arpeggio_template % name) for name in chord_names}
    return u.merge(chord, arpeggio)

def gnumeric_functions():
    try:
        import Gnumeric
    except ImportError:
        def f(*args, **kwargs):
            raise EnvironmentError('This must be run from inside Gnumeric.')
        rep = progression = f
    else:
        def progression(progression_range_ref, string_root_note):
            return s.progression(Gnumeric, progression_range_ref, string_root_note)
        def rep(range_ref, times):
            return s.rep(Gnumeric, range_ref, times)

    return {
        'progression': progression,
        'rep': rep,
    }

def util_functions():
    func_names = ['_'.join(xs) for xs in itertools.product(['from','to'],['scientific','integer'])]
    return {func_name: getattr(u, func_name) for func_name in func_names}

custom_functions = {}
def function_functions():
    def define(x):
        result = eval(x)
        custom_functions[x] = result
        return x

    def call(x, *args):
        return custom_functions[x](*args)

    return {'define': define, 'call': call}

def functions():
    fs = [
        note_functions, scale_functions, chord_functions,
        interval_functions, util_functions,
        gnumeric_functions, function_functions
    ]
    return reduce(u.merge, [f() for f in fs])
