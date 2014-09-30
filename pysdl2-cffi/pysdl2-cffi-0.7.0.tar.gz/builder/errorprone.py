"""
Information about which SDL functions can return an error and how to handle it.
"""

# Most SDL functions return -1 on error.
return_neg1 = set(x.strip() for x in """
SDL_CondBroadcast
SDL_CondSignal
SDL_CondWait
SDL_CondWaitTimeout
SDL_CreateWindowAndRenderer
SDL_FillRect
SDL_GameControllerAddMapping
SDL_GameControllerAddMappingsFromRW
SDL_GetRenderDrawBlendMode
SDL_GetRenderDrawColor
SDL_GetWindowDisplayIndex
SDL_HapticGetEffectStatus
SDL_HapticIndex
SDL_HapticNewEffect
SDL_HapticNumEffectsPlaying
SDL_HapticPause
SDL_HapticRumbleInit
SDL_HapticRumblePlay
SDL_HapticRumbleStop
SDL_HapticRunEffect
SDL_HapticSetAutocenter
SDL_HapticSetGain
SDL_HapticStopAll
SDL_HapticStopEffect
SDL_HapticUnpause
SDL_HapticUpdateEffect
SDL_RenderClear
SDL_RenderCopy
SDL_RenderCopyEx
SDL_RenderDrawLine
SDL_RenderDrawLines
SDL_RenderDrawPoint
SDL_RenderDrawPoints
SDL_RenderDrawRect
SDL_RenderDrawRects
SDL_RenderFillRect
SDL_RenderFillRects
SDL_RenderSetClipRect
SDL_RenderSetViewport
SDL_SemPost
SDL_SetRenderDrawBlendMode
SDL_SetRenderDrawColor
SDL_SetRenderTarget
SDL_ShowMessageBox
SDL_ShowSimpleMessageBox
SDL_TLSSet
SDL_TryLockMutex
SDL_UpdateWindowSurface
SDL_UpdateWindowSurfaceRects
SDL_VideoInit

TTF_Init
""".splitlines())

# The 'NULL on error' list is probably more incomplete than the others:
return_null = set(x.strip() for x in """
SDL_AddTimer
SDL_CreateRenderer
SDL_CreateSoftwareRenderer
SDL_CreateTextureFromSurface
SDL_GameControllerOpen
SDL_GetBasePath
SDL_GetWindowSurface
SDL_HapticName
SDL_HapticOpen
SDL_HapticOpenFromJoystick
SDL_HapticOpenFromMouse
SDL_JoystickOpen
SDL_LoadBMP_RW
SDL_LoadObject
SDL_LoadWAV_RW
SDL_RWFromConstMem
SDL_RWFromFP
SDL_RWFromFile
SDL_RWFromMem

IMG_Load
IMG_Load_RW
IMG_LoadTyped_RW
IMG_LoadCUR_RW
IMG_LoadICO_RW
IMG_LoadBMP_RW
IMG_LoadPNM_RW
IMG_LoadXPM_RW
IMG_LoadXCF_RW
IMG_LoadPCX_RW
IMG_LoadGIF_RW
IMG_LoadJPG_RW
IMG_LoadTIF_RW
IMG_LoadPNG_RW
IMG_LoadTGA_RW
IMG_LoadLBM_RW
IMG_LoadXV_RW
IMG_ReadXPMFromArray

TTF_OpenFont
TTF_OpenFontIndex
TTF_OpenFontRW
TTF_OpenFontIndexRW

TTF_RenderGlyph_Blended
TTF_RenderGlyph_Shaded
TTF_RenderGlyph_Solid
TTF_RenderText_Blended
TTF_RenderText_Blended_Wrapped
TTF_RenderText_Shaded
TTF_RenderText_Solid
TTF_RenderUNICODE_Blended
TTF_RenderUNICODE_Blended_Wrapped
TTF_RenderUNICODE_Shaded
TTF_RenderUNICODE_Solid
TTF_RenderUTF8_Blended
TTF_RenderUTF8_Blended_Wrapped
TTF_RenderUTF8_Shaded
TTF_RenderUTF8_Solid
""".splitlines())

# A few functions actually return 0, not -1, on error.
return_zero = set(x.strip() for x in """
SDL_OpenAudioDevice
""".splitlines())

error_handlers =  ["if rc == -1: raise SDLError()",
                   "if rc == 0: raise SDLError()",
                   "if rc == ffi.NULL: raise SDLError()"]

error_key = zip((return_neg1, return_zero, return_null), error_handlers)

def handler_for_function(fname):
    for functions, handler in error_key:
        if fname in functions:
            return handler
