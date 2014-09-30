"""
Information about which SDL parameters can be passed as NULL
"""

nullable = {
            "SDL_GetWindowGammaRamp": ("red", "blue", "green"),
            "SDL_RenderCopy": ("srcrect", "dstrect"),
            "SDL_RenderCopyEx": ("srcrect", "dstrect"),
            "SDL_RenderDrawRect": ("rect",),
            "SDL_RenderFillRect": ("rect",),
            "SDL_RenderReadPixels": ("rect",),
            "SDL_RenderSetClipRect": ("rect",),
            # TODO
            }