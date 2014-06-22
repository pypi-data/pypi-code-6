from functools import partial

import libsheetmusic.console as c

import Gnumeric

play = partial(c.play, Gnumeric)
loop = partial(c.loop, Gnumeric)
midi = partial(c.midi, Gnumeric)
sheetmusic = partial(c.sheetmusic, Gnumeric)
bold = partial(c.bold, Gnumeric)
