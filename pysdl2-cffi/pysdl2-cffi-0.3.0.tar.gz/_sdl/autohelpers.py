# Automatically generated wrappers.
# Override by adding wrappers to helpers.py.
from .dso import ffi, _LIB
from .structs import Struct, unbox, SDLError

def SDL_AddEventWatch(filter, userdata):
    """
    ``void SDL_AddEventWatch(int SDL_AddEventWatch(void *, SDL_Event *), void *)``
    """
    filter_c = unbox(filter, 'int(*)(void *, SDL_Event *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_AddEventWatch(filter_c, userdata_c)

def SDL_AddHintCallback(name, callback, userdata):
    """
    ``void SDL_AddHintCallback(char const *, void SDL_AddHintCallback(void *, char const *, char const *, char const *), void *)``
    """
    name_c = name
    callback_c = unbox(callback, 'void(*)(void *, char const *, char const *, char const *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_AddHintCallback(name_c, callback_c, userdata_c)

def SDL_AddTimer(interval, callback, param):
    """
    ``int SDL_AddTimer(uint32_t, uint32_t SDL_AddTimer(uint32_t, void *), void *)``
    """
    interval_c = interval
    callback_c = unbox(callback, 'uint32_t(*)(uint32_t, void *)')
    param_c = unbox(param, 'void *')
    rc = _LIB.SDL_AddTimer(interval_c, callback_c, param_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_AllocFormat(pixel_format):
    """
    ``SDL_PixelFormat * SDL_AllocFormat(uint32_t)``
    """
    pixel_format_c = pixel_format
    rc = _LIB.SDL_AllocFormat(pixel_format_c)
    return rc

def SDL_AllocPalette(ncolors):
    """
    ``SDL_Palette * SDL_AllocPalette(int)``
    """
    ncolors_c = ncolors
    rc = _LIB.SDL_AllocPalette(ncolors_c)
    return rc

def SDL_AllocRW():
    """
    ``SDL_RWops * SDL_AllocRW(void)``
    """
    rc = _LIB.SDL_AllocRW()
    return rc

def SDL_AtomicLock(lock=None):
    """
    ``void SDL_AtomicLock(int *)``
    """
    lock_c = unbox(lock, 'int *')
    _LIB.SDL_AtomicLock(lock_c)
    return lock_c[0]

def SDL_AtomicTryLock(lock=None):
    """
    ``SDL_bool SDL_AtomicTryLock(int *)``
    """
    lock_c = unbox(lock, 'int *')
    rc = _LIB.SDL_AtomicTryLock(lock_c)
    return (rc, lock_c[0])

def SDL_AtomicUnlock(lock=None):
    """
    ``void SDL_AtomicUnlock(int *)``
    """
    lock_c = unbox(lock, 'int *')
    _LIB.SDL_AtomicUnlock(lock_c)
    return lock_c[0]

def SDL_AudioInit(driver_name):
    """
    ``int SDL_AudioInit(char const *)``
    """
    driver_name_c = driver_name
    rc = _LIB.SDL_AudioInit(driver_name_c)
    return rc

def SDL_AudioQuit():
    """
    ``void SDL_AudioQuit(void)``
    """
    _LIB.SDL_AudioQuit()

def SDL_BuildAudioCVT(cvt, src_format, src_channels, src_rate, dst_format, dst_channels, dst_rate):
    """
    ``int SDL_BuildAudioCVT(SDL_AudioCVT *, uint16_t, uint8_t, int, uint16_t, uint8_t, int)``
    """
    cvt_c = unbox(cvt, 'SDL_AudioCVT *')
    src_format_c = src_format
    src_channels_c = src_channels
    src_rate_c = src_rate
    dst_format_c = dst_format
    dst_channels_c = dst_channels
    dst_rate_c = dst_rate
    rc = _LIB.SDL_BuildAudioCVT(cvt_c, src_format_c, src_channels_c, src_rate_c, dst_format_c, dst_channels_c, dst_rate_c)
    return rc

def SDL_CalculateGammaRamp(gamma, ramp=None):
    """
    ``void SDL_CalculateGammaRamp(float, uint16_t *)``
    """
    gamma_c = gamma
    ramp_c = unbox(ramp, 'uint16_t *')
    _LIB.SDL_CalculateGammaRamp(gamma_c, ramp_c)
    return ramp_c[0]

def SDL_ClearError():
    """
    ``void SDL_ClearError(void)``
    """
    _LIB.SDL_ClearError()

def SDL_ClearHints():
    """
    ``void SDL_ClearHints(void)``
    """
    _LIB.SDL_ClearHints()

def SDL_CloseAudio():
    """
    ``void SDL_CloseAudio(void)``
    """
    _LIB.SDL_CloseAudio()

def SDL_CloseAudioDevice(dev):
    """
    ``void SDL_CloseAudioDevice(uint32_t)``
    """
    dev_c = dev
    _LIB.SDL_CloseAudioDevice(dev_c)

def SDL_CondBroadcast(cond):
    """
    ``int SDL_CondBroadcast(SDL_cond *)``
    """
    cond_c = unbox(cond, 'SDL_cond *')
    rc = _LIB.SDL_CondBroadcast(cond_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_CondSignal(cond):
    """
    ``int SDL_CondSignal(SDL_cond *)``
    """
    cond_c = unbox(cond, 'SDL_cond *')
    rc = _LIB.SDL_CondSignal(cond_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_CondWait(cond, mutex):
    """
    ``int SDL_CondWait(SDL_cond *, SDL_mutex *)``
    """
    cond_c = unbox(cond, 'SDL_cond *')
    mutex_c = unbox(mutex, 'SDL_mutex *')
    rc = _LIB.SDL_CondWait(cond_c, mutex_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_CondWaitTimeout(cond, mutex, ms):
    """
    ``int SDL_CondWaitTimeout(SDL_cond *, SDL_mutex *, uint32_t)``
    """
    cond_c = unbox(cond, 'SDL_cond *')
    mutex_c = unbox(mutex, 'SDL_mutex *')
    ms_c = ms
    rc = _LIB.SDL_CondWaitTimeout(cond_c, mutex_c, ms_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_ConvertAudio(cvt):
    """
    ``int SDL_ConvertAudio(SDL_AudioCVT *)``
    """
    cvt_c = unbox(cvt, 'SDL_AudioCVT *')
    rc = _LIB.SDL_ConvertAudio(cvt_c)
    return rc

def SDL_ConvertPixels(width, height, src_format, src, src_pitch, dst_format, dst, dst_pitch):
    """
    ``int SDL_ConvertPixels(int, int, uint32_t, void const *, int, uint32_t, void *, int)``
    """
    width_c = width
    height_c = height
    src_format_c = src_format
    src_c = unbox(src, 'void const *')
    src_pitch_c = src_pitch
    dst_format_c = dst_format
    dst_c = unbox(dst, 'void *')
    dst_pitch_c = dst_pitch
    rc = _LIB.SDL_ConvertPixels(width_c, height_c, src_format_c, src_c, src_pitch_c, dst_format_c, dst_c, dst_pitch_c)
    return rc

def SDL_ConvertSurface(src, fmt, flags):
    """
    ``SDL_Surface * SDL_ConvertSurface(SDL_Surface *, SDL_PixelFormat *, uint32_t)``
    """
    src_c = unbox(src, 'SDL_Surface *')
    fmt_c = unbox(fmt, 'SDL_PixelFormat *')
    flags_c = flags
    rc = _LIB.SDL_ConvertSurface(src_c, fmt_c, flags_c)
    return rc

def SDL_ConvertSurfaceFormat(src, pixel_format, flags):
    """
    ``SDL_Surface * SDL_ConvertSurfaceFormat(SDL_Surface *, uint32_t, uint32_t)``
    """
    src_c = unbox(src, 'SDL_Surface *')
    pixel_format_c = pixel_format
    flags_c = flags
    rc = _LIB.SDL_ConvertSurfaceFormat(src_c, pixel_format_c, flags_c)
    return rc

def SDL_CreateColorCursor(surface, hot_x, hot_y):
    """
    ``SDL_Cursor * SDL_CreateColorCursor(SDL_Surface *, int, int)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    hot_x_c = hot_x
    hot_y_c = hot_y
    rc = _LIB.SDL_CreateColorCursor(surface_c, hot_x_c, hot_y_c)
    return rc

def SDL_CreateCond():
    """
    ``SDL_cond * SDL_CreateCond(void)``
    """
    rc = _LIB.SDL_CreateCond()
    return rc

def SDL_CreateCursor(data, mask, w, h, hot_x, hot_y):
    """
    ``SDL_Cursor * SDL_CreateCursor(uint8_t const *, uint8_t const *, int, int, int, int)``
    """
    data_c = unbox(data, 'uint8_t const *')
    mask_c = unbox(mask, 'uint8_t const *')
    w_c = w
    h_c = h
    hot_x_c = hot_x
    hot_y_c = hot_y
    rc = _LIB.SDL_CreateCursor(data_c, mask_c, w_c, h_c, hot_x_c, hot_y_c)
    return rc

def SDL_CreateMutex():
    """
    ``SDL_mutex * SDL_CreateMutex(void)``
    """
    rc = _LIB.SDL_CreateMutex()
    return rc

def SDL_CreateRGBSurface(flags, width, height, depth, Rmask, Gmask, Bmask, Amask):
    """
    ``SDL_Surface * SDL_CreateRGBSurface(uint32_t, int, int, int, uint32_t, uint32_t, uint32_t, uint32_t)``
    """
    flags_c = flags
    width_c = width
    height_c = height
    depth_c = depth
    Rmask_c = Rmask
    Gmask_c = Gmask
    Bmask_c = Bmask
    Amask_c = Amask
    rc = _LIB.SDL_CreateRGBSurface(flags_c, width_c, height_c, depth_c, Rmask_c, Gmask_c, Bmask_c, Amask_c)
    return rc

def SDL_CreateRGBSurfaceFrom(pixels, width, height, depth, pitch, Rmask, Gmask, Bmask, Amask):
    """
    ``SDL_Surface * SDL_CreateRGBSurfaceFrom(void *, int, int, int, int, uint32_t, uint32_t, uint32_t, uint32_t)``
    """
    pixels_c = unbox(pixels, 'void *')
    width_c = width
    height_c = height
    depth_c = depth
    pitch_c = pitch
    Rmask_c = Rmask
    Gmask_c = Gmask
    Bmask_c = Bmask
    Amask_c = Amask
    rc = _LIB.SDL_CreateRGBSurfaceFrom(pixels_c, width_c, height_c, depth_c, pitch_c, Rmask_c, Gmask_c, Bmask_c, Amask_c)
    return rc

def SDL_CreateRenderer(window, index, flags):
    """
    ``SDL_Renderer * SDL_CreateRenderer(SDL_Window *, int, uint32_t)``
    """
    window_c = unbox(window, 'SDL_Window *')
    index_c = index
    flags_c = flags
    rc = _LIB.SDL_CreateRenderer(window_c, index_c, flags_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_CreateSemaphore(initial_value):
    """
    ``SDL_sem * SDL_CreateSemaphore(uint32_t)``
    """
    initial_value_c = initial_value
    rc = _LIB.SDL_CreateSemaphore(initial_value_c)
    return rc

def SDL_CreateSoftwareRenderer(surface):
    """
    ``SDL_Renderer * SDL_CreateSoftwareRenderer(SDL_Surface *)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    rc = _LIB.SDL_CreateSoftwareRenderer(surface_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_CreateSystemCursor(id):
    """
    ``SDL_Cursor * SDL_CreateSystemCursor(SDL_SystemCursor)``
    """
    id_c = id
    rc = _LIB.SDL_CreateSystemCursor(id_c)
    return rc

def SDL_CreateTexture(renderer, format, access, w, h):
    """
    ``SDL_Texture * SDL_CreateTexture(SDL_Renderer *, uint32_t, int, int, int)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    format_c = format
    access_c = access
    w_c = w
    h_c = h
    rc = _LIB.SDL_CreateTexture(renderer_c, format_c, access_c, w_c, h_c)
    return rc

def SDL_CreateTextureFromSurface(renderer, surface):
    """
    ``SDL_Texture * SDL_CreateTextureFromSurface(SDL_Renderer *, SDL_Surface *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    surface_c = unbox(surface, 'SDL_Surface *')
    rc = _LIB.SDL_CreateTextureFromSurface(renderer_c, surface_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_CreateThread(fn, name, data):
    """
    ``SDL_Thread * SDL_CreateThread(int SDL_CreateThread(void *), char const *, void *)``
    """
    fn_c = unbox(fn, 'int(*)(void *)')
    name_c = name
    data_c = unbox(data, 'void *')
    rc = _LIB.SDL_CreateThread(fn_c, name_c, data_c)
    return rc

def SDL_CreateWindow(title, x, y, w, h, flags):
    """
    ``SDL_Window * SDL_CreateWindow(char const *, int, int, int, int, uint32_t)``
    """
    title_c = title
    x_c = x
    y_c = y
    w_c = w
    h_c = h
    flags_c = flags
    rc = _LIB.SDL_CreateWindow(title_c, x_c, y_c, w_c, h_c, flags_c)
    return rc

def SDL_CreateWindowAndRenderer(width, height, window_flags, window, renderer):
    """
    ``int SDL_CreateWindowAndRenderer(int, int, uint32_t, SDL_Window * *, SDL_Renderer * *)``
    """
    width_c = width
    height_c = height
    window_flags_c = window_flags
    window_c = unbox(window, 'SDL_Window * *')
    renderer_c = unbox(renderer, 'SDL_Renderer * *')
    rc = _LIB.SDL_CreateWindowAndRenderer(width_c, height_c, window_flags_c, window_c, renderer_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_CreateWindowFrom(data):
    """
    ``SDL_Window * SDL_CreateWindowFrom(void const *)``
    """
    data_c = unbox(data, 'void const *')
    rc = _LIB.SDL_CreateWindowFrom(data_c)
    return rc

def SDL_DelEventWatch(filter, userdata):
    """
    ``void SDL_DelEventWatch(int SDL_DelEventWatch(void *, SDL_Event *), void *)``
    """
    filter_c = unbox(filter, 'int(*)(void *, SDL_Event *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_DelEventWatch(filter_c, userdata_c)

def SDL_DelHintCallback(name, callback, userdata):
    """
    ``void SDL_DelHintCallback(char const *, void SDL_DelHintCallback(void *, char const *, char const *, char const *), void *)``
    """
    name_c = name
    callback_c = unbox(callback, 'void(*)(void *, char const *, char const *, char const *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_DelHintCallback(name_c, callback_c, userdata_c)

def SDL_Delay(ms):
    """
    ``void SDL_Delay(uint32_t)``
    """
    ms_c = ms
    _LIB.SDL_Delay(ms_c)

def SDL_DestroyCond(cond):
    """
    ``void SDL_DestroyCond(SDL_cond *)``
    """
    cond_c = unbox(cond, 'SDL_cond *')
    _LIB.SDL_DestroyCond(cond_c)

def SDL_DestroyMutex(mutex):
    """
    ``void SDL_DestroyMutex(SDL_mutex *)``
    """
    mutex_c = unbox(mutex, 'SDL_mutex *')
    _LIB.SDL_DestroyMutex(mutex_c)

def SDL_DestroyRenderer(renderer):
    """
    ``void SDL_DestroyRenderer(SDL_Renderer *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    _LIB.SDL_DestroyRenderer(renderer_c)

def SDL_DestroySemaphore(sem):
    """
    ``void SDL_DestroySemaphore(SDL_sem *)``
    """
    sem_c = unbox(sem, 'SDL_sem *')
    _LIB.SDL_DestroySemaphore(sem_c)

def SDL_DestroyTexture(texture):
    """
    ``void SDL_DestroyTexture(SDL_Texture *)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    _LIB.SDL_DestroyTexture(texture_c)

def SDL_DestroyWindow(window):
    """
    ``void SDL_DestroyWindow(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_DestroyWindow(window_c)

def SDL_DisableScreenSaver():
    """
    ``void SDL_DisableScreenSaver(void)``
    """
    _LIB.SDL_DisableScreenSaver()

def SDL_EnableScreenSaver():
    """
    ``void SDL_EnableScreenSaver(void)``
    """
    _LIB.SDL_EnableScreenSaver()

def SDL_EnclosePoints(points, count, clip, result):
    """
    ``SDL_bool SDL_EnclosePoints(SDL_Point const *, int, SDL_Rect const *, SDL_Rect *)``
    """
    points_c = unbox(points, 'SDL_Point const *')
    count_c = count
    clip_c = unbox(clip, 'SDL_Rect const *')
    result_c = unbox(result, 'SDL_Rect *')
    rc = _LIB.SDL_EnclosePoints(points_c, count_c, clip_c, result_c)
    return rc

def SDL_Error(code):
    """
    ``int SDL_Error(SDL_errorcode)``
    """
    code_c = code
    rc = _LIB.SDL_Error(code_c)
    return rc

def SDL_EventState(type, state):
    """
    ``uint8_t SDL_EventState(uint32_t, int)``
    """
    type_c = type
    state_c = state
    rc = _LIB.SDL_EventState(type_c, state_c)
    return rc

def SDL_FillRect(dst, rect, color):
    """
    ``int SDL_FillRect(SDL_Surface *, SDL_Rect const *, uint32_t)``
    """
    dst_c = unbox(dst, 'SDL_Surface *')
    rect_c = unbox(rect, 'SDL_Rect const *')
    color_c = color
    rc = _LIB.SDL_FillRect(dst_c, rect_c, color_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_FillRects(dst, rects, count, color):
    """
    ``int SDL_FillRects(SDL_Surface *, SDL_Rect const *, int, uint32_t)``
    """
    dst_c = unbox(dst, 'SDL_Surface *')
    rects_c = unbox(rects, 'SDL_Rect const *')
    count_c = count
    color_c = color
    rc = _LIB.SDL_FillRects(dst_c, rects_c, count_c, color_c)
    return rc

def SDL_FilterEvents(filter, userdata):
    """
    ``void SDL_FilterEvents(int SDL_FilterEvents(void *, SDL_Event *), void *)``
    """
    filter_c = unbox(filter, 'int(*)(void *, SDL_Event *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_FilterEvents(filter_c, userdata_c)

def SDL_FlushEvent(type):
    """
    ``void SDL_FlushEvent(uint32_t)``
    """
    type_c = type
    _LIB.SDL_FlushEvent(type_c)

def SDL_FlushEvents(minType, maxType):
    """
    ``void SDL_FlushEvents(uint32_t, uint32_t)``
    """
    minType_c = minType
    maxType_c = maxType
    _LIB.SDL_FlushEvents(minType_c, maxType_c)

def SDL_FreeCursor(cursor):
    """
    ``void SDL_FreeCursor(SDL_Cursor *)``
    """
    cursor_c = unbox(cursor, 'SDL_Cursor *')
    _LIB.SDL_FreeCursor(cursor_c)

def SDL_FreeFormat(format):
    """
    ``void SDL_FreeFormat(SDL_PixelFormat *)``
    """
    format_c = unbox(format, 'SDL_PixelFormat *')
    _LIB.SDL_FreeFormat(format_c)

def SDL_FreePalette(palette):
    """
    ``void SDL_FreePalette(SDL_Palette *)``
    """
    palette_c = unbox(palette, 'SDL_Palette *')
    _LIB.SDL_FreePalette(palette_c)

def SDL_FreeRW(area):
    """
    ``void SDL_FreeRW(SDL_RWops *)``
    """
    area_c = unbox(area, 'SDL_RWops *')
    _LIB.SDL_FreeRW(area_c)

def SDL_FreeSurface(surface):
    """
    ``void SDL_FreeSurface(SDL_Surface *)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    _LIB.SDL_FreeSurface(surface_c)

def SDL_FreeWAV(audio_buf=None):
    """
    ``void SDL_FreeWAV(uint8_t *)``
    """
    audio_buf_c = unbox(audio_buf, 'uint8_t *')
    _LIB.SDL_FreeWAV(audio_buf_c)
    return audio_buf_c[0]

def SDL_GL_BindTexture(texture, texw=None, texh=None):
    """
    ``int SDL_GL_BindTexture(SDL_Texture *, float *, float *)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    texw_c = unbox(texw, 'float *')
    texh_c = unbox(texh, 'float *')
    rc = _LIB.SDL_GL_BindTexture(texture_c, texw_c, texh_c)
    return (rc, texw_c[0], texh_c[0])

def SDL_GL_CreateContext(window):
    """
    ``void * SDL_GL_CreateContext(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GL_CreateContext(window_c)
    return rc

def SDL_GL_DeleteContext(context):
    """
    ``void SDL_GL_DeleteContext(void *)``
    """
    context_c = unbox(context, 'void *')
    _LIB.SDL_GL_DeleteContext(context_c)

def SDL_GL_ExtensionSupported(extension):
    """
    ``SDL_bool SDL_GL_ExtensionSupported(char const *)``
    """
    extension_c = extension
    rc = _LIB.SDL_GL_ExtensionSupported(extension_c)
    return rc

def SDL_GL_GetAttribute(attr, value=None):
    """
    ``int SDL_GL_GetAttribute(SDL_GLattr, int *)``
    """
    attr_c = attr
    value_c = unbox(value, 'int *')
    rc = _LIB.SDL_GL_GetAttribute(attr_c, value_c)
    return (rc, value_c[0])

def SDL_GL_GetCurrentContext():
    """
    ``void * SDL_GL_GetCurrentContext(void)``
    """
    rc = _LIB.SDL_GL_GetCurrentContext()
    return rc

def SDL_GL_GetCurrentWindow():
    """
    ``SDL_Window * SDL_GL_GetCurrentWindow(void)``
    """
    rc = _LIB.SDL_GL_GetCurrentWindow()
    return rc

def SDL_GL_GetProcAddress(proc):
    """
    ``void * SDL_GL_GetProcAddress(char const *)``
    """
    proc_c = proc
    rc = _LIB.SDL_GL_GetProcAddress(proc_c)
    return rc

def SDL_GL_GetSwapInterval():
    """
    ``int SDL_GL_GetSwapInterval(void)``
    """
    rc = _LIB.SDL_GL_GetSwapInterval()
    return rc

def SDL_GL_LoadLibrary(path):
    """
    ``int SDL_GL_LoadLibrary(char const *)``
    """
    path_c = path
    rc = _LIB.SDL_GL_LoadLibrary(path_c)
    return rc

def SDL_GL_MakeCurrent(window, context):
    """
    ``int SDL_GL_MakeCurrent(SDL_Window *, void *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    context_c = unbox(context, 'void *')
    rc = _LIB.SDL_GL_MakeCurrent(window_c, context_c)
    return rc

def SDL_GL_SetAttribute(attr, value):
    """
    ``int SDL_GL_SetAttribute(SDL_GLattr, int)``
    """
    attr_c = attr
    value_c = value
    rc = _LIB.SDL_GL_SetAttribute(attr_c, value_c)
    return rc

def SDL_GL_SetSwapInterval(interval):
    """
    ``int SDL_GL_SetSwapInterval(int)``
    """
    interval_c = interval
    rc = _LIB.SDL_GL_SetSwapInterval(interval_c)
    return rc

def SDL_GL_SwapWindow(window):
    """
    ``void SDL_GL_SwapWindow(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_GL_SwapWindow(window_c)

def SDL_GL_UnbindTexture(texture):
    """
    ``int SDL_GL_UnbindTexture(SDL_Texture *)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    rc = _LIB.SDL_GL_UnbindTexture(texture_c)
    return rc

def SDL_GL_UnloadLibrary():
    """
    ``void SDL_GL_UnloadLibrary(void)``
    """
    _LIB.SDL_GL_UnloadLibrary()

def SDL_GameControllerAddMapping(mappingString):
    """
    ``int SDL_GameControllerAddMapping(char const *)``
    """
    mappingString_c = mappingString
    rc = _LIB.SDL_GameControllerAddMapping(mappingString_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_GameControllerClose(gamecontroller):
    """
    ``void SDL_GameControllerClose(SDL_GameController *)``
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    _LIB.SDL_GameControllerClose(gamecontroller_c)

def SDL_GameControllerEventState(state):
    """
    ``int SDL_GameControllerEventState(int)``
    """
    state_c = state
    rc = _LIB.SDL_GameControllerEventState(state_c)
    return rc

def SDL_GameControllerGetAttached(gamecontroller):
    """
    ``SDL_bool SDL_GameControllerGetAttached(SDL_GameController *)``
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    rc = _LIB.SDL_GameControllerGetAttached(gamecontroller_c)
    return rc

def SDL_GameControllerGetAxis(gamecontroller, axis):
    """
    ``int16_t SDL_GameControllerGetAxis(SDL_GameController *, SDL_GameControllerAxis)``
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    axis_c = axis
    rc = _LIB.SDL_GameControllerGetAxis(gamecontroller_c, axis_c)
    return rc

def SDL_GameControllerGetAxisFromString(pchString):
    """
    ``SDL_GameControllerAxis SDL_GameControllerGetAxisFromString(char const *)``
    """
    pchString_c = pchString
    rc = _LIB.SDL_GameControllerGetAxisFromString(pchString_c)
    return rc

def SDL_GameControllerGetBindForAxis(gamecontroller, axis):
    """
    ``SDL_GameControllerButtonBind SDL_GameControllerGetBindForAxis(SDL_GameController *, SDL_GameControllerAxis)``
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    axis_c = axis
    rc = _LIB.SDL_GameControllerGetBindForAxis(gamecontroller_c, axis_c)
    return rc

def SDL_GameControllerGetBindForButton(gamecontroller, button):
    """
    ``SDL_GameControllerButtonBind SDL_GameControllerGetBindForButton(SDL_GameController *, SDL_GameControllerButton)``
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    button_c = button
    rc = _LIB.SDL_GameControllerGetBindForButton(gamecontroller_c, button_c)
    return rc

def SDL_GameControllerGetButton(gamecontroller, button):
    """
    ``uint8_t SDL_GameControllerGetButton(SDL_GameController *, SDL_GameControllerButton)``
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    button_c = button
    rc = _LIB.SDL_GameControllerGetButton(gamecontroller_c, button_c)
    return rc

def SDL_GameControllerGetButtonFromString(pchString):
    """
    ``SDL_GameControllerButton SDL_GameControllerGetButtonFromString(char const *)``
    """
    pchString_c = pchString
    rc = _LIB.SDL_GameControllerGetButtonFromString(pchString_c)
    return rc

def SDL_GameControllerGetJoystick(gamecontroller):
    """
    ``SDL_Joystick * SDL_GameControllerGetJoystick(SDL_GameController *)``
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    rc = _LIB.SDL_GameControllerGetJoystick(gamecontroller_c)
    return rc

def SDL_GameControllerGetStringForAxis(axis):
    """
    ``char const * SDL_GameControllerGetStringForAxis(SDL_GameControllerAxis)``
    """
    axis_c = axis
    rc = _LIB.SDL_GameControllerGetStringForAxis(axis_c)
    return ffi.string(rc)

def SDL_GameControllerGetStringForButton(button):
    """
    ``char const * SDL_GameControllerGetStringForButton(SDL_GameControllerButton)``
    """
    button_c = button
    rc = _LIB.SDL_GameControllerGetStringForButton(button_c)
    return ffi.string(rc)

def SDL_GameControllerMapping(gamecontroller):
    """
    ``char * SDL_GameControllerMapping(SDL_GameController *)``
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    rc = _LIB.SDL_GameControllerMapping(gamecontroller_c)
    return ffi.string(rc)

def SDL_GameControllerMappingForGUID(guid):
    """
    ``char * SDL_GameControllerMappingForGUID(SDL_JoystickGUID)``
    """
    guid_c = unbox(guid, 'SDL_JoystickGUID')
    rc = _LIB.SDL_GameControllerMappingForGUID(guid_c)
    return ffi.string(rc)

def SDL_GameControllerName(gamecontroller):
    """
    ``char const * SDL_GameControllerName(SDL_GameController *)``
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    rc = _LIB.SDL_GameControllerName(gamecontroller_c)
    return ffi.string(rc)

def SDL_GameControllerNameForIndex(joystick_index):
    """
    ``char const * SDL_GameControllerNameForIndex(int)``
    """
    joystick_index_c = joystick_index
    rc = _LIB.SDL_GameControllerNameForIndex(joystick_index_c)
    return ffi.string(rc)

def SDL_GameControllerOpen(joystick_index):
    """
    ``SDL_GameController * SDL_GameControllerOpen(int)``
    """
    joystick_index_c = joystick_index
    rc = _LIB.SDL_GameControllerOpen(joystick_index_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_GameControllerUpdate():
    """
    ``void SDL_GameControllerUpdate(void)``
    """
    _LIB.SDL_GameControllerUpdate()

def SDL_GetAssertionReport():
    """
    ``SDL_assert_data const * SDL_GetAssertionReport(void)``
    """
    rc = _LIB.SDL_GetAssertionReport()
    return rc

def SDL_GetAudioDeviceName(index, iscapture):
    """
    ``char const * SDL_GetAudioDeviceName(int, int)``
    """
    index_c = index
    iscapture_c = iscapture
    rc = _LIB.SDL_GetAudioDeviceName(index_c, iscapture_c)
    return ffi.string(rc)

def SDL_GetAudioDeviceStatus(dev):
    """
    ``SDL_AudioStatus SDL_GetAudioDeviceStatus(uint32_t)``
    """
    dev_c = dev
    rc = _LIB.SDL_GetAudioDeviceStatus(dev_c)
    return rc

def SDL_GetAudioDriver(index):
    """
    ``char const * SDL_GetAudioDriver(int)``
    """
    index_c = index
    rc = _LIB.SDL_GetAudioDriver(index_c)
    return ffi.string(rc)

def SDL_GetAudioStatus():
    """
    ``SDL_AudioStatus SDL_GetAudioStatus(void)``
    """
    rc = _LIB.SDL_GetAudioStatus()
    return rc

def SDL_GetCPUCacheLineSize():
    """
    ``int SDL_GetCPUCacheLineSize(void)``
    """
    rc = _LIB.SDL_GetCPUCacheLineSize()
    return rc

def SDL_GetCPUCount():
    """
    ``int SDL_GetCPUCount(void)``
    """
    rc = _LIB.SDL_GetCPUCount()
    return rc

def SDL_GetClipRect(surface, rect):
    """
    ``void SDL_GetClipRect(SDL_Surface *, SDL_Rect *)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    rect_c = unbox(rect, 'SDL_Rect *')
    _LIB.SDL_GetClipRect(surface_c, rect_c)

def SDL_GetClipboardText():
    """
    ``char * SDL_GetClipboardText(void)``
    """
    rc = _LIB.SDL_GetClipboardText()
    return ffi.string(rc)

def SDL_GetClosestDisplayMode(displayIndex, mode, closest):
    """
    ``SDL_DisplayMode * SDL_GetClosestDisplayMode(int, SDL_DisplayMode const *, SDL_DisplayMode *)``
    """
    displayIndex_c = displayIndex
    mode_c = unbox(mode, 'SDL_DisplayMode const *')
    closest_c = unbox(closest, 'SDL_DisplayMode *')
    rc = _LIB.SDL_GetClosestDisplayMode(displayIndex_c, mode_c, closest_c)
    return rc

def SDL_GetColorKey(surface, key=None):
    """
    ``int SDL_GetColorKey(SDL_Surface *, uint32_t *)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    key_c = unbox(key, 'uint32_t *')
    rc = _LIB.SDL_GetColorKey(surface_c, key_c)
    return (rc, key_c[0])

def SDL_GetCurrentAudioDriver():
    """
    ``char const * SDL_GetCurrentAudioDriver(void)``
    """
    rc = _LIB.SDL_GetCurrentAudioDriver()
    return ffi.string(rc)

def SDL_GetCurrentDisplayMode(displayIndex, mode):
    """
    ``int SDL_GetCurrentDisplayMode(int, SDL_DisplayMode *)``
    """
    displayIndex_c = displayIndex
    mode_c = unbox(mode, 'SDL_DisplayMode *')
    rc = _LIB.SDL_GetCurrentDisplayMode(displayIndex_c, mode_c)
    return rc

def SDL_GetCurrentVideoDriver():
    """
    ``char const * SDL_GetCurrentVideoDriver(void)``
    """
    rc = _LIB.SDL_GetCurrentVideoDriver()
    return ffi.string(rc)

def SDL_GetCursor():
    """
    ``SDL_Cursor * SDL_GetCursor(void)``
    """
    rc = _LIB.SDL_GetCursor()
    return rc

def SDL_GetDefaultCursor():
    """
    ``SDL_Cursor * SDL_GetDefaultCursor(void)``
    """
    rc = _LIB.SDL_GetDefaultCursor()
    return rc

def SDL_GetDesktopDisplayMode(displayIndex, mode):
    """
    ``int SDL_GetDesktopDisplayMode(int, SDL_DisplayMode *)``
    """
    displayIndex_c = displayIndex
    mode_c = unbox(mode, 'SDL_DisplayMode *')
    rc = _LIB.SDL_GetDesktopDisplayMode(displayIndex_c, mode_c)
    return rc

def SDL_GetDisplayBounds(displayIndex, rect):
    """
    ``int SDL_GetDisplayBounds(int, SDL_Rect *)``
    """
    displayIndex_c = displayIndex
    rect_c = unbox(rect, 'SDL_Rect *')
    rc = _LIB.SDL_GetDisplayBounds(displayIndex_c, rect_c)
    return rc

def SDL_GetDisplayMode(displayIndex, modeIndex, mode):
    """
    ``int SDL_GetDisplayMode(int, int, SDL_DisplayMode *)``
    """
    displayIndex_c = displayIndex
    modeIndex_c = modeIndex
    mode_c = unbox(mode, 'SDL_DisplayMode *')
    rc = _LIB.SDL_GetDisplayMode(displayIndex_c, modeIndex_c, mode_c)
    return rc

def SDL_GetDisplayName(displayIndex):
    """
    ``char const * SDL_GetDisplayName(int)``
    """
    displayIndex_c = displayIndex
    rc = _LIB.SDL_GetDisplayName(displayIndex_c)
    return ffi.string(rc)

def SDL_GetError():
    """
    ``char const * SDL_GetError(void)``
    """
    rc = _LIB.SDL_GetError()
    return ffi.string(rc)

def SDL_GetEventFilter(filter, userdata):
    """
    ``SDL_bool SDL_GetEventFilter(int(* *)(void *, SDL_Event *), void * *)``
    """
    filter_c = unbox(filter, 'int(* *)(void *, SDL_Event *)')
    userdata_c = unbox(userdata, 'void * *')
    rc = _LIB.SDL_GetEventFilter(filter_c, userdata_c)
    return rc

def SDL_GetHint(name):
    """
    ``char const * SDL_GetHint(char const *)``
    """
    name_c = name
    rc = _LIB.SDL_GetHint(name_c)
    return ffi.string(rc)

def SDL_GetKeyFromName(name):
    """
    ``int32_t SDL_GetKeyFromName(char const *)``
    """
    name_c = name
    rc = _LIB.SDL_GetKeyFromName(name_c)
    return rc

def SDL_GetKeyFromScancode(scancode):
    """
    ``int32_t SDL_GetKeyFromScancode(SDL_Scancode)``
    """
    scancode_c = scancode
    rc = _LIB.SDL_GetKeyFromScancode(scancode_c)
    return rc

def SDL_GetKeyName(key):
    """
    ``char const * SDL_GetKeyName(int32_t)``
    """
    key_c = key
    rc = _LIB.SDL_GetKeyName(key_c)
    return ffi.string(rc)

def SDL_GetKeyboardFocus():
    """
    ``SDL_Window * SDL_GetKeyboardFocus(void)``
    """
    rc = _LIB.SDL_GetKeyboardFocus()
    return rc

def SDL_GetKeyboardState(numkeys=None):
    """
    ``uint8_t const * SDL_GetKeyboardState(int *)``
    """
    numkeys_c = unbox(numkeys, 'int *')
    rc = _LIB.SDL_GetKeyboardState(numkeys_c)
    return (rc, numkeys_c[0])

def SDL_GetModState():
    """
    ``SDL_Keymod SDL_GetModState(void)``
    """
    rc = _LIB.SDL_GetModState()
    return rc

def SDL_GetMouseFocus():
    """
    ``SDL_Window * SDL_GetMouseFocus(void)``
    """
    rc = _LIB.SDL_GetMouseFocus()
    return rc

def SDL_GetMouseState(x=None, y=None):
    """
    ``uint32_t SDL_GetMouseState(int *, int *)``
    """
    x_c = unbox(x, 'int *')
    y_c = unbox(y, 'int *')
    rc = _LIB.SDL_GetMouseState(x_c, y_c)
    return (rc, x_c[0], y_c[0])

def SDL_GetNumAudioDevices(iscapture):
    """
    ``int SDL_GetNumAudioDevices(int)``
    """
    iscapture_c = iscapture
    rc = _LIB.SDL_GetNumAudioDevices(iscapture_c)
    return rc

def SDL_GetNumAudioDrivers():
    """
    ``int SDL_GetNumAudioDrivers(void)``
    """
    rc = _LIB.SDL_GetNumAudioDrivers()
    return rc

def SDL_GetNumDisplayModes(displayIndex):
    """
    ``int SDL_GetNumDisplayModes(int)``
    """
    displayIndex_c = displayIndex
    rc = _LIB.SDL_GetNumDisplayModes(displayIndex_c)
    return rc

def SDL_GetNumRenderDrivers():
    """
    ``int SDL_GetNumRenderDrivers(void)``
    """
    rc = _LIB.SDL_GetNumRenderDrivers()
    return rc

def SDL_GetNumTouchDevices():
    """
    ``int SDL_GetNumTouchDevices(void)``
    """
    rc = _LIB.SDL_GetNumTouchDevices()
    return rc

def SDL_GetNumTouchFingers(touchID):
    """
    ``int SDL_GetNumTouchFingers(int64_t)``
    """
    touchID_c = touchID
    rc = _LIB.SDL_GetNumTouchFingers(touchID_c)
    return rc

def SDL_GetNumVideoDisplays():
    """
    ``int SDL_GetNumVideoDisplays(void)``
    """
    rc = _LIB.SDL_GetNumVideoDisplays()
    return rc

def SDL_GetNumVideoDrivers():
    """
    ``int SDL_GetNumVideoDrivers(void)``
    """
    rc = _LIB.SDL_GetNumVideoDrivers()
    return rc

def SDL_GetPerformanceCounter():
    """
    ``uint64_t SDL_GetPerformanceCounter(void)``
    """
    rc = _LIB.SDL_GetPerformanceCounter()
    return rc

def SDL_GetPerformanceFrequency():
    """
    ``uint64_t SDL_GetPerformanceFrequency(void)``
    """
    rc = _LIB.SDL_GetPerformanceFrequency()
    return rc

def SDL_GetPixelFormatName(format):
    """
    ``char const * SDL_GetPixelFormatName(uint32_t)``
    """
    format_c = format
    rc = _LIB.SDL_GetPixelFormatName(format_c)
    return ffi.string(rc)

def SDL_GetPlatform():
    """
    ``char const * SDL_GetPlatform(void)``
    """
    rc = _LIB.SDL_GetPlatform()
    return ffi.string(rc)

def SDL_GetPowerInfo(secs=None, pct=None):
    """
    ``SDL_PowerState SDL_GetPowerInfo(int *, int *)``
    """
    secs_c = unbox(secs, 'int *')
    pct_c = unbox(pct, 'int *')
    rc = _LIB.SDL_GetPowerInfo(secs_c, pct_c)
    return (rc, secs_c[0], pct_c[0])

def SDL_GetRGB(pixel, format, r=None, g=None, b=None):
    """
    ``void SDL_GetRGB(uint32_t, SDL_PixelFormat const *, uint8_t *, uint8_t *, uint8_t *)``
    """
    pixel_c = pixel
    format_c = unbox(format, 'SDL_PixelFormat const *')
    r_c = unbox(r, 'uint8_t *')
    g_c = unbox(g, 'uint8_t *')
    b_c = unbox(b, 'uint8_t *')
    _LIB.SDL_GetRGB(pixel_c, format_c, r_c, g_c, b_c)
    return (r_c[0], g_c[0], b_c[0])

def SDL_GetRGBA(pixel, format, r=None, g=None, b=None, a=None):
    """
    ``void SDL_GetRGBA(uint32_t, SDL_PixelFormat const *, uint8_t *, uint8_t *, uint8_t *, uint8_t *)``
    """
    pixel_c = pixel
    format_c = unbox(format, 'SDL_PixelFormat const *')
    r_c = unbox(r, 'uint8_t *')
    g_c = unbox(g, 'uint8_t *')
    b_c = unbox(b, 'uint8_t *')
    a_c = unbox(a, 'uint8_t *')
    _LIB.SDL_GetRGBA(pixel_c, format_c, r_c, g_c, b_c, a_c)
    return (r_c[0], g_c[0], b_c[0], a_c[0])

def SDL_GetRelativeMouseMode():
    """
    ``SDL_bool SDL_GetRelativeMouseMode(void)``
    """
    rc = _LIB.SDL_GetRelativeMouseMode()
    return rc

def SDL_GetRelativeMouseState(x=None, y=None):
    """
    ``uint32_t SDL_GetRelativeMouseState(int *, int *)``
    """
    x_c = unbox(x, 'int *')
    y_c = unbox(y, 'int *')
    rc = _LIB.SDL_GetRelativeMouseState(x_c, y_c)
    return (rc, x_c[0], y_c[0])

def SDL_GetRenderDrawBlendMode(renderer, blendMode):
    """
    ``int SDL_GetRenderDrawBlendMode(SDL_Renderer *, SDL_BlendMode *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    blendMode_c = unbox(blendMode, 'SDL_BlendMode *')
    rc = _LIB.SDL_GetRenderDrawBlendMode(renderer_c, blendMode_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_GetRenderDrawColor(renderer, r=None, g=None, b=None, a=None):
    """
    ``int SDL_GetRenderDrawColor(SDL_Renderer *, uint8_t *, uint8_t *, uint8_t *, uint8_t *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    r_c = unbox(r, 'uint8_t *')
    g_c = unbox(g, 'uint8_t *')
    b_c = unbox(b, 'uint8_t *')
    a_c = unbox(a, 'uint8_t *')
    rc = _LIB.SDL_GetRenderDrawColor(renderer_c, r_c, g_c, b_c, a_c)
    if rc == -1: raise SDLError()
    return (rc, r_c[0], g_c[0], b_c[0], a_c[0])

def SDL_GetRenderDriverInfo(index, info):
    """
    ``int SDL_GetRenderDriverInfo(int, SDL_RendererInfo *)``
    """
    index_c = index
    info_c = unbox(info, 'SDL_RendererInfo *')
    rc = _LIB.SDL_GetRenderDriverInfo(index_c, info_c)
    return rc

def SDL_GetRenderTarget(renderer):
    """
    ``SDL_Texture * SDL_GetRenderTarget(SDL_Renderer *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rc = _LIB.SDL_GetRenderTarget(renderer_c)
    return rc

def SDL_GetRenderer(window):
    """
    ``SDL_Renderer * SDL_GetRenderer(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetRenderer(window_c)
    return rc

def SDL_GetRendererInfo(renderer, info):
    """
    ``int SDL_GetRendererInfo(SDL_Renderer *, SDL_RendererInfo *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    info_c = unbox(info, 'SDL_RendererInfo *')
    rc = _LIB.SDL_GetRendererInfo(renderer_c, info_c)
    return rc

def SDL_GetRendererOutputSize(renderer, w=None, h=None):
    """
    ``int SDL_GetRendererOutputSize(SDL_Renderer *, int *, int *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    rc = _LIB.SDL_GetRendererOutputSize(renderer_c, w_c, h_c)
    return (rc, w_c[0], h_c[0])

def SDL_GetRevision():
    """
    ``char const * SDL_GetRevision(void)``
    """
    rc = _LIB.SDL_GetRevision()
    return ffi.string(rc)

def SDL_GetRevisionNumber():
    """
    ``int SDL_GetRevisionNumber(void)``
    """
    rc = _LIB.SDL_GetRevisionNumber()
    return rc

def SDL_GetScancodeFromKey(key):
    """
    ``SDL_Scancode SDL_GetScancodeFromKey(int32_t)``
    """
    key_c = key
    rc = _LIB.SDL_GetScancodeFromKey(key_c)
    return rc

def SDL_GetScancodeFromName(name):
    """
    ``SDL_Scancode SDL_GetScancodeFromName(char const *)``
    """
    name_c = name
    rc = _LIB.SDL_GetScancodeFromName(name_c)
    return rc

def SDL_GetScancodeName(scancode):
    """
    ``char const * SDL_GetScancodeName(SDL_Scancode)``
    """
    scancode_c = scancode
    rc = _LIB.SDL_GetScancodeName(scancode_c)
    return ffi.string(rc)

def SDL_GetSurfaceAlphaMod(surface, alpha=None):
    """
    ``int SDL_GetSurfaceAlphaMod(SDL_Surface *, uint8_t *)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    alpha_c = unbox(alpha, 'uint8_t *')
    rc = _LIB.SDL_GetSurfaceAlphaMod(surface_c, alpha_c)
    return (rc, alpha_c[0])

def SDL_GetSurfaceBlendMode(surface, blendMode):
    """
    ``int SDL_GetSurfaceBlendMode(SDL_Surface *, SDL_BlendMode *)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    blendMode_c = unbox(blendMode, 'SDL_BlendMode *')
    rc = _LIB.SDL_GetSurfaceBlendMode(surface_c, blendMode_c)
    return rc

def SDL_GetSurfaceColorMod(surface, r=None, g=None, b=None):
    """
    ``int SDL_GetSurfaceColorMod(SDL_Surface *, uint8_t *, uint8_t *, uint8_t *)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    r_c = unbox(r, 'uint8_t *')
    g_c = unbox(g, 'uint8_t *')
    b_c = unbox(b, 'uint8_t *')
    rc = _LIB.SDL_GetSurfaceColorMod(surface_c, r_c, g_c, b_c)
    return (rc, r_c[0], g_c[0], b_c[0])

def SDL_GetTextureAlphaMod(texture, alpha=None):
    """
    ``int SDL_GetTextureAlphaMod(SDL_Texture *, uint8_t *)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    alpha_c = unbox(alpha, 'uint8_t *')
    rc = _LIB.SDL_GetTextureAlphaMod(texture_c, alpha_c)
    return (rc, alpha_c[0])

def SDL_GetTextureBlendMode(texture, blendMode):
    """
    ``int SDL_GetTextureBlendMode(SDL_Texture *, SDL_BlendMode *)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    blendMode_c = unbox(blendMode, 'SDL_BlendMode *')
    rc = _LIB.SDL_GetTextureBlendMode(texture_c, blendMode_c)
    return rc

def SDL_GetTextureColorMod(texture, r=None, g=None, b=None):
    """
    ``int SDL_GetTextureColorMod(SDL_Texture *, uint8_t *, uint8_t *, uint8_t *)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    r_c = unbox(r, 'uint8_t *')
    g_c = unbox(g, 'uint8_t *')
    b_c = unbox(b, 'uint8_t *')
    rc = _LIB.SDL_GetTextureColorMod(texture_c, r_c, g_c, b_c)
    return (rc, r_c[0], g_c[0], b_c[0])

def SDL_GetThreadID(thread):
    """
    ``unsigned long SDL_GetThreadID(SDL_Thread *)``
    """
    thread_c = unbox(thread, 'SDL_Thread *')
    rc = _LIB.SDL_GetThreadID(thread_c)
    return rc

def SDL_GetThreadName(thread):
    """
    ``char const * SDL_GetThreadName(SDL_Thread *)``
    """
    thread_c = unbox(thread, 'SDL_Thread *')
    rc = _LIB.SDL_GetThreadName(thread_c)
    return ffi.string(rc)

def SDL_GetTicks():
    """
    ``uint32_t SDL_GetTicks(void)``
    """
    rc = _LIB.SDL_GetTicks()
    return rc

def SDL_GetTouchDevice(index):
    """
    ``int64_t SDL_GetTouchDevice(int)``
    """
    index_c = index
    rc = _LIB.SDL_GetTouchDevice(index_c)
    return rc

def SDL_GetTouchFinger(touchID, index):
    """
    ``SDL_Finger * SDL_GetTouchFinger(int64_t, int)``
    """
    touchID_c = touchID
    index_c = index
    rc = _LIB.SDL_GetTouchFinger(touchID_c, index_c)
    return rc

def SDL_GetVersion(ver):
    """
    ``void SDL_GetVersion(SDL_version *)``
    """
    ver_c = unbox(ver, 'SDL_version *')
    _LIB.SDL_GetVersion(ver_c)

def SDL_GetVideoDriver(index):
    """
    ``char const * SDL_GetVideoDriver(int)``
    """
    index_c = index
    rc = _LIB.SDL_GetVideoDriver(index_c)
    return ffi.string(rc)

def SDL_GetWindowBrightness(window):
    """
    ``float SDL_GetWindowBrightness(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowBrightness(window_c)
    return rc

def SDL_GetWindowData(window, name):
    """
    ``void * SDL_GetWindowData(SDL_Window *, char const *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    name_c = name
    rc = _LIB.SDL_GetWindowData(window_c, name_c)
    return rc

def SDL_GetWindowDisplayIndex(window):
    """
    ``int SDL_GetWindowDisplayIndex(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowDisplayIndex(window_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_GetWindowDisplayMode(window, mode):
    """
    ``int SDL_GetWindowDisplayMode(SDL_Window *, SDL_DisplayMode *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    mode_c = unbox(mode, 'SDL_DisplayMode *')
    rc = _LIB.SDL_GetWindowDisplayMode(window_c, mode_c)
    return rc

def SDL_GetWindowFlags(window):
    """
    ``uint32_t SDL_GetWindowFlags(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowFlags(window_c)
    return rc

def SDL_GetWindowFromID(id):
    """
    ``SDL_Window * SDL_GetWindowFromID(uint32_t)``
    """
    id_c = id
    rc = _LIB.SDL_GetWindowFromID(id_c)
    return rc

def SDL_GetWindowGammaRamp(window, red=None, green=None, blue=None):
    """
    ``int SDL_GetWindowGammaRamp(SDL_Window *, uint16_t *, uint16_t *, uint16_t *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    red_c = unbox(red, 'uint16_t *')
    green_c = unbox(green, 'uint16_t *')
    blue_c = unbox(blue, 'uint16_t *')
    rc = _LIB.SDL_GetWindowGammaRamp(window_c, red_c, green_c, blue_c)
    return (rc, red_c[0], green_c[0], blue_c[0])

def SDL_GetWindowGrab(window):
    """
    ``SDL_bool SDL_GetWindowGrab(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowGrab(window_c)
    return rc

def SDL_GetWindowID(window):
    """
    ``uint32_t SDL_GetWindowID(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowID(window_c)
    return rc

def SDL_GetWindowMaximumSize(window, w=None, h=None):
    """
    ``void SDL_GetWindowMaximumSize(SDL_Window *, int *, int *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    _LIB.SDL_GetWindowMaximumSize(window_c, w_c, h_c)
    return (w_c[0], h_c[0])

def SDL_GetWindowMinimumSize(window, w=None, h=None):
    """
    ``void SDL_GetWindowMinimumSize(SDL_Window *, int *, int *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    _LIB.SDL_GetWindowMinimumSize(window_c, w_c, h_c)
    return (w_c[0], h_c[0])

def SDL_GetWindowPixelFormat(window):
    """
    ``uint32_t SDL_GetWindowPixelFormat(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowPixelFormat(window_c)
    return rc

def SDL_GetWindowPosition(window, x=None, y=None):
    """
    ``void SDL_GetWindowPosition(SDL_Window *, int *, int *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    x_c = unbox(x, 'int *')
    y_c = unbox(y, 'int *')
    _LIB.SDL_GetWindowPosition(window_c, x_c, y_c)
    return (x_c[0], y_c[0])

def SDL_GetWindowSize(window, w=None, h=None):
    """
    ``void SDL_GetWindowSize(SDL_Window *, int *, int *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    _LIB.SDL_GetWindowSize(window_c, w_c, h_c)
    return (w_c[0], h_c[0])

def SDL_GetWindowSurface(window):
    """
    ``SDL_Surface * SDL_GetWindowSurface(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowSurface(window_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_GetWindowTitle(window):
    """
    ``char const * SDL_GetWindowTitle(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowTitle(window_c)
    return ffi.string(rc)

def SDL_HapticClose(haptic):
    """
    ``void SDL_HapticClose(SDL_Haptic *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    _LIB.SDL_HapticClose(haptic_c)

def SDL_HapticDestroyEffect(haptic, effect):
    """
    ``void SDL_HapticDestroyEffect(SDL_Haptic *, int)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    effect_c = effect
    _LIB.SDL_HapticDestroyEffect(haptic_c, effect_c)

def SDL_HapticEffectSupported(haptic, effect):
    """
    ``int SDL_HapticEffectSupported(SDL_Haptic *, SDL_HapticEffect *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    effect_c = unbox(effect, 'SDL_HapticEffect *')
    rc = _LIB.SDL_HapticEffectSupported(haptic_c, effect_c)
    return rc

def SDL_HapticGetEffectStatus(haptic, effect):
    """
    ``int SDL_HapticGetEffectStatus(SDL_Haptic *, int)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    effect_c = effect
    rc = _LIB.SDL_HapticGetEffectStatus(haptic_c, effect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticIndex(haptic):
    """
    ``int SDL_HapticIndex(SDL_Haptic *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticIndex(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticName(device_index):
    """
    ``char const * SDL_HapticName(int)``
    """
    device_index_c = device_index
    rc = _LIB.SDL_HapticName(device_index_c)
    if rc == ffi.NULL: raise SDLError()
    return ffi.string(rc)

def SDL_HapticNewEffect(haptic, effect):
    """
    ``int SDL_HapticNewEffect(SDL_Haptic *, SDL_HapticEffect *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    effect_c = unbox(effect, 'SDL_HapticEffect *')
    rc = _LIB.SDL_HapticNewEffect(haptic_c, effect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticNumAxes(haptic):
    """
    ``int SDL_HapticNumAxes(SDL_Haptic *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticNumAxes(haptic_c)
    return rc

def SDL_HapticNumEffects(haptic):
    """
    ``int SDL_HapticNumEffects(SDL_Haptic *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticNumEffects(haptic_c)
    return rc

def SDL_HapticNumEffectsPlaying(haptic):
    """
    ``int SDL_HapticNumEffectsPlaying(SDL_Haptic *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticNumEffectsPlaying(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticOpen(device_index):
    """
    ``SDL_Haptic * SDL_HapticOpen(int)``
    """
    device_index_c = device_index
    rc = _LIB.SDL_HapticOpen(device_index_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_HapticOpenFromJoystick(joystick):
    """
    ``SDL_Haptic * SDL_HapticOpenFromJoystick(SDL_Joystick *)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_HapticOpenFromJoystick(joystick_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_HapticOpenFromMouse():
    """
    ``SDL_Haptic * SDL_HapticOpenFromMouse(void)``
    """
    rc = _LIB.SDL_HapticOpenFromMouse()
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_HapticOpened(device_index):
    """
    ``int SDL_HapticOpened(int)``
    """
    device_index_c = device_index
    rc = _LIB.SDL_HapticOpened(device_index_c)
    return rc

def SDL_HapticPause(haptic):
    """
    ``int SDL_HapticPause(SDL_Haptic *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticPause(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticQuery(haptic):
    """
    ``unsigned int SDL_HapticQuery(SDL_Haptic *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticQuery(haptic_c)
    return rc

def SDL_HapticRumbleInit(haptic):
    """
    ``int SDL_HapticRumbleInit(SDL_Haptic *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticRumbleInit(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticRumblePlay(haptic, strength, length):
    """
    ``int SDL_HapticRumblePlay(SDL_Haptic *, float, uint32_t)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    strength_c = strength
    length_c = length
    rc = _LIB.SDL_HapticRumblePlay(haptic_c, strength_c, length_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticRumbleStop(haptic):
    """
    ``int SDL_HapticRumbleStop(SDL_Haptic *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticRumbleStop(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticRumbleSupported(haptic):
    """
    ``int SDL_HapticRumbleSupported(SDL_Haptic *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticRumbleSupported(haptic_c)
    return rc

def SDL_HapticRunEffect(haptic, effect, iterations):
    """
    ``int SDL_HapticRunEffect(SDL_Haptic *, int, uint32_t)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    effect_c = effect
    iterations_c = iterations
    rc = _LIB.SDL_HapticRunEffect(haptic_c, effect_c, iterations_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticSetAutocenter(haptic, autocenter):
    """
    ``int SDL_HapticSetAutocenter(SDL_Haptic *, int)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    autocenter_c = autocenter
    rc = _LIB.SDL_HapticSetAutocenter(haptic_c, autocenter_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticSetGain(haptic, gain):
    """
    ``int SDL_HapticSetGain(SDL_Haptic *, int)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    gain_c = gain
    rc = _LIB.SDL_HapticSetGain(haptic_c, gain_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticStopAll(haptic):
    """
    ``int SDL_HapticStopAll(SDL_Haptic *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticStopAll(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticStopEffect(haptic, effect):
    """
    ``int SDL_HapticStopEffect(SDL_Haptic *, int)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    effect_c = effect
    rc = _LIB.SDL_HapticStopEffect(haptic_c, effect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticUnpause(haptic):
    """
    ``int SDL_HapticUnpause(SDL_Haptic *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticUnpause(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticUpdateEffect(haptic, effect, data):
    """
    ``int SDL_HapticUpdateEffect(SDL_Haptic *, int, SDL_HapticEffect *)``
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    effect_c = effect
    data_c = unbox(data, 'SDL_HapticEffect *')
    rc = _LIB.SDL_HapticUpdateEffect(haptic_c, effect_c, data_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_Has3DNow():
    """
    ``SDL_bool SDL_Has3DNow(void)``
    """
    rc = _LIB.SDL_Has3DNow()
    return rc

def SDL_HasAltiVec():
    """
    ``SDL_bool SDL_HasAltiVec(void)``
    """
    rc = _LIB.SDL_HasAltiVec()
    return rc

def SDL_HasClipboardText():
    """
    ``SDL_bool SDL_HasClipboardText(void)``
    """
    rc = _LIB.SDL_HasClipboardText()
    return rc

def SDL_HasEvent(type):
    """
    ``SDL_bool SDL_HasEvent(uint32_t)``
    """
    type_c = type
    rc = _LIB.SDL_HasEvent(type_c)
    return rc

def SDL_HasEvents(minType, maxType):
    """
    ``SDL_bool SDL_HasEvents(uint32_t, uint32_t)``
    """
    minType_c = minType
    maxType_c = maxType
    rc = _LIB.SDL_HasEvents(minType_c, maxType_c)
    return rc

def SDL_HasIntersection(A, B):
    """
    ``SDL_bool SDL_HasIntersection(SDL_Rect const *, SDL_Rect const *)``
    """
    A_c = unbox(A, 'SDL_Rect const *')
    B_c = unbox(B, 'SDL_Rect const *')
    rc = _LIB.SDL_HasIntersection(A_c, B_c)
    return rc

def SDL_HasMMX():
    """
    ``SDL_bool SDL_HasMMX(void)``
    """
    rc = _LIB.SDL_HasMMX()
    return rc

def SDL_HasRDTSC():
    """
    ``SDL_bool SDL_HasRDTSC(void)``
    """
    rc = _LIB.SDL_HasRDTSC()
    return rc

def SDL_HasSSE():
    """
    ``SDL_bool SDL_HasSSE(void)``
    """
    rc = _LIB.SDL_HasSSE()
    return rc

def SDL_HasSSE2():
    """
    ``SDL_bool SDL_HasSSE2(void)``
    """
    rc = _LIB.SDL_HasSSE2()
    return rc

def SDL_HasSSE3():
    """
    ``SDL_bool SDL_HasSSE3(void)``
    """
    rc = _LIB.SDL_HasSSE3()
    return rc

def SDL_HasSSE41():
    """
    ``SDL_bool SDL_HasSSE41(void)``
    """
    rc = _LIB.SDL_HasSSE41()
    return rc

def SDL_HasSSE42():
    """
    ``SDL_bool SDL_HasSSE42(void)``
    """
    rc = _LIB.SDL_HasSSE42()
    return rc

def SDL_HasScreenKeyboardSupport():
    """
    ``SDL_bool SDL_HasScreenKeyboardSupport(void)``
    """
    rc = _LIB.SDL_HasScreenKeyboardSupport()
    return rc

def SDL_HideWindow(window):
    """
    ``void SDL_HideWindow(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_HideWindow(window_c)

def SDL_Init(flags):
    """
    ``int SDL_Init(uint32_t)``
    """
    flags_c = flags
    rc = _LIB.SDL_Init(flags_c)
    return rc

def SDL_InitSubSystem(flags):
    """
    ``int SDL_InitSubSystem(uint32_t)``
    """
    flags_c = flags
    rc = _LIB.SDL_InitSubSystem(flags_c)
    return rc

def SDL_IntersectRect(A, B, result):
    """
    ``SDL_bool SDL_IntersectRect(SDL_Rect const *, SDL_Rect const *, SDL_Rect *)``
    """
    A_c = unbox(A, 'SDL_Rect const *')
    B_c = unbox(B, 'SDL_Rect const *')
    result_c = unbox(result, 'SDL_Rect *')
    rc = _LIB.SDL_IntersectRect(A_c, B_c, result_c)
    return rc

def SDL_IntersectRectAndLine(rect, X1=None, Y1=None, X2=None, Y2=None):
    """
    ``SDL_bool SDL_IntersectRectAndLine(SDL_Rect const *, int *, int *, int *, int *)``
    """
    rect_c = unbox(rect, 'SDL_Rect const *')
    X1_c = unbox(X1, 'int *')
    Y1_c = unbox(Y1, 'int *')
    X2_c = unbox(X2, 'int *')
    Y2_c = unbox(Y2, 'int *')
    rc = _LIB.SDL_IntersectRectAndLine(rect_c, X1_c, Y1_c, X2_c, Y2_c)
    return (rc, X1_c[0], Y1_c[0], X2_c[0], Y2_c[0])

def SDL_IsGameController(joystick_index):
    """
    ``SDL_bool SDL_IsGameController(int)``
    """
    joystick_index_c = joystick_index
    rc = _LIB.SDL_IsGameController(joystick_index_c)
    return rc

def SDL_IsScreenKeyboardShown(window):
    """
    ``SDL_bool SDL_IsScreenKeyboardShown(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_IsScreenKeyboardShown(window_c)
    return rc

def SDL_IsScreenSaverEnabled():
    """
    ``SDL_bool SDL_IsScreenSaverEnabled(void)``
    """
    rc = _LIB.SDL_IsScreenSaverEnabled()
    return rc

def SDL_IsTextInputActive():
    """
    ``SDL_bool SDL_IsTextInputActive(void)``
    """
    rc = _LIB.SDL_IsTextInputActive()
    return rc

def SDL_JoystickClose(joystick):
    """
    ``void SDL_JoystickClose(SDL_Joystick *)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    _LIB.SDL_JoystickClose(joystick_c)

def SDL_JoystickEventState(state):
    """
    ``int SDL_JoystickEventState(int)``
    """
    state_c = state
    rc = _LIB.SDL_JoystickEventState(state_c)
    return rc

def SDL_JoystickGetAttached(joystick):
    """
    ``SDL_bool SDL_JoystickGetAttached(SDL_Joystick *)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickGetAttached(joystick_c)
    return rc

def SDL_JoystickGetAxis(joystick, axis):
    """
    ``int16_t SDL_JoystickGetAxis(SDL_Joystick *, int)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    axis_c = axis
    rc = _LIB.SDL_JoystickGetAxis(joystick_c, axis_c)
    return rc

def SDL_JoystickGetBall(joystick, ball, dx=None, dy=None):
    """
    ``int SDL_JoystickGetBall(SDL_Joystick *, int, int *, int *)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    ball_c = ball
    dx_c = unbox(dx, 'int *')
    dy_c = unbox(dy, 'int *')
    rc = _LIB.SDL_JoystickGetBall(joystick_c, ball_c, dx_c, dy_c)
    return (rc, dx_c[0], dy_c[0])

def SDL_JoystickGetButton(joystick, button):
    """
    ``uint8_t SDL_JoystickGetButton(SDL_Joystick *, int)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    button_c = button
    rc = _LIB.SDL_JoystickGetButton(joystick_c, button_c)
    return rc

def SDL_JoystickGetDeviceGUID(device_index):
    """
    ``SDL_JoystickGUID SDL_JoystickGetDeviceGUID(int)``
    """
    device_index_c = device_index
    rc = _LIB.SDL_JoystickGetDeviceGUID(device_index_c)
    return rc

def SDL_JoystickGetGUID(joystick):
    """
    ``SDL_JoystickGUID SDL_JoystickGetGUID(SDL_Joystick *)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickGetGUID(joystick_c)
    return rc

def SDL_JoystickGetGUIDFromString(pchGUID):
    """
    ``SDL_JoystickGUID SDL_JoystickGetGUIDFromString(char const *)``
    """
    pchGUID_c = pchGUID
    rc = _LIB.SDL_JoystickGetGUIDFromString(pchGUID_c)
    return rc

def SDL_JoystickGetGUIDString(guid, pszGUID, cbGUID):
    """
    ``void SDL_JoystickGetGUIDString(SDL_JoystickGUID, char *, int)``
    """
    guid_c = unbox(guid, 'SDL_JoystickGUID')
    pszGUID_c = pszGUID
    cbGUID_c = cbGUID
    _LIB.SDL_JoystickGetGUIDString(guid_c, pszGUID_c, cbGUID_c)

def SDL_JoystickGetHat(joystick, hat):
    """
    ``uint8_t SDL_JoystickGetHat(SDL_Joystick *, int)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    hat_c = hat
    rc = _LIB.SDL_JoystickGetHat(joystick_c, hat_c)
    return rc

def SDL_JoystickInstanceID(joystick):
    """
    ``int32_t SDL_JoystickInstanceID(SDL_Joystick *)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickInstanceID(joystick_c)
    return rc

def SDL_JoystickIsHaptic(joystick):
    """
    ``int SDL_JoystickIsHaptic(SDL_Joystick *)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickIsHaptic(joystick_c)
    return rc

def SDL_JoystickName(joystick):
    """
    ``char const * SDL_JoystickName(SDL_Joystick *)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickName(joystick_c)
    return ffi.string(rc)

def SDL_JoystickNameForIndex(device_index):
    """
    ``char const * SDL_JoystickNameForIndex(int)``
    """
    device_index_c = device_index
    rc = _LIB.SDL_JoystickNameForIndex(device_index_c)
    return ffi.string(rc)

def SDL_JoystickNumAxes(joystick):
    """
    ``int SDL_JoystickNumAxes(SDL_Joystick *)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickNumAxes(joystick_c)
    return rc

def SDL_JoystickNumBalls(joystick):
    """
    ``int SDL_JoystickNumBalls(SDL_Joystick *)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickNumBalls(joystick_c)
    return rc

def SDL_JoystickNumButtons(joystick):
    """
    ``int SDL_JoystickNumButtons(SDL_Joystick *)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickNumButtons(joystick_c)
    return rc

def SDL_JoystickNumHats(joystick):
    """
    ``int SDL_JoystickNumHats(SDL_Joystick *)``
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickNumHats(joystick_c)
    return rc

def SDL_JoystickOpen(device_index):
    """
    ``SDL_Joystick * SDL_JoystickOpen(int)``
    """
    device_index_c = device_index
    rc = _LIB.SDL_JoystickOpen(device_index_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_JoystickUpdate():
    """
    ``void SDL_JoystickUpdate(void)``
    """
    _LIB.SDL_JoystickUpdate()

def SDL_LoadBMP_RW(src, freesrc):
    """
    ``SDL_Surface * SDL_LoadBMP_RW(SDL_RWops *, int)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    freesrc_c = freesrc
    rc = _LIB.SDL_LoadBMP_RW(src_c, freesrc_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_LoadDollarTemplates(touchId, src):
    """
    ``int SDL_LoadDollarTemplates(int64_t, SDL_RWops *)``
    """
    touchId_c = touchId
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_LoadDollarTemplates(touchId_c, src_c)
    return rc

def SDL_LoadFunction(handle, name):
    """
    ``void * SDL_LoadFunction(void *, char const *)``
    """
    handle_c = unbox(handle, 'void *')
    name_c = name
    rc = _LIB.SDL_LoadFunction(handle_c, name_c)
    return rc

def SDL_LoadObject(sofile):
    """
    ``void * SDL_LoadObject(char const *)``
    """
    sofile_c = sofile
    rc = _LIB.SDL_LoadObject(sofile_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_LoadWAV_RW(src, freesrc, spec, audio_buf, audio_len=None):
    """
    ``SDL_AudioSpec * SDL_LoadWAV_RW(SDL_RWops *, int, SDL_AudioSpec *, uint8_t * *, uint32_t *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    freesrc_c = freesrc
    spec_c = unbox(spec, 'SDL_AudioSpec *')
    audio_buf_c = unbox(audio_buf, 'uint8_t * *')
    audio_len_c = unbox(audio_len, 'uint32_t *')
    rc = _LIB.SDL_LoadWAV_RW(src_c, freesrc_c, spec_c, audio_buf_c, audio_len_c)
    if rc == ffi.NULL: raise SDLError()
    return (rc, audio_len_c[0])

def SDL_LockAudio():
    """
    ``void SDL_LockAudio(void)``
    """
    _LIB.SDL_LockAudio()

def SDL_LockAudioDevice(dev):
    """
    ``void SDL_LockAudioDevice(uint32_t)``
    """
    dev_c = dev
    _LIB.SDL_LockAudioDevice(dev_c)

def SDL_LockMutex(mutex):
    """
    ``int SDL_LockMutex(SDL_mutex *)``
    """
    mutex_c = unbox(mutex, 'SDL_mutex *')
    rc = _LIB.SDL_LockMutex(mutex_c)
    return rc

def SDL_LockSurface(surface):
    """
    ``int SDL_LockSurface(SDL_Surface *)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    rc = _LIB.SDL_LockSurface(surface_c)
    return rc

def SDL_LockTexture(texture, rect, pixels, pitch=None):
    """
    ``int SDL_LockTexture(SDL_Texture *, SDL_Rect const *, void * *, int *)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    rect_c = unbox(rect, 'SDL_Rect const *')
    pixels_c = unbox(pixels, 'void * *')
    pitch_c = unbox(pitch, 'int *')
    rc = _LIB.SDL_LockTexture(texture_c, rect_c, pixels_c, pitch_c)
    return (rc, pitch_c[0])

def SDL_Log(fmt):
    """
    ``void SDL_Log(char const *, ...)``
    """
    fmt_c = fmt
    _LIB.SDL_Log(fmt_c)

def SDL_LogCritical(category, fmt):
    """
    ``void SDL_LogCritical(int, char const *, ...)``
    """
    category_c = category
    fmt_c = fmt
    _LIB.SDL_LogCritical(category_c, fmt_c)

def SDL_LogDebug(category, fmt):
    """
    ``void SDL_LogDebug(int, char const *, ...)``
    """
    category_c = category
    fmt_c = fmt
    _LIB.SDL_LogDebug(category_c, fmt_c)

def SDL_LogError(category, fmt):
    """
    ``void SDL_LogError(int, char const *, ...)``
    """
    category_c = category
    fmt_c = fmt
    _LIB.SDL_LogError(category_c, fmt_c)

def SDL_LogGetOutputFunction(callback, userdata):
    """
    ``void SDL_LogGetOutputFunction(void(* *)(void *, int, SDL_LogPriority, char const *), void * *)``
    """
    callback_c = unbox(callback, 'void(* *)(void *, int, SDL_LogPriority, char const *)')
    userdata_c = unbox(userdata, 'void * *')
    _LIB.SDL_LogGetOutputFunction(callback_c, userdata_c)

def SDL_LogGetPriority(category):
    """
    ``SDL_LogPriority SDL_LogGetPriority(int)``
    """
    category_c = category
    rc = _LIB.SDL_LogGetPriority(category_c)
    return rc

def SDL_LogInfo(category, fmt):
    """
    ``void SDL_LogInfo(int, char const *, ...)``
    """
    category_c = category
    fmt_c = fmt
    _LIB.SDL_LogInfo(category_c, fmt_c)

def SDL_LogMessage(category, priority, fmt):
    """
    ``void SDL_LogMessage(int, SDL_LogPriority, char const *, ...)``
    """
    category_c = category
    priority_c = priority
    fmt_c = fmt
    _LIB.SDL_LogMessage(category_c, priority_c, fmt_c)

def SDL_LogMessageV(category, priority, fmt, ap):
    """
    ``void SDL_LogMessageV(int, SDL_LogPriority, char const *, int32_t)``
    """
    category_c = category
    priority_c = priority
    fmt_c = fmt
    ap_c = ap
    _LIB.SDL_LogMessageV(category_c, priority_c, fmt_c, ap_c)

def SDL_LogResetPriorities():
    """
    ``void SDL_LogResetPriorities(void)``
    """
    _LIB.SDL_LogResetPriorities()

def SDL_LogSetAllPriority(priority):
    """
    ``void SDL_LogSetAllPriority(SDL_LogPriority)``
    """
    priority_c = priority
    _LIB.SDL_LogSetAllPriority(priority_c)

def SDL_LogSetOutputFunction(callback, userdata):
    """
    ``void SDL_LogSetOutputFunction(void SDL_LogSetOutputFunction(void *, int, SDL_LogPriority, char const *), void *)``
    """
    callback_c = unbox(callback, 'void(*)(void *, int, SDL_LogPriority, char const *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_LogSetOutputFunction(callback_c, userdata_c)

def SDL_LogSetPriority(category, priority):
    """
    ``void SDL_LogSetPriority(int, SDL_LogPriority)``
    """
    category_c = category
    priority_c = priority
    _LIB.SDL_LogSetPriority(category_c, priority_c)

def SDL_LogVerbose(category, fmt):
    """
    ``void SDL_LogVerbose(int, char const *, ...)``
    """
    category_c = category
    fmt_c = fmt
    _LIB.SDL_LogVerbose(category_c, fmt_c)

def SDL_LogWarn(category, fmt):
    """
    ``void SDL_LogWarn(int, char const *, ...)``
    """
    category_c = category
    fmt_c = fmt
    _LIB.SDL_LogWarn(category_c, fmt_c)

def SDL_LowerBlit(src, srcrect, dst, dstrect):
    """
    ``int SDL_LowerBlit(SDL_Surface *, SDL_Rect *, SDL_Surface *, SDL_Rect *)``
    """
    src_c = unbox(src, 'SDL_Surface *')
    srcrect_c = unbox(srcrect, 'SDL_Rect *')
    dst_c = unbox(dst, 'SDL_Surface *')
    dstrect_c = unbox(dstrect, 'SDL_Rect *')
    rc = _LIB.SDL_LowerBlit(src_c, srcrect_c, dst_c, dstrect_c)
    return rc

def SDL_LowerBlitScaled(src, srcrect, dst, dstrect):
    """
    ``int SDL_LowerBlitScaled(SDL_Surface *, SDL_Rect *, SDL_Surface *, SDL_Rect *)``
    """
    src_c = unbox(src, 'SDL_Surface *')
    srcrect_c = unbox(srcrect, 'SDL_Rect *')
    dst_c = unbox(dst, 'SDL_Surface *')
    dstrect_c = unbox(dstrect, 'SDL_Rect *')
    rc = _LIB.SDL_LowerBlitScaled(src_c, srcrect_c, dst_c, dstrect_c)
    return rc

def SDL_MapRGB(format, r, g, b):
    """
    ``uint32_t SDL_MapRGB(SDL_PixelFormat const *, uint8_t, uint8_t, uint8_t)``
    """
    format_c = unbox(format, 'SDL_PixelFormat const *')
    r_c = r
    g_c = g
    b_c = b
    rc = _LIB.SDL_MapRGB(format_c, r_c, g_c, b_c)
    return rc

def SDL_MapRGBA(format, r, g, b, a):
    """
    ``uint32_t SDL_MapRGBA(SDL_PixelFormat const *, uint8_t, uint8_t, uint8_t, uint8_t)``
    """
    format_c = unbox(format, 'SDL_PixelFormat const *')
    r_c = r
    g_c = g
    b_c = b
    a_c = a
    rc = _LIB.SDL_MapRGBA(format_c, r_c, g_c, b_c, a_c)
    return rc

def SDL_MasksToPixelFormatEnum(bpp, Rmask, Gmask, Bmask, Amask):
    """
    ``uint32_t SDL_MasksToPixelFormatEnum(int, uint32_t, uint32_t, uint32_t, uint32_t)``
    """
    bpp_c = bpp
    Rmask_c = Rmask
    Gmask_c = Gmask
    Bmask_c = Bmask
    Amask_c = Amask
    rc = _LIB.SDL_MasksToPixelFormatEnum(bpp_c, Rmask_c, Gmask_c, Bmask_c, Amask_c)
    return rc

def SDL_MaximizeWindow(window):
    """
    ``void SDL_MaximizeWindow(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_MaximizeWindow(window_c)

def SDL_MinimizeWindow(window):
    """
    ``void SDL_MinimizeWindow(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_MinimizeWindow(window_c)

def SDL_MixAudio(dst, src, len, volume):
    """
    ``void SDL_MixAudio(uint8_t *, uint8_t const *, uint32_t, int)``
    """
    dst_c = unbox(dst, 'uint8_t *')
    src_c = unbox(src, 'uint8_t const *')
    len_c = len
    volume_c = volume
    _LIB.SDL_MixAudio(dst_c, src_c, len_c, volume_c)

def SDL_MixAudioFormat(dst, src, format, len, volume):
    """
    ``void SDL_MixAudioFormat(uint8_t *, uint8_t const *, uint16_t, uint32_t, int)``
    """
    dst_c = unbox(dst, 'uint8_t *')
    src_c = unbox(src, 'uint8_t const *')
    format_c = format
    len_c = len
    volume_c = volume
    _LIB.SDL_MixAudioFormat(dst_c, src_c, format_c, len_c, volume_c)

def SDL_MouseIsHaptic():
    """
    ``int SDL_MouseIsHaptic(void)``
    """
    rc = _LIB.SDL_MouseIsHaptic()
    return rc

def SDL_NumHaptics():
    """
    ``int SDL_NumHaptics(void)``
    """
    rc = _LIB.SDL_NumHaptics()
    return rc

def SDL_NumJoysticks():
    """
    ``int SDL_NumJoysticks(void)``
    """
    rc = _LIB.SDL_NumJoysticks()
    return rc

def SDL_OpenAudio(desired, obtained):
    """
    ``int SDL_OpenAudio(SDL_AudioSpec *, SDL_AudioSpec *)``
    """
    desired_c = unbox(desired, 'SDL_AudioSpec *')
    obtained_c = unbox(obtained, 'SDL_AudioSpec *')
    rc = _LIB.SDL_OpenAudio(desired_c, obtained_c)
    return rc

def SDL_OpenAudioDevice(device, iscapture, desired, obtained, allowed_changes):
    """
    ``uint32_t SDL_OpenAudioDevice(char const *, int, SDL_AudioSpec const *, SDL_AudioSpec *, int)``
    """
    device_c = device
    iscapture_c = iscapture
    desired_c = unbox(desired, 'SDL_AudioSpec const *')
    obtained_c = unbox(obtained, 'SDL_AudioSpec *')
    allowed_changes_c = allowed_changes
    rc = _LIB.SDL_OpenAudioDevice(device_c, iscapture_c, desired_c, obtained_c, allowed_changes_c)
    if rc == 0: raise SDLError()
    return rc

def SDL_PauseAudio(pause_on):
    """
    ``void SDL_PauseAudio(int)``
    """
    pause_on_c = pause_on
    _LIB.SDL_PauseAudio(pause_on_c)

def SDL_PauseAudioDevice(dev, pause_on):
    """
    ``void SDL_PauseAudioDevice(uint32_t, int)``
    """
    dev_c = dev
    pause_on_c = pause_on
    _LIB.SDL_PauseAudioDevice(dev_c, pause_on_c)

def SDL_PeepEvents(events, numevents, action, minType, maxType):
    """
    ``int SDL_PeepEvents(SDL_Event *, int, SDL_eventaction, uint32_t, uint32_t)``
    """
    events_c = unbox(events, 'SDL_Event *')
    numevents_c = numevents
    action_c = action
    minType_c = minType
    maxType_c = maxType
    rc = _LIB.SDL_PeepEvents(events_c, numevents_c, action_c, minType_c, maxType_c)
    return rc

def SDL_PixelFormatEnumToMasks(format, bpp=None, Rmask=None, Gmask=None, Bmask=None, Amask=None):
    """
    ``SDL_bool SDL_PixelFormatEnumToMasks(uint32_t, int *, uint32_t *, uint32_t *, uint32_t *, uint32_t *)``
    """
    format_c = format
    bpp_c = unbox(bpp, 'int *')
    Rmask_c = unbox(Rmask, 'uint32_t *')
    Gmask_c = unbox(Gmask, 'uint32_t *')
    Bmask_c = unbox(Bmask, 'uint32_t *')
    Amask_c = unbox(Amask, 'uint32_t *')
    rc = _LIB.SDL_PixelFormatEnumToMasks(format_c, bpp_c, Rmask_c, Gmask_c, Bmask_c, Amask_c)
    return (rc, bpp_c[0], Rmask_c[0], Gmask_c[0], Bmask_c[0], Amask_c[0])

def SDL_PollEvent(event):
    """
    ``int SDL_PollEvent(SDL_Event *)``
    """
    event_c = unbox(event, 'SDL_Event *')
    rc = _LIB.SDL_PollEvent(event_c)
    return rc

def SDL_PumpEvents():
    """
    ``void SDL_PumpEvents(void)``
    """
    _LIB.SDL_PumpEvents()

def SDL_PushEvent(event):
    """
    ``int SDL_PushEvent(SDL_Event *)``
    """
    event_c = unbox(event, 'SDL_Event *')
    rc = _LIB.SDL_PushEvent(event_c)
    return rc

def SDL_QueryTexture(texture, format=None, access=None, w=None, h=None):
    """
    ``int SDL_QueryTexture(SDL_Texture *, uint32_t *, int *, int *, int *)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    format_c = unbox(format, 'uint32_t *')
    access_c = unbox(access, 'int *')
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    rc = _LIB.SDL_QueryTexture(texture_c, format_c, access_c, w_c, h_c)
    return (rc, format_c[0], access_c[0], w_c[0], h_c[0])

def SDL_Quit():
    """
    ``void SDL_Quit(void)``
    """
    _LIB.SDL_Quit()

def SDL_QuitSubSystem(flags):
    """
    ``void SDL_QuitSubSystem(uint32_t)``
    """
    flags_c = flags
    _LIB.SDL_QuitSubSystem(flags_c)

def SDL_RWFromConstMem(mem, size):
    """
    ``SDL_RWops * SDL_RWFromConstMem(void const *, int)``
    """
    mem_c = unbox(mem, 'void const *')
    size_c = size
    rc = _LIB.SDL_RWFromConstMem(mem_c, size_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_RWFromFP(fp, autoclose):
    """
    ``SDL_RWops * SDL_RWFromFP(FILE *, SDL_bool)``
    """
    fp_c = unbox(fp, 'FILE *')
    autoclose_c = autoclose
    rc = _LIB.SDL_RWFromFP(fp_c, autoclose_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_RWFromFile(file, mode):
    """
    ``SDL_RWops * SDL_RWFromFile(char const *, char const *)``
    """
    file_c = file
    mode_c = mode
    rc = _LIB.SDL_RWFromFile(file_c, mode_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_RWFromMem(mem, size):
    """
    ``SDL_RWops * SDL_RWFromMem(void *, int)``
    """
    mem_c = unbox(mem, 'void *')
    size_c = size
    rc = _LIB.SDL_RWFromMem(mem_c, size_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_RaiseWindow(window):
    """
    ``void SDL_RaiseWindow(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_RaiseWindow(window_c)

def SDL_ReadBE16(src):
    """
    ``uint16_t SDL_ReadBE16(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_ReadBE16(src_c)
    return rc

def SDL_ReadBE32(src):
    """
    ``uint32_t SDL_ReadBE32(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_ReadBE32(src_c)
    return rc

def SDL_ReadBE64(src):
    """
    ``uint64_t SDL_ReadBE64(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_ReadBE64(src_c)
    return rc

def SDL_ReadLE16(src):
    """
    ``uint16_t SDL_ReadLE16(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_ReadLE16(src_c)
    return rc

def SDL_ReadLE32(src):
    """
    ``uint32_t SDL_ReadLE32(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_ReadLE32(src_c)
    return rc

def SDL_ReadLE64(src):
    """
    ``uint64_t SDL_ReadLE64(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_ReadLE64(src_c)
    return rc

def SDL_ReadU8(src):
    """
    ``uint8_t SDL_ReadU8(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_ReadU8(src_c)
    return rc

def SDL_RecordGesture(touchId):
    """
    ``int SDL_RecordGesture(int64_t)``
    """
    touchId_c = touchId
    rc = _LIB.SDL_RecordGesture(touchId_c)
    return rc

def SDL_RegisterEvents(numevents):
    """
    ``uint32_t SDL_RegisterEvents(int)``
    """
    numevents_c = numevents
    rc = _LIB.SDL_RegisterEvents(numevents_c)
    return rc

def SDL_RemoveTimer(id):
    """
    ``SDL_bool SDL_RemoveTimer(int)``
    """
    id_c = id
    rc = _LIB.SDL_RemoveTimer(id_c)
    return rc

def SDL_RenderClear(renderer):
    """
    ``int SDL_RenderClear(SDL_Renderer *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rc = _LIB.SDL_RenderClear(renderer_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderCopy(renderer, texture, srcrect, dstrect):
    """
    ``int SDL_RenderCopy(SDL_Renderer *, SDL_Texture *, SDL_Rect const *, SDL_Rect const *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    texture_c = unbox(texture, 'SDL_Texture *')
    srcrect_c = unbox(srcrect, 'SDL_Rect const *')
    dstrect_c = unbox(dstrect, 'SDL_Rect const *')
    rc = _LIB.SDL_RenderCopy(renderer_c, texture_c, srcrect_c, dstrect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderCopyEx(renderer, texture, srcrect, dstrect, angle, center, flip):
    """
    ``int SDL_RenderCopyEx(SDL_Renderer *, SDL_Texture *, SDL_Rect const *, SDL_Rect const *, double, SDL_Point const *, SDL_RendererFlip)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    texture_c = unbox(texture, 'SDL_Texture *')
    srcrect_c = unbox(srcrect, 'SDL_Rect const *')
    dstrect_c = unbox(dstrect, 'SDL_Rect const *')
    angle_c = angle
    center_c = unbox(center, 'SDL_Point const *')
    flip_c = flip
    rc = _LIB.SDL_RenderCopyEx(renderer_c, texture_c, srcrect_c, dstrect_c, angle_c, center_c, flip_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderDrawLine(renderer, x1, y1, x2, y2):
    """
    ``int SDL_RenderDrawLine(SDL_Renderer *, int, int, int, int)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    x1_c = x1
    y1_c = y1
    x2_c = x2
    y2_c = y2
    rc = _LIB.SDL_RenderDrawLine(renderer_c, x1_c, y1_c, x2_c, y2_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderDrawLines(renderer, points, count):
    """
    ``int SDL_RenderDrawLines(SDL_Renderer *, SDL_Point const *, int)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    points_c = unbox(points, 'SDL_Point const *')
    count_c = count
    rc = _LIB.SDL_RenderDrawLines(renderer_c, points_c, count_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderDrawPoint(renderer, x, y):
    """
    ``int SDL_RenderDrawPoint(SDL_Renderer *, int, int)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    x_c = x
    y_c = y
    rc = _LIB.SDL_RenderDrawPoint(renderer_c, x_c, y_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderDrawPoints(renderer, points, count):
    """
    ``int SDL_RenderDrawPoints(SDL_Renderer *, SDL_Point const *, int)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    points_c = unbox(points, 'SDL_Point const *')
    count_c = count
    rc = _LIB.SDL_RenderDrawPoints(renderer_c, points_c, count_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderDrawRect(renderer, rect):
    """
    ``int SDL_RenderDrawRect(SDL_Renderer *, SDL_Rect const *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rect_c = unbox(rect, 'SDL_Rect const *')
    rc = _LIB.SDL_RenderDrawRect(renderer_c, rect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderDrawRects(renderer, rects, count):
    """
    ``int SDL_RenderDrawRects(SDL_Renderer *, SDL_Rect const *, int)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rects_c = unbox(rects, 'SDL_Rect const *')
    count_c = count
    rc = _LIB.SDL_RenderDrawRects(renderer_c, rects_c, count_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderFillRect(renderer, rect):
    """
    ``int SDL_RenderFillRect(SDL_Renderer *, SDL_Rect const *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rect_c = unbox(rect, 'SDL_Rect const *')
    rc = _LIB.SDL_RenderFillRect(renderer_c, rect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderFillRects(renderer, rects, count):
    """
    ``int SDL_RenderFillRects(SDL_Renderer *, SDL_Rect const *, int)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rects_c = unbox(rects, 'SDL_Rect const *')
    count_c = count
    rc = _LIB.SDL_RenderFillRects(renderer_c, rects_c, count_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderGetClipRect(renderer, rect):
    """
    ``void SDL_RenderGetClipRect(SDL_Renderer *, SDL_Rect *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rect_c = unbox(rect, 'SDL_Rect *')
    _LIB.SDL_RenderGetClipRect(renderer_c, rect_c)

def SDL_RenderGetLogicalSize(renderer, w=None, h=None):
    """
    ``void SDL_RenderGetLogicalSize(SDL_Renderer *, int *, int *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    _LIB.SDL_RenderGetLogicalSize(renderer_c, w_c, h_c)
    return (w_c[0], h_c[0])

def SDL_RenderGetScale(renderer, scaleX=None, scaleY=None):
    """
    ``void SDL_RenderGetScale(SDL_Renderer *, float *, float *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    scaleX_c = unbox(scaleX, 'float *')
    scaleY_c = unbox(scaleY, 'float *')
    _LIB.SDL_RenderGetScale(renderer_c, scaleX_c, scaleY_c)
    return (scaleX_c[0], scaleY_c[0])

def SDL_RenderGetViewport(renderer, rect):
    """
    ``void SDL_RenderGetViewport(SDL_Renderer *, SDL_Rect *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rect_c = unbox(rect, 'SDL_Rect *')
    _LIB.SDL_RenderGetViewport(renderer_c, rect_c)

def SDL_RenderPresent(renderer):
    """
    ``void SDL_RenderPresent(SDL_Renderer *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    _LIB.SDL_RenderPresent(renderer_c)

def SDL_RenderReadPixels(renderer, rect, format, pixels, pitch):
    """
    ``int SDL_RenderReadPixels(SDL_Renderer *, SDL_Rect const *, uint32_t, void *, int)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rect_c = unbox(rect, 'SDL_Rect const *')
    format_c = format
    pixels_c = unbox(pixels, 'void *')
    pitch_c = pitch
    rc = _LIB.SDL_RenderReadPixels(renderer_c, rect_c, format_c, pixels_c, pitch_c)
    return rc

def SDL_RenderSetClipRect(renderer, rect):
    """
    ``int SDL_RenderSetClipRect(SDL_Renderer *, SDL_Rect const *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rect_c = unbox(rect, 'SDL_Rect const *')
    rc = _LIB.SDL_RenderSetClipRect(renderer_c, rect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderSetLogicalSize(renderer, w, h):
    """
    ``int SDL_RenderSetLogicalSize(SDL_Renderer *, int, int)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    w_c = w
    h_c = h
    rc = _LIB.SDL_RenderSetLogicalSize(renderer_c, w_c, h_c)
    return rc

def SDL_RenderSetScale(renderer, scaleX, scaleY):
    """
    ``int SDL_RenderSetScale(SDL_Renderer *, float, float)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    scaleX_c = scaleX
    scaleY_c = scaleY
    rc = _LIB.SDL_RenderSetScale(renderer_c, scaleX_c, scaleY_c)
    return rc

def SDL_RenderSetViewport(renderer, rect):
    """
    ``int SDL_RenderSetViewport(SDL_Renderer *, SDL_Rect const *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rect_c = unbox(rect, 'SDL_Rect const *')
    rc = _LIB.SDL_RenderSetViewport(renderer_c, rect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderTargetSupported(renderer):
    """
    ``SDL_bool SDL_RenderTargetSupported(SDL_Renderer *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rc = _LIB.SDL_RenderTargetSupported(renderer_c)
    return rc

def SDL_ReportAssertion():
    """
    ``SDL_assert_state SDL_ReportAssertion(SDL_assert_data *, char const *, char const *, int)``
    """
    rc = _LIB.SDL_ReportAssertion()
    return rc

def SDL_ResetAssertionReport():
    """
    ``void SDL_ResetAssertionReport(void)``
    """
    _LIB.SDL_ResetAssertionReport()

def SDL_RestoreWindow(window):
    """
    ``void SDL_RestoreWindow(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_RestoreWindow(window_c)

def SDL_SaveAllDollarTemplates(src):
    """
    ``int SDL_SaveAllDollarTemplates(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_SaveAllDollarTemplates(src_c)
    return rc

def SDL_SaveBMP_RW(surface, dst, freedst):
    """
    ``int SDL_SaveBMP_RW(SDL_Surface *, SDL_RWops *, int)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    dst_c = unbox(dst, 'SDL_RWops *')
    freedst_c = freedst
    rc = _LIB.SDL_SaveBMP_RW(surface_c, dst_c, freedst_c)
    return rc

def SDL_SaveDollarTemplate(gestureId, src):
    """
    ``int SDL_SaveDollarTemplate(int64_t, SDL_RWops *)``
    """
    gestureId_c = gestureId
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_SaveDollarTemplate(gestureId_c, src_c)
    return rc

def SDL_SemPost(sem):
    """
    ``int SDL_SemPost(SDL_sem *)``
    """
    sem_c = unbox(sem, 'SDL_sem *')
    rc = _LIB.SDL_SemPost(sem_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_SemTryWait(sem):
    """
    ``int SDL_SemTryWait(SDL_sem *)``
    """
    sem_c = unbox(sem, 'SDL_sem *')
    rc = _LIB.SDL_SemTryWait(sem_c)
    return rc

def SDL_SemValue(sem):
    """
    ``uint32_t SDL_SemValue(SDL_sem *)``
    """
    sem_c = unbox(sem, 'SDL_sem *')
    rc = _LIB.SDL_SemValue(sem_c)
    return rc

def SDL_SemWait(sem):
    """
    ``int SDL_SemWait(SDL_sem *)``
    """
    sem_c = unbox(sem, 'SDL_sem *')
    rc = _LIB.SDL_SemWait(sem_c)
    return rc

def SDL_SemWaitTimeout(sem, ms):
    """
    ``int SDL_SemWaitTimeout(SDL_sem *, uint32_t)``
    """
    sem_c = unbox(sem, 'SDL_sem *')
    ms_c = ms
    rc = _LIB.SDL_SemWaitTimeout(sem_c, ms_c)
    return rc

def SDL_SetAssertionHandler(handler, userdata):
    """
    ``void SDL_SetAssertionHandler(SDL_assert_state SDL_SetAssertionHandler(SDL_assert_data const *, void *), void *)``
    """
    handler_c = unbox(handler, 'SDL_assert_state(*)(SDL_assert_data const *, void *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_SetAssertionHandler(handler_c, userdata_c)

def SDL_SetClipRect(surface, rect):
    """
    ``SDL_bool SDL_SetClipRect(SDL_Surface *, SDL_Rect const *)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    rect_c = unbox(rect, 'SDL_Rect const *')
    rc = _LIB.SDL_SetClipRect(surface_c, rect_c)
    return rc

def SDL_SetClipboardText(text):
    """
    ``int SDL_SetClipboardText(char const *)``
    """
    text_c = text
    rc = _LIB.SDL_SetClipboardText(text_c)
    return rc

def SDL_SetColorKey(surface, flag, key):
    """
    ``int SDL_SetColorKey(SDL_Surface *, int, uint32_t)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    flag_c = flag
    key_c = key
    rc = _LIB.SDL_SetColorKey(surface_c, flag_c, key_c)
    return rc

def SDL_SetCursor(cursor):
    """
    ``void SDL_SetCursor(SDL_Cursor *)``
    """
    cursor_c = unbox(cursor, 'SDL_Cursor *')
    _LIB.SDL_SetCursor(cursor_c)

def SDL_SetError(fmt):
    """
    ``int SDL_SetError(char const *, ...)``
    """
    fmt_c = fmt
    rc = _LIB.SDL_SetError(fmt_c)
    return rc

def SDL_SetEventFilter(filter, userdata):
    """
    ``void SDL_SetEventFilter(int SDL_SetEventFilter(void *, SDL_Event *), void *)``
    """
    filter_c = unbox(filter, 'int(*)(void *, SDL_Event *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_SetEventFilter(filter_c, userdata_c)

def SDL_SetHint(name, value):
    """
    ``SDL_bool SDL_SetHint(char const *, char const *)``
    """
    name_c = name
    value_c = value
    rc = _LIB.SDL_SetHint(name_c, value_c)
    return rc

def SDL_SetHintWithPriority(name, value, priority):
    """
    ``SDL_bool SDL_SetHintWithPriority(char const *, char const *, SDL_HintPriority)``
    """
    name_c = name
    value_c = value
    priority_c = priority
    rc = _LIB.SDL_SetHintWithPriority(name_c, value_c, priority_c)
    return rc

def SDL_SetMainReady():
    """
    ``void SDL_SetMainReady(void)``
    """
    _LIB.SDL_SetMainReady()

def SDL_SetModState(modstate):
    """
    ``void SDL_SetModState(SDL_Keymod)``
    """
    modstate_c = modstate
    _LIB.SDL_SetModState(modstate_c)

def SDL_SetPaletteColors(palette, colors, firstcolor, ncolors):
    """
    ``int SDL_SetPaletteColors(SDL_Palette *, SDL_Color const *, int, int)``
    """
    palette_c = unbox(palette, 'SDL_Palette *')
    colors_c = unbox(colors, 'SDL_Color const *')
    firstcolor_c = firstcolor
    ncolors_c = ncolors
    rc = _LIB.SDL_SetPaletteColors(palette_c, colors_c, firstcolor_c, ncolors_c)
    return rc

def SDL_SetPixelFormatPalette(format, palette):
    """
    ``int SDL_SetPixelFormatPalette(SDL_PixelFormat *, SDL_Palette *)``
    """
    format_c = unbox(format, 'SDL_PixelFormat *')
    palette_c = unbox(palette, 'SDL_Palette *')
    rc = _LIB.SDL_SetPixelFormatPalette(format_c, palette_c)
    return rc

def SDL_SetRelativeMouseMode(enabled):
    """
    ``int SDL_SetRelativeMouseMode(SDL_bool)``
    """
    enabled_c = enabled
    rc = _LIB.SDL_SetRelativeMouseMode(enabled_c)
    return rc

def SDL_SetRenderDrawBlendMode(renderer, blendMode):
    """
    ``int SDL_SetRenderDrawBlendMode(SDL_Renderer *, SDL_BlendMode)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    blendMode_c = blendMode
    rc = _LIB.SDL_SetRenderDrawBlendMode(renderer_c, blendMode_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_SetRenderDrawColor(renderer, r, g, b, a):
    """
    ``int SDL_SetRenderDrawColor(SDL_Renderer *, uint8_t, uint8_t, uint8_t, uint8_t)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    r_c = r
    g_c = g
    b_c = b
    a_c = a
    rc = _LIB.SDL_SetRenderDrawColor(renderer_c, r_c, g_c, b_c, a_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_SetRenderTarget(renderer, texture):
    """
    ``int SDL_SetRenderTarget(SDL_Renderer *, SDL_Texture *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    texture_c = unbox(texture, 'SDL_Texture *')
    rc = _LIB.SDL_SetRenderTarget(renderer_c, texture_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_SetSurfaceAlphaMod(surface, alpha):
    """
    ``int SDL_SetSurfaceAlphaMod(SDL_Surface *, uint8_t)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    alpha_c = alpha
    rc = _LIB.SDL_SetSurfaceAlphaMod(surface_c, alpha_c)
    return rc

def SDL_SetSurfaceBlendMode(surface, blendMode):
    """
    ``int SDL_SetSurfaceBlendMode(SDL_Surface *, SDL_BlendMode)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    blendMode_c = blendMode
    rc = _LIB.SDL_SetSurfaceBlendMode(surface_c, blendMode_c)
    return rc

def SDL_SetSurfaceColorMod(surface, r, g, b):
    """
    ``int SDL_SetSurfaceColorMod(SDL_Surface *, uint8_t, uint8_t, uint8_t)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    r_c = r
    g_c = g
    b_c = b
    rc = _LIB.SDL_SetSurfaceColorMod(surface_c, r_c, g_c, b_c)
    return rc

def SDL_SetSurfacePalette(surface, palette):
    """
    ``int SDL_SetSurfacePalette(SDL_Surface *, SDL_Palette *)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    palette_c = unbox(palette, 'SDL_Palette *')
    rc = _LIB.SDL_SetSurfacePalette(surface_c, palette_c)
    return rc

def SDL_SetSurfaceRLE(surface, flag):
    """
    ``int SDL_SetSurfaceRLE(SDL_Surface *, int)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    flag_c = flag
    rc = _LIB.SDL_SetSurfaceRLE(surface_c, flag_c)
    return rc

def SDL_SetTextInputRect(rect):
    """
    ``void SDL_SetTextInputRect(SDL_Rect *)``
    """
    rect_c = unbox(rect, 'SDL_Rect *')
    _LIB.SDL_SetTextInputRect(rect_c)

def SDL_SetTextureAlphaMod(texture, alpha):
    """
    ``int SDL_SetTextureAlphaMod(SDL_Texture *, uint8_t)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    alpha_c = alpha
    rc = _LIB.SDL_SetTextureAlphaMod(texture_c, alpha_c)
    return rc

def SDL_SetTextureBlendMode(texture, blendMode):
    """
    ``int SDL_SetTextureBlendMode(SDL_Texture *, SDL_BlendMode)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    blendMode_c = blendMode
    rc = _LIB.SDL_SetTextureBlendMode(texture_c, blendMode_c)
    return rc

def SDL_SetTextureColorMod(texture, r, g, b):
    """
    ``int SDL_SetTextureColorMod(SDL_Texture *, uint8_t, uint8_t, uint8_t)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    r_c = r
    g_c = g
    b_c = b
    rc = _LIB.SDL_SetTextureColorMod(texture_c, r_c, g_c, b_c)
    return rc

def SDL_SetThreadPriority(priority):
    """
    ``int SDL_SetThreadPriority(SDL_ThreadPriority)``
    """
    priority_c = priority
    rc = _LIB.SDL_SetThreadPriority(priority_c)
    return rc

def SDL_SetWindowBordered(window, bordered):
    """
    ``void SDL_SetWindowBordered(SDL_Window *, SDL_bool)``
    """
    window_c = unbox(window, 'SDL_Window *')
    bordered_c = bordered
    _LIB.SDL_SetWindowBordered(window_c, bordered_c)

def SDL_SetWindowBrightness(window, brightness):
    """
    ``int SDL_SetWindowBrightness(SDL_Window *, float)``
    """
    window_c = unbox(window, 'SDL_Window *')
    brightness_c = brightness
    rc = _LIB.SDL_SetWindowBrightness(window_c, brightness_c)
    return rc

def SDL_SetWindowData(window, name, userdata):
    """
    ``void * SDL_SetWindowData(SDL_Window *, char const *, void *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    name_c = name
    userdata_c = unbox(userdata, 'void *')
    rc = _LIB.SDL_SetWindowData(window_c, name_c, userdata_c)
    return rc

def SDL_SetWindowDisplayMode(window, mode):
    """
    ``int SDL_SetWindowDisplayMode(SDL_Window *, SDL_DisplayMode const *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    mode_c = unbox(mode, 'SDL_DisplayMode const *')
    rc = _LIB.SDL_SetWindowDisplayMode(window_c, mode_c)
    return rc

def SDL_SetWindowFullscreen(window, flags):
    """
    ``int SDL_SetWindowFullscreen(SDL_Window *, uint32_t)``
    """
    window_c = unbox(window, 'SDL_Window *')
    flags_c = flags
    rc = _LIB.SDL_SetWindowFullscreen(window_c, flags_c)
    return rc

def SDL_SetWindowGammaRamp(window, red=None, green=None, blue=None):
    """
    ``int SDL_SetWindowGammaRamp(SDL_Window *, uint16_t const *, uint16_t const *, uint16_t const *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    red_c = unbox(red, 'uint16_t const *')
    green_c = unbox(green, 'uint16_t const *')
    blue_c = unbox(blue, 'uint16_t const *')
    rc = _LIB.SDL_SetWindowGammaRamp(window_c, red_c, green_c, blue_c)
    return (rc, red_c[0], green_c[0], blue_c[0])

def SDL_SetWindowGrab(window, grabbed):
    """
    ``void SDL_SetWindowGrab(SDL_Window *, SDL_bool)``
    """
    window_c = unbox(window, 'SDL_Window *')
    grabbed_c = grabbed
    _LIB.SDL_SetWindowGrab(window_c, grabbed_c)

def SDL_SetWindowIcon(window, icon):
    """
    ``void SDL_SetWindowIcon(SDL_Window *, SDL_Surface *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    icon_c = unbox(icon, 'SDL_Surface *')
    _LIB.SDL_SetWindowIcon(window_c, icon_c)

def SDL_SetWindowMaximumSize(window, max_w, max_h):
    """
    ``void SDL_SetWindowMaximumSize(SDL_Window *, int, int)``
    """
    window_c = unbox(window, 'SDL_Window *')
    max_w_c = max_w
    max_h_c = max_h
    _LIB.SDL_SetWindowMaximumSize(window_c, max_w_c, max_h_c)

def SDL_SetWindowMinimumSize(window, min_w, min_h):
    """
    ``void SDL_SetWindowMinimumSize(SDL_Window *, int, int)``
    """
    window_c = unbox(window, 'SDL_Window *')
    min_w_c = min_w
    min_h_c = min_h
    _LIB.SDL_SetWindowMinimumSize(window_c, min_w_c, min_h_c)

def SDL_SetWindowPosition(window, x, y):
    """
    ``void SDL_SetWindowPosition(SDL_Window *, int, int)``
    """
    window_c = unbox(window, 'SDL_Window *')
    x_c = x
    y_c = y
    _LIB.SDL_SetWindowPosition(window_c, x_c, y_c)

def SDL_SetWindowSize(window, w, h):
    """
    ``void SDL_SetWindowSize(SDL_Window *, int, int)``
    """
    window_c = unbox(window, 'SDL_Window *')
    w_c = w
    h_c = h
    _LIB.SDL_SetWindowSize(window_c, w_c, h_c)

def SDL_SetWindowTitle(window, title):
    """
    ``void SDL_SetWindowTitle(SDL_Window *, char const *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    title_c = title
    _LIB.SDL_SetWindowTitle(window_c, title_c)

def SDL_ShowCursor(toggle):
    """
    ``int SDL_ShowCursor(int)``
    """
    toggle_c = toggle
    rc = _LIB.SDL_ShowCursor(toggle_c)
    return rc

def SDL_ShowMessageBox(messageboxdata, buttonid=None):
    """
    ``int SDL_ShowMessageBox(SDL_MessageBoxData const *, int *)``
    """
    messageboxdata_c = unbox(messageboxdata, 'SDL_MessageBoxData const *')
    buttonid_c = unbox(buttonid, 'int *')
    rc = _LIB.SDL_ShowMessageBox(messageboxdata_c, buttonid_c)
    if rc == -1: raise SDLError()
    return (rc, buttonid_c[0])

def SDL_ShowSimpleMessageBox(flags, title, message, window):
    """
    ``int SDL_ShowSimpleMessageBox(uint32_t, char const *, char const *, SDL_Window *)``
    """
    flags_c = flags
    title_c = title
    message_c = message
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_ShowSimpleMessageBox(flags_c, title_c, message_c, window_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_ShowWindow(window):
    """
    ``void SDL_ShowWindow(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_ShowWindow(window_c)

def SDL_SoftStretch(src, srcrect, dst, dstrect):
    """
    ``int SDL_SoftStretch(SDL_Surface *, SDL_Rect const *, SDL_Surface *, SDL_Rect const *)``
    """
    src_c = unbox(src, 'SDL_Surface *')
    srcrect_c = unbox(srcrect, 'SDL_Rect const *')
    dst_c = unbox(dst, 'SDL_Surface *')
    dstrect_c = unbox(dstrect, 'SDL_Rect const *')
    rc = _LIB.SDL_SoftStretch(src_c, srcrect_c, dst_c, dstrect_c)
    return rc

def SDL_StartTextInput():
    """
    ``void SDL_StartTextInput(void)``
    """
    _LIB.SDL_StartTextInput()

def SDL_StopTextInput():
    """
    ``void SDL_StopTextInput(void)``
    """
    _LIB.SDL_StopTextInput()

def SDL_TLSCreate():
    """
    ``unsigned int SDL_TLSCreate(void)``
    """
    rc = _LIB.SDL_TLSCreate()
    return rc

def SDL_TLSGet(id):
    """
    ``void * SDL_TLSGet(unsigned int)``
    """
    id_c = id
    rc = _LIB.SDL_TLSGet(id_c)
    return rc

def SDL_TLSSet(id, value, destructor):
    """
    ``int SDL_TLSSet(unsigned int, void const *, void SDL_TLSSet(void *))``
    """
    id_c = id
    value_c = unbox(value, 'void const *')
    destructor_c = unbox(destructor, 'void(*)(void *)')
    rc = _LIB.SDL_TLSSet(id_c, value_c, destructor_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_ThreadID():
    """
    ``unsigned long SDL_ThreadID(void)``
    """
    rc = _LIB.SDL_ThreadID()
    return rc

def SDL_TryLockMutex(mutex):
    """
    ``int SDL_TryLockMutex(SDL_mutex *)``
    """
    mutex_c = unbox(mutex, 'SDL_mutex *')
    rc = _LIB.SDL_TryLockMutex(mutex_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_UnionRect(A, B, result):
    """
    ``void SDL_UnionRect(SDL_Rect const *, SDL_Rect const *, SDL_Rect *)``
    """
    A_c = unbox(A, 'SDL_Rect const *')
    B_c = unbox(B, 'SDL_Rect const *')
    result_c = unbox(result, 'SDL_Rect *')
    _LIB.SDL_UnionRect(A_c, B_c, result_c)

def SDL_UnloadObject(handle):
    """
    ``void SDL_UnloadObject(void *)``
    """
    handle_c = unbox(handle, 'void *')
    _LIB.SDL_UnloadObject(handle_c)

def SDL_UnlockAudio():
    """
    ``void SDL_UnlockAudio(void)``
    """
    _LIB.SDL_UnlockAudio()

def SDL_UnlockAudioDevice(dev):
    """
    ``void SDL_UnlockAudioDevice(uint32_t)``
    """
    dev_c = dev
    _LIB.SDL_UnlockAudioDevice(dev_c)

def SDL_UnlockMutex(mutex):
    """
    ``int SDL_UnlockMutex(SDL_mutex *)``
    """
    mutex_c = unbox(mutex, 'SDL_mutex *')
    rc = _LIB.SDL_UnlockMutex(mutex_c)
    return rc

def SDL_UnlockSurface(surface):
    """
    ``void SDL_UnlockSurface(SDL_Surface *)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    _LIB.SDL_UnlockSurface(surface_c)

def SDL_UnlockTexture(texture):
    """
    ``void SDL_UnlockTexture(SDL_Texture *)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    _LIB.SDL_UnlockTexture(texture_c)

def SDL_UpdateTexture(texture, rect, pixels, pitch):
    """
    ``int SDL_UpdateTexture(SDL_Texture *, SDL_Rect const *, void const *, int)``
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    rect_c = unbox(rect, 'SDL_Rect const *')
    pixels_c = unbox(pixels, 'void const *')
    pitch_c = pitch
    rc = _LIB.SDL_UpdateTexture(texture_c, rect_c, pixels_c, pitch_c)
    return rc

def SDL_UpdateWindowSurface(window):
    """
    ``int SDL_UpdateWindowSurface(SDL_Window *)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_UpdateWindowSurface(window_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_UpdateWindowSurfaceRects(window, rects, numrects):
    """
    ``int SDL_UpdateWindowSurfaceRects(SDL_Window *, SDL_Rect const *, int)``
    """
    window_c = unbox(window, 'SDL_Window *')
    rects_c = unbox(rects, 'SDL_Rect const *')
    numrects_c = numrects
    rc = _LIB.SDL_UpdateWindowSurfaceRects(window_c, rects_c, numrects_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_UpperBlit(src, srcrect, dst, dstrect):
    """
    ``int SDL_UpperBlit(SDL_Surface *, SDL_Rect const *, SDL_Surface *, SDL_Rect *)``
    """
    src_c = unbox(src, 'SDL_Surface *')
    srcrect_c = unbox(srcrect, 'SDL_Rect const *')
    dst_c = unbox(dst, 'SDL_Surface *')
    dstrect_c = unbox(dstrect, 'SDL_Rect *')
    rc = _LIB.SDL_UpperBlit(src_c, srcrect_c, dst_c, dstrect_c)
    return rc

def SDL_UpperBlitScaled(src, srcrect, dst, dstrect):
    """
    ``int SDL_UpperBlitScaled(SDL_Surface *, SDL_Rect const *, SDL_Surface *, SDL_Rect *)``
    """
    src_c = unbox(src, 'SDL_Surface *')
    srcrect_c = unbox(srcrect, 'SDL_Rect const *')
    dst_c = unbox(dst, 'SDL_Surface *')
    dstrect_c = unbox(dstrect, 'SDL_Rect *')
    rc = _LIB.SDL_UpperBlitScaled(src_c, srcrect_c, dst_c, dstrect_c)
    return rc

def SDL_VideoInit(driver_name):
    """
    ``int SDL_VideoInit(char const *)``
    """
    driver_name_c = driver_name
    rc = _LIB.SDL_VideoInit(driver_name_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_VideoQuit():
    """
    ``void SDL_VideoQuit(void)``
    """
    _LIB.SDL_VideoQuit()

def SDL_WaitEvent(event):
    """
    ``int SDL_WaitEvent(SDL_Event *)``
    """
    event_c = unbox(event, 'SDL_Event *')
    rc = _LIB.SDL_WaitEvent(event_c)
    return rc

def SDL_WaitEventTimeout(event, timeout):
    """
    ``int SDL_WaitEventTimeout(SDL_Event *, int)``
    """
    event_c = unbox(event, 'SDL_Event *')
    timeout_c = timeout
    rc = _LIB.SDL_WaitEventTimeout(event_c, timeout_c)
    return rc

def SDL_WaitThread(thread, status=None):
    """
    ``void SDL_WaitThread(SDL_Thread *, int *)``
    """
    thread_c = unbox(thread, 'SDL_Thread *')
    status_c = unbox(status, 'int *')
    _LIB.SDL_WaitThread(thread_c, status_c)
    return status_c[0]

def SDL_WarpMouseInWindow(window, x, y):
    """
    ``void SDL_WarpMouseInWindow(SDL_Window *, int, int)``
    """
    window_c = unbox(window, 'SDL_Window *')
    x_c = x
    y_c = y
    _LIB.SDL_WarpMouseInWindow(window_c, x_c, y_c)

def SDL_WasInit(flags):
    """
    ``uint32_t SDL_WasInit(uint32_t)``
    """
    flags_c = flags
    rc = _LIB.SDL_WasInit(flags_c)
    return rc

def SDL_WriteBE16(dst, value):
    """
    ``size_t SDL_WriteBE16(SDL_RWops *, uint16_t)``
    """
    dst_c = unbox(dst, 'SDL_RWops *')
    value_c = value
    rc = _LIB.SDL_WriteBE16(dst_c, value_c)
    return rc

def SDL_WriteBE32(dst, value):
    """
    ``size_t SDL_WriteBE32(SDL_RWops *, uint32_t)``
    """
    dst_c = unbox(dst, 'SDL_RWops *')
    value_c = value
    rc = _LIB.SDL_WriteBE32(dst_c, value_c)
    return rc

def SDL_WriteBE64(dst, value):
    """
    ``size_t SDL_WriteBE64(SDL_RWops *, uint64_t)``
    """
    dst_c = unbox(dst, 'SDL_RWops *')
    value_c = value
    rc = _LIB.SDL_WriteBE64(dst_c, value_c)
    return rc

def SDL_WriteLE16(dst, value):
    """
    ``size_t SDL_WriteLE16(SDL_RWops *, uint16_t)``
    """
    dst_c = unbox(dst, 'SDL_RWops *')
    value_c = value
    rc = _LIB.SDL_WriteLE16(dst_c, value_c)
    return rc

def SDL_WriteLE32(dst, value):
    """
    ``size_t SDL_WriteLE32(SDL_RWops *, uint32_t)``
    """
    dst_c = unbox(dst, 'SDL_RWops *')
    value_c = value
    rc = _LIB.SDL_WriteLE32(dst_c, value_c)
    return rc

def SDL_WriteLE64(dst, value):
    """
    ``size_t SDL_WriteLE64(SDL_RWops *, uint64_t)``
    """
    dst_c = unbox(dst, 'SDL_RWops *')
    value_c = value
    rc = _LIB.SDL_WriteLE64(dst_c, value_c)
    return rc

def SDL_WriteU8(dst, value):
    """
    ``size_t SDL_WriteU8(SDL_RWops *, uint8_t)``
    """
    dst_c = unbox(dst, 'SDL_RWops *')
    value_c = value
    rc = _LIB.SDL_WriteU8(dst_c, value_c)
    return rc

def SDL_abs(x):
    """
    ``int SDL_abs(int)``
    """
    x_c = x
    rc = _LIB.SDL_abs(x_c)
    return rc

def SDL_atan(x):
    """
    ``double SDL_atan(double)``
    """
    x_c = x
    rc = _LIB.SDL_atan(x_c)
    return rc

def SDL_atan2(x, y):
    """
    ``double SDL_atan2(double, double)``
    """
    x_c = x
    y_c = y
    rc = _LIB.SDL_atan2(x_c, y_c)
    return rc

def SDL_atof(str):
    """
    ``double SDL_atof(char const *)``
    """
    str_c = str
    rc = _LIB.SDL_atof(str_c)
    return rc

def SDL_atoi(str):
    """
    ``int SDL_atoi(char const *)``
    """
    str_c = str
    rc = _LIB.SDL_atoi(str_c)
    return rc

def SDL_calloc(nmemb, size):
    """
    ``void * SDL_calloc(size_t, size_t)``
    """
    nmemb_c = nmemb
    size_c = size
    rc = _LIB.SDL_calloc(nmemb_c, size_c)
    return rc

def SDL_ceil(x):
    """
    ``double SDL_ceil(double)``
    """
    x_c = x
    rc = _LIB.SDL_ceil(x_c)
    return rc

def SDL_copysign(x, y):
    """
    ``double SDL_copysign(double, double)``
    """
    x_c = x
    y_c = y
    rc = _LIB.SDL_copysign(x_c, y_c)
    return rc

def SDL_cos(x):
    """
    ``double SDL_cos(double)``
    """
    x_c = x
    rc = _LIB.SDL_cos(x_c)
    return rc

def SDL_cosf(x):
    """
    ``float SDL_cosf(float)``
    """
    x_c = x
    rc = _LIB.SDL_cosf(x_c)
    return rc

def SDL_fabs(x):
    """
    ``double SDL_fabs(double)``
    """
    x_c = x
    rc = _LIB.SDL_fabs(x_c)
    return rc

def SDL_floor(x):
    """
    ``double SDL_floor(double)``
    """
    x_c = x
    rc = _LIB.SDL_floor(x_c)
    return rc

def SDL_free(mem):
    """
    ``void SDL_free(void *)``
    """
    mem_c = unbox(mem, 'void *')
    _LIB.SDL_free(mem_c)

def SDL_getenv(name):
    """
    ``char * SDL_getenv(char const *)``
    """
    name_c = name
    rc = _LIB.SDL_getenv(name_c)
    return ffi.string(rc)

def SDL_iconv(cd, inbuf, inbytesleft, outbuf, outbytesleft=None):
    """
    ``size_t SDL_iconv(struct _SDL_iconv_t *, char const * *, size_t *, char * *, size_t *)``
    """
    cd_c = unbox(cd, 'struct _SDL_iconv_t *')
    inbuf_c = unbox(inbuf, 'char const * *')
    inbytesleft_c = unbox(inbytesleft, 'size_t *')
    outbuf_c = unbox(outbuf, 'char * *')
    outbytesleft_c = unbox(outbytesleft, 'size_t *')
    rc = _LIB.SDL_iconv(cd_c, inbuf_c, inbytesleft_c, outbuf_c, outbytesleft_c)
    return (rc, outbytesleft_c[0])

def SDL_iconv_close(cd):
    """
    ``int SDL_iconv_close(struct _SDL_iconv_t *)``
    """
    cd_c = unbox(cd, 'struct _SDL_iconv_t *')
    rc = _LIB.SDL_iconv_close(cd_c)
    return rc

def SDL_iconv_open(tocode, fromcode):
    """
    ``struct _SDL_iconv_t * SDL_iconv_open(char const *, char const *)``
    """
    tocode_c = tocode
    fromcode_c = fromcode
    rc = _LIB.SDL_iconv_open(tocode_c, fromcode_c)
    return rc

def SDL_iconv_string(tocode, fromcode, inbuf, inbytesleft):
    """
    ``char * SDL_iconv_string(char const *, char const *, char const *, size_t)``
    """
    tocode_c = tocode
    fromcode_c = fromcode
    inbuf_c = inbuf
    inbytesleft_c = inbytesleft
    rc = _LIB.SDL_iconv_string(tocode_c, fromcode_c, inbuf_c, inbytesleft_c)
    return ffi.string(rc)

def SDL_isdigit(x):
    """
    ``int SDL_isdigit(int)``
    """
    x_c = x
    rc = _LIB.SDL_isdigit(x_c)
    return rc

def SDL_isspace(x):
    """
    ``int SDL_isspace(int)``
    """
    x_c = x
    rc = _LIB.SDL_isspace(x_c)
    return rc

def SDL_itoa(value, str, radix):
    """
    ``char * SDL_itoa(int, char *, int)``
    """
    value_c = value
    str_c = str
    radix_c = radix
    rc = _LIB.SDL_itoa(value_c, str_c, radix_c)
    return ffi.string(rc)

def SDL_lltoa(value, str, radix):
    """
    ``char * SDL_lltoa(int64_t, char *, int)``
    """
    value_c = value
    str_c = str
    radix_c = radix
    rc = _LIB.SDL_lltoa(value_c, str_c, radix_c)
    return ffi.string(rc)

def SDL_log(x):
    """
    ``double SDL_log(double)``
    """
    x_c = x
    rc = _LIB.SDL_log(x_c)
    return rc

def SDL_ltoa(value, str, radix):
    """
    ``char * SDL_ltoa(long, char *, int)``
    """
    value_c = value
    str_c = str
    radix_c = radix
    rc = _LIB.SDL_ltoa(value_c, str_c, radix_c)
    return ffi.string(rc)

def SDL_main(argc, argv):
    """
    ``int SDL_main(int, char * *)``
    """
    argc_c = argc
    argv_c = unbox(argv, 'char * *')
    rc = _LIB.SDL_main(argc_c, argv_c)
    return rc

def SDL_malloc(size):
    """
    ``void * SDL_malloc(size_t)``
    """
    size_c = size
    rc = _LIB.SDL_malloc(size_c)
    return rc

def SDL_memcmp(s1, s2, len):
    """
    ``int SDL_memcmp(void const *, void const *, size_t)``
    """
    s1_c = unbox(s1, 'void const *')
    s2_c = unbox(s2, 'void const *')
    len_c = len
    rc = _LIB.SDL_memcmp(s1_c, s2_c, len_c)
    return rc

def SDL_memcpy(dst, src, len):
    """
    ``void * SDL_memcpy(void *, void const *, size_t)``
    """
    dst_c = unbox(dst, 'void *')
    src_c = unbox(src, 'void const *')
    len_c = len
    rc = _LIB.SDL_memcpy(dst_c, src_c, len_c)
    return rc

def SDL_memmove(dst, src, len):
    """
    ``void * SDL_memmove(void *, void const *, size_t)``
    """
    dst_c = unbox(dst, 'void *')
    src_c = unbox(src, 'void const *')
    len_c = len
    rc = _LIB.SDL_memmove(dst_c, src_c, len_c)
    return rc

def SDL_memset(dst, c, len):
    """
    ``void * SDL_memset(void *, int, size_t)``
    """
    dst_c = unbox(dst, 'void *')
    c_c = c
    len_c = len
    rc = _LIB.SDL_memset(dst_c, c_c, len_c)
    return rc

def SDL_pow(x, y):
    """
    ``double SDL_pow(double, double)``
    """
    x_c = x
    y_c = y
    rc = _LIB.SDL_pow(x_c, y_c)
    return rc

def SDL_qsort(base, nmemb, size, compare):
    """
    ``void SDL_qsort(void *, size_t, size_t, int SDL_qsort(void const *, void const *))``
    """
    base_c = unbox(base, 'void *')
    nmemb_c = nmemb
    size_c = size
    compare_c = unbox(compare, 'int(*)(void const *, void const *)')
    _LIB.SDL_qsort(base_c, nmemb_c, size_c, compare_c)

def SDL_realloc(mem, size):
    """
    ``void * SDL_realloc(void *, size_t)``
    """
    mem_c = unbox(mem, 'void *')
    size_c = size
    rc = _LIB.SDL_realloc(mem_c, size_c)
    return rc

def SDL_scalbn(x, n):
    """
    ``double SDL_scalbn(double, int)``
    """
    x_c = x
    n_c = n
    rc = _LIB.SDL_scalbn(x_c, n_c)
    return rc

def SDL_setenv(name, value, overwrite):
    """
    ``int SDL_setenv(char const *, char const *, int)``
    """
    name_c = name
    value_c = value
    overwrite_c = overwrite
    rc = _LIB.SDL_setenv(name_c, value_c, overwrite_c)
    return rc

def SDL_sin(x):
    """
    ``double SDL_sin(double)``
    """
    x_c = x
    rc = _LIB.SDL_sin(x_c)
    return rc

def SDL_sinf(x):
    """
    ``float SDL_sinf(float)``
    """
    x_c = x
    rc = _LIB.SDL_sinf(x_c)
    return rc

def SDL_snprintf(text, maxlen, fmt):
    """
    ``int SDL_snprintf(char *, size_t, char const *, ...)``
    """
    text_c = text
    maxlen_c = maxlen
    fmt_c = fmt
    rc = _LIB.SDL_snprintf(text_c, maxlen_c, fmt_c)
    return rc

def SDL_sqrt(x):
    """
    ``double SDL_sqrt(double)``
    """
    x_c = x
    rc = _LIB.SDL_sqrt(x_c)
    return rc

def SDL_sscanf(text, fmt):
    """
    ``int SDL_sscanf(char const *, char const *, ...)``
    """
    text_c = text
    fmt_c = fmt
    rc = _LIB.SDL_sscanf(text_c, fmt_c)
    return rc

def SDL_strcasecmp(str1, str2):
    """
    ``int SDL_strcasecmp(char const *, char const *)``
    """
    str1_c = str1
    str2_c = str2
    rc = _LIB.SDL_strcasecmp(str1_c, str2_c)
    return rc

def SDL_strchr(str, c):
    """
    ``char * SDL_strchr(char const *, int)``
    """
    str_c = str
    c_c = c
    rc = _LIB.SDL_strchr(str_c, c_c)
    return ffi.string(rc)

def SDL_strcmp(str1, str2):
    """
    ``int SDL_strcmp(char const *, char const *)``
    """
    str1_c = str1
    str2_c = str2
    rc = _LIB.SDL_strcmp(str1_c, str2_c)
    return rc

def SDL_strdup(str):
    """
    ``char * SDL_strdup(char const *)``
    """
    str_c = str
    rc = _LIB.SDL_strdup(str_c)
    return ffi.string(rc)

def SDL_strlcat(dst, src, maxlen):
    """
    ``size_t SDL_strlcat(char *, char const *, size_t)``
    """
    dst_c = dst
    src_c = src
    maxlen_c = maxlen
    rc = _LIB.SDL_strlcat(dst_c, src_c, maxlen_c)
    return rc

def SDL_strlcpy(dst, src, maxlen):
    """
    ``size_t SDL_strlcpy(char *, char const *, size_t)``
    """
    dst_c = dst
    src_c = src
    maxlen_c = maxlen
    rc = _LIB.SDL_strlcpy(dst_c, src_c, maxlen_c)
    return rc

def SDL_strlen(str):
    """
    ``size_t SDL_strlen(char const *)``
    """
    str_c = str
    rc = _LIB.SDL_strlen(str_c)
    return rc

def SDL_strlwr(str):
    """
    ``char * SDL_strlwr(char *)``
    """
    str_c = str
    rc = _LIB.SDL_strlwr(str_c)
    return ffi.string(rc)

def SDL_strncasecmp(str1, str2, len):
    """
    ``int SDL_strncasecmp(char const *, char const *, size_t)``
    """
    str1_c = str1
    str2_c = str2
    len_c = len
    rc = _LIB.SDL_strncasecmp(str1_c, str2_c, len_c)
    return rc

def SDL_strncmp(str1, str2, maxlen):
    """
    ``int SDL_strncmp(char const *, char const *, size_t)``
    """
    str1_c = str1
    str2_c = str2
    maxlen_c = maxlen
    rc = _LIB.SDL_strncmp(str1_c, str2_c, maxlen_c)
    return rc

def SDL_strrchr(str, c):
    """
    ``char * SDL_strrchr(char const *, int)``
    """
    str_c = str
    c_c = c
    rc = _LIB.SDL_strrchr(str_c, c_c)
    return ffi.string(rc)

def SDL_strrev(str):
    """
    ``char * SDL_strrev(char *)``
    """
    str_c = str
    rc = _LIB.SDL_strrev(str_c)
    return ffi.string(rc)

def SDL_strstr(haystack, needle):
    """
    ``char * SDL_strstr(char const *, char const *)``
    """
    haystack_c = haystack
    needle_c = needle
    rc = _LIB.SDL_strstr(haystack_c, needle_c)
    return ffi.string(rc)

def SDL_strtod(str, endp):
    """
    ``double SDL_strtod(char const *, char * *)``
    """
    str_c = str
    endp_c = unbox(endp, 'char * *')
    rc = _LIB.SDL_strtod(str_c, endp_c)
    return rc

def SDL_strtol(str, endp, base):
    """
    ``long SDL_strtol(char const *, char * *, int)``
    """
    str_c = str
    endp_c = unbox(endp, 'char * *')
    base_c = base
    rc = _LIB.SDL_strtol(str_c, endp_c, base_c)
    return rc

def SDL_strtoll(str, endp, base):
    """
    ``int64_t SDL_strtoll(char const *, char * *, int)``
    """
    str_c = str
    endp_c = unbox(endp, 'char * *')
    base_c = base
    rc = _LIB.SDL_strtoll(str_c, endp_c, base_c)
    return rc

def SDL_strtoul(str, endp, base):
    """
    ``unsigned long SDL_strtoul(char const *, char * *, int)``
    """
    str_c = str
    endp_c = unbox(endp, 'char * *')
    base_c = base
    rc = _LIB.SDL_strtoul(str_c, endp_c, base_c)
    return rc

def SDL_strtoull(str, endp, base):
    """
    ``uint64_t SDL_strtoull(char const *, char * *, int)``
    """
    str_c = str
    endp_c = unbox(endp, 'char * *')
    base_c = base
    rc = _LIB.SDL_strtoull(str_c, endp_c, base_c)
    return rc

def SDL_strupr(str):
    """
    ``char * SDL_strupr(char *)``
    """
    str_c = str
    rc = _LIB.SDL_strupr(str_c)
    return ffi.string(rc)

def SDL_tolower(x):
    """
    ``int SDL_tolower(int)``
    """
    x_c = x
    rc = _LIB.SDL_tolower(x_c)
    return rc

def SDL_toupper(x):
    """
    ``int SDL_toupper(int)``
    """
    x_c = x
    rc = _LIB.SDL_toupper(x_c)
    return rc

def SDL_uitoa(value, str, radix):
    """
    ``char * SDL_uitoa(unsigned int, char *, int)``
    """
    value_c = value
    str_c = str
    radix_c = radix
    rc = _LIB.SDL_uitoa(value_c, str_c, radix_c)
    return ffi.string(rc)

def SDL_ulltoa(value, str, radix):
    """
    ``char * SDL_ulltoa(uint64_t, char *, int)``
    """
    value_c = value
    str_c = str
    radix_c = radix
    rc = _LIB.SDL_ulltoa(value_c, str_c, radix_c)
    return ffi.string(rc)

def SDL_ultoa(value, str, radix):
    """
    ``char * SDL_ultoa(unsigned long, char *, int)``
    """
    value_c = value
    str_c = str
    radix_c = radix
    rc = _LIB.SDL_ultoa(value_c, str_c, radix_c)
    return ffi.string(rc)

def SDL_utf8strlcpy(dst, src, dst_bytes):
    """
    ``size_t SDL_utf8strlcpy(char *, char const *, size_t)``
    """
    dst_c = dst
    src_c = src
    dst_bytes_c = dst_bytes
    rc = _LIB.SDL_utf8strlcpy(dst_c, src_c, dst_bytes_c)
    return rc

def SDL_vsnprintf(text, maxlen, fmt, ap):
    """
    ``int SDL_vsnprintf(char *, size_t, char const *, int32_t)``
    """
    text_c = text
    maxlen_c = maxlen
    fmt_c = fmt
    ap_c = ap
    rc = _LIB.SDL_vsnprintf(text_c, maxlen_c, fmt_c, ap_c)
    return rc

def SDL_wcslcat(dst, src, maxlen):
    """
    ``size_t SDL_wcslcat(wchar_t *, wchar_t const *, size_t)``
    """
    dst_c = unbox(dst, 'wchar_t *')
    src_c = unbox(src, 'wchar_t const *')
    maxlen_c = maxlen
    rc = _LIB.SDL_wcslcat(dst_c, src_c, maxlen_c)
    return rc

def SDL_wcslcpy(dst, src, maxlen):
    """
    ``size_t SDL_wcslcpy(wchar_t *, wchar_t const *, size_t)``
    """
    dst_c = unbox(dst, 'wchar_t *')
    src_c = unbox(src, 'wchar_t const *')
    maxlen_c = maxlen
    rc = _LIB.SDL_wcslcpy(dst_c, src_c, maxlen_c)
    return rc

def SDL_wcslen(wstr=None):
    """
    ``size_t SDL_wcslen(wchar_t const *)``
    """
    wstr_c = unbox(wstr, 'wchar_t const *')
    rc = _LIB.SDL_wcslen(wstr_c)
    return (rc, wstr_c[0])

SDL_PIXELFORMAT_UNKNOWN = _LIB.SDL_PIXELFORMAT_UNKNOWN

SDL_LOG_CATEGORY_APPLICATION = _LIB.SDL_LOG_CATEGORY_APPLICATION
SDL_LOG_CATEGORY_ERROR = _LIB.SDL_LOG_CATEGORY_ERROR
SDL_LOG_CATEGORY_ASSERT = _LIB.SDL_LOG_CATEGORY_ASSERT
SDL_LOG_CATEGORY_SYSTEM = _LIB.SDL_LOG_CATEGORY_SYSTEM
SDL_LOG_CATEGORY_AUDIO = _LIB.SDL_LOG_CATEGORY_AUDIO
SDL_LOG_CATEGORY_VIDEO = _LIB.SDL_LOG_CATEGORY_VIDEO
SDL_LOG_CATEGORY_RENDER = _LIB.SDL_LOG_CATEGORY_RENDER
SDL_LOG_CATEGORY_INPUT = _LIB.SDL_LOG_CATEGORY_INPUT
SDL_LOG_CATEGORY_TEST = _LIB.SDL_LOG_CATEGORY_TEST
SDL_LOG_CATEGORY_RESERVED1 = _LIB.SDL_LOG_CATEGORY_RESERVED1
SDL_LOG_CATEGORY_RESERVED2 = _LIB.SDL_LOG_CATEGORY_RESERVED2
SDL_LOG_CATEGORY_RESERVED3 = _LIB.SDL_LOG_CATEGORY_RESERVED3
SDL_LOG_CATEGORY_RESERVED4 = _LIB.SDL_LOG_CATEGORY_RESERVED4
SDL_LOG_CATEGORY_RESERVED5 = _LIB.SDL_LOG_CATEGORY_RESERVED5
SDL_LOG_CATEGORY_RESERVED6 = _LIB.SDL_LOG_CATEGORY_RESERVED6
SDL_LOG_CATEGORY_RESERVED7 = _LIB.SDL_LOG_CATEGORY_RESERVED7
SDL_LOG_CATEGORY_RESERVED8 = _LIB.SDL_LOG_CATEGORY_RESERVED8
SDL_LOG_CATEGORY_RESERVED9 = _LIB.SDL_LOG_CATEGORY_RESERVED9
SDL_LOG_CATEGORY_RESERVED10 = _LIB.SDL_LOG_CATEGORY_RESERVED10
SDL_LOG_CATEGORY_CUSTOM = _LIB.SDL_LOG_CATEGORY_CUSTOM

SDL_PIXELTYPE_UNKNOWN = _LIB.SDL_PIXELTYPE_UNKNOWN
SDL_PIXELTYPE_INDEX1 = _LIB.SDL_PIXELTYPE_INDEX1
SDL_PIXELTYPE_INDEX4 = _LIB.SDL_PIXELTYPE_INDEX4
SDL_PIXELTYPE_INDEX8 = _LIB.SDL_PIXELTYPE_INDEX8
SDL_PIXELTYPE_PACKED8 = _LIB.SDL_PIXELTYPE_PACKED8
SDL_PIXELTYPE_PACKED16 = _LIB.SDL_PIXELTYPE_PACKED16
SDL_PIXELTYPE_PACKED32 = _LIB.SDL_PIXELTYPE_PACKED32
SDL_PIXELTYPE_ARRAYU8 = _LIB.SDL_PIXELTYPE_ARRAYU8
SDL_PIXELTYPE_ARRAYU16 = _LIB.SDL_PIXELTYPE_ARRAYU16
SDL_PIXELTYPE_ARRAYU32 = _LIB.SDL_PIXELTYPE_ARRAYU32
SDL_PIXELTYPE_ARRAYF16 = _LIB.SDL_PIXELTYPE_ARRAYF16
SDL_PIXELTYPE_ARRAYF32 = _LIB.SDL_PIXELTYPE_ARRAYF32

SDL_BITMAPORDER_NONE = _LIB.SDL_BITMAPORDER_NONE
SDL_BITMAPORDER_4321 = _LIB.SDL_BITMAPORDER_4321
SDL_BITMAPORDER_1234 = _LIB.SDL_BITMAPORDER_1234

SDL_PACKEDORDER_NONE = _LIB.SDL_PACKEDORDER_NONE
SDL_PACKEDORDER_XRGB = _LIB.SDL_PACKEDORDER_XRGB
SDL_PACKEDORDER_RGBX = _LIB.SDL_PACKEDORDER_RGBX
SDL_PACKEDORDER_ARGB = _LIB.SDL_PACKEDORDER_ARGB
SDL_PACKEDORDER_RGBA = _LIB.SDL_PACKEDORDER_RGBA
SDL_PACKEDORDER_XBGR = _LIB.SDL_PACKEDORDER_XBGR
SDL_PACKEDORDER_BGRX = _LIB.SDL_PACKEDORDER_BGRX
SDL_PACKEDORDER_ABGR = _LIB.SDL_PACKEDORDER_ABGR
SDL_PACKEDORDER_BGRA = _LIB.SDL_PACKEDORDER_BGRA

SDL_ARRAYORDER_NONE = _LIB.SDL_ARRAYORDER_NONE
SDL_ARRAYORDER_RGB = _LIB.SDL_ARRAYORDER_RGB
SDL_ARRAYORDER_RGBA = _LIB.SDL_ARRAYORDER_RGBA
SDL_ARRAYORDER_ARGB = _LIB.SDL_ARRAYORDER_ARGB
SDL_ARRAYORDER_BGR = _LIB.SDL_ARRAYORDER_BGR
SDL_ARRAYORDER_BGRA = _LIB.SDL_ARRAYORDER_BGRA
SDL_ARRAYORDER_ABGR = _LIB.SDL_ARRAYORDER_ABGR

SDL_PACKEDLAYOUT_NONE = _LIB.SDL_PACKEDLAYOUT_NONE
SDL_PACKEDLAYOUT_332 = _LIB.SDL_PACKEDLAYOUT_332
SDL_PACKEDLAYOUT_4444 = _LIB.SDL_PACKEDLAYOUT_4444
SDL_PACKEDLAYOUT_1555 = _LIB.SDL_PACKEDLAYOUT_1555
SDL_PACKEDLAYOUT_5551 = _LIB.SDL_PACKEDLAYOUT_5551
SDL_PACKEDLAYOUT_565 = _LIB.SDL_PACKEDLAYOUT_565
SDL_PACKEDLAYOUT_8888 = _LIB.SDL_PACKEDLAYOUT_8888
SDL_PACKEDLAYOUT_2101010 = _LIB.SDL_PACKEDLAYOUT_2101010
SDL_PACKEDLAYOUT_1010102 = _LIB.SDL_PACKEDLAYOUT_1010102

SDL_AUDIO_STOPPED = _LIB.SDL_AUDIO_STOPPED
SDL_AUDIO_PLAYING = _LIB.SDL_AUDIO_PLAYING
SDL_AUDIO_PAUSED = _LIB.SDL_AUDIO_PAUSED

SDL_BLENDMODE_NONE = _LIB.SDL_BLENDMODE_NONE
SDL_BLENDMODE_BLEND = _LIB.SDL_BLENDMODE_BLEND
SDL_BLENDMODE_ADD = _LIB.SDL_BLENDMODE_ADD
SDL_BLENDMODE_MOD = _LIB.SDL_BLENDMODE_MOD

SDL_FIRSTEVENT = _LIB.SDL_FIRSTEVENT
SDL_QUIT = _LIB.SDL_QUIT
SDL_APP_TERMINATING = _LIB.SDL_APP_TERMINATING
SDL_APP_LOWMEMORY = _LIB.SDL_APP_LOWMEMORY
SDL_APP_WILLENTERBACKGROUND = _LIB.SDL_APP_WILLENTERBACKGROUND
SDL_APP_DIDENTERBACKGROUND = _LIB.SDL_APP_DIDENTERBACKGROUND
SDL_APP_WILLENTERFOREGROUND = _LIB.SDL_APP_WILLENTERFOREGROUND
SDL_APP_DIDENTERFOREGROUND = _LIB.SDL_APP_DIDENTERFOREGROUND
SDL_WINDOWEVENT = _LIB.SDL_WINDOWEVENT
SDL_SYSWMEVENT = _LIB.SDL_SYSWMEVENT
SDL_KEYDOWN = _LIB.SDL_KEYDOWN
SDL_KEYUP = _LIB.SDL_KEYUP
SDL_TEXTEDITING = _LIB.SDL_TEXTEDITING
SDL_TEXTINPUT = _LIB.SDL_TEXTINPUT
SDL_MOUSEMOTION = _LIB.SDL_MOUSEMOTION
SDL_MOUSEBUTTONDOWN = _LIB.SDL_MOUSEBUTTONDOWN
SDL_MOUSEBUTTONUP = _LIB.SDL_MOUSEBUTTONUP
SDL_MOUSEWHEEL = _LIB.SDL_MOUSEWHEEL
SDL_JOYAXISMOTION = _LIB.SDL_JOYAXISMOTION
SDL_JOYBALLMOTION = _LIB.SDL_JOYBALLMOTION
SDL_JOYHATMOTION = _LIB.SDL_JOYHATMOTION
SDL_JOYBUTTONDOWN = _LIB.SDL_JOYBUTTONDOWN
SDL_JOYBUTTONUP = _LIB.SDL_JOYBUTTONUP
SDL_JOYDEVICEADDED = _LIB.SDL_JOYDEVICEADDED
SDL_JOYDEVICEREMOVED = _LIB.SDL_JOYDEVICEREMOVED
SDL_CONTROLLERAXISMOTION = _LIB.SDL_CONTROLLERAXISMOTION
SDL_CONTROLLERBUTTONDOWN = _LIB.SDL_CONTROLLERBUTTONDOWN
SDL_CONTROLLERBUTTONUP = _LIB.SDL_CONTROLLERBUTTONUP
SDL_CONTROLLERDEVICEADDED = _LIB.SDL_CONTROLLERDEVICEADDED
SDL_CONTROLLERDEVICEREMOVED = _LIB.SDL_CONTROLLERDEVICEREMOVED
SDL_CONTROLLERDEVICEREMAPPED = _LIB.SDL_CONTROLLERDEVICEREMAPPED
SDL_FINGERDOWN = _LIB.SDL_FINGERDOWN
SDL_FINGERUP = _LIB.SDL_FINGERUP
SDL_FINGERMOTION = _LIB.SDL_FINGERMOTION
SDL_DOLLARGESTURE = _LIB.SDL_DOLLARGESTURE
SDL_DOLLARRECORD = _LIB.SDL_DOLLARRECORD
SDL_MULTIGESTURE = _LIB.SDL_MULTIGESTURE
SDL_CLIPBOARDUPDATE = _LIB.SDL_CLIPBOARDUPDATE
SDL_DROPFILE = _LIB.SDL_DROPFILE
SDL_USEREVENT = _LIB.SDL_USEREVENT
SDL_LASTEVENT = _LIB.SDL_LASTEVENT

SDL_GL_RED_SIZE = _LIB.SDL_GL_RED_SIZE
SDL_GL_GREEN_SIZE = _LIB.SDL_GL_GREEN_SIZE
SDL_GL_BLUE_SIZE = _LIB.SDL_GL_BLUE_SIZE
SDL_GL_ALPHA_SIZE = _LIB.SDL_GL_ALPHA_SIZE
SDL_GL_BUFFER_SIZE = _LIB.SDL_GL_BUFFER_SIZE
SDL_GL_DOUBLEBUFFER = _LIB.SDL_GL_DOUBLEBUFFER
SDL_GL_DEPTH_SIZE = _LIB.SDL_GL_DEPTH_SIZE
SDL_GL_STENCIL_SIZE = _LIB.SDL_GL_STENCIL_SIZE
SDL_GL_ACCUM_RED_SIZE = _LIB.SDL_GL_ACCUM_RED_SIZE
SDL_GL_ACCUM_GREEN_SIZE = _LIB.SDL_GL_ACCUM_GREEN_SIZE
SDL_GL_ACCUM_BLUE_SIZE = _LIB.SDL_GL_ACCUM_BLUE_SIZE
SDL_GL_ACCUM_ALPHA_SIZE = _LIB.SDL_GL_ACCUM_ALPHA_SIZE
SDL_GL_STEREO = _LIB.SDL_GL_STEREO
SDL_GL_MULTISAMPLEBUFFERS = _LIB.SDL_GL_MULTISAMPLEBUFFERS
SDL_GL_MULTISAMPLESAMPLES = _LIB.SDL_GL_MULTISAMPLESAMPLES
SDL_GL_ACCELERATED_VISUAL = _LIB.SDL_GL_ACCELERATED_VISUAL
SDL_GL_RETAINED_BACKING = _LIB.SDL_GL_RETAINED_BACKING
SDL_GL_CONTEXT_MAJOR_VERSION = _LIB.SDL_GL_CONTEXT_MAJOR_VERSION
SDL_GL_CONTEXT_MINOR_VERSION = _LIB.SDL_GL_CONTEXT_MINOR_VERSION
SDL_GL_CONTEXT_EGL = _LIB.SDL_GL_CONTEXT_EGL
SDL_GL_CONTEXT_FLAGS = _LIB.SDL_GL_CONTEXT_FLAGS
SDL_GL_CONTEXT_PROFILE_MASK = _LIB.SDL_GL_CONTEXT_PROFILE_MASK
SDL_GL_SHARE_WITH_CURRENT_CONTEXT = _LIB.SDL_GL_SHARE_WITH_CURRENT_CONTEXT

SDL_GL_CONTEXT_DEBUG_FLAG = _LIB.SDL_GL_CONTEXT_DEBUG_FLAG
SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG = _LIB.SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG
SDL_GL_CONTEXT_ROBUST_ACCESS_FLAG = _LIB.SDL_GL_CONTEXT_ROBUST_ACCESS_FLAG
SDL_GL_CONTEXT_RESET_ISOLATION_FLAG = _LIB.SDL_GL_CONTEXT_RESET_ISOLATION_FLAG

SDL_GL_CONTEXT_PROFILE_CORE = _LIB.SDL_GL_CONTEXT_PROFILE_CORE
SDL_GL_CONTEXT_PROFILE_COMPATIBILITY = _LIB.SDL_GL_CONTEXT_PROFILE_COMPATIBILITY
SDL_GL_CONTEXT_PROFILE_ES = _LIB.SDL_GL_CONTEXT_PROFILE_ES

SDL_CONTROLLER_AXIS_INVALID = _LIB.SDL_CONTROLLER_AXIS_INVALID
SDL_CONTROLLER_AXIS_LEFTX = _LIB.SDL_CONTROLLER_AXIS_LEFTX
SDL_CONTROLLER_AXIS_LEFTY = _LIB.SDL_CONTROLLER_AXIS_LEFTY
SDL_CONTROLLER_AXIS_RIGHTX = _LIB.SDL_CONTROLLER_AXIS_RIGHTX
SDL_CONTROLLER_AXIS_RIGHTY = _LIB.SDL_CONTROLLER_AXIS_RIGHTY
SDL_CONTROLLER_AXIS_TRIGGERLEFT = _LIB.SDL_CONTROLLER_AXIS_TRIGGERLEFT
SDL_CONTROLLER_AXIS_TRIGGERRIGHT = _LIB.SDL_CONTROLLER_AXIS_TRIGGERRIGHT
SDL_CONTROLLER_AXIS_MAX = _LIB.SDL_CONTROLLER_AXIS_MAX

SDL_CONTROLLER_BINDTYPE_NONE = _LIB.SDL_CONTROLLER_BINDTYPE_NONE
SDL_CONTROLLER_BINDTYPE_BUTTON = _LIB.SDL_CONTROLLER_BINDTYPE_BUTTON
SDL_CONTROLLER_BINDTYPE_AXIS = _LIB.SDL_CONTROLLER_BINDTYPE_AXIS
SDL_CONTROLLER_BINDTYPE_HAT = _LIB.SDL_CONTROLLER_BINDTYPE_HAT

SDL_CONTROLLER_BUTTON_INVALID = _LIB.SDL_CONTROLLER_BUTTON_INVALID
SDL_CONTROLLER_BUTTON_A = _LIB.SDL_CONTROLLER_BUTTON_A
SDL_CONTROLLER_BUTTON_B = _LIB.SDL_CONTROLLER_BUTTON_B
SDL_CONTROLLER_BUTTON_X = _LIB.SDL_CONTROLLER_BUTTON_X
SDL_CONTROLLER_BUTTON_Y = _LIB.SDL_CONTROLLER_BUTTON_Y
SDL_CONTROLLER_BUTTON_BACK = _LIB.SDL_CONTROLLER_BUTTON_BACK
SDL_CONTROLLER_BUTTON_GUIDE = _LIB.SDL_CONTROLLER_BUTTON_GUIDE
SDL_CONTROLLER_BUTTON_START = _LIB.SDL_CONTROLLER_BUTTON_START
SDL_CONTROLLER_BUTTON_LEFTSTICK = _LIB.SDL_CONTROLLER_BUTTON_LEFTSTICK
SDL_CONTROLLER_BUTTON_RIGHTSTICK = _LIB.SDL_CONTROLLER_BUTTON_RIGHTSTICK
SDL_CONTROLLER_BUTTON_LEFTSHOULDER = _LIB.SDL_CONTROLLER_BUTTON_LEFTSHOULDER
SDL_CONTROLLER_BUTTON_RIGHTSHOULDER = _LIB.SDL_CONTROLLER_BUTTON_RIGHTSHOULDER
SDL_CONTROLLER_BUTTON_DPAD_UP = _LIB.SDL_CONTROLLER_BUTTON_DPAD_UP
SDL_CONTROLLER_BUTTON_DPAD_DOWN = _LIB.SDL_CONTROLLER_BUTTON_DPAD_DOWN
SDL_CONTROLLER_BUTTON_DPAD_LEFT = _LIB.SDL_CONTROLLER_BUTTON_DPAD_LEFT
SDL_CONTROLLER_BUTTON_DPAD_RIGHT = _LIB.SDL_CONTROLLER_BUTTON_DPAD_RIGHT
SDL_CONTROLLER_BUTTON_MAX = _LIB.SDL_CONTROLLER_BUTTON_MAX

SDL_HINT_DEFAULT = _LIB.SDL_HINT_DEFAULT
SDL_HINT_NORMAL = _LIB.SDL_HINT_NORMAL
SDL_HINT_OVERRIDE = _LIB.SDL_HINT_OVERRIDE

SDL_KMOD_NONE = _LIB.SDL_KMOD_NONE
SDL_KMOD_LSHIFT = _LIB.SDL_KMOD_LSHIFT
SDL_KMOD_RSHIFT = _LIB.SDL_KMOD_RSHIFT
SDL_KMOD_LCTRL = _LIB.SDL_KMOD_LCTRL
SDL_KMOD_RCTRL = _LIB.SDL_KMOD_RCTRL
SDL_KMOD_LALT = _LIB.SDL_KMOD_LALT
SDL_KMOD_RALT = _LIB.SDL_KMOD_RALT
SDL_KMOD_LGUI = _LIB.SDL_KMOD_LGUI
SDL_KMOD_RGUI = _LIB.SDL_KMOD_RGUI
SDL_KMOD_NUM = _LIB.SDL_KMOD_NUM
SDL_KMOD_CAPS = _LIB.SDL_KMOD_CAPS
SDL_KMOD_MODE = _LIB.SDL_KMOD_MODE
SDL_KMOD_RESERVED = _LIB.SDL_KMOD_RESERVED

SDL_LOG_PRIORITY_VERBOSE = _LIB.SDL_LOG_PRIORITY_VERBOSE
SDL_LOG_PRIORITY_DEBUG = _LIB.SDL_LOG_PRIORITY_DEBUG
SDL_LOG_PRIORITY_INFO = _LIB.SDL_LOG_PRIORITY_INFO
SDL_LOG_PRIORITY_WARN = _LIB.SDL_LOG_PRIORITY_WARN
SDL_LOG_PRIORITY_ERROR = _LIB.SDL_LOG_PRIORITY_ERROR
SDL_LOG_PRIORITY_CRITICAL = _LIB.SDL_LOG_PRIORITY_CRITICAL
SDL_NUM_LOG_PRIORITIES = _LIB.SDL_NUM_LOG_PRIORITIES

SDL_MESSAGEBOX_BUTTON_RETURNKEY_DEFAULT = _LIB.SDL_MESSAGEBOX_BUTTON_RETURNKEY_DEFAULT
SDL_MESSAGEBOX_BUTTON_ESCAPEKEY_DEFAULT = _LIB.SDL_MESSAGEBOX_BUTTON_ESCAPEKEY_DEFAULT

SDL_MESSAGEBOX_COLOR_BACKGROUND = _LIB.SDL_MESSAGEBOX_COLOR_BACKGROUND
SDL_MESSAGEBOX_COLOR_TEXT = _LIB.SDL_MESSAGEBOX_COLOR_TEXT
SDL_MESSAGEBOX_COLOR_BUTTON_BORDER = _LIB.SDL_MESSAGEBOX_COLOR_BUTTON_BORDER
SDL_MESSAGEBOX_COLOR_BUTTON_BACKGROUND = _LIB.SDL_MESSAGEBOX_COLOR_BUTTON_BACKGROUND
SDL_MESSAGEBOX_COLOR_BUTTON_SELECTED = _LIB.SDL_MESSAGEBOX_COLOR_BUTTON_SELECTED
SDL_MESSAGEBOX_COLOR_MAX = _LIB.SDL_MESSAGEBOX_COLOR_MAX

SDL_MESSAGEBOX_ERROR = _LIB.SDL_MESSAGEBOX_ERROR
SDL_MESSAGEBOX_WARNING = _LIB.SDL_MESSAGEBOX_WARNING
SDL_MESSAGEBOX_INFORMATION = _LIB.SDL_MESSAGEBOX_INFORMATION

SDL_POWERSTATE_UNKNOWN = _LIB.SDL_POWERSTATE_UNKNOWN
SDL_POWERSTATE_ON_BATTERY = _LIB.SDL_POWERSTATE_ON_BATTERY
SDL_POWERSTATE_NO_BATTERY = _LIB.SDL_POWERSTATE_NO_BATTERY
SDL_POWERSTATE_CHARGING = _LIB.SDL_POWERSTATE_CHARGING
SDL_POWERSTATE_CHARGED = _LIB.SDL_POWERSTATE_CHARGED

SDL_RENDERER_SOFTWARE = _LIB.SDL_RENDERER_SOFTWARE
SDL_RENDERER_ACCELERATED = _LIB.SDL_RENDERER_ACCELERATED
SDL_RENDERER_PRESENTVSYNC = _LIB.SDL_RENDERER_PRESENTVSYNC
SDL_RENDERER_TARGETTEXTURE = _LIB.SDL_RENDERER_TARGETTEXTURE

SDL_FLIP_NONE = _LIB.SDL_FLIP_NONE
SDL_FLIP_HORIZONTAL = _LIB.SDL_FLIP_HORIZONTAL
SDL_FLIP_VERTICAL = _LIB.SDL_FLIP_VERTICAL

SDL_SCANCODE_UNKNOWN = _LIB.SDL_SCANCODE_UNKNOWN
SDL_SCANCODE_A = _LIB.SDL_SCANCODE_A
SDL_SCANCODE_B = _LIB.SDL_SCANCODE_B
SDL_SCANCODE_C = _LIB.SDL_SCANCODE_C
SDL_SCANCODE_D = _LIB.SDL_SCANCODE_D
SDL_SCANCODE_E = _LIB.SDL_SCANCODE_E
SDL_SCANCODE_F = _LIB.SDL_SCANCODE_F
SDL_SCANCODE_G = _LIB.SDL_SCANCODE_G
SDL_SCANCODE_H = _LIB.SDL_SCANCODE_H
SDL_SCANCODE_I = _LIB.SDL_SCANCODE_I
SDL_SCANCODE_J = _LIB.SDL_SCANCODE_J
SDL_SCANCODE_K = _LIB.SDL_SCANCODE_K
SDL_SCANCODE_L = _LIB.SDL_SCANCODE_L
SDL_SCANCODE_M = _LIB.SDL_SCANCODE_M
SDL_SCANCODE_N = _LIB.SDL_SCANCODE_N
SDL_SCANCODE_O = _LIB.SDL_SCANCODE_O
SDL_SCANCODE_P = _LIB.SDL_SCANCODE_P
SDL_SCANCODE_Q = _LIB.SDL_SCANCODE_Q
SDL_SCANCODE_R = _LIB.SDL_SCANCODE_R
SDL_SCANCODE_S = _LIB.SDL_SCANCODE_S
SDL_SCANCODE_T = _LIB.SDL_SCANCODE_T
SDL_SCANCODE_U = _LIB.SDL_SCANCODE_U
SDL_SCANCODE_V = _LIB.SDL_SCANCODE_V
SDL_SCANCODE_W = _LIB.SDL_SCANCODE_W
SDL_SCANCODE_X = _LIB.SDL_SCANCODE_X
SDL_SCANCODE_Y = _LIB.SDL_SCANCODE_Y
SDL_SCANCODE_Z = _LIB.SDL_SCANCODE_Z
SDL_SCANCODE_1 = _LIB.SDL_SCANCODE_1
SDL_SCANCODE_2 = _LIB.SDL_SCANCODE_2
SDL_SCANCODE_3 = _LIB.SDL_SCANCODE_3
SDL_SCANCODE_4 = _LIB.SDL_SCANCODE_4
SDL_SCANCODE_5 = _LIB.SDL_SCANCODE_5
SDL_SCANCODE_6 = _LIB.SDL_SCANCODE_6
SDL_SCANCODE_7 = _LIB.SDL_SCANCODE_7
SDL_SCANCODE_8 = _LIB.SDL_SCANCODE_8
SDL_SCANCODE_9 = _LIB.SDL_SCANCODE_9
SDL_SCANCODE_0 = _LIB.SDL_SCANCODE_0
SDL_SCANCODE_RETURN = _LIB.SDL_SCANCODE_RETURN
SDL_SCANCODE_ESCAPE = _LIB.SDL_SCANCODE_ESCAPE
SDL_SCANCODE_BACKSPACE = _LIB.SDL_SCANCODE_BACKSPACE
SDL_SCANCODE_TAB = _LIB.SDL_SCANCODE_TAB
SDL_SCANCODE_SPACE = _LIB.SDL_SCANCODE_SPACE
SDL_SCANCODE_MINUS = _LIB.SDL_SCANCODE_MINUS
SDL_SCANCODE_EQUALS = _LIB.SDL_SCANCODE_EQUALS
SDL_SCANCODE_LEFTBRACKET = _LIB.SDL_SCANCODE_LEFTBRACKET
SDL_SCANCODE_RIGHTBRACKET = _LIB.SDL_SCANCODE_RIGHTBRACKET
SDL_SCANCODE_BACKSLASH = _LIB.SDL_SCANCODE_BACKSLASH
SDL_SCANCODE_NONUSHASH = _LIB.SDL_SCANCODE_NONUSHASH
SDL_SCANCODE_SEMICOLON = _LIB.SDL_SCANCODE_SEMICOLON
SDL_SCANCODE_APOSTROPHE = _LIB.SDL_SCANCODE_APOSTROPHE
SDL_SCANCODE_GRAVE = _LIB.SDL_SCANCODE_GRAVE
SDL_SCANCODE_COMMA = _LIB.SDL_SCANCODE_COMMA
SDL_SCANCODE_PERIOD = _LIB.SDL_SCANCODE_PERIOD
SDL_SCANCODE_SLASH = _LIB.SDL_SCANCODE_SLASH
SDL_SCANCODE_CAPSLOCK = _LIB.SDL_SCANCODE_CAPSLOCK
SDL_SCANCODE_F1 = _LIB.SDL_SCANCODE_F1
SDL_SCANCODE_F2 = _LIB.SDL_SCANCODE_F2
SDL_SCANCODE_F3 = _LIB.SDL_SCANCODE_F3
SDL_SCANCODE_F4 = _LIB.SDL_SCANCODE_F4
SDL_SCANCODE_F5 = _LIB.SDL_SCANCODE_F5
SDL_SCANCODE_F6 = _LIB.SDL_SCANCODE_F6
SDL_SCANCODE_F7 = _LIB.SDL_SCANCODE_F7
SDL_SCANCODE_F8 = _LIB.SDL_SCANCODE_F8
SDL_SCANCODE_F9 = _LIB.SDL_SCANCODE_F9
SDL_SCANCODE_F10 = _LIB.SDL_SCANCODE_F10
SDL_SCANCODE_F11 = _LIB.SDL_SCANCODE_F11
SDL_SCANCODE_F12 = _LIB.SDL_SCANCODE_F12
SDL_SCANCODE_PRINTSCREEN = _LIB.SDL_SCANCODE_PRINTSCREEN
SDL_SCANCODE_SCROLLLOCK = _LIB.SDL_SCANCODE_SCROLLLOCK
SDL_SCANCODE_PAUSE = _LIB.SDL_SCANCODE_PAUSE
SDL_SCANCODE_INSERT = _LIB.SDL_SCANCODE_INSERT
SDL_SCANCODE_HOME = _LIB.SDL_SCANCODE_HOME
SDL_SCANCODE_PAGEUP = _LIB.SDL_SCANCODE_PAGEUP
SDL_SCANCODE_DELETE = _LIB.SDL_SCANCODE_DELETE
SDL_SCANCODE_END = _LIB.SDL_SCANCODE_END
SDL_SCANCODE_PAGEDOWN = _LIB.SDL_SCANCODE_PAGEDOWN
SDL_SCANCODE_RIGHT = _LIB.SDL_SCANCODE_RIGHT
SDL_SCANCODE_LEFT = _LIB.SDL_SCANCODE_LEFT
SDL_SCANCODE_DOWN = _LIB.SDL_SCANCODE_DOWN
SDL_SCANCODE_UP = _LIB.SDL_SCANCODE_UP
SDL_SCANCODE_NUMLOCKCLEAR = _LIB.SDL_SCANCODE_NUMLOCKCLEAR
SDL_SCANCODE_KP_DIVIDE = _LIB.SDL_SCANCODE_KP_DIVIDE
SDL_SCANCODE_KP_MULTIPLY = _LIB.SDL_SCANCODE_KP_MULTIPLY
SDL_SCANCODE_KP_MINUS = _LIB.SDL_SCANCODE_KP_MINUS
SDL_SCANCODE_KP_PLUS = _LIB.SDL_SCANCODE_KP_PLUS
SDL_SCANCODE_KP_ENTER = _LIB.SDL_SCANCODE_KP_ENTER
SDL_SCANCODE_KP_1 = _LIB.SDL_SCANCODE_KP_1
SDL_SCANCODE_KP_2 = _LIB.SDL_SCANCODE_KP_2
SDL_SCANCODE_KP_3 = _LIB.SDL_SCANCODE_KP_3
SDL_SCANCODE_KP_4 = _LIB.SDL_SCANCODE_KP_4
SDL_SCANCODE_KP_5 = _LIB.SDL_SCANCODE_KP_5
SDL_SCANCODE_KP_6 = _LIB.SDL_SCANCODE_KP_6
SDL_SCANCODE_KP_7 = _LIB.SDL_SCANCODE_KP_7
SDL_SCANCODE_KP_8 = _LIB.SDL_SCANCODE_KP_8
SDL_SCANCODE_KP_9 = _LIB.SDL_SCANCODE_KP_9
SDL_SCANCODE_KP_0 = _LIB.SDL_SCANCODE_KP_0
SDL_SCANCODE_KP_PERIOD = _LIB.SDL_SCANCODE_KP_PERIOD
SDL_SCANCODE_NONUSBACKSLASH = _LIB.SDL_SCANCODE_NONUSBACKSLASH
SDL_SCANCODE_APPLICATION = _LIB.SDL_SCANCODE_APPLICATION
SDL_SCANCODE_POWER = _LIB.SDL_SCANCODE_POWER
SDL_SCANCODE_KP_EQUALS = _LIB.SDL_SCANCODE_KP_EQUALS
SDL_SCANCODE_F13 = _LIB.SDL_SCANCODE_F13
SDL_SCANCODE_F14 = _LIB.SDL_SCANCODE_F14
SDL_SCANCODE_F15 = _LIB.SDL_SCANCODE_F15
SDL_SCANCODE_F16 = _LIB.SDL_SCANCODE_F16
SDL_SCANCODE_F17 = _LIB.SDL_SCANCODE_F17
SDL_SCANCODE_F18 = _LIB.SDL_SCANCODE_F18
SDL_SCANCODE_F19 = _LIB.SDL_SCANCODE_F19
SDL_SCANCODE_F20 = _LIB.SDL_SCANCODE_F20
SDL_SCANCODE_F21 = _LIB.SDL_SCANCODE_F21
SDL_SCANCODE_F22 = _LIB.SDL_SCANCODE_F22
SDL_SCANCODE_F23 = _LIB.SDL_SCANCODE_F23
SDL_SCANCODE_F24 = _LIB.SDL_SCANCODE_F24
SDL_SCANCODE_EXECUTE = _LIB.SDL_SCANCODE_EXECUTE
SDL_SCANCODE_HELP = _LIB.SDL_SCANCODE_HELP
SDL_SCANCODE_MENU = _LIB.SDL_SCANCODE_MENU
SDL_SCANCODE_SELECT = _LIB.SDL_SCANCODE_SELECT
SDL_SCANCODE_STOP = _LIB.SDL_SCANCODE_STOP
SDL_SCANCODE_AGAIN = _LIB.SDL_SCANCODE_AGAIN
SDL_SCANCODE_UNDO = _LIB.SDL_SCANCODE_UNDO
SDL_SCANCODE_CUT = _LIB.SDL_SCANCODE_CUT
SDL_SCANCODE_COPY = _LIB.SDL_SCANCODE_COPY
SDL_SCANCODE_PASTE = _LIB.SDL_SCANCODE_PASTE
SDL_SCANCODE_FIND = _LIB.SDL_SCANCODE_FIND
SDL_SCANCODE_MUTE = _LIB.SDL_SCANCODE_MUTE
SDL_SCANCODE_VOLUMEUP = _LIB.SDL_SCANCODE_VOLUMEUP
SDL_SCANCODE_VOLUMEDOWN = _LIB.SDL_SCANCODE_VOLUMEDOWN
SDL_SCANCODE_KP_COMMA = _LIB.SDL_SCANCODE_KP_COMMA
SDL_SCANCODE_KP_EQUALSAS400 = _LIB.SDL_SCANCODE_KP_EQUALSAS400
SDL_SCANCODE_INTERNATIONAL1 = _LIB.SDL_SCANCODE_INTERNATIONAL1
SDL_SCANCODE_INTERNATIONAL2 = _LIB.SDL_SCANCODE_INTERNATIONAL2
SDL_SCANCODE_INTERNATIONAL3 = _LIB.SDL_SCANCODE_INTERNATIONAL3
SDL_SCANCODE_INTERNATIONAL4 = _LIB.SDL_SCANCODE_INTERNATIONAL4
SDL_SCANCODE_INTERNATIONAL5 = _LIB.SDL_SCANCODE_INTERNATIONAL5
SDL_SCANCODE_INTERNATIONAL6 = _LIB.SDL_SCANCODE_INTERNATIONAL6
SDL_SCANCODE_INTERNATIONAL7 = _LIB.SDL_SCANCODE_INTERNATIONAL7
SDL_SCANCODE_INTERNATIONAL8 = _LIB.SDL_SCANCODE_INTERNATIONAL8
SDL_SCANCODE_INTERNATIONAL9 = _LIB.SDL_SCANCODE_INTERNATIONAL9
SDL_SCANCODE_LANG1 = _LIB.SDL_SCANCODE_LANG1
SDL_SCANCODE_LANG2 = _LIB.SDL_SCANCODE_LANG2
SDL_SCANCODE_LANG3 = _LIB.SDL_SCANCODE_LANG3
SDL_SCANCODE_LANG4 = _LIB.SDL_SCANCODE_LANG4
SDL_SCANCODE_LANG5 = _LIB.SDL_SCANCODE_LANG5
SDL_SCANCODE_LANG6 = _LIB.SDL_SCANCODE_LANG6
SDL_SCANCODE_LANG7 = _LIB.SDL_SCANCODE_LANG7
SDL_SCANCODE_LANG8 = _LIB.SDL_SCANCODE_LANG8
SDL_SCANCODE_LANG9 = _LIB.SDL_SCANCODE_LANG9
SDL_SCANCODE_ALTERASE = _LIB.SDL_SCANCODE_ALTERASE
SDL_SCANCODE_SYSREQ = _LIB.SDL_SCANCODE_SYSREQ
SDL_SCANCODE_CANCEL = _LIB.SDL_SCANCODE_CANCEL
SDL_SCANCODE_CLEAR = _LIB.SDL_SCANCODE_CLEAR
SDL_SCANCODE_PRIOR = _LIB.SDL_SCANCODE_PRIOR
SDL_SCANCODE_RETURN2 = _LIB.SDL_SCANCODE_RETURN2
SDL_SCANCODE_SEPARATOR = _LIB.SDL_SCANCODE_SEPARATOR
SDL_SCANCODE_OUT = _LIB.SDL_SCANCODE_OUT
SDL_SCANCODE_OPER = _LIB.SDL_SCANCODE_OPER
SDL_SCANCODE_CLEARAGAIN = _LIB.SDL_SCANCODE_CLEARAGAIN
SDL_SCANCODE_CRSEL = _LIB.SDL_SCANCODE_CRSEL
SDL_SCANCODE_EXSEL = _LIB.SDL_SCANCODE_EXSEL
SDL_SCANCODE_KP_00 = _LIB.SDL_SCANCODE_KP_00
SDL_SCANCODE_KP_000 = _LIB.SDL_SCANCODE_KP_000
SDL_SCANCODE_THOUSANDSSEPARATOR = _LIB.SDL_SCANCODE_THOUSANDSSEPARATOR
SDL_SCANCODE_DECIMALSEPARATOR = _LIB.SDL_SCANCODE_DECIMALSEPARATOR
SDL_SCANCODE_CURRENCYUNIT = _LIB.SDL_SCANCODE_CURRENCYUNIT
SDL_SCANCODE_CURRENCYSUBUNIT = _LIB.SDL_SCANCODE_CURRENCYSUBUNIT
SDL_SCANCODE_KP_LEFTPAREN = _LIB.SDL_SCANCODE_KP_LEFTPAREN
SDL_SCANCODE_KP_RIGHTPAREN = _LIB.SDL_SCANCODE_KP_RIGHTPAREN
SDL_SCANCODE_KP_LEFTBRACE = _LIB.SDL_SCANCODE_KP_LEFTBRACE
SDL_SCANCODE_KP_RIGHTBRACE = _LIB.SDL_SCANCODE_KP_RIGHTBRACE
SDL_SCANCODE_KP_TAB = _LIB.SDL_SCANCODE_KP_TAB
SDL_SCANCODE_KP_BACKSPACE = _LIB.SDL_SCANCODE_KP_BACKSPACE
SDL_SCANCODE_KP_A = _LIB.SDL_SCANCODE_KP_A
SDL_SCANCODE_KP_B = _LIB.SDL_SCANCODE_KP_B
SDL_SCANCODE_KP_C = _LIB.SDL_SCANCODE_KP_C
SDL_SCANCODE_KP_D = _LIB.SDL_SCANCODE_KP_D
SDL_SCANCODE_KP_E = _LIB.SDL_SCANCODE_KP_E
SDL_SCANCODE_KP_F = _LIB.SDL_SCANCODE_KP_F
SDL_SCANCODE_KP_XOR = _LIB.SDL_SCANCODE_KP_XOR
SDL_SCANCODE_KP_POWER = _LIB.SDL_SCANCODE_KP_POWER
SDL_SCANCODE_KP_PERCENT = _LIB.SDL_SCANCODE_KP_PERCENT
SDL_SCANCODE_KP_LESS = _LIB.SDL_SCANCODE_KP_LESS
SDL_SCANCODE_KP_GREATER = _LIB.SDL_SCANCODE_KP_GREATER
SDL_SCANCODE_KP_AMPERSAND = _LIB.SDL_SCANCODE_KP_AMPERSAND
SDL_SCANCODE_KP_DBLAMPERSAND = _LIB.SDL_SCANCODE_KP_DBLAMPERSAND
SDL_SCANCODE_KP_VERTICALBAR = _LIB.SDL_SCANCODE_KP_VERTICALBAR
SDL_SCANCODE_KP_DBLVERTICALBAR = _LIB.SDL_SCANCODE_KP_DBLVERTICALBAR
SDL_SCANCODE_KP_COLON = _LIB.SDL_SCANCODE_KP_COLON
SDL_SCANCODE_KP_HASH = _LIB.SDL_SCANCODE_KP_HASH
SDL_SCANCODE_KP_SPACE = _LIB.SDL_SCANCODE_KP_SPACE
SDL_SCANCODE_KP_AT = _LIB.SDL_SCANCODE_KP_AT
SDL_SCANCODE_KP_EXCLAM = _LIB.SDL_SCANCODE_KP_EXCLAM
SDL_SCANCODE_KP_MEMSTORE = _LIB.SDL_SCANCODE_KP_MEMSTORE
SDL_SCANCODE_KP_MEMRECALL = _LIB.SDL_SCANCODE_KP_MEMRECALL
SDL_SCANCODE_KP_MEMCLEAR = _LIB.SDL_SCANCODE_KP_MEMCLEAR
SDL_SCANCODE_KP_MEMADD = _LIB.SDL_SCANCODE_KP_MEMADD
SDL_SCANCODE_KP_MEMSUBTRACT = _LIB.SDL_SCANCODE_KP_MEMSUBTRACT
SDL_SCANCODE_KP_MEMMULTIPLY = _LIB.SDL_SCANCODE_KP_MEMMULTIPLY
SDL_SCANCODE_KP_MEMDIVIDE = _LIB.SDL_SCANCODE_KP_MEMDIVIDE
SDL_SCANCODE_KP_PLUSMINUS = _LIB.SDL_SCANCODE_KP_PLUSMINUS
SDL_SCANCODE_KP_CLEAR = _LIB.SDL_SCANCODE_KP_CLEAR
SDL_SCANCODE_KP_CLEARENTRY = _LIB.SDL_SCANCODE_KP_CLEARENTRY
SDL_SCANCODE_KP_BINARY = _LIB.SDL_SCANCODE_KP_BINARY
SDL_SCANCODE_KP_OCTAL = _LIB.SDL_SCANCODE_KP_OCTAL
SDL_SCANCODE_KP_DECIMAL = _LIB.SDL_SCANCODE_KP_DECIMAL
SDL_SCANCODE_KP_HEXADECIMAL = _LIB.SDL_SCANCODE_KP_HEXADECIMAL
SDL_SCANCODE_LCTRL = _LIB.SDL_SCANCODE_LCTRL
SDL_SCANCODE_LSHIFT = _LIB.SDL_SCANCODE_LSHIFT
SDL_SCANCODE_LALT = _LIB.SDL_SCANCODE_LALT
SDL_SCANCODE_LGUI = _LIB.SDL_SCANCODE_LGUI
SDL_SCANCODE_RCTRL = _LIB.SDL_SCANCODE_RCTRL
SDL_SCANCODE_RSHIFT = _LIB.SDL_SCANCODE_RSHIFT
SDL_SCANCODE_RALT = _LIB.SDL_SCANCODE_RALT
SDL_SCANCODE_RGUI = _LIB.SDL_SCANCODE_RGUI
SDL_SCANCODE_MODE = _LIB.SDL_SCANCODE_MODE
SDL_SCANCODE_AUDIONEXT = _LIB.SDL_SCANCODE_AUDIONEXT
SDL_SCANCODE_AUDIOPREV = _LIB.SDL_SCANCODE_AUDIOPREV
SDL_SCANCODE_AUDIOSTOP = _LIB.SDL_SCANCODE_AUDIOSTOP
SDL_SCANCODE_AUDIOPLAY = _LIB.SDL_SCANCODE_AUDIOPLAY
SDL_SCANCODE_AUDIOMUTE = _LIB.SDL_SCANCODE_AUDIOMUTE
SDL_SCANCODE_MEDIASELECT = _LIB.SDL_SCANCODE_MEDIASELECT
SDL_SCANCODE_WWW = _LIB.SDL_SCANCODE_WWW
SDL_SCANCODE_MAIL = _LIB.SDL_SCANCODE_MAIL
SDL_SCANCODE_CALCULATOR = _LIB.SDL_SCANCODE_CALCULATOR
SDL_SCANCODE_COMPUTER = _LIB.SDL_SCANCODE_COMPUTER
SDL_SCANCODE_AC_SEARCH = _LIB.SDL_SCANCODE_AC_SEARCH
SDL_SCANCODE_AC_HOME = _LIB.SDL_SCANCODE_AC_HOME
SDL_SCANCODE_AC_BACK = _LIB.SDL_SCANCODE_AC_BACK
SDL_SCANCODE_AC_FORWARD = _LIB.SDL_SCANCODE_AC_FORWARD
SDL_SCANCODE_AC_STOP = _LIB.SDL_SCANCODE_AC_STOP
SDL_SCANCODE_AC_REFRESH = _LIB.SDL_SCANCODE_AC_REFRESH
SDL_SCANCODE_AC_BOOKMARKS = _LIB.SDL_SCANCODE_AC_BOOKMARKS
SDL_SCANCODE_BRIGHTNESSDOWN = _LIB.SDL_SCANCODE_BRIGHTNESSDOWN
SDL_SCANCODE_BRIGHTNESSUP = _LIB.SDL_SCANCODE_BRIGHTNESSUP
SDL_SCANCODE_DISPLAYSWITCH = _LIB.SDL_SCANCODE_DISPLAYSWITCH
SDL_SCANCODE_KBDILLUMTOGGLE = _LIB.SDL_SCANCODE_KBDILLUMTOGGLE
SDL_SCANCODE_KBDILLUMDOWN = _LIB.SDL_SCANCODE_KBDILLUMDOWN
SDL_SCANCODE_KBDILLUMUP = _LIB.SDL_SCANCODE_KBDILLUMUP
SDL_SCANCODE_EJECT = _LIB.SDL_SCANCODE_EJECT
SDL_SCANCODE_SLEEP = _LIB.SDL_SCANCODE_SLEEP
SDL_SCANCODE_APP1 = _LIB.SDL_SCANCODE_APP1
SDL_SCANCODE_APP2 = _LIB.SDL_SCANCODE_APP2
SDL_NUM_SCANCODES = _LIB.SDL_NUM_SCANCODES

SDL_SYSTEM_CURSOR_ARROW = _LIB.SDL_SYSTEM_CURSOR_ARROW
SDL_SYSTEM_CURSOR_IBEAM = _LIB.SDL_SYSTEM_CURSOR_IBEAM
SDL_SYSTEM_CURSOR_WAIT = _LIB.SDL_SYSTEM_CURSOR_WAIT
SDL_SYSTEM_CURSOR_CROSSHAIR = _LIB.SDL_SYSTEM_CURSOR_CROSSHAIR
SDL_SYSTEM_CURSOR_WAITARROW = _LIB.SDL_SYSTEM_CURSOR_WAITARROW
SDL_SYSTEM_CURSOR_SIZENWSE = _LIB.SDL_SYSTEM_CURSOR_SIZENWSE
SDL_SYSTEM_CURSOR_SIZENESW = _LIB.SDL_SYSTEM_CURSOR_SIZENESW
SDL_SYSTEM_CURSOR_SIZEWE = _LIB.SDL_SYSTEM_CURSOR_SIZEWE
SDL_SYSTEM_CURSOR_SIZENS = _LIB.SDL_SYSTEM_CURSOR_SIZENS
SDL_SYSTEM_CURSOR_SIZEALL = _LIB.SDL_SYSTEM_CURSOR_SIZEALL
SDL_SYSTEM_CURSOR_NO = _LIB.SDL_SYSTEM_CURSOR_NO
SDL_SYSTEM_CURSOR_HAND = _LIB.SDL_SYSTEM_CURSOR_HAND
SDL_NUM_SYSTEM_CURSORS = _LIB.SDL_NUM_SYSTEM_CURSORS

SDL_TEXTUREACCESS_STATIC = _LIB.SDL_TEXTUREACCESS_STATIC
SDL_TEXTUREACCESS_STREAMING = _LIB.SDL_TEXTUREACCESS_STREAMING
SDL_TEXTUREACCESS_TARGET = _LIB.SDL_TEXTUREACCESS_TARGET

SDL_TEXTUREMODULATE_NONE = _LIB.SDL_TEXTUREMODULATE_NONE
SDL_TEXTUREMODULATE_COLOR = _LIB.SDL_TEXTUREMODULATE_COLOR
SDL_TEXTUREMODULATE_ALPHA = _LIB.SDL_TEXTUREMODULATE_ALPHA

SDL_THREAD_PRIORITY_LOW = _LIB.SDL_THREAD_PRIORITY_LOW
SDL_THREAD_PRIORITY_NORMAL = _LIB.SDL_THREAD_PRIORITY_NORMAL
SDL_THREAD_PRIORITY_HIGH = _LIB.SDL_THREAD_PRIORITY_HIGH

SDL_WINDOWEVENT_NONE = _LIB.SDL_WINDOWEVENT_NONE
SDL_WINDOWEVENT_SHOWN = _LIB.SDL_WINDOWEVENT_SHOWN
SDL_WINDOWEVENT_HIDDEN = _LIB.SDL_WINDOWEVENT_HIDDEN
SDL_WINDOWEVENT_EXPOSED = _LIB.SDL_WINDOWEVENT_EXPOSED
SDL_WINDOWEVENT_MOVED = _LIB.SDL_WINDOWEVENT_MOVED
SDL_WINDOWEVENT_RESIZED = _LIB.SDL_WINDOWEVENT_RESIZED
SDL_WINDOWEVENT_SIZE_CHANGED = _LIB.SDL_WINDOWEVENT_SIZE_CHANGED
SDL_WINDOWEVENT_MINIMIZED = _LIB.SDL_WINDOWEVENT_MINIMIZED
SDL_WINDOWEVENT_MAXIMIZED = _LIB.SDL_WINDOWEVENT_MAXIMIZED
SDL_WINDOWEVENT_RESTORED = _LIB.SDL_WINDOWEVENT_RESTORED
SDL_WINDOWEVENT_ENTER = _LIB.SDL_WINDOWEVENT_ENTER
SDL_WINDOWEVENT_LEAVE = _LIB.SDL_WINDOWEVENT_LEAVE
SDL_WINDOWEVENT_FOCUS_GAINED = _LIB.SDL_WINDOWEVENT_FOCUS_GAINED
SDL_WINDOWEVENT_FOCUS_LOST = _LIB.SDL_WINDOWEVENT_FOCUS_LOST
SDL_WINDOWEVENT_CLOSE = _LIB.SDL_WINDOWEVENT_CLOSE

SDL_WINDOW_FULLSCREEN = _LIB.SDL_WINDOW_FULLSCREEN
SDL_WINDOW_OPENGL = _LIB.SDL_WINDOW_OPENGL
SDL_WINDOW_SHOWN = _LIB.SDL_WINDOW_SHOWN
SDL_WINDOW_HIDDEN = _LIB.SDL_WINDOW_HIDDEN
SDL_WINDOW_BORDERLESS = _LIB.SDL_WINDOW_BORDERLESS
SDL_WINDOW_RESIZABLE = _LIB.SDL_WINDOW_RESIZABLE
SDL_WINDOW_MINIMIZED = _LIB.SDL_WINDOW_MINIMIZED
SDL_WINDOW_MAXIMIZED = _LIB.SDL_WINDOW_MAXIMIZED
SDL_WINDOW_INPUT_GRABBED = _LIB.SDL_WINDOW_INPUT_GRABBED
SDL_WINDOW_INPUT_FOCUS = _LIB.SDL_WINDOW_INPUT_FOCUS
SDL_WINDOW_MOUSE_FOCUS = _LIB.SDL_WINDOW_MOUSE_FOCUS
SDL_WINDOW_FOREIGN = _LIB.SDL_WINDOW_FOREIGN

SDL_ASSERTION_RETRY = _LIB.SDL_ASSERTION_RETRY
SDL_ASSERTION_BREAK = _LIB.SDL_ASSERTION_BREAK
SDL_ASSERTION_ABORT = _LIB.SDL_ASSERTION_ABORT
SDL_ASSERTION_IGNORE = _LIB.SDL_ASSERTION_IGNORE
SDL_ASSERTION_ALWAYS_IGNORE = _LIB.SDL_ASSERTION_ALWAYS_IGNORE

SDL_FALSE = _LIB.SDL_FALSE
SDL_TRUE = _LIB.SDL_TRUE

SDL_ENOMEM = _LIB.SDL_ENOMEM
SDL_EFREAD = _LIB.SDL_EFREAD
SDL_EFWRITE = _LIB.SDL_EFWRITE
SDL_EFSEEK = _LIB.SDL_EFSEEK
SDL_UNSUPPORTED = _LIB.SDL_UNSUPPORTED
SDL_LASTERROR = _LIB.SDL_LASTERROR

SDL_ADDEVENT = _LIB.SDL_ADDEVENT
SDL_PEEKEVENT = _LIB.SDL_PEEKEVENT
SDL_GETEVENT = _LIB.SDL_GETEVENT

class FILE(Struct):
    """Wrap `FILE`"""
    rWFromFP = SDL_RWFromFP

class SDL_AudioCVT(Struct):
    """Wrap `SDL_AudioCVT`"""
    buildAudioCVT = SDL_BuildAudioCVT
    convertAudio = SDL_ConvertAudio

class SDL_AudioSpec(Struct):
    """Wrap `SDL_AudioSpec`"""
    openAudio = SDL_OpenAudio

class SDL_Color(Struct):
    """Wrap `SDL_Color`"""
    pass

class SDL_CommonEvent(Struct):
    """Wrap `SDL_CommonEvent`"""
    pass

class SDL_ControllerAxisEvent(Struct):
    """Wrap `SDL_ControllerAxisEvent`"""
    pass

class SDL_ControllerButtonEvent(Struct):
    """Wrap `SDL_ControllerButtonEvent`"""
    pass

class SDL_ControllerDeviceEvent(Struct):
    """Wrap `SDL_ControllerDeviceEvent`"""
    pass

class SDL_Cursor(Struct):
    """Wrap `SDL_Cursor`"""
    freeCursor = SDL_FreeCursor
    setCursor = SDL_SetCursor

class SDL_DisplayMode(Struct):
    """Wrap `SDL_DisplayMode`"""
    pass

class SDL_DollarGestureEvent(Struct):
    """Wrap `SDL_DollarGestureEvent`"""
    pass

class SDL_DropEvent(Struct):
    """Wrap `SDL_DropEvent`"""
    pass

class SDL_Event(Struct):
    """Wrap `SDL_Event`"""
    peepEvents = SDL_PeepEvents
    pollEvent = SDL_PollEvent
    pushEvent = SDL_PushEvent
    waitEvent = SDL_WaitEvent
    waitEventTimeout = SDL_WaitEventTimeout

class SDL_Finger(Struct):
    """Wrap `SDL_Finger`"""
    pass

class SDL_GameController(Struct):
    """Wrap `SDL_GameController`"""
    gameControllerClose = SDL_GameControllerClose
    gameControllerGetAttached = SDL_GameControllerGetAttached
    gameControllerGetAxis = SDL_GameControllerGetAxis
    gameControllerGetBindForAxis = SDL_GameControllerGetBindForAxis
    gameControllerGetBindForButton = SDL_GameControllerGetBindForButton
    gameControllerGetButton = SDL_GameControllerGetButton
    gameControllerGetJoystick = SDL_GameControllerGetJoystick
    gameControllerMapping = SDL_GameControllerMapping
    gameControllerName = SDL_GameControllerName

class SDL_GameControllerButtonBind(Struct):
    """Wrap `SDL_GameControllerButtonBind`"""
    pass

class SDL_Haptic(Struct):
    """Wrap `SDL_Haptic`"""
    hapticClose = SDL_HapticClose
    hapticDestroyEffect = SDL_HapticDestroyEffect
    hapticEffectSupported = SDL_HapticEffectSupported
    hapticGetEffectStatus = SDL_HapticGetEffectStatus
    hapticIndex = SDL_HapticIndex
    hapticNewEffect = SDL_HapticNewEffect
    hapticNumAxes = SDL_HapticNumAxes
    hapticNumEffects = SDL_HapticNumEffects
    hapticNumEffectsPlaying = SDL_HapticNumEffectsPlaying
    hapticPause = SDL_HapticPause
    hapticQuery = SDL_HapticQuery
    hapticRumbleInit = SDL_HapticRumbleInit
    hapticRumblePlay = SDL_HapticRumblePlay
    hapticRumbleStop = SDL_HapticRumbleStop
    hapticRumbleSupported = SDL_HapticRumbleSupported
    hapticRunEffect = SDL_HapticRunEffect
    hapticSetAutocenter = SDL_HapticSetAutocenter
    hapticSetGain = SDL_HapticSetGain
    hapticStopAll = SDL_HapticStopAll
    hapticStopEffect = SDL_HapticStopEffect
    hapticUnpause = SDL_HapticUnpause
    hapticUpdateEffect = SDL_HapticUpdateEffect

class SDL_HapticCondition(Struct):
    """Wrap `SDL_HapticCondition`"""
    pass

class SDL_HapticConstant(Struct):
    """Wrap `SDL_HapticConstant`"""
    pass

class SDL_HapticCustom(Struct):
    """Wrap `SDL_HapticCustom`"""
    pass

class SDL_HapticDirection(Struct):
    """Wrap `SDL_HapticDirection`"""
    pass

class SDL_HapticEffect(Struct):
    """Wrap `SDL_HapticEffect`"""
    pass

class SDL_HapticLeftRight(Struct):
    """Wrap `SDL_HapticLeftRight`"""
    pass

class SDL_HapticPeriodic(Struct):
    """Wrap `SDL_HapticPeriodic`"""
    pass

class SDL_HapticRamp(Struct):
    """Wrap `SDL_HapticRamp`"""
    pass

class SDL_JoyAxisEvent(Struct):
    """Wrap `SDL_JoyAxisEvent`"""
    pass

class SDL_JoyBallEvent(Struct):
    """Wrap `SDL_JoyBallEvent`"""
    pass

class SDL_JoyButtonEvent(Struct):
    """Wrap `SDL_JoyButtonEvent`"""
    pass

class SDL_JoyDeviceEvent(Struct):
    """Wrap `SDL_JoyDeviceEvent`"""
    pass

class SDL_JoyHatEvent(Struct):
    """Wrap `SDL_JoyHatEvent`"""
    pass

class SDL_Joystick(Struct):
    """Wrap `SDL_Joystick`"""
    hapticOpenFromJoystick = SDL_HapticOpenFromJoystick
    joystickClose = SDL_JoystickClose
    joystickGetAttached = SDL_JoystickGetAttached
    joystickGetAxis = SDL_JoystickGetAxis
    joystickGetBall = SDL_JoystickGetBall
    joystickGetButton = SDL_JoystickGetButton
    joystickGetGUID = SDL_JoystickGetGUID
    joystickGetHat = SDL_JoystickGetHat
    joystickInstanceID = SDL_JoystickInstanceID
    joystickIsHaptic = SDL_JoystickIsHaptic
    joystickName = SDL_JoystickName
    joystickNumAxes = SDL_JoystickNumAxes
    joystickNumBalls = SDL_JoystickNumBalls
    joystickNumButtons = SDL_JoystickNumButtons
    joystickNumHats = SDL_JoystickNumHats

class SDL_JoystickGUID(Struct):
    """Wrap `SDL_JoystickGUID`"""
    pass

class SDL_KeyboardEvent(Struct):
    """Wrap `SDL_KeyboardEvent`"""
    pass

class SDL_Keysym(Struct):
    """Wrap `SDL_Keysym`"""
    pass

class SDL_MessageBoxButtonData(Struct):
    """Wrap `SDL_MessageBoxButtonData`"""
    pass

class SDL_MessageBoxColor(Struct):
    """Wrap `SDL_MessageBoxColor`"""
    pass

class SDL_MessageBoxColorScheme(Struct):
    """Wrap `SDL_MessageBoxColorScheme`"""
    pass

class SDL_MessageBoxData(Struct):
    """Wrap `SDL_MessageBoxData`"""
    showMessageBox = SDL_ShowMessageBox

class SDL_MouseButtonEvent(Struct):
    """Wrap `SDL_MouseButtonEvent`"""
    pass

class SDL_MouseMotionEvent(Struct):
    """Wrap `SDL_MouseMotionEvent`"""
    pass

class SDL_MouseWheelEvent(Struct):
    """Wrap `SDL_MouseWheelEvent`"""
    pass

class SDL_MultiGestureEvent(Struct):
    """Wrap `SDL_MultiGestureEvent`"""
    pass

class SDL_OSEvent(Struct):
    """Wrap `SDL_OSEvent`"""
    pass

class SDL_Palette(Struct):
    """Wrap `SDL_Palette`"""
    freePalette = SDL_FreePalette
    setPaletteColors = SDL_SetPaletteColors

class SDL_PixelFormat(Struct):
    """Wrap `SDL_PixelFormat`"""
    freeFormat = SDL_FreeFormat
    mapRGB = SDL_MapRGB
    mapRGBA = SDL_MapRGBA
    setPixelFormatPalette = SDL_SetPixelFormatPalette

class SDL_Point(Struct):
    """Wrap `SDL_Point`"""
    enclosePoints = SDL_EnclosePoints

class SDL_QuitEvent(Struct):
    """Wrap `SDL_QuitEvent`"""
    pass

class SDL_RWops(Struct):
    """Wrap `SDL_RWops`"""
    freeRW = SDL_FreeRW
    loadBMP_RW = SDL_LoadBMP_RW
    loadWAV_RW = SDL_LoadWAV_RW
    readBE16 = SDL_ReadBE16
    readBE32 = SDL_ReadBE32
    readBE64 = SDL_ReadBE64
    readLE16 = SDL_ReadLE16
    readLE32 = SDL_ReadLE32
    readLE64 = SDL_ReadLE64
    readU8 = SDL_ReadU8
    saveAllDollarTemplates = SDL_SaveAllDollarTemplates
    writeBE16 = SDL_WriteBE16
    writeBE32 = SDL_WriteBE32
    writeBE64 = SDL_WriteBE64
    writeLE16 = SDL_WriteLE16
    writeLE32 = SDL_WriteLE32
    writeLE64 = SDL_WriteLE64
    writeU8 = SDL_WriteU8

class SDL_Rect(Struct):
    """Wrap `SDL_Rect`"""
    hasIntersection = SDL_HasIntersection
    intersectRect = SDL_IntersectRect
    intersectRectAndLine = SDL_IntersectRectAndLine
    setTextInputRect = SDL_SetTextInputRect
    unionRect = SDL_UnionRect

class SDL_Renderer(Struct):
    """Wrap `SDL_Renderer`"""
    createTexture = SDL_CreateTexture
    createTextureFromSurface = SDL_CreateTextureFromSurface
    destroyRenderer = SDL_DestroyRenderer
    getRenderDrawBlendMode = SDL_GetRenderDrawBlendMode
    getRenderDrawColor = SDL_GetRenderDrawColor
    getRenderTarget = SDL_GetRenderTarget
    getRendererInfo = SDL_GetRendererInfo
    getRendererOutputSize = SDL_GetRendererOutputSize
    renderClear = SDL_RenderClear
    renderCopy = SDL_RenderCopy
    renderCopyEx = SDL_RenderCopyEx
    renderDrawLine = SDL_RenderDrawLine
    renderDrawLines = SDL_RenderDrawLines
    renderDrawPoint = SDL_RenderDrawPoint
    renderDrawPoints = SDL_RenderDrawPoints
    renderDrawRect = SDL_RenderDrawRect
    renderDrawRects = SDL_RenderDrawRects
    renderFillRect = SDL_RenderFillRect
    renderFillRects = SDL_RenderFillRects
    renderGetClipRect = SDL_RenderGetClipRect
    renderGetLogicalSize = SDL_RenderGetLogicalSize
    renderGetScale = SDL_RenderGetScale
    renderGetViewport = SDL_RenderGetViewport
    renderPresent = SDL_RenderPresent
    renderReadPixels = SDL_RenderReadPixels
    renderSetClipRect = SDL_RenderSetClipRect
    renderSetLogicalSize = SDL_RenderSetLogicalSize
    renderSetScale = SDL_RenderSetScale
    renderSetViewport = SDL_RenderSetViewport
    renderTargetSupported = SDL_RenderTargetSupported
    setRenderDrawBlendMode = SDL_SetRenderDrawBlendMode
    setRenderDrawColor = SDL_SetRenderDrawColor
    setRenderTarget = SDL_SetRenderTarget

class SDL_RendererInfo(Struct):
    """Wrap `SDL_RendererInfo`"""
    pass

class SDL_Surface(Struct):
    """Wrap `SDL_Surface`"""
    convertSurface = SDL_ConvertSurface
    convertSurfaceFormat = SDL_ConvertSurfaceFormat
    createColorCursor = SDL_CreateColorCursor
    createSoftwareRenderer = SDL_CreateSoftwareRenderer
    fillRect = SDL_FillRect
    fillRects = SDL_FillRects
    freeSurface = SDL_FreeSurface
    getClipRect = SDL_GetClipRect
    getColorKey = SDL_GetColorKey
    getSurfaceAlphaMod = SDL_GetSurfaceAlphaMod
    getSurfaceBlendMode = SDL_GetSurfaceBlendMode
    getSurfaceColorMod = SDL_GetSurfaceColorMod
    lockSurface = SDL_LockSurface
    lowerBlit = SDL_LowerBlit
    lowerBlitScaled = SDL_LowerBlitScaled
    saveBMP_RW = SDL_SaveBMP_RW
    setClipRect = SDL_SetClipRect
    setColorKey = SDL_SetColorKey
    setSurfaceAlphaMod = SDL_SetSurfaceAlphaMod
    setSurfaceBlendMode = SDL_SetSurfaceBlendMode
    setSurfaceColorMod = SDL_SetSurfaceColorMod
    setSurfacePalette = SDL_SetSurfacePalette
    setSurfaceRLE = SDL_SetSurfaceRLE
    softStretch = SDL_SoftStretch
    unlockSurface = SDL_UnlockSurface
    upperBlit = SDL_UpperBlit
    upperBlitScaled = SDL_UpperBlitScaled

class SDL_SysWMEvent(Struct):
    """Wrap `SDL_SysWMEvent`"""
    pass

class SDL_SysWMmsg(Struct):
    """Wrap `SDL_SysWMmsg`"""
    pass

class SDL_TextEditingEvent(Struct):
    """Wrap `SDL_TextEditingEvent`"""
    pass

class SDL_TextInputEvent(Struct):
    """Wrap `SDL_TextInputEvent`"""
    pass

class SDL_Texture(Struct):
    """Wrap `SDL_Texture`"""
    destroyTexture = SDL_DestroyTexture
    gL_BindTexture = SDL_GL_BindTexture
    gL_UnbindTexture = SDL_GL_UnbindTexture
    getTextureAlphaMod = SDL_GetTextureAlphaMod
    getTextureBlendMode = SDL_GetTextureBlendMode
    getTextureColorMod = SDL_GetTextureColorMod
    lockTexture = SDL_LockTexture
    queryTexture = SDL_QueryTexture
    setTextureAlphaMod = SDL_SetTextureAlphaMod
    setTextureBlendMode = SDL_SetTextureBlendMode
    setTextureColorMod = SDL_SetTextureColorMod
    unlockTexture = SDL_UnlockTexture
    updateTexture = SDL_UpdateTexture

class SDL_Thread(Struct):
    """Wrap `SDL_Thread`"""
    getThreadID = SDL_GetThreadID
    getThreadName = SDL_GetThreadName
    waitThread = SDL_WaitThread

class SDL_TouchFingerEvent(Struct):
    """Wrap `SDL_TouchFingerEvent`"""
    pass

class SDL_UserEvent(Struct):
    """Wrap `SDL_UserEvent`"""
    pass

class SDL_Window(Struct):
    """Wrap `SDL_Window`"""
    createRenderer = SDL_CreateRenderer
    destroyWindow = SDL_DestroyWindow
    gL_CreateContext = SDL_GL_CreateContext
    gL_MakeCurrent = SDL_GL_MakeCurrent
    gL_SwapWindow = SDL_GL_SwapWindow
    getRenderer = SDL_GetRenderer
    getWindowBrightness = SDL_GetWindowBrightness
    getWindowData = SDL_GetWindowData
    getWindowDisplayIndex = SDL_GetWindowDisplayIndex
    getWindowDisplayMode = SDL_GetWindowDisplayMode
    getWindowFlags = SDL_GetWindowFlags
    getWindowGammaRamp = SDL_GetWindowGammaRamp
    getWindowGrab = SDL_GetWindowGrab
    getWindowID = SDL_GetWindowID
    getWindowMaximumSize = SDL_GetWindowMaximumSize
    getWindowMinimumSize = SDL_GetWindowMinimumSize
    getWindowPixelFormat = SDL_GetWindowPixelFormat
    getWindowPosition = SDL_GetWindowPosition
    getWindowSize = SDL_GetWindowSize
    getWindowSurface = SDL_GetWindowSurface
    getWindowTitle = SDL_GetWindowTitle
    hideWindow = SDL_HideWindow
    isScreenKeyboardShown = SDL_IsScreenKeyboardShown
    maximizeWindow = SDL_MaximizeWindow
    minimizeWindow = SDL_MinimizeWindow
    raiseWindow = SDL_RaiseWindow
    restoreWindow = SDL_RestoreWindow
    setWindowBordered = SDL_SetWindowBordered
    setWindowBrightness = SDL_SetWindowBrightness
    setWindowData = SDL_SetWindowData
    setWindowDisplayMode = SDL_SetWindowDisplayMode
    setWindowFullscreen = SDL_SetWindowFullscreen
    setWindowGammaRamp = SDL_SetWindowGammaRamp
    setWindowGrab = SDL_SetWindowGrab
    setWindowIcon = SDL_SetWindowIcon
    setWindowMaximumSize = SDL_SetWindowMaximumSize
    setWindowMinimumSize = SDL_SetWindowMinimumSize
    setWindowPosition = SDL_SetWindowPosition
    setWindowSize = SDL_SetWindowSize
    setWindowTitle = SDL_SetWindowTitle
    showWindow = SDL_ShowWindow
    updateWindowSurface = SDL_UpdateWindowSurface
    updateWindowSurfaceRects = SDL_UpdateWindowSurfaceRects
    warpMouseInWindow = SDL_WarpMouseInWindow

class SDL_WindowEvent(Struct):
    """Wrap `SDL_WindowEvent`"""
    pass

class SDL_assert_data(Struct):
    """Wrap `SDL_assert_data`"""
    reportAssertion = SDL_ReportAssertion

class SDL_atomic_t(Struct):
    """Wrap `SDL_atomic_t`"""
    pass

class SDL_cond(Struct):
    """Wrap `SDL_cond`"""
    condBroadcast = SDL_CondBroadcast
    condSignal = SDL_CondSignal
    condWait = SDL_CondWait
    condWaitTimeout = SDL_CondWaitTimeout
    destroyCond = SDL_DestroyCond

class SDL_mutex(Struct):
    """Wrap `SDL_mutex`"""
    destroyMutex = SDL_DestroyMutex
    lockMutex = SDL_LockMutex
    tryLockMutex = SDL_TryLockMutex
    unlockMutex = SDL_UnlockMutex

class SDL_sem(Struct):
    """Wrap `SDL_sem`"""
    destroySemaphore = SDL_DestroySemaphore
    semPost = SDL_SemPost
    semTryWait = SDL_SemTryWait
    semValue = SDL_SemValue
    semWait = SDL_SemWait
    semWaitTimeout = SDL_SemWaitTimeout

class SDL_version(Struct):
    """Wrap `SDL_version`"""
    getVersion = SDL_GetVersion

