# Stub versions of some common SDL_test functions.
# Daniel Holth <dholth@fastmail.fm>, 2014

import sdl
import collections

CommonEventStatus = collections.namedtuple("CommonEventStatus", ("done",))

def SDLTest_CommonEvent(event):
    """Check for events that indicate we are finished."""
    done = False

    if event.type == sdl.WINDOWEVENT:
        if event.window.event == sdl.WINDOWEVENT_CLOSE:
            done = True
    elif event.type == sdl.KEYDOWN:
        keysym = event.key.keysym.sym
        if keysym == sdl.K_ESCAPE:
            done = True

    return CommonEventStatus(done=done)
