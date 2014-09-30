# Names to expose to the outside

import sdl

from .constants import *
from .autohelpers import *

def Mix_PlayChannel(channel, chunk, loops):
    return Mix_PlayChannelTimed(channel, chunk, loops, -1)

def Mix_LoadWAV(file):
    return Mix_LoadWAV_RW(sdl.RWFromFile(file, b"rb"), 1)

def Mix_FadeInChannel(channel,chunk,loops,ms):
    return Mix_FadeInChannelTimed(channel,chunk,loops,ms,-1)