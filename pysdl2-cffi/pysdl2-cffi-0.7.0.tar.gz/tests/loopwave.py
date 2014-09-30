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

# Program to load a wave file and loop playing it using SDL sound

# loopwaves.c is much more robust in handling WAVE files --
#    This is only for simple WAVEs

import sys
from _sdl.lib import *

class wave():
    spec = SDL_AudioSpec()
    sound_p = ffi.new("uint8_t **")
    soundlen_p = ffi.new("uint32_t *")
    soundpos = 0
    soundlen = 0

def SDL_Log(message):
    sys.stderr.write(message)

SDL_LogError = SDL_Log

# Call this instead of exit(), so we can clean up SDL: atexit() is evil.
def quit(rc):
    SDL_Quit()
    sys.exit(rc)

def fillerup(unused, stream, len):
    # print("fillerup", stream, len)
    # Set up the pointers
    waveptr = wave.sound_p[0] + wave.soundpos
    waveleft = wave.soundlen_p[0] - wave.soundpos

    # Go!
    while waveleft <= len:
        SDL_memcpy(stream, waveptr, waveleft)
        stream += waveleft
        len -= waveleft
        waveptr = wave.sound_p[0]
        waveleft = wave.soundlen_p[0]
        wave.soundpos = 0
    SDL_memcpy(stream, waveptr, len)
    wave.soundpos += len

done = 0
def poked(sig):
    global done
    done = 1

def main():
    # Enable standard application logging
    SDL_LogSetPriority(SDL_LOG_CATEGORY_APPLICATION, SDL_LOG_PRIORITY_INFO)

    # Load the SDL library
    if SDL_Init(SDL_INIT_AUDIO) < 0:
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION,
                     "Couldn't initialize SDL: %s\n" % (SDL_GetError()))
        return 1

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "sample.wav"

    # Load the wave file into memory
    rwops = SDL_RWFromFile(filename, "rb")

    if SDL_LoadWAV_RW(rwops,
                      1,
                      wave.spec,
                      wave.sound_p,
                      wave.soundlen_p) == ffi.NULL:
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION,
                     "Couldn't load %s: %s\n" % (filename, SDL_GetError()))
        quit(1)
    else:
        print("Loaded " + filename)

    wave.spec.callback = ffi.callback("SDL_AudioCallback", fillerup)

# #if HAVE_SIGNAL_H
#     # Set the signals
# #ifdef SIGHUP
#     signal(SIGHUP, poked)
# #endif
#     signal(SIGINT, poked)
# #ifdef SIGQUIT
#     signal(SIGQUIT, poked)
# #endif
#     signal(SIGTERM, poked)
# #endif # HAVE_SIGNAL_H

    # Show the list of available drivers
    SDL_Log("Available audio drivers:")
    for i in range(SDL_GetNumAudioDrivers()):
        SDL_Log("%i: %s" % (i, SDL_GetAudioDriver(i)))

    # Initialize fillerup() variables
    if SDL_OpenAudio(wave.spec, ffi.NULL) < 0:
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION,
                     "Couldn't open audio: %s\n" % (SDL_GetError()))
        SDL_FreeWAV(wave.sound)
        quit(2)

    SDL_Log("Using audio driver: %s\n" % (SDL_GetCurrentAudioDriver()))

    # Let the audio run
    SDL_PauseAudio(0)
    while not done and (SDL_GetAudioStatus() == SDL_AUDIO_PLAYING):
        SDL_Delay(1000)

    # Clean up on signal
    SDL_CloseAudio()
    SDL_FreeWAV(wave.sound_p[0])
    SDL_Quit()
    return 0

if __name__ == "__main__":
    main()
