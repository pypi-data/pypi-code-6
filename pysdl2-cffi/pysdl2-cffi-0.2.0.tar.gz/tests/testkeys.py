#
# Copyright (C) 1997-2014 Sam Lantinga <slouken@libsdl.org>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely.
#

# Print out all the scancodes we have, just to verify them

import os, sys

from _sdl.lib import *

def main():
    if SDL_Init(SDL_INIT_VIDEO) < 0:
        sys.stderr.write("Couldn't initialize SDL: %s\n" % (SDL_GetError()))
        os.exit(1)
    for scancode in range(SDL_NUM_SCANCODES):
        sys.stdout.write("Scancode #%d, \"%s\"\n" %
                         (scancode,
                          SDL_GetScancodeName(scancode)))
    SDL_Quit()
    return (0)

if __name__ == "__main__":
    main()