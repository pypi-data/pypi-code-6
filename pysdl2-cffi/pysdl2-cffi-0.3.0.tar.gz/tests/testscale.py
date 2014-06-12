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
# Simple program:  Move N sprites around on the screen as fast as possible

# Translated to Python by Daniel Holth <dholth@fastmail.fm>

import sys
import time

from _sdl.lib import *

#include "SDL_test_common.h"

WINDOW_WIDTH	= 640
WINDOW_HEIGHT	= 480

class DrawState(object):
    def __init__(self):
        self.window = None
        self.renderer = None
        self.background = None
        self.sprite = None
        self.sprite_rect = SDL_Rect()
        self.scale_direction = 0

# Call this instead of exit(), so we can clean up SDL: atexit() is evil.
def quit(rc):
    # SDLTest_CommonQuit(state)
    sys.exit(rc)

def LoadTexture(renderer, file, transparent):
    # Load the sprite image
    rwops = SDL_RWFromFile(file, 'r')
    temp = SDL_LoadBMP_RW(rwops, True)
    if temp == ffi.NULL:
        sys.stderr.write("Couldn't load %s: %s\n" % (file, SDL_GetError()))
        return None

    # Set transparent pixel as the pixel at (0,0)
    if transparent:
        if temp.format.palette:
            SDL_SetColorKey(temp, True, ffi.cast("uint8_t *", temp.pixels)[0])
        else:
            # TODO ffi.cast to correct-width type
            bpp = temp.format.BitsPerPixel
            if bbp == 15:
                SDL_SetColorKey(temp, True, temp.pixels[0] & 0x00007FFF)
            elif bpp == 16:
                SDL_SetColorKey(temp, SDL_TRUE, temp.pixels[0])
            elif bpp == 24:
                SDL_SetColorKey(temp, True, temp.pixels[0] & 0x00FFFFFF)
            elif bpp == 32:
                SDL_SetColorKey(temp, True, temp.pixels[0])

    # Create textures from the image
    texture = SDL_CreateTextureFromSurface(renderer, temp)
    SDL_FreeSurface(temp)
    if not texture:
        sys.stderr.write("Couldn't create texture: %s\n" % (SDL_GetError()))
        return None

    # We're ready to roll. :)
    return texture

def Draw(s):
    viewport = SDL_Rect()
    SDL_RenderGetViewport(s.renderer, viewport)

    # Draw the background
    SDL_RenderCopy(s.renderer, s.background, ffi.NULL, ffi.NULL)

    # Scale and draw the sprite
    s.sprite_rect.w += s.scale_direction
    s.sprite_rect.h += s.scale_direction
    if s.scale_direction > 0:
        if s.sprite_rect.w >= viewport.w or s.sprite_rect.h >= viewport.h:
            s.scale_direction = -1
    else:
        if s.sprite_rect.w <= 1 or s.sprite_rect.h <= 1:
            s.scale_direction = 1
    s.sprite_rect.x = (viewport.w - s.sprite_rect.w) // 2
    s.sprite_rect.y = (viewport.h - s.sprite_rect.h) // 2

    SDL_RenderCopy(s.renderer, s.sprite, ffi.NULL, s.sprite_rect)

    # Update the screen!
    SDL_RenderPresent(s.renderer)

def main():
    event = SDL_Event()

    SDL_Init(SDL_INIT_VIDEO)

    # Initialize test framework
#    state = SDLTest_CommonCreateState(argv, SDL_INIT_VIDEO)
#     if not state:
#         return 1

#     for (i = 1; i < argc;) {
#
#         consumed = SDLTest_CommonArg(state, i)
#         if consumed == 0:
#             SDL_Log("Usage: %s %s\n" % (argv[0], SDLTest_CommonUsage(state)))
#             return 1
#         i += consumed
#     if not SDLTest_CommonInit(state):
#         quit(2)

    drawstates = [DrawState()]
    for i in range(len(drawstates)):
        drawstate = drawstates[i]

        drawstate.window = SDL_CreateWindow("Scale %d" % i,
                                            SDL_WINDOWPOS_UNDEFINED,
                                            SDL_WINDOWPOS_UNDEFINED,
                                            640, 480,
                                            SDL_WINDOW_SHOWN)

        drawstate.renderer = SDL_CreateRenderer(drawstate.window, -1, 0)
        drawstate.sprite = LoadTexture(drawstate.renderer, "icon.bmp", True)
        drawstate.background = LoadTexture(drawstate.renderer, "sample.bmp", False)
        if not drawstate.sprite or not drawstate.background:
            quit(2)
        rc, format, access, w, h = SDL_QueryTexture(drawstate.sprite)
        drawstate.sprite_rect.w = w
        drawstate.sprite_rect.h = h
        drawstate.scale_direction = 1

    # Main render loop
    frames = 0
    then = SDL_GetTicks()
    done = 0
    while not done:
        # Check for events
        frames += 1
        while SDL_PollEvent(event):
            if event.type == SDL_QUIT:
                done = 1
        for i in range(len(drawstates)):
            if not drawstates[i].window:
                continue
            Draw(drawstates[i])

    # Print out some timing information
    now = SDL_GetTicks()
    if now > then:
        fps = (frames * 1000) / (now - then)
        sys.stderr.write("%2.2f frames per second\n" % (fps))

    # TODO for x in drawstates: free stuff

    quit(0)
    return 0

if __name__ == "__main__":
    main()
