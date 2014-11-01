from functools import partial

import libsheetmusic.console as c

try:
    import Gnumeric
except ImportError:
    pass
else:
    play = partial(c.play, Gnumeric)
    loop = partial(c.loop, Gnumeric)
    midi = partial(c.midi, Gnumeric)
    sheetmusic = partial(c.sheetmusic, Gnumeric)
    init = c.init
#   bold = partial(c.bold, Gnumeric)
#   show_track = partial(c.show_track, Gnumeric)
#   show_rendered_text = partial(c.show_rendered_text, Gnumeric)
#   show_range_coords = partial(c.show_range_coords, Gnumeric)
