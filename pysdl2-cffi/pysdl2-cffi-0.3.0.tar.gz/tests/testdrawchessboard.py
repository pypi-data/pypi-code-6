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
# This file is created by : Nitin Jain (nitin.j4@samsung.com)
#

# Sample program:  Draw a Chess Board  by using SDL_CreateSoftwareRenderer API

from _sdl.lib import *

def DrawChessBoard(renderer):
    row = 0
    coloum = 0
    x = 0
    rect = SDL_Rect()
    darea = SDL_Rect()

    # Get the Size of drawing surface
    SDL_RenderGetViewport(renderer, darea)

    for row in range(8):
        coloum = row%2
        x = x + coloum

        for coloum in range(coloum, 4+(row%2)):

            SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0xFF)

            rect.w = darea.w/8
            rect.h = darea.h/8
            rect.x = x * rect.w
            rect.y = row * rect.h
            x = x + 2
            SDL_RenderFillRect(renderer, rect)

        x = 0

def main():
    # Enable standard application logging
    SDL_LogSetPriority(SDL_LOG_CATEGORY_APPLICATION, SDL_LOG_PRIORITY_INFO)

    # Initialize SDL
    if SDL_Init(SDL_INIT_VIDEO) != 0:
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "SDL_Init fail : %s\n" % (SDL_GetError()))
        return 1


    # Create window and renderer for given surface
    window = SDL_CreateWindow("Chess Board", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 640, 480, SDL_WINDOW_SHOWN)
    if not window:
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Window creation fail : %s\n" % (SDL_GetError()))
        return 1
    surface = SDL_GetWindowSurface(window)
    renderer = SDL_CreateSoftwareRenderer(surface)
    if not renderer:
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Render creation for surface fail : %s\n" % (SDL_GetError()))
        return 1

    # Clear the rendering surface with the specified color
    SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, 0xFF)
    SDL_RenderClear(renderer)

    # Draw the Image on rendering surface
    e = SDL_Event()
    while True:
        if SDL_PollEvent(e):
            if e.type == SDL_QUIT:
                break

            if e.key.keysym.sym == SDLK_ESCAPE:
                break

        DrawChessBoard(renderer)

        # Got everything on rendering surface,
        # now Update the drawing image on window screen
        SDL_UpdateWindowSurface(window)

if __name__ == "__main__":
    main()
