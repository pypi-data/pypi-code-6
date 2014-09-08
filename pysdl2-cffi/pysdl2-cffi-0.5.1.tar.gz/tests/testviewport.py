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
# Simple program:  Check viewports

import os

from _sdl.lib import *
from sdl_test import SDLTest_CommonEvent

# Call this instead of exit(), so we can clean up SDL: atexit() is evil.
def quit(rc):
    # SDLTest_CommonQuit(state)
    os.exit(rc)


def DrawOnViewport(renderer, viewport):
    # Set the viewport
    SDL_RenderSetViewport(renderer, viewport)

    # Draw a gray background
    SDL_SetRenderDrawColor(renderer, 0x80, 0x80, 0x80, 0xFF)
    SDL_RenderClear(renderer)

    # Test inside points
    SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xF, 0xFF)
    SDL_RenderDrawPoint(renderer, viewport.h//2 + 10, viewport.w//2)
    SDL_RenderDrawPoint(renderer, viewport.h//2 - 10, viewport.w//2)
    SDL_RenderDrawPoint(renderer, viewport.h//2     , viewport.w//2 - 10)
    SDL_RenderDrawPoint(renderer, viewport.h//2     , viewport.w//2 + 10)

    # Test horizontal and vertical lines
    SDL_SetRenderDrawColor(renderer, 0x00, 0xFF, 0x00, 0xFF)
    SDL_RenderDrawLine(renderer, 1, 0, viewport.w-2, 0)
    SDL_RenderDrawLine(renderer, 1, viewport.h-1, viewport.w-2, viewport.h-1)
    SDL_RenderDrawLine(renderer, 0, 1, 0, viewport.h-2)
    SDL_RenderDrawLine(renderer, viewport.w-1, 1, viewport.w-1, viewport.h-2)

    # Test diagonal lines
    SDL_SetRenderDrawColor(renderer, 0x00, 0x00, 0xFF, 0xFF)
    SDL_RenderDrawLine(renderer, 0, 0,
                       viewport.w-1, viewport.h-1)
    SDL_RenderDrawLine(renderer, viewport.w-1, 0,
                       0, viewport.h-1)

    # Test outside points
    SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xF, 0xFF)
    SDL_RenderDrawPoint(renderer, viewport.h/2 + viewport.h, viewport.w/2)
    SDL_RenderDrawPoint(renderer, viewport.h/2 - viewport.h, viewport.w/2)
    SDL_RenderDrawPoint(renderer, viewport.h/2     , viewport.w/2 - viewport.w)
    SDL_RenderDrawPoint(renderer, viewport.h/2     , viewport.w/2 + viewport.w)

    rect = SDL_Rect()

    # Add a box at the top
    rect.w = 8
    rect.h = 8
    rect.x = (viewport.w - rect.w) / 2
    rect.y = 0

    SDL_RenderFillRect(renderer, rect)

def main():
    use_target = False

    SDL_Init(SDL_INIT_VIDEO)

    i = 0
    window = SDL_CreateWindow("It's a window",
                              SDL_WINDOWPOS_UNDEFINED,
                              SDL_WINDOWPOS_UNDEFINED,
                              640, 480,
                              0)
    renderer = SDL_CreateRenderer(window, -1, 0)

    SDL_SetRenderDrawColor(renderer, 0xA0, 0xA0, 0xA0, 0xFF)
    SDL_RenderClear(renderer)

    viewport = SDL_Rect()
    event = SDL_Event()

    # Main render loop
    frames = 0
    then = SDL_GetTicks()
    done = 0
    j = 0
    while not done:
        # Check for events
        frames += 1
        while SDL_PollEvent(event):
            done = SDLTest_CommonEvent(event=event).done
            if done:
                break

        # Move a viewport box in steps around the screen
        viewport.x = j * 100
        viewport.y = viewport.x
        viewport.w = 100 + j * 50
        viewport.h = 100 + j * 50
        j = (j + 1) % 4
        print("Current Viewport x=%i y=%i w=%i h=%i\n" % (viewport.x, viewport.y, viewport.w, viewport.h))

        for i in range(1):
            # Draw using viewport
            DrawOnViewport(renderer, viewport)

            # Update the screen!
            SDL_RenderPresent(renderer)

        SDL_Delay(1000)

    # Print out some timing information
    now = SDL_GetTicks()
    if now > then:
        fps = (frames * 1000.0) / (now - then)
        print("%2.2f frames per second\n" % (fps))

    return 0

if __name__ == "__main__":
    main()
