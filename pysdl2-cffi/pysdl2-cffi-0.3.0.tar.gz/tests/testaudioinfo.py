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

import sys
from _sdl.lib import *

def SDL_Log(message):
    sys.stderr.write(message)

def print_devices(iscapture):
    typestr = "capture" if iscapture else "output"
    n = SDL_GetNumAudioDevices(iscapture)

    SDL_Log("%s devices:\n" % (typestr))

    if n == -1:
        SDL_Log("  Driver can't detect specific %s devices.\n\n" % (typestr))
    elif n == 0:
        SDL_Log("  No %s devices found.\n\n" % (typestr))
    else:
        for i in range(n):
            SDL_Log("  %s\n" % (SDL_GetAudioDeviceName(i, iscapture)))
        SDL_Log("\n")

def main():
    # Enable standard application logging
    SDL_LogSetPriority(SDL_LOG_CATEGORY_APPLICATION, SDL_LOG_PRIORITY_INFO)

    # Load the SDL library
    if SDL_Init(SDL_INIT_AUDIO) < 0:
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Couldn't initialize SDL: %s\n" % (SDL_GetError()))
        return (1)

    # Print available audio drivers
    n = SDL_GetNumAudioDrivers()
    if n == 0:
        SDL_Log("No built-in audio drivers\n\n")
    else:
        SDL_Log("Built-in audio drivers:\n")
        for i in range(n):
            SDL_Log("  %s\n" % (SDL_GetAudioDriver(i)))
        SDL_Log("\n")

    SDL_Log("Using audio driver: %s\n\n" % (SDL_GetCurrentAudioDriver()))

    print_devices(0)
    print_devices(1)

    SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())
