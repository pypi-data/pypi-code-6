# PLAYMUS:  A test application for the SDL mixer library.
# Copyright (C) 1997-2013 Sam Lantinga <slouken@libsdl.org>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

import os
import sys

from _sdl.lib import SDL_Init, SDL_Delay, SDL_Quit, SDL_INIT_AUDIO, SDL_GetError
from _sdl_mixer.lib import *

audio_open = 0
music = ffi.NULL
next_track = 0

def CleanUp(exitcode):
    global music, audio_open
    if Mix_PlayingMusic():
        Mix_FadeOutMusic(1500)
        SDL_Delay(1500)
    if music:
        Mix_FreeMusic(music)
        music = NULL
    if audio_open:
        Mix_CloseAudio()
        audio_open = 0
    SDL_Quit()
    sys.exit(exitcode)

def Usage(argv0):
    sys.stderr.write("Usage: %s [-i] [-l] [-8] [-r rate] [-c channels] [-b buffers] [-v N] [-rwops] <musicfile>\n" % (argv0))

def Menu():
    sys.stdout.write("Available commands: (p)ause (r)esume (h)alt volume(v#) > ")
    sys.stdin.flush()

#     if (scanf("%s" % (buf)) == 1)
#         switch buf[0]:
#         case 'p': case 'P':
#             Mix_PauseMusic()
#             break
#         case 'r': case 'R':
#             Mix_ResumeMusic()
#             break
#         case 'h': case 'H':
#             Mix_HaltMusic()
#             break
#         case 'v': case 'V':
#             Mix_VolumeMusic(int(buf+1))
#             break
#
#     printf("Music playing: %s Paused: %s\n" % (Mix_PlayingMusic() ? "yes" : "no",
#            Mix_PausedMusic() ? "yes" : "no")

def main():
    audio_format = None
    audio_volume = MIX_MAX_VOLUME
    looping = 0
    interactive = 0
    rwops = 0

    # Initialize variables
    audio_rate = 22050*2
    audio_format = AUDIO_S16
    audio_channels = 2
    audio_buffers = 4096

    # Initialize the SDL library
    if SDL_Init(SDL_INIT_AUDIO) < 0 :
        sys.stderr.write("Couldn't initialize SDL: %s\n" % (SDL_GetError()))
        return 255

    # Open the audio device
    if Mix_OpenAudio(audio_rate, audio_format, audio_channels, audio_buffers) < 0:
        sys.stderr.write("Couldn't open audio: %s\n" % (SDL_GetError()))
        return(2)
    else:
        audio_rate = ffi.new("int *")
        audio_format = ffi.new("uint16_t *")
        audio_channels = ffi.new("int *")
        Mix_QuerySpec(audio_rate, audio_format, audio_channels)
        sys.stdout.write("Opened audio at %d Hz %d bit %s (%s), %d bytes audio buffer\n" % (audio_rate[0],
            (audio_format[0] & 0xFF),
            "surround" if (audio_channels[0] > 2)  else "stereo" if (audio_channels[0] > 1) else "mono",
            "BE" if (audio_format[0] & 0x1000) else "LE",
            audio_buffers))
    audio_open = 1

    # Set the music volume
    Mix_VolumeMusic(audio_volume)

    # Set the external music player, if any
    if os.getenv("MUSIC_CMD"):
        Mix_SetMusicCMD(os.getenv("MUSIC_CMD"))

    next_track = 0

    i = 1

    filename = sys.argv[i].encode('utf-8')

    # Load the requested music file
    if rwops:
        music = Mix_LoadMUS_RW(SDL_RWFromFile(filename, "rb"), SDL_TRUE)
    else:
        music = Mix_LoadMUS(filename)
    if  music == ffi.NULL :
        sys.stderr.write("Couldn't load %s: %s\n" % (sys.argv[i], SDL_GetError()))
        CleanUp(2)

    # Play and then exit
    sys.stdout.write("Playing %s\n" % (sys.argv[i]))
    Mix_FadeInMusic(music, looping, 2000)
    while not next_track and (Mix_PlayingMusic() or Mix_PausedMusic()):
        if interactive:
            Menu()
        else:
            SDL_Delay(100)
    Mix_FreeMusic(music)
    music = ffi.NULL

    # If the user presses Ctrl-C more than once, exit.
    SDL_Delay(500)
    if next_track > 1: return

    i += 1

    CleanUp(0)

    # Not reached, but fixes compiler warnings
    return 0

if __name__ == "__main__":
    sys.exit(main())
