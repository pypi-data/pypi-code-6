# Automatically generated wrappers.
# Override by adding wrappers to helpers.py.
from .dso import ffi, _LIB
from .structs import Struct, unbox, SDLError, u8

def SDL_AddEventWatch(filter, userdata):
    """
    ``void SDL_AddEventWatch(int SDL_AddEventWatch(void *, SDL_Event *), void *)``
    
    Add a function which is called when an event is added to the queue.
    """
    filter_c = unbox(filter, 'int(*)(void *, SDL_Event *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_AddEventWatch(filter_c, userdata_c)

def SDL_AddHintCallback(name, callback, userdata):
    """
    ``void SDL_AddHintCallback(char const *, void SDL_AddHintCallback(void *, char const *, char const *, char const *), void *)``
    """
    name_c = u8(name)
    callback_c = unbox(callback, 'void(*)(void *, char const *, char const *, char const *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_AddHintCallback(name_c, callback_c, userdata_c)

def SDL_AddTimer(interval, callback, param):
    """
    ``int SDL_AddTimer(uint32_t, uint32_t SDL_AddTimer(uint32_t, void *), void *)``
    
    Add a new timer to the pool of timers already running.
    
    :return: A timer ID, or NULL when an error occurs.
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
    
    Create an SDL_PixelFormat structure from a pixel format enum.
    """
    pixel_format_c = pixel_format
    rc = _LIB.SDL_AllocFormat(pixel_format_c)
    return SDL_PixelFormat(rc)

def SDL_AllocPalette(ncolors):
    """
    ``SDL_Palette * SDL_AllocPalette(int)``
    
    Create a palette structure with the specified number of color entries.
    
    :return: A new palette, or NULL if there wasn't enough memory.
    
    The palette entries are initialized to white.
    
    See also SDL_FreePalette()
    """
    ncolors_c = ncolors
    rc = _LIB.SDL_AllocPalette(ncolors_c)
    return SDL_Palette(rc)

def SDL_AllocRW():
    """
    ``SDL_RWops * SDL_AllocRW(void)``
    """
    rc = _LIB.SDL_AllocRW()
    return SDL_RWops(rc)

def SDL_AtomicLock(lock=None):
    """
    ``void SDL_AtomicLock(int *)``
    
    Lock a spin lock by setting it to a non-zero value.
    
    :param lock: Points to the lock.
    """
    lock_c = unbox(lock, 'int *')
    _LIB.SDL_AtomicLock(lock_c)
    return lock_c[0]

def SDL_AtomicTryLock(lock=None):
    """
    ``SDL_bool SDL_AtomicTryLock(int *)``
    
    Try to lock a spin lock by setting it to a non-zero value.
    
    :param lock: Points to the lock.
    :return: SDL_TRUE if the lock succeeded, SDL_FALSE if the lock is
        already held.
    """
    lock_c = unbox(lock, 'int *')
    rc = _LIB.SDL_AtomicTryLock(lock_c)
    return (rc, lock_c[0])

def SDL_AtomicUnlock(lock=None):
    """
    ``void SDL_AtomicUnlock(int *)``
    
    Unlock a spin lock by setting it to 0. Always returns immediately.
    
    :param lock: Points to the lock.
    """
    lock_c = unbox(lock, 'int *')
    _LIB.SDL_AtomicUnlock(lock_c)
    return lock_c[0]

def SDL_AudioInit(driver_name):
    """
    ``int SDL_AudioInit(char const *)``
    """
    driver_name_c = u8(driver_name)
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
    
    This function takes a source format and rate and a destination format
    and rate, and initializes the cvt structure with information needed by
    SDL_ConvertAudio() to convert a buffer of audio data from one format
    to the other.
    
    :return: -1 if the format conversion is not supported, 0 if there's no
        conversion needed, or 1 if the audio filter is set up.
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
    
    Calculate a 256 entry gamma ramp for a gamma value.
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
    
    Clear all hints.
    
    This function is called during SDL_Quit() to free stored hints.
    """
    _LIB.SDL_ClearHints()

def SDL_CloseAudio():
    """
    ``void SDL_CloseAudio(void)``
    
    This function shuts down audio processing and closes the audio device.
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
    
    Restart all threads that are waiting on the condition variable.
    
    :return: 0 or -1 on error.
    """
    cond_c = unbox(cond, 'SDL_cond *')
    rc = _LIB.SDL_CondBroadcast(cond_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_CondSignal(cond):
    """
    ``int SDL_CondSignal(SDL_cond *)``
    
    Restart one of the threads that are waiting on the condition variable.
    
    :return: 0 or -1 on error.
    """
    cond_c = unbox(cond, 'SDL_cond *')
    rc = _LIB.SDL_CondSignal(cond_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_CondWait(cond, mutex):
    """
    ``int SDL_CondWait(SDL_cond *, SDL_mutex *)``
    
    Wait on the condition variable, unlocking the provided mutex.
    
    The mutex must be locked before entering this function!
    
    The mutex is re-locked once the condition variable is signaled.
    
    :return: 0 when it is signaled, or -1 on error.
    """
    cond_c = unbox(cond, 'SDL_cond *')
    mutex_c = unbox(mutex, 'SDL_mutex *')
    rc = _LIB.SDL_CondWait(cond_c, mutex_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_CondWaitTimeout(cond, mutex, ms):
    """
    ``int SDL_CondWaitTimeout(SDL_cond *, SDL_mutex *, uint32_t)``
    
    Waits for at most ms milliseconds, and returns 0 if the condition
    variable is signaled, SDL_MUTEX_TIMEDOUT if the condition is not
    signaled in the allotted time, and -1 on error.
    
    On some platforms this function is implemented by looping with a delay
    of 1 ms, and so should be avoided if possible.
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
    
    Once you have initialized the cvt structure using SDL_BuildAudioCVT(),
    created an audio buffer cvt->buf, and filled it with cvt->len bytes of
    audio data in the source format, this function will convert it in-
    place to the desired format.
    
    The data conversion may expand the size of the audio data, so the
    buffer cvt->buf should be allocated after the cvt structure is
    initialized by SDL_BuildAudioCVT(), and should be
    cvt->len*cvt->len_mult bytes long.
    """
    cvt_c = unbox(cvt, 'SDL_AudioCVT *')
    rc = _LIB.SDL_ConvertAudio(cvt_c)
    return rc

def SDL_ConvertPixels(width, height, src_format, src, src_pitch, dst_format, dst, dst_pitch):
    """
    ``int SDL_ConvertPixels(int, int, uint32_t, void const *, int, uint32_t, void *, int)``
    
    Copy a block of pixels of one format to another format.
    
    :return: 0 on success, or -1 if there was an error
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
    
    Creates a new surface of the specified format, and then copies and
    maps the given surface to it so the blit of the converted surface will
    be as fast as possible. If this function fails, it returns NULL.
    
    The flags parameter is passed to SDL_CreateRGBSurface() and has those
    semantics. You can also pass SDL_RLEACCEL in the flags parameter and
    SDL will try to RLE accelerate colorkey and alpha blits in the
    resulting surface.
    """
    src_c = unbox(src, 'SDL_Surface *')
    fmt_c = unbox(fmt, 'SDL_PixelFormat *')
    flags_c = flags
    rc = _LIB.SDL_ConvertSurface(src_c, fmt_c, flags_c)
    return SDL_Surface(rc)

def SDL_ConvertSurfaceFormat(src, pixel_format, flags):
    """
    ``SDL_Surface * SDL_ConvertSurfaceFormat(SDL_Surface *, uint32_t, uint32_t)``
    """
    src_c = unbox(src, 'SDL_Surface *')
    pixel_format_c = pixel_format
    flags_c = flags
    rc = _LIB.SDL_ConvertSurfaceFormat(src_c, pixel_format_c, flags_c)
    return SDL_Surface(rc)

def SDL_CreateColorCursor(surface, hot_x, hot_y):
    """
    ``SDL_Cursor * SDL_CreateColorCursor(SDL_Surface *, int, int)``
    
    Create a color cursor.
    
    See also SDL_FreeCursor()
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    hot_x_c = hot_x
    hot_y_c = hot_y
    rc = _LIB.SDL_CreateColorCursor(surface_c, hot_x_c, hot_y_c)
    return SDL_Cursor(rc)

def SDL_CreateCond():
    """
    ``SDL_cond * SDL_CreateCond(void)``
    
    Create a condition variable.
    
    Typical use of condition variables:
    
    Thread A: SDL_LockMutex(lock); while ( ! condition ) {
    SDL_CondWait(cond, lock); } SDL_UnlockMutex(lock);
    
    Thread B: SDL_LockMutex(lock); ... condition = true; ...
    SDL_CondSignal(cond); SDL_UnlockMutex(lock);
    
    There is some discussion whether to signal the condition variable with
    the mutex locked or not. There is some potential performance benefit
    to unlocking first on some platforms, but there are some potential
    race conditions depending on how your code is structured.
    
    In general it's safer to signal the condition variable while the mutex
    is locked.
    """
    rc = _LIB.SDL_CreateCond()
    return SDL_cond(rc)

def SDL_CreateCursor(data, mask, w, h, hot_x, hot_y):
    """
    ``SDL_Cursor * SDL_CreateCursor(uint8_t const *, uint8_t const *, int, int, int, int)``
    
    Create a cursor, using the specified bitmap data and mask (in MSB
    format).
    
    The cursor width must be a multiple of 8 bits.
    
    The cursor is created in black and white according to the following:
    data
    
    mask
    
    resulting pixel on screen
    
    0
    
    1
    
    White
    
    1
    
    1
    
    Black
    
    0
    
    0
    
    Transparent
    
    1
    
    0
    
    Inverted color if possible, black if not.
    
    See also SDL_FreeCursor()
    """
    data_c = unbox(data, 'uint8_t const *')
    mask_c = unbox(mask, 'uint8_t const *')
    w_c = w
    h_c = h
    hot_x_c = hot_x
    hot_y_c = hot_y
    rc = _LIB.SDL_CreateCursor(data_c, mask_c, w_c, h_c, hot_x_c, hot_y_c)
    return SDL_Cursor(rc)

def SDL_CreateMutex():
    """
    ``SDL_mutex * SDL_CreateMutex(void)``
    
    Create a mutex, initialized unlocked.
    """
    rc = _LIB.SDL_CreateMutex()
    return SDL_mutex(rc)

def SDL_CreateRGBSurface(flags, width, height, depth, Rmask, Gmask, Bmask, Amask):
    """
    ``SDL_Surface * SDL_CreateRGBSurface(uint32_t, int, int, int, uint32_t, uint32_t, uint32_t, uint32_t)``
    
    Allocate and free an RGB surface.
    
    If the depth is 4 or 8 bits, an empty palette is allocated for the
    surface. If the depth is greater than 8 bits, the pixel format is set
    using the flags '[RGB]mask'.
    
    If the function runs out of memory, it will return NULL.
    
    :param flags: The flags are obsolete and should be set to 0.
    :param width: The width in pixels of the surface to create.
    :param height: The height in pixels of the surface to create.
    :param depth: The depth in bits of the surface to create.
    :param Rmask: The red mask of the surface to create.
    :param Gmask: The green mask of the surface to create.
    :param Bmask: The blue mask of the surface to create.
    :param Amask: The alpha mask of the surface to create.
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
    return SDL_Surface(rc)

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
    return SDL_Surface(rc)

def SDL_CreateRenderer(window, index, flags):
    """
    ``SDL_Renderer * SDL_CreateRenderer(SDL_Window *, int, uint32_t)``
    
    Create a 2D rendering context for a window.
    
    :param window: The window where rendering is displayed.
    :param index: The index of the rendering driver to initialize, or -1
        to initialize the first one supporting the requested flags.
    :param flags: SDL_RendererFlags.
    :return: A valid rendering context or NULL if there was an error.
    
    See also SDL_CreateSoftwareRenderer()
    """
    window_c = unbox(window, 'SDL_Window *')
    index_c = index
    flags_c = flags
    rc = _LIB.SDL_CreateRenderer(window_c, index_c, flags_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Renderer(rc)

def SDL_CreateSemaphore(initial_value):
    """
    ``SDL_sem * SDL_CreateSemaphore(uint32_t)``
    
    Create a semaphore, initialized with value, returns NULL on failure.
    """
    initial_value_c = initial_value
    rc = _LIB.SDL_CreateSemaphore(initial_value_c)
    return SDL_sem(rc)

def SDL_CreateSoftwareRenderer(surface):
    """
    ``SDL_Renderer * SDL_CreateSoftwareRenderer(SDL_Surface *)``
    
    Create a 2D software rendering context for a surface.
    
    :param surface: The surface where rendering is done.
    :return: A valid rendering context or NULL if there was an error.
    
    See also SDL_CreateRenderer()
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    rc = _LIB.SDL_CreateSoftwareRenderer(surface_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Renderer(rc)

def SDL_CreateSystemCursor(id):
    """
    ``SDL_Cursor * SDL_CreateSystemCursor(SDL_SystemCursor)``
    
    Create a system cursor.
    
    See also SDL_FreeCursor()
    """
    id_c = id
    rc = _LIB.SDL_CreateSystemCursor(id_c)
    return SDL_Cursor(rc)

def SDL_CreateTexture(renderer, format, access, w, h):
    """
    ``SDL_Texture * SDL_CreateTexture(SDL_Renderer *, uint32_t, int, int, int)``
    
    Create a texture for a rendering context.
    
    :param renderer: The renderer.
    :param format: The format of the texture.
    :param access: One of the enumerated values in SDL_TextureAccess.
    :param w: The width of the texture in pixels.
    :param h: The height of the texture in pixels.
    :return: The created texture is returned, or 0 if no rendering context
        was active, the format was unsupported, or the width or height
        were out of range.
    
    See also SDL_QueryTexture()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    format_c = format
    access_c = access
    w_c = w
    h_c = h
    rc = _LIB.SDL_CreateTexture(renderer_c, format_c, access_c, w_c, h_c)
    return SDL_Texture(rc)

def SDL_CreateTextureFromSurface(renderer, surface):
    """
    ``SDL_Texture * SDL_CreateTextureFromSurface(SDL_Renderer *, SDL_Surface *)``
    
    Create a texture from an existing surface.
    
    :param renderer: The renderer.
    :param surface: The surface containing pixel data used to fill the
        texture.
    :return: The created texture is returned, or 0 on error.
    
    The surface is not modified or freed by this function.
    
    See also SDL_QueryTexture()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    surface_c = unbox(surface, 'SDL_Surface *')
    rc = _LIB.SDL_CreateTextureFromSurface(renderer_c, surface_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Texture(rc)

def SDL_CreateThread(fn, name, data):
    """
    ``SDL_Thread * SDL_CreateThread(int SDL_CreateThread(void *), char const *, void *)``
    
    Create a thread.
    """
    fn_c = unbox(fn, 'int(*)(void *)')
    name_c = u8(name)
    data_c = unbox(data, 'void *')
    rc = _LIB.SDL_CreateThread(fn_c, name_c, data_c)
    return SDL_Thread(rc)

def SDL_CreateWindow(title, x, y, w, h, flags):
    """
    ``SDL_Window * SDL_CreateWindow(char const *, int, int, int, int, uint32_t)``
    
    Create a window with the specified position, dimensions, and flags.
    
    :param title: The title of the window, in UTF-8 encoding.
    :param x: The x position of the window, SDL_WINDOWPOS_CENTERED, or
        SDL_WINDOWPOS_UNDEFINED.
    :param y: The y position of the window, SDL_WINDOWPOS_CENTERED, or
        SDL_WINDOWPOS_UNDEFINED.
    :param w: The width of the window.
    :param h: The height of the window.
    :param flags: The flags for the window, a mask of any of the
        following: SDL_WINDOW_FULLSCREEN, SDL_WINDOW_OPENGL,
        SDL_WINDOW_HIDDEN, SDL_WINDOW_BORDERLESS, SDL_WINDOW_RESIZABLE,
        SDL_WINDOW_MAXIMIZED, SDL_WINDOW_MINIMIZED,
        SDL_WINDOW_INPUT_GRABBED, SDL_WINDOW_ALLOW_HIGHDPI.
    :return: The id of the window created, or zero if window creation
        failed.
    
    See also SDL_DestroyWindow()
    """
    title_c = u8(title)
    x_c = x
    y_c = y
    w_c = w
    h_c = h
    flags_c = flags
    rc = _LIB.SDL_CreateWindow(title_c, x_c, y_c, w_c, h_c, flags_c)
    return SDL_Window(rc)

def SDL_CreateWindowAndRenderer(width, height, window_flags, window, renderer):
    """
    ``int SDL_CreateWindowAndRenderer(int, int, uint32_t, SDL_Window * *, SDL_Renderer * *)``
    
    Create a window and default renderer.
    
    :param width: The width of the window
    :param height: The height of the window
    :param window_flags: The flags used to create the window
    :param window: A pointer filled with the window, or NULL on error
    :param renderer: A pointer filled with the renderer, or NULL on error
    :return: 0 on success, or -1 on error
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
    
    Create an SDL window from an existing native window.
    
    :param data: A pointer to driver-dependent window creation data
    :return: The id of the window created, or zero if window creation
        failed.
    
    See also SDL_DestroyWindow()
    """
    data_c = unbox(data, 'void const *')
    rc = _LIB.SDL_CreateWindowFrom(data_c)
    return SDL_Window(rc)

def SDL_DelEventWatch(filter, userdata):
    """
    ``void SDL_DelEventWatch(int SDL_DelEventWatch(void *, SDL_Event *), void *)``
    
    Remove an event watch function added with SDL_AddEventWatch()
    """
    filter_c = unbox(filter, 'int(*)(void *, SDL_Event *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_DelEventWatch(filter_c, userdata_c)

def SDL_DelHintCallback(name, callback, userdata):
    """
    ``void SDL_DelHintCallback(char const *, void SDL_DelHintCallback(void *, char const *, char const *, char const *), void *)``
    
    Remove a function watching a particular hint.
    
    :param name: The hint being watched
    :param callback: The function being called when the hint value changes
    :param userdata: A pointer being passed to the callback function
    """
    name_c = u8(name)
    callback_c = unbox(callback, 'void(*)(void *, char const *, char const *, char const *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_DelHintCallback(name_c, callback_c, userdata_c)

def SDL_Delay(ms):
    """
    ``void SDL_Delay(uint32_t)``
    
    Wait a specified number of milliseconds before returning.
    """
    ms_c = ms
    _LIB.SDL_Delay(ms_c)

def SDL_DestroyCond(cond):
    """
    ``void SDL_DestroyCond(SDL_cond *)``
    
    Destroy a condition variable.
    """
    cond_c = unbox(cond, 'SDL_cond *')
    _LIB.SDL_DestroyCond(cond_c)

def SDL_DestroyMutex(mutex):
    """
    ``void SDL_DestroyMutex(SDL_mutex *)``
    
    Destroy a mutex.
    """
    mutex_c = unbox(mutex, 'SDL_mutex *')
    _LIB.SDL_DestroyMutex(mutex_c)

def SDL_DestroyRenderer(renderer):
    """
    ``void SDL_DestroyRenderer(SDL_Renderer *)``
    
    Destroy the rendering context for a window and free associated
    textures.
    
    See also SDL_CreateRenderer()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    _LIB.SDL_DestroyRenderer(renderer_c)

def SDL_DestroySemaphore(sem):
    """
    ``void SDL_DestroySemaphore(SDL_sem *)``
    
    Destroy a semaphore.
    """
    sem_c = unbox(sem, 'SDL_sem *')
    _LIB.SDL_DestroySemaphore(sem_c)

def SDL_DestroyTexture(texture):
    """
    ``void SDL_DestroyTexture(SDL_Texture *)``
    
    Destroy the specified texture.
    
    See also SDL_CreateTexture()
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    _LIB.SDL_DestroyTexture(texture_c)

def SDL_DestroyWindow(window):
    """
    ``void SDL_DestroyWindow(SDL_Window *)``
    
    Destroy a window.
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_DestroyWindow(window_c)

def SDL_DisableScreenSaver():
    """
    ``void SDL_DisableScreenSaver(void)``
    
    Prevent the screen from being blanked by a screensaver.
    
    See also SDL_IsScreenSaverEnabled()
    """
    _LIB.SDL_DisableScreenSaver()

def SDL_EnableScreenSaver():
    """
    ``void SDL_EnableScreenSaver(void)``
    
    Allow the screen to be blanked by a screensaver.
    
    See also SDL_IsScreenSaverEnabled()
    """
    _LIB.SDL_EnableScreenSaver()

def SDL_EnclosePoints(points, count, clip, result):
    """
    ``SDL_bool SDL_EnclosePoints(SDL_Point const *, int, SDL_Rect const *, SDL_Rect *)``
    
    Calculate a minimal rectangle enclosing a set of points.
    
    :return: SDL_TRUE if any points were within the clipping rect
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
    
    This function allows you to set the state of processing certain
    events.If state is set to SDL_IGNORE, that event will be automatically
    dropped from the event queue and will not event be filtered.
    
    If state is set to SDL_ENABLE, that event will be processed normally.
    
    If state is set to SDL_QUERY, SDL_EventState() will return the current
    processing state of the specified event.
    """
    type_c = type
    state_c = state
    rc = _LIB.SDL_EventState(type_c, state_c)
    return rc

def SDL_FillRect(dst, rect, color):
    """
    ``int SDL_FillRect(SDL_Surface *, SDL_Rect const *, uint32_t)``
    
    Performs a fast fill of the given rectangle with color.
    
    If rect is NULL, the whole surface will be filled with color.
    
    The color should be a pixel of the format used by the surface, and can
    be generated by the SDL_MapRGB() function.
    
    :return: 0 on success, or -1 on error.
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
    
    Run the filter function on the current event queue, removing any
    events for which the filter returns 0.
    """
    filter_c = unbox(filter, 'int(*)(void *, SDL_Event *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_FilterEvents(filter_c, userdata_c)

def SDL_FlushEvent(type):
    """
    ``void SDL_FlushEvent(uint32_t)``
    
    This function clears events from the event queue
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
    
    Frees a cursor created with SDL_CreateCursor().
    
    See also SDL_CreateCursor()
    """
    cursor_c = unbox(cursor, 'SDL_Cursor *')
    _LIB.SDL_FreeCursor(cursor_c)

def SDL_FreeFormat(format):
    """
    ``void SDL_FreeFormat(SDL_PixelFormat *)``
    
    Free an SDL_PixelFormat structure.
    """
    format_c = unbox(format, 'SDL_PixelFormat *')
    _LIB.SDL_FreeFormat(format_c)

def SDL_FreePalette(palette):
    """
    ``void SDL_FreePalette(SDL_Palette *)``
    
    Free a palette created with SDL_AllocPalette().
    
    See also SDL_AllocPalette()
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
    
    This function frees data previously allocated with SDL_LoadWAV_RW()
    """
    audio_buf_c = unbox(audio_buf, 'uint8_t *')
    _LIB.SDL_FreeWAV(audio_buf_c)
    return audio_buf_c[0]

def SDL_GL_BindTexture(texture, texw=None, texh=None):
    """
    ``int SDL_GL_BindTexture(SDL_Texture *, float *, float *)``
    
    Bind the texture to the current OpenGL/ES/ES2 context for use with
    OpenGL instructions.
    
    :param texture: The SDL texture to bind
    :param texw: A pointer to a float that will be filled with the texture
        width
    :param texh: A pointer to a float that will be filled with the texture
        height
    :return: 0 on success, or -1 if the operation is not supported
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    texw_c = unbox(texw, 'float *')
    texh_c = unbox(texh, 'float *')
    rc = _LIB.SDL_GL_BindTexture(texture_c, texw_c, texh_c)
    return (rc, texw_c[0], texh_c[0])

def SDL_GL_CreateContext(window):
    """
    ``void * SDL_GL_CreateContext(SDL_Window *)``
    
    Create an OpenGL context for use with an OpenGL window, and make it
    current.
    
    See also SDL_GL_DeleteContext()
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GL_CreateContext(window_c)
    return rc

def SDL_GL_DeleteContext(context):
    """
    ``void SDL_GL_DeleteContext(void *)``
    
    Delete an OpenGL context.
    
    See also SDL_GL_CreateContext()
    """
    context_c = unbox(context, 'void *')
    _LIB.SDL_GL_DeleteContext(context_c)

def SDL_GL_ExtensionSupported(extension):
    """
    ``SDL_bool SDL_GL_ExtensionSupported(char const *)``
    
    Return true if an OpenGL extension is supported for the current
    context.
    """
    extension_c = u8(extension)
    rc = _LIB.SDL_GL_ExtensionSupported(extension_c)
    return rc

def SDL_GL_GetAttribute(attr, value=None):
    """
    ``int SDL_GL_GetAttribute(SDL_GLattr, int *)``
    
    Get the actual value for an attribute from the current context.
    """
    attr_c = attr
    value_c = unbox(value, 'int *')
    rc = _LIB.SDL_GL_GetAttribute(attr_c, value_c)
    return (rc, value_c[0])

def SDL_GL_GetCurrentContext():
    """
    ``void * SDL_GL_GetCurrentContext(void)``
    
    Get the currently active OpenGL context.
    """
    rc = _LIB.SDL_GL_GetCurrentContext()
    return rc

def SDL_GL_GetCurrentWindow():
    """
    ``SDL_Window * SDL_GL_GetCurrentWindow(void)``
    
    Get the currently active OpenGL window.
    """
    rc = _LIB.SDL_GL_GetCurrentWindow()
    return SDL_Window(rc)

def SDL_GL_GetProcAddress(proc):
    """
    ``void * SDL_GL_GetProcAddress(char const *)``
    
    Get the address of an OpenGL function.
    """
    proc_c = u8(proc)
    rc = _LIB.SDL_GL_GetProcAddress(proc_c)
    return rc

def SDL_GL_GetSwapInterval():
    """
    ``int SDL_GL_GetSwapInterval(void)``
    
    Get the swap interval for the current OpenGL context.
    
    :return: 0 if there is no vertical retrace synchronization, 1 if the
        buffer swap is synchronized with the vertical retrace, and -1 if
        late swaps happen immediately instead of waiting for the next
        retrace. If the system can't determine the swap interval, or there
        isn't a valid current context, this will return 0 as a safe
        default.
    
    See also SDL_GL_SetSwapInterval()
    """
    rc = _LIB.SDL_GL_GetSwapInterval()
    return rc

def SDL_GL_LoadLibrary(path):
    """
    ``int SDL_GL_LoadLibrary(char const *)``
    
    Dynamically load an OpenGL library.
    
    :param path: The platform dependent OpenGL library name, or NULL to
        open the default OpenGL library.
    :return: 0 on success, or -1 if the library couldn't be loaded.
    
    This should be done after initializing the video driver, but before
    creating any OpenGL windows. If no OpenGL library is loaded, the
    default library will be loaded upon creation of the first OpenGL
    window.
    
    If you do this, you need to retrieve all of the GL functions used in
    your program from the dynamic library using SDL_GL_GetProcAddress().
    
    See also SDL_GL_GetProcAddress()
    """
    path_c = u8(path)
    rc = _LIB.SDL_GL_LoadLibrary(path_c)
    return rc

def SDL_GL_MakeCurrent(window, context):
    """
    ``int SDL_GL_MakeCurrent(SDL_Window *, void *)``
    
    Set up an OpenGL context for rendering into an OpenGL window.
    
    The context must have been created with a compatible window.
    """
    window_c = unbox(window, 'SDL_Window *')
    context_c = unbox(context, 'void *')
    rc = _LIB.SDL_GL_MakeCurrent(window_c, context_c)
    return rc

def SDL_GL_SetAttribute(attr, value):
    """
    ``int SDL_GL_SetAttribute(SDL_GLattr, int)``
    
    Set an OpenGL window attribute before window creation.
    """
    attr_c = attr
    value_c = value
    rc = _LIB.SDL_GL_SetAttribute(attr_c, value_c)
    return rc

def SDL_GL_SetSwapInterval(interval):
    """
    ``int SDL_GL_SetSwapInterval(int)``
    
    Set the swap interval for the current OpenGL context.
    
    :param interval: 0 for immediate updates, 1 for updates synchronized
        with the vertical retrace. If the system supports it, you may
        specify -1 to allow late swaps to happen immediately instead of
        waiting for the next retrace.
    :return: 0 on success, or -1 if setting the swap interval is not
        supported.
    
    See also SDL_GL_GetSwapInterval()
    """
    interval_c = interval
    rc = _LIB.SDL_GL_SetSwapInterval(interval_c)
    return rc

def SDL_GL_SwapWindow(window):
    """
    ``void SDL_GL_SwapWindow(SDL_Window *)``
    
    Swap the OpenGL buffers for a window, if double-buffering is
    supported.
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_GL_SwapWindow(window_c)

def SDL_GL_UnbindTexture(texture):
    """
    ``int SDL_GL_UnbindTexture(SDL_Texture *)``
    
    Unbind a texture from the current OpenGL/ES/ES2 context.
    
    :param texture: The SDL texture to unbind
    :return: 0 on success, or -1 if the operation is not supported
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    rc = _LIB.SDL_GL_UnbindTexture(texture_c)
    return rc

def SDL_GL_UnloadLibrary():
    """
    ``void SDL_GL_UnloadLibrary(void)``
    
    Unload the OpenGL library previously loaded by SDL_GL_LoadLibrary().
    
    See also SDL_GL_LoadLibrary()
    """
    _LIB.SDL_GL_UnloadLibrary()

def SDL_GameControllerAddMapping(mappingString):
    """
    ``int SDL_GameControllerAddMapping(char const *)``
    
    Add or update an existing mapping configuration
    
    :return: 1 if mapping is added, 0 if updated, -1 on error
    """
    mappingString_c = u8(mappingString)
    rc = _LIB.SDL_GameControllerAddMapping(mappingString_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_GameControllerClose(gamecontroller):
    """
    ``void SDL_GameControllerClose(SDL_GameController *)``
    
    Close a controller previously opened with SDL_GameControllerOpen().
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    _LIB.SDL_GameControllerClose(gamecontroller_c)

def SDL_GameControllerEventState(state):
    """
    ``int SDL_GameControllerEventState(int)``
    
    Enable/disable controller event polling.
    
    If controller events are disabled, you must call
    SDL_GameControllerUpdate() yourself and check the state of the
    controller when you want controller information.
    
    The state can be one of SDL_QUERY, SDL_ENABLE or SDL_IGNORE.
    """
    state_c = state
    rc = _LIB.SDL_GameControllerEventState(state_c)
    return rc

def SDL_GameControllerGetAttached(gamecontroller):
    """
    ``SDL_bool SDL_GameControllerGetAttached(SDL_GameController *)``
    
    Returns SDL_TRUE if the controller has been opened and currently
    connected, or SDL_FALSE if it has not.
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    rc = _LIB.SDL_GameControllerGetAttached(gamecontroller_c)
    return rc

def SDL_GameControllerGetAxis(gamecontroller, axis):
    """
    ``int16_t SDL_GameControllerGetAxis(SDL_GameController *, SDL_GameControllerAxis)``
    
    Get the current state of an axis control on a game controller.
    
    The state is a value ranging from -32768 to 32767.
    
    The axis indices start at index 0.
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    axis_c = axis
    rc = _LIB.SDL_GameControllerGetAxis(gamecontroller_c, axis_c)
    return rc

def SDL_GameControllerGetAxisFromString(pchString):
    """
    ``SDL_GameControllerAxis SDL_GameControllerGetAxisFromString(char const *)``
    
    turn this string into a axis mapping
    """
    pchString_c = u8(pchString)
    rc = _LIB.SDL_GameControllerGetAxisFromString(pchString_c)
    return rc

def SDL_GameControllerGetBindForAxis(gamecontroller, axis):
    """
    ``SDL_GameControllerButtonBind SDL_GameControllerGetBindForAxis(SDL_GameController *, SDL_GameControllerAxis)``
    
    Get the SDL joystick layer binding for this controller button mapping
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    axis_c = axis
    rc = _LIB.SDL_GameControllerGetBindForAxis(gamecontroller_c, axis_c)
    return SDL_GameControllerButtonBind(rc)

def SDL_GameControllerGetBindForButton(gamecontroller, button):
    """
    ``SDL_GameControllerButtonBind SDL_GameControllerGetBindForButton(SDL_GameController *, SDL_GameControllerButton)``
    
    Get the SDL joystick layer binding for this controller button mapping
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    button_c = button
    rc = _LIB.SDL_GameControllerGetBindForButton(gamecontroller_c, button_c)
    return SDL_GameControllerButtonBind(rc)

def SDL_GameControllerGetButton(gamecontroller, button):
    """
    ``uint8_t SDL_GameControllerGetButton(SDL_GameController *, SDL_GameControllerButton)``
    
    Get the current state of a button on a game controller.
    
    The button indices start at index 0.
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    button_c = button
    rc = _LIB.SDL_GameControllerGetButton(gamecontroller_c, button_c)
    return rc

def SDL_GameControllerGetButtonFromString(pchString):
    """
    ``SDL_GameControllerButton SDL_GameControllerGetButtonFromString(char const *)``
    
    turn this string into a button mapping
    """
    pchString_c = u8(pchString)
    rc = _LIB.SDL_GameControllerGetButtonFromString(pchString_c)
    return rc

def SDL_GameControllerGetJoystick(gamecontroller):
    """
    ``SDL_Joystick * SDL_GameControllerGetJoystick(SDL_GameController *)``
    
    Get the underlying joystick object used by a controller
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    rc = _LIB.SDL_GameControllerGetJoystick(gamecontroller_c)
    return SDL_Joystick(rc)

def SDL_GameControllerGetStringForAxis(axis):
    """
    ``char const * SDL_GameControllerGetStringForAxis(SDL_GameControllerAxis)``
    
    turn this axis enum into a string mapping
    """
    axis_c = axis
    rc = _LIB.SDL_GameControllerGetStringForAxis(axis_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GameControllerGetStringForButton(button):
    """
    ``char const * SDL_GameControllerGetStringForButton(SDL_GameControllerButton)``
    
    turn this button enum into a string mapping
    """
    button_c = button
    rc = _LIB.SDL_GameControllerGetStringForButton(button_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GameControllerMapping(gamecontroller):
    """
    ``char * SDL_GameControllerMapping(SDL_GameController *)``
    
    Get a mapping string for an open GameController
    
    :return: the mapping string. Must be freed with SDL_free. Returns NULL
        if no mapping is available
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    rc = _LIB.SDL_GameControllerMapping(gamecontroller_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GameControllerMappingForGUID(guid):
    """
    ``char * SDL_GameControllerMappingForGUID(SDL_JoystickGUID)``
    
    Get a mapping string for a GUID
    
    :return: the mapping string. Must be freed with SDL_free. Returns NULL
        if no mapping is available
    """
    guid_c = unbox(guid, 'SDL_JoystickGUID')
    rc = _LIB.SDL_GameControllerMappingForGUID(guid_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GameControllerName(gamecontroller):
    """
    ``char const * SDL_GameControllerName(SDL_GameController *)``
    
    Return the name for this currently opened controller
    """
    gamecontroller_c = unbox(gamecontroller, 'SDL_GameController *')
    rc = _LIB.SDL_GameControllerName(gamecontroller_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GameControllerNameForIndex(joystick_index):
    """
    ``char const * SDL_GameControllerNameForIndex(int)``
    
    Get the implementation dependent name of a game controller. This can
    be called before any controllers are opened. If no name can be found,
    this function returns NULL.
    """
    joystick_index_c = joystick_index
    rc = _LIB.SDL_GameControllerNameForIndex(joystick_index_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GameControllerOpen(joystick_index):
    """
    ``SDL_GameController * SDL_GameControllerOpen(int)``
    
    Open a game controller for use. The index passed as an argument refers
    to the N'th game controller on the system. This index is the value
    which will identify this controller in future controller events.
    
    :return: A controller identifier, or NULL if an error occurred.
    """
    joystick_index_c = joystick_index
    rc = _LIB.SDL_GameControllerOpen(joystick_index_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_GameController(rc)

def SDL_GameControllerUpdate():
    """
    ``void SDL_GameControllerUpdate(void)``
    
    Update the current state of the open game controllers.
    
    This is called automatically by the event loop if any game controller
    events are enabled.
    """
    _LIB.SDL_GameControllerUpdate()

def SDL_GetAssertionReport():
    """
    ``SDL_assert_data const * SDL_GetAssertionReport(void)``
    
    Get a list of all assertion failures.
    
    Get all assertions triggered since last call to
    SDL_ResetAssertionReport(), or the start of the program.
    
    The proper way to examine this data looks something like this:
    
    const SDL_assert_data *item = SDL_GetAssertionReport(); while (item) {
    printf("'%s', %s (%s:%d), triggered %u times, always ignore: %s.\n",
    item->condition, item->function, item->filename, item->linenum,
    item->trigger_count, item->always_ignore ? "yes" : "no"); item =
    item->next; }
    
    :return: List of all assertions.
    
    See also SDL_ResetAssertionReport
    """
    rc = _LIB.SDL_GetAssertionReport()
    return SDL_assert_data(rc)

def SDL_GetAudioDeviceName(index, iscapture):
    """
    ``char const * SDL_GetAudioDeviceName(int, int)``
    
    Get the human-readable name of a specific audio device. Must be a
    value between 0 and (number of audio devices-1). Only valid after a
    successfully initializing the audio subsystem. The values returned by
    this function reflect the latest call to SDL_GetNumAudioDevices();
    recall that function to redetect available hardware.
    
    The string returned by this function is UTF-8 encoded, read-only, and
    managed internally. You are not to free it. If you need to keep the
    string for any length of time, you should make your own copy of it, as
    it will be invalid next time any of several other SDL functions is
    called.
    """
    index_c = index
    iscapture_c = iscapture
    rc = _LIB.SDL_GetAudioDeviceName(index_c, iscapture_c)
    return ffi.string(rc).decode('utf-8')

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
    return ffi.string(rc).decode('utf-8')

def SDL_GetAudioStatus():
    """
    ``SDL_AudioStatus SDL_GetAudioStatus(void)``
    """
    rc = _LIB.SDL_GetAudioStatus()
    return rc

def SDL_GetCPUCacheLineSize():
    """
    ``int SDL_GetCPUCacheLineSize(void)``
    
    This function returns the L1 cache line size of the CPU
    
    This is useful for determining multi-threaded structure padding or
    SIMD prefetch sizes.
    """
    rc = _LIB.SDL_GetCPUCacheLineSize()
    return rc

def SDL_GetCPUCount():
    """
    ``int SDL_GetCPUCount(void)``
    
    This function returns the number of CPU cores available.
    """
    rc = _LIB.SDL_GetCPUCount()
    return rc

def SDL_GetClipRect(surface, rect):
    """
    ``void SDL_GetClipRect(SDL_Surface *, SDL_Rect *)``
    
    Gets the clipping rectangle for the destination surface in a blit.
    
    rect must be a pointer to a valid rectangle which will be filled with
    the correct values.
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    rect_c = unbox(rect, 'SDL_Rect *')
    _LIB.SDL_GetClipRect(surface_c, rect_c)

def SDL_GetClipboardText():
    """
    ``char * SDL_GetClipboardText(void)``
    
    Get UTF-8 text from the clipboard, which must be freed with SDL_free()
    
    See also SDL_SetClipboardText()
    """
    rc = _LIB.SDL_GetClipboardText()
    return ffi.string(rc).decode('utf-8')

def SDL_GetClosestDisplayMode(displayIndex, mode, closest):
    """
    ``SDL_DisplayMode * SDL_GetClosestDisplayMode(int, SDL_DisplayMode const *, SDL_DisplayMode *)``
    
    Get the closest match to the requested display mode.
    
    :param displayIndex: The index of display from which mode should be
        queried.
    :param mode: The desired display mode
    :param closest: A pointer to a display mode to be filled in with the
        closest match of the available display modes.
    :return: The passed in value
    
    The available display modes are scanned, and closest is filled in with
    the closest mode matching the requested mode and returned. The mode
    format and refresh_rate default to the desktop mode if they are 0. The
    modes are scanned with size being first priority, format being second
    priority, and finally checking the refresh_rate. If all the available
    modes are too small, then NULL is returned.
    
    See also SDL_GetNumDisplayModes()
    """
    displayIndex_c = displayIndex
    mode_c = unbox(mode, 'SDL_DisplayMode const *')
    closest_c = unbox(closest, 'SDL_DisplayMode *')
    rc = _LIB.SDL_GetClosestDisplayMode(displayIndex_c, mode_c, closest_c)
    return SDL_DisplayMode(rc)

def SDL_GetColorKey(surface, key=None):
    """
    ``int SDL_GetColorKey(SDL_Surface *, uint32_t *)``
    
    Gets the color key (transparent pixel) in a blittable surface.
    
    :param surface: The surface to update
    :param key: A pointer filled in with the transparent pixel in the
        native surface format
    :return: 0 on success, or -1 if the surface is not valid or colorkey
        is not enabled.
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    key_c = unbox(key, 'uint32_t *')
    rc = _LIB.SDL_GetColorKey(surface_c, key_c)
    return (rc, key_c[0])

def SDL_GetCurrentAudioDriver():
    """
    ``char const * SDL_GetCurrentAudioDriver(void)``
    
    This function returns the name of the current audio driver, or NULL if
    no driver has been initialized.
    """
    rc = _LIB.SDL_GetCurrentAudioDriver()
    return ffi.string(rc).decode('utf-8')

def SDL_GetCurrentDisplayMode(displayIndex, mode):
    """
    ``int SDL_GetCurrentDisplayMode(int, SDL_DisplayMode *)``
    
    Fill in information about the current display mode.
    """
    displayIndex_c = displayIndex
    mode_c = unbox(mode, 'SDL_DisplayMode *')
    rc = _LIB.SDL_GetCurrentDisplayMode(displayIndex_c, mode_c)
    return rc

def SDL_GetCurrentVideoDriver():
    """
    ``char const * SDL_GetCurrentVideoDriver(void)``
    
    Returns the name of the currently initialized video driver.
    
    :return: The name of the current video driver or NULL if no driver has
        been initialized
    
    See also SDL_GetNumVideoDrivers()
    """
    rc = _LIB.SDL_GetCurrentVideoDriver()
    return ffi.string(rc).decode('utf-8')

def SDL_GetCursor():
    """
    ``SDL_Cursor * SDL_GetCursor(void)``
    
    Return the active cursor.
    """
    rc = _LIB.SDL_GetCursor()
    return SDL_Cursor(rc)

def SDL_GetDefaultCursor():
    """
    ``SDL_Cursor * SDL_GetDefaultCursor(void)``
    
    Return the default cursor.
    """
    rc = _LIB.SDL_GetDefaultCursor()
    return SDL_Cursor(rc)

def SDL_GetDesktopDisplayMode(displayIndex, mode):
    """
    ``int SDL_GetDesktopDisplayMode(int, SDL_DisplayMode *)``
    
    Fill in information about the desktop display mode.
    """
    displayIndex_c = displayIndex
    mode_c = unbox(mode, 'SDL_DisplayMode *')
    rc = _LIB.SDL_GetDesktopDisplayMode(displayIndex_c, mode_c)
    return rc

def SDL_GetDisplayBounds(displayIndex, rect):
    """
    ``int SDL_GetDisplayBounds(int, SDL_Rect *)``
    
    Get the desktop area represented by a display, with the primary
    display located at 0,0.
    
    :return: 0 on success, or -1 if the index is out of range.
    
    See also SDL_GetNumVideoDisplays()
    """
    displayIndex_c = displayIndex
    rect_c = unbox(rect, 'SDL_Rect *')
    rc = _LIB.SDL_GetDisplayBounds(displayIndex_c, rect_c)
    return rc

def SDL_GetDisplayMode(displayIndex, modeIndex, mode):
    """
    ``int SDL_GetDisplayMode(int, int, SDL_DisplayMode *)``
    
    Fill in information about a specific display mode.
    
    The display modes are sorted in this priority: bits per pixel -> more
    colors to fewer colors
    
    width -> largest to smallest
    
    height -> largest to smallest
    
    refresh rate -> highest to lowest
    
    See also SDL_GetNumDisplayModes()
    """
    displayIndex_c = displayIndex
    modeIndex_c = modeIndex
    mode_c = unbox(mode, 'SDL_DisplayMode *')
    rc = _LIB.SDL_GetDisplayMode(displayIndex_c, modeIndex_c, mode_c)
    return rc

def SDL_GetDisplayName(displayIndex):
    """
    ``char const * SDL_GetDisplayName(int)``
    
    Get the name of a display in UTF-8 encoding.
    
    :return: The name of a display, or NULL for an invalid display index.
    
    See also SDL_GetNumVideoDisplays()
    """
    displayIndex_c = displayIndex
    rc = _LIB.SDL_GetDisplayName(displayIndex_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GetError():
    """
    ``char const * SDL_GetError(void)``
    """
    rc = _LIB.SDL_GetError()
    return ffi.string(rc).decode('utf-8')

def SDL_GetEventFilter(filter, userdata):
    """
    ``SDL_bool SDL_GetEventFilter(int(* *)(void *, SDL_Event *), void * *)``
    
    Return the current event filter - can be used to "chain" filters. If
    there is no event filter set, this function returns SDL_FALSE.
    """
    filter_c = unbox(filter, 'int(* *)(void *, SDL_Event *)')
    userdata_c = unbox(userdata, 'void * *')
    rc = _LIB.SDL_GetEventFilter(filter_c, userdata_c)
    return rc

def SDL_GetHint(name):
    """
    ``char const * SDL_GetHint(char const *)``
    
    Get a hint.
    
    :return: The string value of a hint variable.
    """
    name_c = u8(name)
    rc = _LIB.SDL_GetHint(name_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GetKeyFromName(name):
    """
    ``int32_t SDL_GetKeyFromName(char const *)``
    
    Get a key code from a human-readable name.
    
    :return: key code, or SDLK_UNKNOWN if the name wasn't recognized
    
    See also SDL_Keycode
    """
    name_c = u8(name)
    rc = _LIB.SDL_GetKeyFromName(name_c)
    return rc

def SDL_GetKeyFromScancode(scancode):
    """
    ``int32_t SDL_GetKeyFromScancode(SDL_Scancode)``
    
    Get the key code corresponding to the given scancode according to the
    current keyboard layout.
    
    See SDL_Keycode for details.
    
    See also SDL_GetKeyName()
    """
    scancode_c = scancode
    rc = _LIB.SDL_GetKeyFromScancode(scancode_c)
    return rc

def SDL_GetKeyName(key):
    """
    ``char const * SDL_GetKeyName(int32_t)``
    
    Get a human-readable name for a key.
    
    :return: A pointer to a UTF-8 string that stays valid at least until
        the next call to this function. If you need it around any longer,
        you must copy it. If the key doesn't have a name, this function
        returns an empty string ("").
    
    See also SDL_Key
    """
    key_c = key
    rc = _LIB.SDL_GetKeyName(key_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GetKeyboardFocus():
    """
    ``SDL_Window * SDL_GetKeyboardFocus(void)``
    
    Get the window which currently has keyboard focus.
    """
    rc = _LIB.SDL_GetKeyboardFocus()
    return SDL_Window(rc)

def SDL_GetKeyboardState(numkeys=None):
    """
    ``uint8_t const * SDL_GetKeyboardState(int *)``
    
    Get a snapshot of the current state of the keyboard.
    
    :param numkeys: if non-NULL, receives the length of the returned
        array.
    :return: An array of key states. Indexes into this array are obtained
        by using
    
    Example:::
    
       const Uint8 *state = SDL_GetKeyboardState(NULL);
       if ( state[SDL_SCANCODE_RETURN] )   {
           printf("<RETURN> is pressed.\n");
       }
    
    """
    numkeys_c = unbox(numkeys, 'int *')
    rc = _LIB.SDL_GetKeyboardState(numkeys_c)
    return (rc, numkeys_c[0])

def SDL_GetModState():
    """
    ``SDL_Keymod SDL_GetModState(void)``
    
    Get the current key modifier state for the keyboard.
    """
    rc = _LIB.SDL_GetModState()
    return rc

def SDL_GetMouseFocus():
    """
    ``SDL_Window * SDL_GetMouseFocus(void)``
    
    Get the window which currently has mouse focus.
    """
    rc = _LIB.SDL_GetMouseFocus()
    return SDL_Window(rc)

def SDL_GetMouseState(x=None, y=None):
    """
    ``uint32_t SDL_GetMouseState(int *, int *)``
    
    Retrieve the current state of the mouse.
    
    The current button state is returned as a button bitmask, which can be
    tested using the SDL_BUTTON(X) macros, and x and y are set to the
    mouse cursor position relative to the focus window for the currently
    selected mouse. You can pass NULL for either x or y.
    """
    x_c = unbox(x, 'int *')
    y_c = unbox(y, 'int *')
    rc = _LIB.SDL_GetMouseState(x_c, y_c)
    return (rc, x_c[0], y_c[0])

def SDL_GetNumAudioDevices(iscapture):
    """
    ``int SDL_GetNumAudioDevices(int)``
    
    Get the number of available devices exposed by the current driver.
    Only valid after a successfully initializing the audio subsystem.
    Returns -1 if an explicit list of devices can't be determined; this is
    not an error. For example, if SDL is set up to talk to a remote audio
    server, it can't list every one available on the Internet, but it will
    still allow a specific host to be specified to SDL_OpenAudioDevice().
    
    In many common cases, when this function returns a value <= 0, it can
    still successfully open the default device (NULL for first argument of
    SDL_OpenAudioDevice()).
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
    
    Returns the number of available display modes.
    
    See also SDL_GetDisplayMode()
    """
    displayIndex_c = displayIndex
    rc = _LIB.SDL_GetNumDisplayModes(displayIndex_c)
    return rc

def SDL_GetNumRenderDrivers():
    """
    ``int SDL_GetNumRenderDrivers(void)``
    
    Get the number of 2D rendering drivers available for the current
    display.
    
    A render driver is a set of code that handles rendering and texture
    management on a particular display. Normally there is only one, but
    some drivers may have several available with different capabilities.
    
    See also SDL_GetRenderDriverInfo()
    """
    rc = _LIB.SDL_GetNumRenderDrivers()
    return rc

def SDL_GetNumTouchDevices():
    """
    ``int SDL_GetNumTouchDevices(void)``
    
    Get the number of registered touch devices.
    """
    rc = _LIB.SDL_GetNumTouchDevices()
    return rc

def SDL_GetNumTouchFingers(touchID):
    """
    ``int SDL_GetNumTouchFingers(int64_t)``
    
    Get the number of active fingers for a given touch device.
    """
    touchID_c = touchID
    rc = _LIB.SDL_GetNumTouchFingers(touchID_c)
    return rc

def SDL_GetNumVideoDisplays():
    """
    ``int SDL_GetNumVideoDisplays(void)``
    
    Returns the number of available video displays.
    
    See also SDL_GetDisplayBounds()
    """
    rc = _LIB.SDL_GetNumVideoDisplays()
    return rc

def SDL_GetNumVideoDrivers():
    """
    ``int SDL_GetNumVideoDrivers(void)``
    
    Get the number of video drivers compiled into SDL.
    
    See also SDL_GetVideoDriver()
    """
    rc = _LIB.SDL_GetNumVideoDrivers()
    return rc

def SDL_GetPerformanceCounter():
    """
    ``uint64_t SDL_GetPerformanceCounter(void)``
    
    Get the current value of the high resolution counter.
    """
    rc = _LIB.SDL_GetPerformanceCounter()
    return rc

def SDL_GetPerformanceFrequency():
    """
    ``uint64_t SDL_GetPerformanceFrequency(void)``
    
    Get the count per second of the high resolution counter.
    """
    rc = _LIB.SDL_GetPerformanceFrequency()
    return rc

def SDL_GetPixelFormatName(format):
    """
    ``char const * SDL_GetPixelFormatName(uint32_t)``
    
    Get the human readable name of a pixel format.
    """
    format_c = format
    rc = _LIB.SDL_GetPixelFormatName(format_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GetPlatform():
    """
    ``char const * SDL_GetPlatform(void)``
    
    Gets the name of the platform.
    """
    rc = _LIB.SDL_GetPlatform()
    return ffi.string(rc).decode('utf-8')

def SDL_GetPowerInfo(secs=None, pct=None):
    """
    ``SDL_PowerState SDL_GetPowerInfo(int *, int *)``
    
    Get the current power supply details.
    
    :param secs: Seconds of battery life left. You can pass a NULL here if
        you don't care. Will return -1 if we can't determine a value, or
        we're not running on a battery.
    :param pct: Percentage of battery life left, between 0 and 100. You
        can pass a NULL here if you don't care. Will return -1 if we can't
        determine a value, or we're not running on a battery.
    :return: The state of the battery (if any).
    """
    secs_c = unbox(secs, 'int *')
    pct_c = unbox(pct, 'int *')
    rc = _LIB.SDL_GetPowerInfo(secs_c, pct_c)
    return (rc, secs_c[0], pct_c[0])

def SDL_GetRGB(pixel, format, r=None, g=None, b=None):
    """
    ``void SDL_GetRGB(uint32_t, SDL_PixelFormat const *, uint8_t *, uint8_t *, uint8_t *)``
    
    Get the RGB components from a pixel of the specified format.
    
    See also SDL_GetRGBA
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
    
    Get the RGBA components from a pixel of the specified format.
    
    See also SDL_GetRGB
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
    
    Query whether relative mouse mode is enabled.
    
    See also SDL_SetRelativeMouseMode()
    """
    rc = _LIB.SDL_GetRelativeMouseMode()
    return rc

def SDL_GetRelativeMouseState(x=None, y=None):
    """
    ``uint32_t SDL_GetRelativeMouseState(int *, int *)``
    
    Retrieve the relative state of the mouse.
    
    The current button state is returned as a button bitmask, which can be
    tested using the SDL_BUTTON(X) macros, and x and y are set to the
    mouse deltas since the last call to SDL_GetRelativeMouseState().
    """
    x_c = unbox(x, 'int *')
    y_c = unbox(y, 'int *')
    rc = _LIB.SDL_GetRelativeMouseState(x_c, y_c)
    return (rc, x_c[0], y_c[0])

def SDL_GetRenderDrawBlendMode(renderer, blendMode):
    """
    ``int SDL_GetRenderDrawBlendMode(SDL_Renderer *, SDL_BlendMode *)``
    
    Get the blend mode used for drawing operations.
    
    :param renderer: The renderer from which blend mode should be queried.
    :param blendMode: A pointer filled in with the current blend mode.
    :return: 0 on success, or -1 on error
    
    See also SDL_SetRenderDrawBlendMode()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    blendMode_c = unbox(blendMode, 'SDL_BlendMode *')
    rc = _LIB.SDL_GetRenderDrawBlendMode(renderer_c, blendMode_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_GetRenderDrawColor(renderer, r=None, g=None, b=None, a=None):
    """
    ``int SDL_GetRenderDrawColor(SDL_Renderer *, uint8_t *, uint8_t *, uint8_t *, uint8_t *)``
    
    Get the color used for drawing operations (Rect, Line and Clear).
    
    :param renderer: The renderer from which drawing color should be
        queried.
    :param r: A pointer to the red value used to draw on the rendering
        target.
    :param g: A pointer to the green value used to draw on the rendering
        target.
    :param b: A pointer to the blue value used to draw on the rendering
        target.
    :param a: A pointer to the alpha value used to draw on the rendering
        target, usually SDL_ALPHA_OPAQUE (255).
    :return: 0 on success, or -1 on error
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
    
    Get information about a specific 2D rendering driver for the current
    display.
    
    :param index: The index of the driver to query information about.
    :param info: A pointer to an SDL_RendererInfo struct to be filled with
        information on the rendering driver.
    :return: 0 on success, -1 if the index was out of range.
    
    See also SDL_CreateRenderer()
    """
    index_c = index
    info_c = unbox(info, 'SDL_RendererInfo *')
    rc = _LIB.SDL_GetRenderDriverInfo(index_c, info_c)
    return rc

def SDL_GetRenderTarget(renderer):
    """
    ``SDL_Texture * SDL_GetRenderTarget(SDL_Renderer *)``
    
    Get the current render target or NULL for the default render target.
    
    :return: The current render target
    
    See also SDL_SetRenderTarget()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rc = _LIB.SDL_GetRenderTarget(renderer_c)
    return SDL_Texture(rc)

def SDL_GetRenderer(window):
    """
    ``SDL_Renderer * SDL_GetRenderer(SDL_Window *)``
    
    Get the renderer associated with a window.
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetRenderer(window_c)
    return SDL_Renderer(rc)

def SDL_GetRendererInfo(renderer, info):
    """
    ``int SDL_GetRendererInfo(SDL_Renderer *, SDL_RendererInfo *)``
    
    Get information about a rendering context.
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    info_c = unbox(info, 'SDL_RendererInfo *')
    rc = _LIB.SDL_GetRendererInfo(renderer_c, info_c)
    return rc

def SDL_GetRendererOutputSize(renderer, w=None, h=None):
    """
    ``int SDL_GetRendererOutputSize(SDL_Renderer *, int *, int *)``
    
    Get the output size of a rendering context.
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    rc = _LIB.SDL_GetRendererOutputSize(renderer_c, w_c, h_c)
    return (rc, w_c[0], h_c[0])

def SDL_GetRevision():
    """
    ``char const * SDL_GetRevision(void)``
    
    Get the code revision of SDL that is linked against your program.
    
    Returns an arbitrary string (a hash value) uniquely identifying the
    exact revision of the SDL library in use, and is only useful in
    comparing against other revisions. It is NOT an incrementing number.
    """
    rc = _LIB.SDL_GetRevision()
    return ffi.string(rc).decode('utf-8')

def SDL_GetRevisionNumber():
    """
    ``int SDL_GetRevisionNumber(void)``
    
    Get the revision number of SDL that is linked against your program.
    
    Returns a number uniquely identifying the exact revision of the SDL
    library in use. It is an incrementing number based on commits to
    hg.libsdl.org.
    """
    rc = _LIB.SDL_GetRevisionNumber()
    return rc

def SDL_GetScancodeFromKey(key):
    """
    ``SDL_Scancode SDL_GetScancodeFromKey(int32_t)``
    
    Get the scancode corresponding to the given key code according to the
    current keyboard layout.
    
    See SDL_Scancode for details.
    
    See also SDL_GetScancodeName()
    """
    key_c = key
    rc = _LIB.SDL_GetScancodeFromKey(key_c)
    return rc

def SDL_GetScancodeFromName(name):
    """
    ``SDL_Scancode SDL_GetScancodeFromName(char const *)``
    
    Get a scancode from a human-readable name.
    
    :return: scancode, or SDL_SCANCODE_UNKNOWN if the name wasn't
        recognized
    
    See also SDL_Scancode
    """
    name_c = u8(name)
    rc = _LIB.SDL_GetScancodeFromName(name_c)
    return rc

def SDL_GetScancodeName(scancode):
    """
    ``char const * SDL_GetScancodeName(SDL_Scancode)``
    
    Get a human-readable name for a scancode.
    
    :return: A pointer to the name for the scancode. If the scancode
        doesn't have a name, this function returns an empty string ("").
    
    See also SDL_Scancode
    """
    scancode_c = scancode
    rc = _LIB.SDL_GetScancodeName(scancode_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GetSurfaceAlphaMod(surface, alpha=None):
    """
    ``int SDL_GetSurfaceAlphaMod(SDL_Surface *, uint8_t *)``
    
    Get the additional alpha value used in blit operations.
    
    :param surface: The surface to query.
    :param alpha: A pointer filled in with the current alpha value.
    :return: 0 on success, or -1 if the surface is not valid.
    
    See also SDL_SetSurfaceAlphaMod()
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    alpha_c = unbox(alpha, 'uint8_t *')
    rc = _LIB.SDL_GetSurfaceAlphaMod(surface_c, alpha_c)
    return (rc, alpha_c[0])

def SDL_GetSurfaceBlendMode(surface, blendMode):
    """
    ``int SDL_GetSurfaceBlendMode(SDL_Surface *, SDL_BlendMode *)``
    
    Get the blend mode used for blit operations.
    
    :param surface: The surface to query.
    :param blendMode: A pointer filled in with the current blend mode.
    :return: 0 on success, or -1 if the surface is not valid.
    
    See also SDL_SetSurfaceBlendMode()
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    blendMode_c = unbox(blendMode, 'SDL_BlendMode *')
    rc = _LIB.SDL_GetSurfaceBlendMode(surface_c, blendMode_c)
    return rc

def SDL_GetSurfaceColorMod(surface, r=None, g=None, b=None):
    """
    ``int SDL_GetSurfaceColorMod(SDL_Surface *, uint8_t *, uint8_t *, uint8_t *)``
    
    Get the additional color value used in blit operations.
    
    :param surface: The surface to query.
    :param r: A pointer filled in with the current red color value.
    :param g: A pointer filled in with the current green color value.
    :param b: A pointer filled in with the current blue color value.
    :return: 0 on success, or -1 if the surface is not valid.
    
    See also SDL_SetSurfaceColorMod()
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
    
    Get the additional alpha value used in render copy operations.
    
    :param texture: The texture to query.
    :param alpha: A pointer filled in with the current alpha value.
    :return: 0 on success, or -1 if the texture is not valid.
    
    See also SDL_SetTextureAlphaMod()
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    alpha_c = unbox(alpha, 'uint8_t *')
    rc = _LIB.SDL_GetTextureAlphaMod(texture_c, alpha_c)
    return (rc, alpha_c[0])

def SDL_GetTextureBlendMode(texture, blendMode):
    """
    ``int SDL_GetTextureBlendMode(SDL_Texture *, SDL_BlendMode *)``
    
    Get the blend mode used for texture copy operations.
    
    :param texture: The texture to query.
    :param blendMode: A pointer filled in with the current blend mode.
    :return: 0 on success, or -1 if the texture is not valid.
    
    See also SDL_SetTextureBlendMode()
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    blendMode_c = unbox(blendMode, 'SDL_BlendMode *')
    rc = _LIB.SDL_GetTextureBlendMode(texture_c, blendMode_c)
    return rc

def SDL_GetTextureColorMod(texture, r=None, g=None, b=None):
    """
    ``int SDL_GetTextureColorMod(SDL_Texture *, uint8_t *, uint8_t *, uint8_t *)``
    
    Get the additional color value used in render copy operations.
    
    :param texture: The texture to query.
    :param r: A pointer filled in with the current red color value.
    :param g: A pointer filled in with the current green color value.
    :param b: A pointer filled in with the current blue color value.
    :return: 0 on success, or -1 if the texture is not valid.
    
    See also SDL_SetTextureColorMod()
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
    
    Get the thread identifier for the specified thread.
    
    Equivalent to SDL_ThreadID() if the specified thread is NULL.
    """
    thread_c = unbox(thread, 'SDL_Thread *')
    rc = _LIB.SDL_GetThreadID(thread_c)
    return rc

def SDL_GetThreadName(thread):
    """
    ``char const * SDL_GetThreadName(SDL_Thread *)``
    
    Get the thread name, as it was specified in SDL_CreateThread(). This
    function returns a pointer to a UTF-8 string that names the specified
    thread, or NULL if it doesn't have a name. This is internal memory,
    not to be free()'d by the caller, and remains valid until the
    specified thread is cleaned up by SDL_WaitThread().
    """
    thread_c = unbox(thread, 'SDL_Thread *')
    rc = _LIB.SDL_GetThreadName(thread_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GetTicks():
    """
    ``uint32_t SDL_GetTicks(void)``
    
    Get the number of milliseconds since the SDL library initialization.
    
    This value wraps if the program runs for more than ~49 days.
    """
    rc = _LIB.SDL_GetTicks()
    return rc

def SDL_GetTouchDevice(index):
    """
    ``int64_t SDL_GetTouchDevice(int)``
    
    Get the touch ID with the given index, or 0 if the index is invalid.
    """
    index_c = index
    rc = _LIB.SDL_GetTouchDevice(index_c)
    return rc

def SDL_GetTouchFinger(touchID, index):
    """
    ``SDL_Finger * SDL_GetTouchFinger(int64_t, int)``
    
    Get the finger object of the given touch, with the given index.
    """
    touchID_c = touchID
    index_c = index
    rc = _LIB.SDL_GetTouchFinger(touchID_c, index_c)
    return SDL_Finger(rc)

def SDL_GetVersion(ver):
    """
    ``void SDL_GetVersion(SDL_version *)``
    
    Get the version of SDL that is linked against your program.
    
    If you are linking to SDL dynamically, then it is possible that the
    current version will be different than the version you compiled
    against. This function returns the current version, while
    SDL_VERSION() is a macro that tells you what version you compiled
    with.
    
    ::
    
       SDL_version compiled;
       SDL_version linked;
    
    
    
       SDL_VERSION(&compiled);
       SDL_GetVersion(&linked);
       printf("We compiled against SDL version %d.%d.%d ...\n",
              compiled.major, compiled.minor, compiled.patch);
       printf("But we linked against SDL version %d.%d.%d.\n",
              linked.major, linked.minor, linked.patch);
    
    
    This function may be called safely at any time, even before
    SDL_Init().
    
    See also SDL_VERSION
    """
    ver_c = unbox(ver, 'SDL_version *')
    _LIB.SDL_GetVersion(ver_c)

def SDL_GetVideoDriver(index):
    """
    ``char const * SDL_GetVideoDriver(int)``
    
    Get the name of a built in video driver.
    
    The video drivers are presented in the order in which they are
    normally checked during initialization.
    
    See also SDL_GetNumVideoDrivers()
    """
    index_c = index
    rc = _LIB.SDL_GetVideoDriver(index_c)
    return ffi.string(rc).decode('utf-8')

def SDL_GetWindowBrightness(window):
    """
    ``float SDL_GetWindowBrightness(SDL_Window *)``
    
    Get the brightness (gamma correction) for a window.
    
    :return: The last brightness value passed to
    
    See also SDL_SetWindowBrightness()
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowBrightness(window_c)
    return rc

def SDL_GetWindowData(window, name):
    """
    ``void * SDL_GetWindowData(SDL_Window *, char const *)``
    
    Retrieve the data pointer associated with a window.
    
    :param window: The window to query.
    :param name: The name of the pointer.
    :return: The value associated with 'name'
    
    See also SDL_SetWindowData()
    """
    window_c = unbox(window, 'SDL_Window *')
    name_c = u8(name)
    rc = _LIB.SDL_GetWindowData(window_c, name_c)
    return rc

def SDL_GetWindowDisplayIndex(window):
    """
    ``int SDL_GetWindowDisplayIndex(SDL_Window *)``
    
    Get the display index associated with a window.
    
    :return: the display index of the display containing the center of the
        window, or -1 on error.
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowDisplayIndex(window_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_GetWindowDisplayMode(window, mode):
    """
    ``int SDL_GetWindowDisplayMode(SDL_Window *, SDL_DisplayMode *)``
    
    Fill in information about the display mode used when a fullscreen
    window is visible.
    
    See also SDL_SetWindowDisplayMode()
    """
    window_c = unbox(window, 'SDL_Window *')
    mode_c = unbox(mode, 'SDL_DisplayMode *')
    rc = _LIB.SDL_GetWindowDisplayMode(window_c, mode_c)
    return rc

def SDL_GetWindowFlags(window):
    """
    ``uint32_t SDL_GetWindowFlags(SDL_Window *)``
    
    Get the window flags.
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowFlags(window_c)
    return rc

def SDL_GetWindowFromID(id):
    """
    ``SDL_Window * SDL_GetWindowFromID(uint32_t)``
    
    Get a window from a stored ID, or NULL if it doesn't exist.
    """
    id_c = id
    rc = _LIB.SDL_GetWindowFromID(id_c)
    return SDL_Window(rc)

def SDL_GetWindowGammaRamp(window, red=None, green=None, blue=None):
    """
    ``int SDL_GetWindowGammaRamp(SDL_Window *, uint16_t *, uint16_t *, uint16_t *)``
    
    Get the gamma ramp for a window.
    
    :param window: The window from which the gamma ramp should be queried.
    :param red: A pointer to a 256 element array of 16-bit quantities to
        hold the translation table for the red channel, or NULL.
    :param green: A pointer to a 256 element array of 16-bit quantities to
        hold the translation table for the green channel, or NULL.
    :param blue: A pointer to a 256 element array of 16-bit quantities to
        hold the translation table for the blue channel, or NULL.
    :return: 0 on success, or -1 if gamma ramps are unsupported.
    
    See also SDL_SetWindowGammaRamp()
    """
    window_c = unbox(window, 'SDL_Window *', nullable=True)
    red_c = unbox(red, 'uint16_t *', nullable=True)
    green_c = unbox(green, 'uint16_t *', nullable=True)
    blue_c = unbox(blue, 'uint16_t *', nullable=True)
    rc = _LIB.SDL_GetWindowGammaRamp(window_c, red_c, green_c, blue_c)
    return (rc, red_c[0], green_c[0], blue_c[0])

def SDL_GetWindowGrab(window):
    """
    ``SDL_bool SDL_GetWindowGrab(SDL_Window *)``
    
    Get a window's input grab mode.
    
    :return: This returns SDL_TRUE if input is grabbed, and SDL_FALSE
        otherwise.
    
    See also SDL_SetWindowGrab()
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowGrab(window_c)
    return rc

def SDL_GetWindowID(window):
    """
    ``uint32_t SDL_GetWindowID(SDL_Window *)``
    
    Get the numeric ID of a window, for logging purposes.
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowID(window_c)
    return rc

def SDL_GetWindowMaximumSize(window, w=None, h=None):
    """
    ``void SDL_GetWindowMaximumSize(SDL_Window *, int *, int *)``
    
    Get the maximum size of a window's client area.
    
    :param window: The window to query.
    :param w: Pointer to variable for storing the maximum width, may be
        NULL
    :param h: Pointer to variable for storing the maximum height, may be
        NULL
    
    See also SDL_GetWindowMinimumSize()
    """
    window_c = unbox(window, 'SDL_Window *')
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    _LIB.SDL_GetWindowMaximumSize(window_c, w_c, h_c)
    return (w_c[0], h_c[0])

def SDL_GetWindowMinimumSize(window, w=None, h=None):
    """
    ``void SDL_GetWindowMinimumSize(SDL_Window *, int *, int *)``
    
    Get the minimum size of a window's client area.
    
    :param window: The window to query.
    :param w: Pointer to variable for storing the minimum width, may be
        NULL
    :param h: Pointer to variable for storing the minimum height, may be
        NULL
    
    See also SDL_GetWindowMaximumSize()
    """
    window_c = unbox(window, 'SDL_Window *')
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    _LIB.SDL_GetWindowMinimumSize(window_c, w_c, h_c)
    return (w_c[0], h_c[0])

def SDL_GetWindowPixelFormat(window):
    """
    ``uint32_t SDL_GetWindowPixelFormat(SDL_Window *)``
    
    Get the pixel format associated with the window.
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowPixelFormat(window_c)
    return rc

def SDL_GetWindowPosition(window, x=None, y=None):
    """
    ``void SDL_GetWindowPosition(SDL_Window *, int *, int *)``
    
    Get the position of a window.
    
    :param window: The window to query.
    :param x: Pointer to variable for storing the x position, may be NULL
    :param y: Pointer to variable for storing the y position, may be NULL
    
    See also SDL_SetWindowPosition()
    """
    window_c = unbox(window, 'SDL_Window *')
    x_c = unbox(x, 'int *')
    y_c = unbox(y, 'int *')
    _LIB.SDL_GetWindowPosition(window_c, x_c, y_c)
    return (x_c[0], y_c[0])

def SDL_GetWindowSize(window, w=None, h=None):
    """
    ``void SDL_GetWindowSize(SDL_Window *, int *, int *)``
    
    Get the size of a window's client area.
    
    :param window: The window to query.
    :param w: Pointer to variable for storing the width, may be NULL
    :param h: Pointer to variable for storing the height, may be NULL
    
    See also SDL_SetWindowSize()
    """
    window_c = unbox(window, 'SDL_Window *')
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    _LIB.SDL_GetWindowSize(window_c, w_c, h_c)
    return (w_c[0], h_c[0])

def SDL_GetWindowSurface(window):
    """
    ``SDL_Surface * SDL_GetWindowSurface(SDL_Window *)``
    
    Get the SDL surface associated with the window.
    
    :return: The window's framebuffer surface, or NULL on error.
    
    A new surface will be created with the optimal format for the window,
    if necessary. This surface will be freed when the window is destroyed.
    
    You may not combine this with 3D or the rendering API on this window.
    
    See also SDL_UpdateWindowSurface()
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowSurface(window_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def SDL_GetWindowTitle(window):
    """
    ``char const * SDL_GetWindowTitle(SDL_Window *)``
    
    Get the title of a window, in UTF-8 format.
    
    See also SDL_SetWindowTitle()
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_GetWindowTitle(window_c)
    return ffi.string(rc).decode('utf-8')

def SDL_HapticClose(haptic):
    """
    ``void SDL_HapticClose(SDL_Haptic *)``
    
    Closes a Haptic device previously opened with SDL_HapticOpen().
    
    :param haptic: Haptic device to close.
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    _LIB.SDL_HapticClose(haptic_c)

def SDL_HapticDestroyEffect(haptic, effect):
    """
    ``void SDL_HapticDestroyEffect(SDL_Haptic *, int)``
    
    Destroys a haptic effect on the device.
    
    This will stop the effect if it's running. Effects are automatically
    destroyed when the device is closed.
    
    :param haptic: Device to destroy the effect on.
    :param effect: Identifier of the effect to destroy.
    
    See also SDL_HapticNewEffect
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    effect_c = effect
    _LIB.SDL_HapticDestroyEffect(haptic_c, effect_c)

def SDL_HapticEffectSupported(haptic, effect):
    """
    ``int SDL_HapticEffectSupported(SDL_Haptic *, SDL_HapticEffect *)``
    
    Checks to see if effect is supported by haptic.
    
    :param haptic: Haptic device to check on.
    :param effect: Effect to check to see if it is supported.
    :return: SDL_TRUE if effect is supported, SDL_FALSE if it isn't or -1
        on error.
    
    See also SDL_HapticQuery
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    effect_c = unbox(effect, 'SDL_HapticEffect *')
    rc = _LIB.SDL_HapticEffectSupported(haptic_c, effect_c)
    return rc

def SDL_HapticGetEffectStatus(haptic, effect):
    """
    ``int SDL_HapticGetEffectStatus(SDL_Haptic *, int)``
    
    Gets the status of the current effect on the haptic device.
    
    Device must support the SDL_HAPTIC_STATUS feature.
    
    :param haptic: Haptic device to query the effect status on.
    :param effect: Identifier of the effect to query its status.
    :return: 0 if it isn't playing, 1 if it is playing or -1 on error.
    
    See also SDL_HapticRunEffect
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    effect_c = effect
    rc = _LIB.SDL_HapticGetEffectStatus(haptic_c, effect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticIndex(haptic):
    """
    ``int SDL_HapticIndex(SDL_Haptic *)``
    
    Gets the index of a haptic device.
    
    :param haptic: Haptic device to get the index of.
    :return: The index of the haptic device or -1 on error.
    
    See also SDL_HapticOpen
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticIndex(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticName(device_index):
    """
    ``char const * SDL_HapticName(int)``
    
    Get the implementation dependent name of a Haptic device.
    
    This can be called before any joysticks are opened. If no name can be
    found, this function returns NULL.
    
    :param device_index: Index of the device to get its name.
    :return: Name of the device or NULL on error.
    
    See also SDL_NumHaptics
    """
    device_index_c = device_index
    rc = _LIB.SDL_HapticName(device_index_c)
    if rc == ffi.NULL: raise SDLError()
    return ffi.string(rc).decode('utf-8')

def SDL_HapticNewEffect(haptic, effect):
    """
    ``int SDL_HapticNewEffect(SDL_Haptic *, SDL_HapticEffect *)``
    
    Creates a new haptic effect on the device.
    
    :param haptic: Haptic device to create the effect on.
    :param effect: Properties of the effect to create.
    :return: The id of the effect on success or -1 on error.
    
    See also SDL_HapticUpdateEffect
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    effect_c = unbox(effect, 'SDL_HapticEffect *')
    rc = _LIB.SDL_HapticNewEffect(haptic_c, effect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticNumAxes(haptic):
    """
    ``int SDL_HapticNumAxes(SDL_Haptic *)``
    
    Gets the number of haptic axes the device has.
    
    See also SDL_HapticDirection
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticNumAxes(haptic_c)
    return rc

def SDL_HapticNumEffects(haptic):
    """
    ``int SDL_HapticNumEffects(SDL_Haptic *)``
    
    Returns the number of effects a haptic device can store.
    
    On some platforms this isn't fully supported, and therefore is an
    approximation. Always check to see if your created effect was actually
    created and do not rely solely on SDL_HapticNumEffects().
    
    :param haptic: The haptic device to query effect max.
    :return: The number of effects the haptic device can store or -1 on
        error.
    
    See also SDL_HapticNumEffectsPlaying
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticNumEffects(haptic_c)
    return rc

def SDL_HapticNumEffectsPlaying(haptic):
    """
    ``int SDL_HapticNumEffectsPlaying(SDL_Haptic *)``
    
    Returns the number of effects a haptic device can play at the same
    time.
    
    This is not supported on all platforms, but will always return a
    value. Added here for the sake of completeness.
    
    :param haptic: The haptic device to query maximum playing effects.
    :return: The number of effects the haptic device can play at the same
        time or -1 on error.
    
    See also SDL_HapticNumEffects
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticNumEffectsPlaying(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticOpen(device_index):
    """
    ``SDL_Haptic * SDL_HapticOpen(int)``
    
    Opens a Haptic device for usage.
    
    The index passed as an argument refers to the N'th Haptic device on
    this system.
    
    When opening a haptic device, its gain will be set to maximum and
    autocenter will be disabled. To modify these values use
    SDL_HapticSetGain() and SDL_HapticSetAutocenter().
    
    :param device_index: Index of the device to open.
    :return: Device identifier or NULL on error.
    
    See also SDL_HapticIndex
    """
    device_index_c = device_index
    rc = _LIB.SDL_HapticOpen(device_index_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Haptic(rc)

def SDL_HapticOpenFromJoystick(joystick):
    """
    ``SDL_Haptic * SDL_HapticOpenFromJoystick(SDL_Joystick *)``
    
    Opens a Haptic device for usage from a Joystick device.
    
    You must still close the haptic device seperately. It will not be
    closed with the joystick.
    
    When opening from a joystick you should first close the haptic device
    before closing the joystick device. If not, on some implementations
    the haptic device will also get unallocated and you'll be unable to
    use force feedback on that device.
    
    :param joystick: Joystick to create a haptic device from.
    :return: A valid haptic device identifier on success or NULL on error.
    
    See also SDL_HapticOpen
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_HapticOpenFromJoystick(joystick_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Haptic(rc)

def SDL_HapticOpenFromMouse():
    """
    ``SDL_Haptic * SDL_HapticOpenFromMouse(void)``
    
    Tries to open a haptic device from the current mouse.
    
    :return: The haptic device identifier or NULL on error.
    
    See also SDL_MouseIsHaptic
    """
    rc = _LIB.SDL_HapticOpenFromMouse()
    if rc == ffi.NULL: raise SDLError()
    return SDL_Haptic(rc)

def SDL_HapticOpened(device_index):
    """
    ``int SDL_HapticOpened(int)``
    
    Checks if the haptic device at index has been opened.
    
    :param device_index: Index to check to see if it has been opened.
    :return: 1 if it has been opened or 0 if it hasn't.
    
    See also SDL_HapticOpen
    """
    device_index_c = device_index
    rc = _LIB.SDL_HapticOpened(device_index_c)
    return rc

def SDL_HapticPause(haptic):
    """
    ``int SDL_HapticPause(SDL_Haptic *)``
    
    Pauses a haptic device.
    
    Device must support the SDL_HAPTIC_PAUSE feature. Call
    SDL_HapticUnpause() to resume playback.
    
    Do not modify the effects nor add new ones while the device is paused.
    That can cause all sorts of weird errors.
    
    :param haptic: Haptic device to pause.
    :return: 0 on success or -1 on error.
    
    See also SDL_HapticUnpause
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticPause(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticQuery(haptic):
    """
    ``unsigned int SDL_HapticQuery(SDL_Haptic *)``
    
    Gets the haptic devices supported features in bitwise matter.
    
    Example: ::
    
       if (SDL_HapticQuery(haptic) & SDL_HAPTIC_CONSTANT) {
           printf("We have constant haptic effect!");
       }
    
    
    :param haptic: The haptic device to query.
    :return: Haptic features in bitwise manner (OR'd).
    
    See also SDL_HapticNumEffects
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticQuery(haptic_c)
    return rc

def SDL_HapticRumbleInit(haptic):
    """
    ``int SDL_HapticRumbleInit(SDL_Haptic *)``
    
    Initializes the haptic device for simple rumble playback.
    
    :param haptic: Haptic device to initialize for simple rumble playback.
    :return: 0 on success or -1 on error.
    
    See also SDL_HapticOpen
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticRumbleInit(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticRumblePlay(haptic, strength, length):
    """
    ``int SDL_HapticRumblePlay(SDL_Haptic *, float, uint32_t)``
    
    Runs simple rumble on a haptic device.
    
    :param haptic: Haptic device to play rumble effect on.
    :param strength: Strength of the rumble to play as a 0-1 float value.
    :param length: Length of the rumble to play in milliseconds.
    :return: 0 on success or -1 on error.
    
    See also SDL_HapticRumbleSupported
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
    
    Stops the simple rumble on a haptic device.
    
    :param haptic: Haptic to stop the rumble on.
    :return: 0 on success or -1 on error.
    
    See also SDL_HapticRumbleSupported
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticRumbleStop(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticRumbleSupported(haptic):
    """
    ``int SDL_HapticRumbleSupported(SDL_Haptic *)``
    
    Checks to see if rumble is supported on a haptic device.
    
    :param haptic: Haptic device to check to see if it supports rumble.
    :return: SDL_TRUE if effect is supported, SDL_FALSE if it isn't or -1
        on error.
    
    See also SDL_HapticRumbleInit
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticRumbleSupported(haptic_c)
    return rc

def SDL_HapticRunEffect(haptic, effect, iterations):
    """
    ``int SDL_HapticRunEffect(SDL_Haptic *, int, uint32_t)``
    
    Runs the haptic effect on its associated haptic device.
    
    If iterations are SDL_HAPTIC_INFINITY, it'll run the effect over and
    over repeating the envelope (attack and fade) every time. If you only
    want the effect to last forever, set SDL_HAPTIC_INFINITY in the
    effect's length parameter.
    
    :param haptic: Haptic device to run the effect on.
    :param effect: Identifier of the haptic effect to run.
    :param iterations: Number of iterations to run the effect. Use
        SDL_HAPTIC_INFINITY for infinity.
    :return: 0 on success or -1 on error.
    
    See also SDL_HapticStopEffect
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
    
    Sets the global autocenter of the device.
    
    Autocenter should be between 0 and 100. Setting it to 0 will disable
    autocentering.
    
    Device must support the SDL_HAPTIC_AUTOCENTER feature.
    
    :param haptic: Haptic device to set autocentering on.
    :param autocenter: Value to set autocenter to, 0 disables
        autocentering.
    :return: 0 on success or -1 on error.
    
    See also SDL_HapticQuery
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    autocenter_c = autocenter
    rc = _LIB.SDL_HapticSetAutocenter(haptic_c, autocenter_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticSetGain(haptic, gain):
    """
    ``int SDL_HapticSetGain(SDL_Haptic *, int)``
    
    Sets the global gain of the device.
    
    Device must support the SDL_HAPTIC_GAIN feature.
    
    The user may specify the maximum gain by setting the environment
    variable SDL_HAPTIC_GAIN_MAX which should be between 0 and 100. All
    calls to SDL_HapticSetGain() will scale linearly using
    SDL_HAPTIC_GAIN_MAX as the maximum.
    
    :param haptic: Haptic device to set the gain on.
    :param gain: Value to set the gain to, should be between 0 and 100.
    :return: 0 on success or -1 on error.
    
    See also SDL_HapticQuery
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    gain_c = gain
    rc = _LIB.SDL_HapticSetGain(haptic_c, gain_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticStopAll(haptic):
    """
    ``int SDL_HapticStopAll(SDL_Haptic *)``
    
    Stops all the currently playing effects on a haptic device.
    
    :param haptic: Haptic device to stop.
    :return: 0 on success or -1 on error.
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticStopAll(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticStopEffect(haptic, effect):
    """
    ``int SDL_HapticStopEffect(SDL_Haptic *, int)``
    
    Stops the haptic effect on its associated haptic device.
    
    :param haptic: Haptic device to stop the effect on.
    :param effect: Identifier of the effect to stop.
    :return: 0 on success or -1 on error.
    
    See also SDL_HapticRunEffect
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    effect_c = effect
    rc = _LIB.SDL_HapticStopEffect(haptic_c, effect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticUnpause(haptic):
    """
    ``int SDL_HapticUnpause(SDL_Haptic *)``
    
    Unpauses a haptic device.
    
    Call to unpause after SDL_HapticPause().
    
    :param haptic: Haptic device to pause.
    :return: 0 on success or -1 on error.
    
    See also SDL_HapticPause
    """
    haptic_c = unbox(haptic, 'SDL_Haptic *')
    rc = _LIB.SDL_HapticUnpause(haptic_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_HapticUpdateEffect(haptic, effect, data):
    """
    ``int SDL_HapticUpdateEffect(SDL_Haptic *, int, SDL_HapticEffect *)``
    
    Updates the properties of an effect.
    
    Can be used dynamically, although behaviour when dynamically changing
    direction may be strange. Specifically the effect may reupload itself
    and start playing from the start. You cannot change the type either
    when running SDL_HapticUpdateEffect().
    
    :param haptic: Haptic device that has the effect.
    :param effect: Effect to update.
    :param data: New effect properties to use.
    :return: 0 on success or -1 on error.
    
    See also SDL_HapticNewEffect
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
    
    This function returns true if the CPU has 3DNow! features.
    """
    rc = _LIB.SDL_Has3DNow()
    return rc

def SDL_HasAltiVec():
    """
    ``SDL_bool SDL_HasAltiVec(void)``
    
    This function returns true if the CPU has AltiVec features.
    """
    rc = _LIB.SDL_HasAltiVec()
    return rc

def SDL_HasClipboardText():
    """
    ``SDL_bool SDL_HasClipboardText(void)``
    
    Returns a flag indicating whether the clipboard exists and contains a
    text string that is non-empty.
    
    See also SDL_GetClipboardText()
    """
    rc = _LIB.SDL_HasClipboardText()
    return rc

def SDL_HasEvent(type):
    """
    ``SDL_bool SDL_HasEvent(uint32_t)``
    
    Checks to see if certain event types are in the event queue.
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
    
    Determine whether two rectangles intersect.
    
    :return: SDL_TRUE if there is an intersection, SDL_FALSE otherwise.
    """
    A_c = unbox(A, 'SDL_Rect const *')
    B_c = unbox(B, 'SDL_Rect const *')
    rc = _LIB.SDL_HasIntersection(A_c, B_c)
    return rc

def SDL_HasMMX():
    """
    ``SDL_bool SDL_HasMMX(void)``
    
    This function returns true if the CPU has MMX features.
    """
    rc = _LIB.SDL_HasMMX()
    return rc

def SDL_HasRDTSC():
    """
    ``SDL_bool SDL_HasRDTSC(void)``
    
    This function returns true if the CPU has the RDTSC instruction.
    """
    rc = _LIB.SDL_HasRDTSC()
    return rc

def SDL_HasSSE():
    """
    ``SDL_bool SDL_HasSSE(void)``
    
    This function returns true if the CPU has SSE features.
    """
    rc = _LIB.SDL_HasSSE()
    return rc

def SDL_HasSSE2():
    """
    ``SDL_bool SDL_HasSSE2(void)``
    
    This function returns true if the CPU has SSE2 features.
    """
    rc = _LIB.SDL_HasSSE2()
    return rc

def SDL_HasSSE3():
    """
    ``SDL_bool SDL_HasSSE3(void)``
    
    This function returns true if the CPU has SSE3 features.
    """
    rc = _LIB.SDL_HasSSE3()
    return rc

def SDL_HasSSE41():
    """
    ``SDL_bool SDL_HasSSE41(void)``
    
    This function returns true if the CPU has SSE4.1 features.
    """
    rc = _LIB.SDL_HasSSE41()
    return rc

def SDL_HasSSE42():
    """
    ``SDL_bool SDL_HasSSE42(void)``
    
    This function returns true if the CPU has SSE4.2 features.
    """
    rc = _LIB.SDL_HasSSE42()
    return rc

def SDL_HasScreenKeyboardSupport():
    """
    ``SDL_bool SDL_HasScreenKeyboardSupport(void)``
    
    Returns whether the platform has some screen keyboard support.
    
    :return: SDL_TRUE if some keyboard support is available else
        SDL_FALSE.
    
    Not all screen keyboard functions are supported on all platforms.
    
    See also SDL_IsScreenKeyboardShown()
    """
    rc = _LIB.SDL_HasScreenKeyboardSupport()
    return rc

def SDL_HideWindow(window):
    """
    ``void SDL_HideWindow(SDL_Window *)``
    
    Hide a window.
    
    See also SDL_ShowWindow()
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_HideWindow(window_c)

def SDL_Init(flags):
    """
    ``int SDL_Init(uint32_t)``
    
    This function initializes the subsystems specified by flags Unless the
    SDL_INIT_NOPARACHUTE flag is set, it will install cleanup signal
    handlers for some commonly ignored fatal signals (like SIGSEGV).
    """
    flags_c = flags
    rc = _LIB.SDL_Init(flags_c)
    return rc

def SDL_InitSubSystem(flags):
    """
    ``int SDL_InitSubSystem(uint32_t)``
    
    This function initializes specific SDL subsystems
    """
    flags_c = flags
    rc = _LIB.SDL_InitSubSystem(flags_c)
    return rc

def SDL_IntersectRect(A, B, result):
    """
    ``SDL_bool SDL_IntersectRect(SDL_Rect const *, SDL_Rect const *, SDL_Rect *)``
    
    Calculate the intersection of two rectangles.
    
    :return: SDL_TRUE if there is an intersection, SDL_FALSE otherwise.
    """
    A_c = unbox(A, 'SDL_Rect const *')
    B_c = unbox(B, 'SDL_Rect const *')
    result_c = unbox(result, 'SDL_Rect *')
    rc = _LIB.SDL_IntersectRect(A_c, B_c, result_c)
    return rc

def SDL_IntersectRectAndLine(rect, X1=None, Y1=None, X2=None, Y2=None):
    """
    ``SDL_bool SDL_IntersectRectAndLine(SDL_Rect const *, int *, int *, int *, int *)``
    
    Calculate the intersection of a rectangle and line segment.
    
    :return: SDL_TRUE if there is an intersection, SDL_FALSE otherwise.
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
    
    Is the joystick on this index supported by the game controller
    interface?
    """
    joystick_index_c = joystick_index
    rc = _LIB.SDL_IsGameController(joystick_index_c)
    return rc

def SDL_IsScreenKeyboardShown(window):
    """
    ``SDL_bool SDL_IsScreenKeyboardShown(SDL_Window *)``
    
    Returns whether the screen keyboard is shown for given window.
    
    :param window: The window for which screen keyboard should be queried.
    :return: SDL_TRUE if screen keyboard is shown else SDL_FALSE.
    
    See also SDL_HasScreenKeyboardSupport()
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_IsScreenKeyboardShown(window_c)
    return rc

def SDL_IsScreenSaverEnabled():
    """
    ``SDL_bool SDL_IsScreenSaverEnabled(void)``
    
    Returns whether the screensaver is currently enabled (default on).
    
    See also SDL_EnableScreenSaver()
    """
    rc = _LIB.SDL_IsScreenSaverEnabled()
    return rc

def SDL_IsTextInputActive():
    """
    ``SDL_bool SDL_IsTextInputActive(void)``
    
    Return whether or not Unicode text input events are enabled.
    
    See also SDL_StartTextInput()
    """
    rc = _LIB.SDL_IsTextInputActive()
    return rc

def SDL_JoystickClose(joystick):
    """
    ``void SDL_JoystickClose(SDL_Joystick *)``
    
    Close a joystick previously opened with SDL_JoystickOpen().
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    _LIB.SDL_JoystickClose(joystick_c)

def SDL_JoystickEventState(state):
    """
    ``int SDL_JoystickEventState(int)``
    
    Enable/disable joystick event polling.
    
    If joystick events are disabled, you must call SDL_JoystickUpdate()
    yourself and check the state of the joystick when you want joystick
    information.
    
    The state can be one of SDL_QUERY, SDL_ENABLE or SDL_IGNORE.
    """
    state_c = state
    rc = _LIB.SDL_JoystickEventState(state_c)
    return rc

def SDL_JoystickGetAttached(joystick):
    """
    ``SDL_bool SDL_JoystickGetAttached(SDL_Joystick *)``
    
    Returns SDL_TRUE if the joystick has been opened and currently
    connected, or SDL_FALSE if it has not.
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickGetAttached(joystick_c)
    return rc

def SDL_JoystickGetAxis(joystick, axis):
    """
    ``int16_t SDL_JoystickGetAxis(SDL_Joystick *, int)``
    
    Get the current state of an axis control on a joystick.
    
    The state is a value ranging from -32768 to 32767.
    
    The axis indices start at index 0.
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    axis_c = axis
    rc = _LIB.SDL_JoystickGetAxis(joystick_c, axis_c)
    return rc

def SDL_JoystickGetBall(joystick, ball, dx=None, dy=None):
    """
    ``int SDL_JoystickGetBall(SDL_Joystick *, int, int *, int *)``
    
    Get the ball axis change since the last poll.
    
    :return: 0, or -1 if you passed it invalid parameters.
    
    The ball indices start at index 0.
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
    
    Get the current state of a button on a joystick.
    
    The button indices start at index 0.
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    button_c = button
    rc = _LIB.SDL_JoystickGetButton(joystick_c, button_c)
    return rc

def SDL_JoystickGetDeviceGUID(device_index):
    """
    ``SDL_JoystickGUID SDL_JoystickGetDeviceGUID(int)``
    
    Return the GUID for the joystick at this index
    """
    device_index_c = device_index
    rc = _LIB.SDL_JoystickGetDeviceGUID(device_index_c)
    return SDL_JoystickGUID(rc)

def SDL_JoystickGetGUID(joystick):
    """
    ``SDL_JoystickGUID SDL_JoystickGetGUID(SDL_Joystick *)``
    
    Return the GUID for this opened joystick
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickGetGUID(joystick_c)
    return SDL_JoystickGUID(rc)

def SDL_JoystickGetGUIDFromString(pchGUID):
    """
    ``SDL_JoystickGUID SDL_JoystickGetGUIDFromString(char const *)``
    
    convert a string into a joystick formatted guid
    """
    pchGUID_c = u8(pchGUID)
    rc = _LIB.SDL_JoystickGetGUIDFromString(pchGUID_c)
    return SDL_JoystickGUID(rc)

def SDL_JoystickGetGUIDString(guid, pszGUID, cbGUID):
    """
    ``void SDL_JoystickGetGUIDString(SDL_JoystickGUID, char *, int)``
    
    Return a string representation for this guid. pszGUID must point to at
    least 33 bytes (32 for the string plus a NULL terminator).
    """
    guid_c = unbox(guid, 'SDL_JoystickGUID')
    pszGUID_c = u8(pszGUID)
    cbGUID_c = cbGUID
    _LIB.SDL_JoystickGetGUIDString(guid_c, pszGUID_c, cbGUID_c)

def SDL_JoystickGetHat(joystick, hat):
    """
    ``uint8_t SDL_JoystickGetHat(SDL_Joystick *, int)``
    
    Get the current state of a POV hat on a joystick.
    
    The hat indices start at index 0.
    
    :return: The return value is one of the following positions:
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    hat_c = hat
    rc = _LIB.SDL_JoystickGetHat(joystick_c, hat_c)
    return rc

def SDL_JoystickInstanceID(joystick):
    """
    ``int32_t SDL_JoystickInstanceID(SDL_Joystick *)``
    
    Get the instance ID of an opened joystick or -1 if the joystick is
    invalid.
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickInstanceID(joystick_c)
    return rc

def SDL_JoystickIsHaptic(joystick):
    """
    ``int SDL_JoystickIsHaptic(SDL_Joystick *)``
    
    Checks to see if a joystick has haptic features.
    
    :param joystick: Joystick to test for haptic capabilities.
    :return: 1 if the joystick is haptic, 0 if it isn't or -1 if an error
        ocurred.
    
    See also SDL_HapticOpenFromJoystick
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickIsHaptic(joystick_c)
    return rc

def SDL_JoystickName(joystick):
    """
    ``char const * SDL_JoystickName(SDL_Joystick *)``
    
    Return the name for this currently opened joystick. If no name can be
    found, this function returns NULL.
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickName(joystick_c)
    return ffi.string(rc).decode('utf-8')

def SDL_JoystickNameForIndex(device_index):
    """
    ``char const * SDL_JoystickNameForIndex(int)``
    
    Get the implementation dependent name of a joystick. This can be
    called before any joysticks are opened. If no name can be found, this
    function returns NULL.
    """
    device_index_c = device_index
    rc = _LIB.SDL_JoystickNameForIndex(device_index_c)
    return ffi.string(rc).decode('utf-8')

def SDL_JoystickNumAxes(joystick):
    """
    ``int SDL_JoystickNumAxes(SDL_Joystick *)``
    
    Get the number of general axis controls on a joystick.
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickNumAxes(joystick_c)
    return rc

def SDL_JoystickNumBalls(joystick):
    """
    ``int SDL_JoystickNumBalls(SDL_Joystick *)``
    
    Get the number of trackballs on a joystick.
    
    Joystick trackballs have only relative motion events associated with
    them and their state cannot be polled.
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickNumBalls(joystick_c)
    return rc

def SDL_JoystickNumButtons(joystick):
    """
    ``int SDL_JoystickNumButtons(SDL_Joystick *)``
    
    Get the number of buttons on a joystick.
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickNumButtons(joystick_c)
    return rc

def SDL_JoystickNumHats(joystick):
    """
    ``int SDL_JoystickNumHats(SDL_Joystick *)``
    
    Get the number of POV hats on a joystick.
    """
    joystick_c = unbox(joystick, 'SDL_Joystick *')
    rc = _LIB.SDL_JoystickNumHats(joystick_c)
    return rc

def SDL_JoystickOpen(device_index):
    """
    ``SDL_Joystick * SDL_JoystickOpen(int)``
    
    Open a joystick for use. The index passed as an argument refers tothe
    N'th joystick on the system. This index is the value which will
    identify this joystick in future joystick events.
    
    :return: A joystick identifier, or NULL if an error occurred.
    """
    device_index_c = device_index
    rc = _LIB.SDL_JoystickOpen(device_index_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Joystick(rc)

def SDL_JoystickUpdate():
    """
    ``void SDL_JoystickUpdate(void)``
    
    Update the current state of the open joysticks.
    
    This is called automatically by the event loop if any joystick events
    are enabled.
    """
    _LIB.SDL_JoystickUpdate()

def SDL_LoadBMP_RW(src, freesrc):
    """
    ``SDL_Surface * SDL_LoadBMP_RW(SDL_RWops *, int)``
    
    Load a surface from a seekable SDL data stream (memory or file).
    
    If freesrc is non-zero, the stream will be closed after being read.
    
    The new surface should be freed with SDL_FreeSurface().
    
    :return: the new surface, or NULL if there was an error.
    """
    src_c = unbox(src, 'SDL_RWops *')
    freesrc_c = freesrc
    rc = _LIB.SDL_LoadBMP_RW(src_c, freesrc_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def SDL_LoadDollarTemplates(touchId, src):
    """
    ``int SDL_LoadDollarTemplates(int64_t, SDL_RWops *)``
    
    Load Dollar Gesture templates from a file.
    """
    touchId_c = touchId
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_LoadDollarTemplates(touchId_c, src_c)
    return rc

def SDL_LoadFunction(handle, name):
    """
    ``void * SDL_LoadFunction(void *, char const *)``
    
    Given an object handle, this function looks up the address of the
    named function in the shared object and returns it. This address is no
    longer valid after calling SDL_UnloadObject().
    """
    handle_c = unbox(handle, 'void *')
    name_c = u8(name)
    rc = _LIB.SDL_LoadFunction(handle_c, name_c)
    return rc

def SDL_LoadObject(sofile):
    """
    ``void * SDL_LoadObject(char const *)``
    
    This function dynamically loads a shared object and returns a pointer
    to the object handle (or NULL if there was an error). The 'sofile'
    parameter is a system dependent name of the object file.
    """
    sofile_c = u8(sofile)
    rc = _LIB.SDL_LoadObject(sofile_c)
    if rc == ffi.NULL: raise SDLError()
    return rc

def SDL_LoadWAV_RW(src, freesrc, spec, audio_buf, audio_len=None):
    """
    ``SDL_AudioSpec * SDL_LoadWAV_RW(SDL_RWops *, int, SDL_AudioSpec *, uint8_t * *, uint32_t *)``
    
    This function loads a WAVE from the data source, automatically freeing
    that source if freesrc is non-zero. For example, to load a WAVE file,
    you could do: ::
    
           SDL_LoadWAV_RW(SDL_RWFromFile("sample.wav", "rb"), 1, ...);
    
    
    If this function succeeds, it returns the given SDL_AudioSpec, filled
    with the audio data format of the wave data, and sets *audio_buf to a
    malloc()'d buffer containing the audio data, and sets *audio_len to
    the length of that audio buffer, in bytes. You need to free the audio
    buffer with SDL_FreeWAV() when you are done with it.
    
    This function returns NULL and sets the SDL error message if the wave
    file cannot be opened, uses an unknown data format, or is corrupt.
    Currently raw and MS-ADPCM WAVE files are supported.
    """
    src_c = unbox(src, 'SDL_RWops *')
    freesrc_c = freesrc
    spec_c = unbox(spec, 'SDL_AudioSpec *')
    audio_buf_c = unbox(audio_buf, 'uint8_t * *')
    audio_len_c = unbox(audio_len, 'uint32_t *')
    rc = _LIB.SDL_LoadWAV_RW(src_c, freesrc_c, spec_c, audio_buf_c, audio_len_c)
    if rc == ffi.NULL: raise SDLError()
    return (SDL_AudioSpec(rc), audio_len_c[0])

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
    
    Sets up a surface for directly accessing the pixels.
    
    Between calls to SDL_LockSurface() / SDL_UnlockSurface(), you can
    write to and read from surface->pixels, using the pixel format stored
    in surface->format. Once you are done accessing the surface, you
    should use SDL_UnlockSurface() to release it.
    
    Not all surfaces require locking. If SDL_MUSTLOCK(surface) evaluates
    to 0, then you can read and write to the surface at any time, and the
    pixel format of the surface will not change.
    
    No operating system or library calls should be made between
    lock/unlock pairs, as critical system locks may be held during this
    time.
    
    SDL_LockSurface() returns 0, or -1 if the surface couldn't be locked.
    
    See also SDL_UnlockSurface()
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    rc = _LIB.SDL_LockSurface(surface_c)
    return rc

def SDL_LockTexture(texture, rect, pixels, pitch=None):
    """
    ``int SDL_LockTexture(SDL_Texture *, SDL_Rect const *, void * *, int *)``
    
    Lock a portion of the texture for write-only pixel access.
    
    :param texture: The texture to lock for access, which was created with
        SDL_TEXTUREACCESS_STREAMING.
    :param rect: A pointer to the rectangle to lock for access. If the
        rect is NULL, the entire texture will be locked.
    :param pixels: This is filled in with a pointer to the locked pixels,
        appropriately offset by the locked area.
    :param pitch: This is filled in with the pitch of the locked pixels.
    :return: 0 on success, or -1 if the texture is not valid or was not
        created with
    
    See also SDL_UnlockTexture()
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
    
    Log a message with SDL_LOG_CATEGORY_APPLICATION and
    SDL_LOG_PRIORITY_INFO.
    """
    fmt_c = u8(fmt)
    _LIB.SDL_Log(fmt_c)

def SDL_LogCritical(category, fmt):
    """
    ``void SDL_LogCritical(int, char const *, ...)``
    
    Log a message with SDL_LOG_PRIORITY_CRITICAL.
    """
    category_c = category
    fmt_c = u8(fmt)
    _LIB.SDL_LogCritical(category_c, fmt_c)

def SDL_LogDebug(category, fmt):
    """
    ``void SDL_LogDebug(int, char const *, ...)``
    
    Log a message with SDL_LOG_PRIORITY_DEBUG.
    """
    category_c = category
    fmt_c = u8(fmt)
    _LIB.SDL_LogDebug(category_c, fmt_c)

def SDL_LogError(category, fmt):
    """
    ``void SDL_LogError(int, char const *, ...)``
    
    Log a message with SDL_LOG_PRIORITY_ERROR.
    """
    category_c = category
    fmt_c = u8(fmt)
    _LIB.SDL_LogError(category_c, fmt_c)

def SDL_LogGetOutputFunction(callback, userdata):
    """
    ``void SDL_LogGetOutputFunction(void(* *)(void *, int, SDL_LogPriority, char const *), void * *)``
    
    Get the current log output function.
    """
    callback_c = unbox(callback, 'void(* *)(void *, int, SDL_LogPriority, char const *)')
    userdata_c = unbox(userdata, 'void * *')
    _LIB.SDL_LogGetOutputFunction(callback_c, userdata_c)

def SDL_LogGetPriority(category):
    """
    ``SDL_LogPriority SDL_LogGetPriority(int)``
    
    Get the priority of a particular log category.
    """
    category_c = category
    rc = _LIB.SDL_LogGetPriority(category_c)
    return rc

def SDL_LogInfo(category, fmt):
    """
    ``void SDL_LogInfo(int, char const *, ...)``
    
    Log a message with SDL_LOG_PRIORITY_INFO.
    """
    category_c = category
    fmt_c = u8(fmt)
    _LIB.SDL_LogInfo(category_c, fmt_c)

def SDL_LogMessage(category, priority, fmt):
    """
    ``void SDL_LogMessage(int, SDL_LogPriority, char const *, ...)``
    
    Log a message with the specified category and priority.
    """
    category_c = category
    priority_c = priority
    fmt_c = u8(fmt)
    _LIB.SDL_LogMessage(category_c, priority_c, fmt_c)

def SDL_LogMessageV(category, priority, fmt, ap):
    """
    ``void SDL_LogMessageV(int, SDL_LogPriority, char const *, int32_t)``
    
    Log a message with the specified category and priority.
    """
    category_c = category
    priority_c = priority
    fmt_c = u8(fmt)
    ap_c = ap
    _LIB.SDL_LogMessageV(category_c, priority_c, fmt_c, ap_c)

def SDL_LogResetPriorities():
    """
    ``void SDL_LogResetPriorities(void)``
    
    Reset all priorities to default.
    
    This is called in SDL_Quit().
    """
    _LIB.SDL_LogResetPriorities()

def SDL_LogSetAllPriority(priority):
    """
    ``void SDL_LogSetAllPriority(SDL_LogPriority)``
    
    Set the priority of all log categories.
    """
    priority_c = priority
    _LIB.SDL_LogSetAllPriority(priority_c)

def SDL_LogSetOutputFunction(callback, userdata):
    """
    ``void SDL_LogSetOutputFunction(void SDL_LogSetOutputFunction(void *, int, SDL_LogPriority, char const *), void *)``
    
    This function allows you to replace the default log output function
    with one of your own.
    """
    callback_c = unbox(callback, 'void(*)(void *, int, SDL_LogPriority, char const *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_LogSetOutputFunction(callback_c, userdata_c)

def SDL_LogSetPriority(category, priority):
    """
    ``void SDL_LogSetPriority(int, SDL_LogPriority)``
    
    Set the priority of a particular log category.
    """
    category_c = category
    priority_c = priority
    _LIB.SDL_LogSetPriority(category_c, priority_c)

def SDL_LogVerbose(category, fmt):
    """
    ``void SDL_LogVerbose(int, char const *, ...)``
    
    Log a message with SDL_LOG_PRIORITY_VERBOSE.
    """
    category_c = category
    fmt_c = u8(fmt)
    _LIB.SDL_LogVerbose(category_c, fmt_c)

def SDL_LogWarn(category, fmt):
    """
    ``void SDL_LogWarn(int, char const *, ...)``
    
    Log a message with SDL_LOG_PRIORITY_WARN.
    """
    category_c = category
    fmt_c = u8(fmt)
    _LIB.SDL_LogWarn(category_c, fmt_c)

def SDL_LowerBlit(src, srcrect, dst, dstrect):
    """
    ``int SDL_LowerBlit(SDL_Surface *, SDL_Rect *, SDL_Surface *, SDL_Rect *)``
    
    This is a semi-private blit function and it performs low-level surface
    blitting only.
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
    
    This is a semi-private blit function and it performs low-level surface
    scaled blitting only.
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
    
    Maps an RGB triple to an opaque pixel value for a given pixel format.
    
    See also SDL_MapRGBA
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
    
    Maps an RGBA quadruple to a pixel value for a given pixel format.
    
    See also SDL_MapRGB
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
    
    Convert a bpp and RGBA masks to an enumerated pixel format.
    
    :return: The pixel format, or
    
    See also SDL_PixelFormatEnumToMasks()
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
    
    Make a window as large as possible.
    
    See also SDL_RestoreWindow()
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_MaximizeWindow(window_c)

def SDL_MinimizeWindow(window):
    """
    ``void SDL_MinimizeWindow(SDL_Window *)``
    
    Minimize a window to an iconic representation.
    
    See also SDL_RestoreWindow()
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_MinimizeWindow(window_c)

def SDL_MixAudio(dst, src, len, volume):
    """
    ``void SDL_MixAudio(uint8_t *, uint8_t const *, uint32_t, int)``
    
    This takes two audio buffers of the playing audio format and mixes
    them, performing addition, volume adjustment, and overflow clipping.
    The volume ranges from 0 - 128, and should be set to SDL_MIX_MAXVOLUME
    for full audio volume. Note this does not change hardware volume. This
    is provided for convenience  you can mix your own audio data.
    """
    dst_c = unbox(dst, 'uint8_t *')
    src_c = unbox(src, 'uint8_t const *')
    len_c = len
    volume_c = volume
    _LIB.SDL_MixAudio(dst_c, src_c, len_c, volume_c)

def SDL_MixAudioFormat(dst, src, format, len, volume):
    """
    ``void SDL_MixAudioFormat(uint8_t *, uint8_t const *, uint16_t, uint32_t, int)``
    
    This works like SDL_MixAudio(), but you specify the audio format
    instead of using the format of audio device 1. Thus it can be used
    when no audio device is open at all.
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
    
    Gets whether or not the current mouse has haptic capabilities.
    
    :return: SDL_TRUE if the mouse is haptic, SDL_FALSE if it isn't.
    
    See also SDL_HapticOpenFromMouse
    """
    rc = _LIB.SDL_MouseIsHaptic()
    return rc

def SDL_NumHaptics():
    """
    ``int SDL_NumHaptics(void)``
    
    Count the number of haptic devices attached to the system.
    
    :return: Number of haptic devices detected on the system.
    """
    rc = _LIB.SDL_NumHaptics()
    return rc

def SDL_NumJoysticks():
    """
    ``int SDL_NumJoysticks(void)``
    
    Count the number of joysticks attached to the system right now
    """
    rc = _LIB.SDL_NumJoysticks()
    return rc

def SDL_OpenAudio(desired, obtained):
    """
    ``int SDL_OpenAudio(SDL_AudioSpec *, SDL_AudioSpec *)``
    
    This function opens the audio device with the desired parameters, and
    returns 0 if successful, placing the actual hardware parameters in the
    structure pointed to by obtained. If obtained is NULL, the audio data
    passed to the callback function will be guaranteed to be in the
    requested format, and will be automatically converted to the hardware
    audio format if necessary. This function returns -1 if it failed to
    open the audio device, or couldn't set up the audio thread.
    
    When filling in the desired audio spec structure,desired->freq should
    be the desired audio frequency in samples-per- second.
    
    desired->format should be the desired audio format.
    
    desired->samples is the desired size of the audio buffer, in samples.
    This number should be a power of two, and may be adjusted by the audio
    driver to a value more suitable for the hardware. Good values seem to
    range between 512 and 8096 inclusive, depending on the application and
    CPU speed. Smaller values yield faster response time, but can lead to
    underflow if the application is doing heavy processing and cannot fill
    the audio buffer in time. A stereo sample consists of both right and
    left channels in LR ordering. Note that the number of samples is
    directly related to time by the following formula:::
    
    ms = (samples*1000)/freq
    
    desired->size is the size in bytes of the audio buffer, and is
    calculated by SDL_OpenAudio().
    
    desired->silence is the value used to set the buffer to silence, and
    is calculated by SDL_OpenAudio().
    
    desired->callback should be set to a function that will be called when
    the audio device is ready for more data. It is passed a pointer to the
    audio buffer, and the length in bytes of the audio buffer. This
    function usually runs in a separate thread, and so you should protect
    data structures that it accesses by calling SDL_LockAudio() and
    SDL_UnlockAudio() in your code.
    
    desired->userdata is passed as the first parameter to your callback
    function.
    
    The audio device starts out playing silence when it's opened, and
    should be enabled for playing by calling SDL_PauseAudio(0) when you
    are ready for your audio callback function to be called. Since the
    audio driver may modify the requested size of the audio buffer, you
    should allocate any local mixing buffers after you open the audio
    device.
    """
    desired_c = unbox(desired, 'SDL_AudioSpec *')
    obtained_c = unbox(obtained, 'SDL_AudioSpec *')
    rc = _LIB.SDL_OpenAudio(desired_c, obtained_c)
    return rc

def SDL_OpenAudioDevice(device, iscapture, desired, obtained, allowed_changes):
    """
    ``uint32_t SDL_OpenAudioDevice(char const *, int, SDL_AudioSpec const *, SDL_AudioSpec *, int)``
    
    Open a specific audio device. Passing in a device name of NULL
    requests the most reasonable default (and is equivalent to calling
    SDL_OpenAudio()).
    
    The device name is a UTF-8 string reported by
    SDL_GetAudioDeviceName(), but some drivers allow arbitrary and driver-
    specific strings, such as a hostname/IP address for a remote audio
    server, or a filename in the diskaudio driver.
    
    :return: 0 on error, a valid device ID that is >= 2 on success.
    
    SDL_OpenAudio(), unlike this function, always acts on device ID 1.
    """
    device_c = u8(device)
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
    
    Checks the event queue for messages and optionally returns them.
    
    If action is SDL_ADDEVENT, up to numevents events will be added to the
    back of the event queue.
    
    If action is SDL_PEEKEVENT, up to numevents events at the front of the
    event queue, within the specified minimum and maximum type, will be
    returned and will not be removed from the queue.
    
    If action is SDL_GETEVENT, up to numevents events at the front of the
    event queue, within the specified minimum and maximum type, will be
    returned and will be removed from the queue.
    
    :return: The number of events actually stored, or -1 if there was an
        error.
    
    This function is thread-safe.
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
    
    Convert one of the enumerated pixel formats to a bpp and RGBA masks.
    
    :return: SDL_TRUE, or SDL_FALSE if the conversion wasn't possible.
    
    See also SDL_MasksToPixelFormatEnum()
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
    
    Polls for currently pending events.
    
    :return: 1 if there are any pending events, or 0 if there are none
        available.
    :param event: If not NULL, the next event is removed from the queue
        and stored in that area.
    """
    event_c = unbox(event, 'SDL_Event *')
    rc = _LIB.SDL_PollEvent(event_c)
    return rc

def SDL_PumpEvents():
    """
    ``void SDL_PumpEvents(void)``
    
    Pumps the event loop, gathering events from the input devices.
    
    This function updates the event queue and internal input device state.
    
    This should only be run in the thread that sets the video mode.
    """
    _LIB.SDL_PumpEvents()

def SDL_PushEvent(event):
    """
    ``int SDL_PushEvent(SDL_Event *)``
    
    Add an event to the event queue.
    
    :return: 1 on success, 0 if the event was filtered, or -1 if the event
        queue was full or there was some other error.
    """
    event_c = unbox(event, 'SDL_Event *')
    rc = _LIB.SDL_PushEvent(event_c)
    return rc

def SDL_QueryTexture(texture, format=None, access=None, w=None, h=None):
    """
    ``int SDL_QueryTexture(SDL_Texture *, uint32_t *, int *, int *, int *)``
    
    Query the attributes of a texture.
    
    :param texture: A texture to be queried.
    :param format: A pointer filled in with the raw format of the texture.
        The actual format may differ, but pixel transfers will use this
        format.
    :param access: A pointer filled in with the actual access to the
        texture.
    :param w: A pointer filled in with the width of the texture in pixels.
    :param h: A pointer filled in with the height of the texture in
        pixels.
    :return: 0 on success, or -1 if the texture is not valid.
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
    
    This function cleans up all initialized subsystems. You should call it
    upon all exit conditions.
    """
    _LIB.SDL_Quit()

def SDL_QuitSubSystem(flags):
    """
    ``void SDL_QuitSubSystem(uint32_t)``
    
    This function cleans up specific SDL subsystems
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
    return SDL_RWops(rc)

def SDL_RWFromFP(fp, autoclose):
    """
    ``SDL_RWops * SDL_RWFromFP(FILE *, SDL_bool)``
    """
    fp_c = unbox(fp, 'FILE *')
    autoclose_c = autoclose
    rc = _LIB.SDL_RWFromFP(fp_c, autoclose_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_RWops(rc)

def SDL_RWFromFile(file, mode):
    """
    ``SDL_RWops * SDL_RWFromFile(char const *, char const *)``
    """
    file_c = u8(file)
    mode_c = u8(mode)
    rc = _LIB.SDL_RWFromFile(file_c, mode_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_RWops(rc)

def SDL_RWFromMem(mem, size):
    """
    ``SDL_RWops * SDL_RWFromMem(void *, int)``
    """
    mem_c = unbox(mem, 'void *')
    size_c = size
    rc = _LIB.SDL_RWFromMem(mem_c, size_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_RWops(rc)

def SDL_RaiseWindow(window):
    """
    ``void SDL_RaiseWindow(SDL_Window *)``
    
    Raise a window above other windows and set the input focus.
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
    
    Begin Recording a gesture on the specified touch, or all touches (-1)
    """
    touchId_c = touchId
    rc = _LIB.SDL_RecordGesture(touchId_c)
    return rc

def SDL_RegisterEvents(numevents):
    """
    ``uint32_t SDL_RegisterEvents(int)``
    
    This function allocates a set of user-defined events, and returns the
    beginning event number for that set of events.
    
    If there aren't enough user-defined events left, this function returns
    (Uint32)-1
    """
    numevents_c = numevents
    rc = _LIB.SDL_RegisterEvents(numevents_c)
    return rc

def SDL_RemoveTimer(id):
    """
    ``SDL_bool SDL_RemoveTimer(int)``
    
    Remove a timer knowing its ID.
    
    :return: A boolean value indicating success or failure.
    
    It is not safe to remove a timer multiple times.
    """
    id_c = id
    rc = _LIB.SDL_RemoveTimer(id_c)
    return rc

def SDL_RenderClear(renderer):
    """
    ``int SDL_RenderClear(SDL_Renderer *)``
    
    Clear the current rendering target with the drawing color.
    
    This function clears the entire rendering target, ignoring the
    viewport.
    
    :return: 0 on success, or -1 on error
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rc = _LIB.SDL_RenderClear(renderer_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderCopy(renderer, texture, srcrect, dstrect):
    """
    ``int SDL_RenderCopy(SDL_Renderer *, SDL_Texture *, SDL_Rect const *, SDL_Rect const *)``
    
    Copy a portion of the texture to the current rendering target.
    
    :param renderer: The renderer which should copy parts of a texture.
    :param texture: The source texture.
    :param srcrect: A pointer to the source rectangle, or NULL for the
        entire texture.
    :param dstrect: A pointer to the destination rectangle, or NULL for
        the entire rendering target.
    :return: 0 on success, or -1 on error
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *', nullable=True)
    texture_c = unbox(texture, 'SDL_Texture *', nullable=True)
    srcrect_c = unbox(srcrect, 'SDL_Rect const *', nullable=True)
    dstrect_c = unbox(dstrect, 'SDL_Rect const *', nullable=True)
    rc = _LIB.SDL_RenderCopy(renderer_c, texture_c, srcrect_c, dstrect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderCopyEx(renderer, texture, srcrect, dstrect, angle, center, flip):
    """
    ``int SDL_RenderCopyEx(SDL_Renderer *, SDL_Texture *, SDL_Rect const *, SDL_Rect const *, double, SDL_Point const *, SDL_RendererFlip)``
    
    Copy a portion of the source texture to the current rendering target,
    rotating it by angle around the given center.
    
    :param renderer: The renderer which should copy parts of a texture.
    :param texture: The source texture.
    :param srcrect: A pointer to the source rectangle, or NULL for the
        entire texture.
    :param dstrect: A pointer to the destination rectangle, or NULL for
        the entire rendering target.
    :param angle: An angle in degrees that indicates the rotation that
        will be applied to dstrect
    :param center: A pointer to a point indicating the point around which
        dstrect will be rotated (if NULL, rotation will be done aroud
        dstrect.w/2, dstrect.h/2)
    :param flip: An SDL_RendererFlip value stating which flipping actions
        should be performed on the texture
    :return: 0 on success, or -1 on error
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *', nullable=True)
    texture_c = unbox(texture, 'SDL_Texture *', nullable=True)
    srcrect_c = unbox(srcrect, 'SDL_Rect const *', nullable=True)
    dstrect_c = unbox(dstrect, 'SDL_Rect const *', nullable=True)
    angle_c = angle
    center_c = unbox(center, 'SDL_Point const *', nullable=True)
    flip_c = flip
    rc = _LIB.SDL_RenderCopyEx(renderer_c, texture_c, srcrect_c, dstrect_c, angle_c, center_c, flip_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderDrawLine(renderer, x1, y1, x2, y2):
    """
    ``int SDL_RenderDrawLine(SDL_Renderer *, int, int, int, int)``
    
    Draw a line on the current rendering target.
    
    :param renderer: The renderer which should draw a line.
    :param x1: The x coordinate of the start point.
    :param y1: The y coordinate of the start point.
    :param x2: The x coordinate of the end point.
    :param y2: The y coordinate of the end point.
    :return: 0 on success, or -1 on error
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
    
    Draw a series of connected lines on the current rendering target.
    
    :param renderer: The renderer which should draw multiple lines.
    :param points: The points along the lines
    :param count: The number of points, drawing count-1 lines
    :return: 0 on success, or -1 on error
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
    
    Draw a point on the current rendering target.
    
    :param renderer: The renderer which should draw a point.
    :param x: The x coordinate of the point.
    :param y: The y coordinate of the point.
    :return: 0 on success, or -1 on error
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
    
    Draw multiple points on the current rendering target.
    
    :param renderer: The renderer which should draw multiple points.
    :param points: The points to draw
    :param count: The number of points to draw
    :return: 0 on success, or -1 on error
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
    
    Draw a rectangle on the current rendering target.
    
    :param renderer: The renderer which should draw a rectangle.
    :param rect: A pointer to the destination rectangle, or NULL to
        outline the entire rendering target.
    :return: 0 on success, or -1 on error
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *', nullable=True)
    rect_c = unbox(rect, 'SDL_Rect const *', nullable=True)
    rc = _LIB.SDL_RenderDrawRect(renderer_c, rect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderDrawRects(renderer, rects, count):
    """
    ``int SDL_RenderDrawRects(SDL_Renderer *, SDL_Rect const *, int)``
    
    Draw some number of rectangles on the current rendering target.
    
    :param renderer: The renderer which should draw multiple rectangles.
    :param rects: A pointer to an array of destination rectangles.
    :param count: The number of rectangles.
    :return: 0 on success, or -1 on error
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
    
    Fill a rectangle on the current rendering target with the drawing
    color.
    
    :param renderer: The renderer which should fill a rectangle.
    :param rect: A pointer to the destination rectangle, or NULL for the
        entire rendering target.
    :return: 0 on success, or -1 on error
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *', nullable=True)
    rect_c = unbox(rect, 'SDL_Rect const *', nullable=True)
    rc = _LIB.SDL_RenderFillRect(renderer_c, rect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderFillRects(renderer, rects, count):
    """
    ``int SDL_RenderFillRects(SDL_Renderer *, SDL_Rect const *, int)``
    
    Fill some number of rectangles on the current rendering target with
    the drawing color.
    
    :param renderer: The renderer which should fill multiple rectangles.
    :param rects: A pointer to an array of destination rectangles.
    :param count: The number of rectangles.
    :return: 0 on success, or -1 on error
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
    
    Get the clip rectangle for the current target.
    
    :param renderer: The renderer from which clip rectangle should be
        queried.
    :param rect: A pointer filled in with the current clip rectangle, or
        an empty rectangle if clipping is disabled.
    
    See also SDL_RenderSetClipRect()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rect_c = unbox(rect, 'SDL_Rect *')
    _LIB.SDL_RenderGetClipRect(renderer_c, rect_c)

def SDL_RenderGetLogicalSize(renderer, w=None, h=None):
    """
    ``void SDL_RenderGetLogicalSize(SDL_Renderer *, int *, int *)``
    
    Get device independent resolution for rendering.
    
    :param renderer: The renderer from which resolution should be queried.
    :param w: A pointer filled with the width of the logical resolution
    :param h: A pointer filled with the height of the logical resolution
    
    See also SDL_RenderSetLogicalSize()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    _LIB.SDL_RenderGetLogicalSize(renderer_c, w_c, h_c)
    return (w_c[0], h_c[0])

def SDL_RenderGetScale(renderer, scaleX=None, scaleY=None):
    """
    ``void SDL_RenderGetScale(SDL_Renderer *, float *, float *)``
    
    Get the drawing scale for the current target.
    
    :param renderer: The renderer from which drawing scale should be
        queried.
    :param scaleX: A pointer filled in with the horizontal scaling factor
    :param scaleY: A pointer filled in with the vertical scaling factor
    
    See also SDL_RenderSetScale()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    scaleX_c = unbox(scaleX, 'float *')
    scaleY_c = unbox(scaleY, 'float *')
    _LIB.SDL_RenderGetScale(renderer_c, scaleX_c, scaleY_c)
    return (scaleX_c[0], scaleY_c[0])

def SDL_RenderGetViewport(renderer, rect):
    """
    ``void SDL_RenderGetViewport(SDL_Renderer *, SDL_Rect *)``
    
    Get the drawing area for the current target.
    
    See also SDL_RenderSetViewport()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rect_c = unbox(rect, 'SDL_Rect *')
    _LIB.SDL_RenderGetViewport(renderer_c, rect_c)

def SDL_RenderPresent(renderer):
    """
    ``void SDL_RenderPresent(SDL_Renderer *)``
    
    Update the screen with rendering performed.
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    _LIB.SDL_RenderPresent(renderer_c)

def SDL_RenderReadPixels(renderer, rect, format, pixels, pitch):
    """
    ``int SDL_RenderReadPixels(SDL_Renderer *, SDL_Rect const *, uint32_t, void *, int)``
    
    Read pixels from the current rendering target.
    
    :param renderer: The renderer from which pixels should be read.
    :param rect: A pointer to the rectangle to read, or NULL for the
        entire render target.
    :param format: The desired format of the pixel data, or 0 to use the
        format of the rendering target
    :param pixels: A pointer to be filled in with the pixel data
    :param pitch: The pitch of the pixels parameter.
    :return: 0 on success, or -1 if pixel reading is not supported.
    
    This is a very slow operation, and should not be used frequently.
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *', nullable=True)
    rect_c = unbox(rect, 'SDL_Rect const *', nullable=True)
    format_c = format
    pixels_c = unbox(pixels, 'void *', nullable=True)
    pitch_c = pitch
    rc = _LIB.SDL_RenderReadPixels(renderer_c, rect_c, format_c, pixels_c, pitch_c)
    return rc

def SDL_RenderSetClipRect(renderer, rect):
    """
    ``int SDL_RenderSetClipRect(SDL_Renderer *, SDL_Rect const *)``
    
    Set the clip rectangle for the current target.
    
    :param renderer: The renderer for which clip rectangle should be set.
    :param rect: A pointer to the rectangle to set as the clip rectangle,
        or NULL to disable clipping.
    :return: 0 on success, or -1 on error
    
    See also SDL_RenderGetClipRect()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *', nullable=True)
    rect_c = unbox(rect, 'SDL_Rect const *', nullable=True)
    rc = _LIB.SDL_RenderSetClipRect(renderer_c, rect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderSetLogicalSize(renderer, w, h):
    """
    ``int SDL_RenderSetLogicalSize(SDL_Renderer *, int, int)``
    
    Set device independent resolution for rendering.
    
    :param renderer: The renderer for which resolution should be set.
    :param w: The width of the logical resolution
    :param h: The height of the logical resolution
    
    This function uses the viewport and scaling functionality to allow a
    fixed logical resolution for rendering, regardless of the actual
    output resolution. If the actual output resolution doesn't have the
    same aspect ratio the output rendering will be centered within the
    output display.
    
    If the output display is a window, mouse events in the window will be
    filtered and scaled so they seem to arrive within the logical
    resolution.
    
    If this function results in scaling or subpixel drawing by the
    rendering backend, it will be handled using the appropriate quality
    hints.
    
    See also SDL_RenderGetLogicalSize()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    w_c = w
    h_c = h
    rc = _LIB.SDL_RenderSetLogicalSize(renderer_c, w_c, h_c)
    return rc

def SDL_RenderSetScale(renderer, scaleX, scaleY):
    """
    ``int SDL_RenderSetScale(SDL_Renderer *, float, float)``
    
    Set the drawing scale for rendering on the current target.
    
    :param renderer: The renderer for which the drawing scale should be
        set.
    :param scaleX: The horizontal scaling factor
    :param scaleY: The vertical scaling factor
    
    The drawing coordinates are scaled by the x/y scaling factors before
    they are used by the renderer. This allows resolution independent
    drawing with a single coordinate system.
    
    If this results in scaling or subpixel drawing by the rendering
    backend, it will be handled using the appropriate quality hints. For
    best results use integer scaling factors.
    
    See also SDL_RenderGetScale()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    scaleX_c = scaleX
    scaleY_c = scaleY
    rc = _LIB.SDL_RenderSetScale(renderer_c, scaleX_c, scaleY_c)
    return rc

def SDL_RenderSetViewport(renderer, rect):
    """
    ``int SDL_RenderSetViewport(SDL_Renderer *, SDL_Rect const *)``
    
    Set the drawing area for rendering on the current target.
    
    :param renderer: The renderer for which the drawing area should be
        set.
    :param rect: The rectangle representing the drawing area, or NULL to
        set the viewport to the entire target.
    
    The x,y of the viewport rect represents the origin for rendering.
    
    :return: 0 on success, or -1 on error
    
    If the window associated with the renderer is resized, the viewport is
    automatically reset.
    
    See also SDL_RenderGetViewport()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    rect_c = unbox(rect, 'SDL_Rect const *')
    rc = _LIB.SDL_RenderSetViewport(renderer_c, rect_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_RenderTargetSupported(renderer):
    """
    ``SDL_bool SDL_RenderTargetSupported(SDL_Renderer *)``
    
    Determines whether a window supports the use of render targets.
    
    :param renderer: The renderer that will be checked
    :return: SDL_TRUE if supported, SDL_FALSE if not.
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
    
    Reset the list of all assertion failures.
    
    Reset list of all assertions triggered.
    
    See also SDL_GetAssertionReport
    """
    _LIB.SDL_ResetAssertionReport()

def SDL_RestoreWindow(window):
    """
    ``void SDL_RestoreWindow(SDL_Window *)``
    
    Restore the size and position of a minimized or maximized window.
    
    See also SDL_MaximizeWindow()
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_RestoreWindow(window_c)

def SDL_SaveAllDollarTemplates(src):
    """
    ``int SDL_SaveAllDollarTemplates(SDL_RWops *)``
    
    Save all currently loaded Dollar Gesture templates.
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_SaveAllDollarTemplates(src_c)
    return rc

def SDL_SaveBMP_RW(surface, dst, freedst):
    """
    ``int SDL_SaveBMP_RW(SDL_Surface *, SDL_RWops *, int)``
    
    Save a surface to a seekable SDL data stream (memory or file).
    
    If freedst is non-zero, the stream will be closed after being written.
    
    :return: 0 if successful or -1 if there was an error.
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    dst_c = unbox(dst, 'SDL_RWops *')
    freedst_c = freedst
    rc = _LIB.SDL_SaveBMP_RW(surface_c, dst_c, freedst_c)
    return rc

def SDL_SaveDollarTemplate(gestureId, src):
    """
    ``int SDL_SaveDollarTemplate(int64_t, SDL_RWops *)``
    
    Save a currently loaded Dollar Gesture template.
    """
    gestureId_c = gestureId
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.SDL_SaveDollarTemplate(gestureId_c, src_c)
    return rc

def SDL_SemPost(sem):
    """
    ``int SDL_SemPost(SDL_sem *)``
    
    Atomically increases the semaphore's count (not blocking).
    
    :return: 0, or -1 on error.
    """
    sem_c = unbox(sem, 'SDL_sem *')
    rc = _LIB.SDL_SemPost(sem_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_SemTryWait(sem):
    """
    ``int SDL_SemTryWait(SDL_sem *)``
    
    Non-blocking variant of SDL_SemWait().
    
    :return: 0 if the wait succeeds,
    """
    sem_c = unbox(sem, 'SDL_sem *')
    rc = _LIB.SDL_SemTryWait(sem_c)
    return rc

def SDL_SemValue(sem):
    """
    ``uint32_t SDL_SemValue(SDL_sem *)``
    
    Returns the current count of the semaphore.
    """
    sem_c = unbox(sem, 'SDL_sem *')
    rc = _LIB.SDL_SemValue(sem_c)
    return rc

def SDL_SemWait(sem):
    """
    ``int SDL_SemWait(SDL_sem *)``
    
    This function suspends the calling thread until the semaphore pointed
    to by sem has a positive count. It then atomically decreases the
    semaphore count.
    """
    sem_c = unbox(sem, 'SDL_sem *')
    rc = _LIB.SDL_SemWait(sem_c)
    return rc

def SDL_SemWaitTimeout(sem, ms):
    """
    ``int SDL_SemWaitTimeout(SDL_sem *, uint32_t)``
    
    Variant of SDL_SemWait() with a timeout in milliseconds.
    
    :return: 0 if the wait succeeds,
    
    On some platforms this function is implemented by looping with a delay
    of 1 ms, and so should be avoided if possible.
    """
    sem_c = unbox(sem, 'SDL_sem *')
    ms_c = ms
    rc = _LIB.SDL_SemWaitTimeout(sem_c, ms_c)
    return rc

def SDL_SetAssertionHandler(handler, userdata):
    """
    ``void SDL_SetAssertionHandler(SDL_assert_state SDL_SetAssertionHandler(SDL_assert_data const *, void *), void *)``
    
    Set an application-defined assertion handler.
    
    This allows an app to show its own assertion UI and/or force the
    response to an assertion failure. If the app doesn't provide this, SDL
    will try to do the right thing, popping up a system-specific GUI
    dialog, and probably minimizing any fullscreen windows.
    
    This callback may fire from any thread, but it runs wrapped in a
    mutex, so it will only fire from one thread at a time.
    
    Setting the callback to NULL restores SDL's original internal handler.
    
    This callback is NOT reset to SDL's internal handler upon SDL_Quit()!
    
    :return: SDL_assert_state value of how to handle the assertion
        failure.
    :param handler: Callback function, called when an assertion fails.
    :param userdata: A pointer passed to the callback as-is.
    """
    handler_c = unbox(handler, 'SDL_assert_state(*)(SDL_assert_data const *, void *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_SetAssertionHandler(handler_c, userdata_c)

def SDL_SetClipRect(surface, rect):
    """
    ``SDL_bool SDL_SetClipRect(SDL_Surface *, SDL_Rect const *)``
    
    Sets the clipping rectangle for the destination surface in a blit.
    
    If the clip rectangle is NULL, clipping will be disabled.
    
    If the clip rectangle doesn't intersect the surface, the function will
    return SDL_FALSE and blits will be completely clipped. Otherwise the
    function returns SDL_TRUE and blits to the surface will be clipped to
    the intersection of the surface area and the clipping rectangle.
    
    Note that blits are automatically clipped to the edges of the source
    and destination surfaces.
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    rect_c = unbox(rect, 'SDL_Rect const *')
    rc = _LIB.SDL_SetClipRect(surface_c, rect_c)
    return rc

def SDL_SetClipboardText(text):
    """
    ``int SDL_SetClipboardText(char const *)``
    
    Put UTF-8 text into the clipboard.
    
    See also SDL_GetClipboardText()
    """
    text_c = u8(text)
    rc = _LIB.SDL_SetClipboardText(text_c)
    return rc

def SDL_SetColorKey(surface, flag, key):
    """
    ``int SDL_SetColorKey(SDL_Surface *, int, uint32_t)``
    
    Sets the color key (transparent pixel) in a blittable surface.
    
    :param surface: The surface to update
    :param flag: Non-zero to enable colorkey and 0 to disable colorkey
    :param key: The transparent pixel in the native surface format
    :return: 0 on success, or -1 if the surface is not valid
    
    You can pass SDL_RLEACCEL to enable RLE accelerated blits.
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    flag_c = flag
    key_c = key
    rc = _LIB.SDL_SetColorKey(surface_c, flag_c, key_c)
    return rc

def SDL_SetCursor(cursor):
    """
    ``void SDL_SetCursor(SDL_Cursor *)``
    
    Set the active cursor.
    """
    cursor_c = unbox(cursor, 'SDL_Cursor *')
    _LIB.SDL_SetCursor(cursor_c)

def SDL_SetError(fmt):
    """
    ``int SDL_SetError(char const *, ...)``
    """
    fmt_c = u8(fmt)
    rc = _LIB.SDL_SetError(fmt_c)
    return rc

def SDL_SetEventFilter(filter, userdata):
    """
    ``void SDL_SetEventFilter(int SDL_SetEventFilter(void *, SDL_Event *), void *)``
    
    Sets up a filter to process all events before they change internal
    state and are posted to the internal event queue.
    
    The filter is prototyped as: ::
    
           int SDL_EventFilter(void *userdata, SDL_Event * event);
    
    
    If the filter returns 1, then the event will be added to the internal
    queue. If it returns 0, then the event will be dropped from the queue,
    but the internal state will still be updated. This allows selective
    filtering of dynamically arriving events.
    
    Be very careful of what you do in the event filter function, as it may
    run in a different thread!
    
    There is one caveat when dealing with the SDL_QuitEvent event type.
    The event filter is only called when the window manager desires to
    close the application window. If the event filter returns 1, then the
    window will be closed, otherwise the window will remain open if
    possible.
    
    If the quit event is generated by an interrupt signal, it will bypass
    the internal queue and be delivered to the application at the next
    event poll.
    """
    filter_c = unbox(filter, 'int(*)(void *, SDL_Event *)')
    userdata_c = unbox(userdata, 'void *')
    _LIB.SDL_SetEventFilter(filter_c, userdata_c)

def SDL_SetHint(name, value):
    """
    ``SDL_bool SDL_SetHint(char const *, char const *)``
    
    Set a hint with normal priority.
    
    :return: SDL_TRUE if the hint was set, SDL_FALSE otherwise
    """
    name_c = u8(name)
    value_c = u8(value)
    rc = _LIB.SDL_SetHint(name_c, value_c)
    return rc

def SDL_SetHintWithPriority(name, value, priority):
    """
    ``SDL_bool SDL_SetHintWithPriority(char const *, char const *, SDL_HintPriority)``
    
    Set a hint with a specific priority.
    
    The priority controls the behavior when setting a hint that already
    has a value. Hints will replace existing hints of their priority and
    lower. Environment variables are considered to have override priority.
    
    :return: SDL_TRUE if the hint was set, SDL_FALSE otherwise
    """
    name_c = u8(name)
    value_c = u8(value)
    priority_c = priority
    rc = _LIB.SDL_SetHintWithPriority(name_c, value_c, priority_c)
    return rc

def SDL_SetMainReady():
    """
    ``void SDL_SetMainReady(void)``
    
    This is called by the real SDL main function to let the rest of the
    library know that initialization was done properly.
    
    Calling this yourself without knowing what you're doing can cause
    crashes and hard to diagnose problems with your application.
    """
    _LIB.SDL_SetMainReady()

def SDL_SetModState(modstate):
    """
    ``void SDL_SetModState(SDL_Keymod)``
    
    Set the current key modifier state for the keyboard.
    
    This does not change the keyboard state, only the key modifier flags.
    """
    modstate_c = modstate
    _LIB.SDL_SetModState(modstate_c)

def SDL_SetPaletteColors(palette, colors, firstcolor, ncolors):
    """
    ``int SDL_SetPaletteColors(SDL_Palette *, SDL_Color const *, int, int)``
    
    Set a range of colors in a palette.
    
    :param palette: The palette to modify.
    :param colors: An array of colors to copy into the palette.
    :param firstcolor: The index of the first palette entry to modify.
    :param ncolors: The number of entries to modify.
    :return: 0 on success, or -1 if not all of the colors could be set.
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
    
    Set the palette for a pixel format structure.
    """
    format_c = unbox(format, 'SDL_PixelFormat *')
    palette_c = unbox(palette, 'SDL_Palette *')
    rc = _LIB.SDL_SetPixelFormatPalette(format_c, palette_c)
    return rc

def SDL_SetRelativeMouseMode(enabled):
    """
    ``int SDL_SetRelativeMouseMode(SDL_bool)``
    
    Set relative mouse mode.
    
    :param enabled: Whether or not to enable relative mode
    :return: 0 on success, or -1 if relative mode is not supported.
    
    While the mouse is in relative mode, the cursor is hidden, and the
    driver will try to report continuous motion in the current window.
    Only relative motion events will be delivered, the mouse position will
    not change.
    
    This function will flush any pending mouse motion.
    
    See also SDL_GetRelativeMouseMode()
    """
    enabled_c = enabled
    rc = _LIB.SDL_SetRelativeMouseMode(enabled_c)
    return rc

def SDL_SetRenderDrawBlendMode(renderer, blendMode):
    """
    ``int SDL_SetRenderDrawBlendMode(SDL_Renderer *, SDL_BlendMode)``
    
    Set the blend mode used for drawing operations (Fill and Line).
    
    :param renderer: The renderer for which blend mode should be set.
    :param blendMode: SDL_BlendMode to use for blending.
    :return: 0 on success, or -1 on error
    
    If the blend mode is not supported, the closest supported mode is
    chosen.
    
    See also SDL_GetRenderDrawBlendMode()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    blendMode_c = blendMode
    rc = _LIB.SDL_SetRenderDrawBlendMode(renderer_c, blendMode_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_SetRenderDrawColor(renderer, r, g, b, a):
    """
    ``int SDL_SetRenderDrawColor(SDL_Renderer *, uint8_t, uint8_t, uint8_t, uint8_t)``
    
    Set the color used for drawing operations (Rect, Line and Clear).
    
    :param renderer: The renderer for which drawing color should be set.
    :param r: The red value used to draw on the rendering target.
    :param g: The green value used to draw on the rendering target.
    :param b: The blue value used to draw on the rendering target.
    :param a: The alpha value used to draw on the rendering target,
        usually SDL_ALPHA_OPAQUE (255).
    :return: 0 on success, or -1 on error
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
    
    Set a texture as the current rendering target.
    
    :param renderer: The renderer.
    :param texture: The targeted texture, which must be created with the
        SDL_TEXTUREACCESS_TARGET flag, or NULL for the default render
        target
    :return: 0 on success, or -1 on error
    
    See also SDL_GetRenderTarget()
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    texture_c = unbox(texture, 'SDL_Texture *')
    rc = _LIB.SDL_SetRenderTarget(renderer_c, texture_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_SetSurfaceAlphaMod(surface, alpha):
    """
    ``int SDL_SetSurfaceAlphaMod(SDL_Surface *, uint8_t)``
    
    Set an additional alpha value used in blit operations.
    
    :param surface: The surface to update.
    :param alpha: The alpha value multiplied into blit operations.
    :return: 0 on success, or -1 if the surface is not valid.
    
    See also SDL_GetSurfaceAlphaMod()
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    alpha_c = alpha
    rc = _LIB.SDL_SetSurfaceAlphaMod(surface_c, alpha_c)
    return rc

def SDL_SetSurfaceBlendMode(surface, blendMode):
    """
    ``int SDL_SetSurfaceBlendMode(SDL_Surface *, SDL_BlendMode)``
    
    Set the blend mode used for blit operations.
    
    :param surface: The surface to update.
    :param blendMode: SDL_BlendMode to use for blit blending.
    :return: 0 on success, or -1 if the parameters are not valid.
    
    See also SDL_GetSurfaceBlendMode()
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    blendMode_c = blendMode
    rc = _LIB.SDL_SetSurfaceBlendMode(surface_c, blendMode_c)
    return rc

def SDL_SetSurfaceColorMod(surface, r, g, b):
    """
    ``int SDL_SetSurfaceColorMod(SDL_Surface *, uint8_t, uint8_t, uint8_t)``
    
    Set an additional color value used in blit operations.
    
    :param surface: The surface to update.
    :param r: The red color value multiplied into blit operations.
    :param g: The green color value multiplied into blit operations.
    :param b: The blue color value multiplied into blit operations.
    :return: 0 on success, or -1 if the surface is not valid.
    
    See also SDL_GetSurfaceColorMod()
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
    
    Set the palette used by a surface.
    
    :return: 0, or -1 if the surface format doesn't use a palette.
    
    A single palette can be shared with many surfaces.
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    palette_c = unbox(palette, 'SDL_Palette *')
    rc = _LIB.SDL_SetSurfacePalette(surface_c, palette_c)
    return rc

def SDL_SetSurfaceRLE(surface, flag):
    """
    ``int SDL_SetSurfaceRLE(SDL_Surface *, int)``
    
    Sets the RLE acceleration hint for a surface.
    
    :return: 0 on success, or -1 if the surface is not valid
    
    If RLE is enabled, colorkey and alpha blending blits are much faster,
    but the surface must be locked before directly accessing the pixels.
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    flag_c = flag
    rc = _LIB.SDL_SetSurfaceRLE(surface_c, flag_c)
    return rc

def SDL_SetTextInputRect(rect):
    """
    ``void SDL_SetTextInputRect(SDL_Rect *)``
    
    Set the rectangle used to type Unicode text inputs. This is used as a
    hint for IME and on-screen keyboard placement.
    
    See also SDL_StartTextInput()
    """
    rect_c = unbox(rect, 'SDL_Rect *')
    _LIB.SDL_SetTextInputRect(rect_c)

def SDL_SetTextureAlphaMod(texture, alpha):
    """
    ``int SDL_SetTextureAlphaMod(SDL_Texture *, uint8_t)``
    
    Set an additional alpha value used in render copy operations.
    
    :param texture: The texture to update.
    :param alpha: The alpha value multiplied into copy operations.
    :return: 0 on success, or -1 if the texture is not valid or alpha
        modulation is not supported.
    
    See also SDL_GetTextureAlphaMod()
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    alpha_c = alpha
    rc = _LIB.SDL_SetTextureAlphaMod(texture_c, alpha_c)
    return rc

def SDL_SetTextureBlendMode(texture, blendMode):
    """
    ``int SDL_SetTextureBlendMode(SDL_Texture *, SDL_BlendMode)``
    
    Set the blend mode used for texture copy operations.
    
    :param texture: The texture to update.
    :param blendMode: SDL_BlendMode to use for texture blending.
    :return: 0 on success, or -1 if the texture is not valid or the blend
        mode is not supported.
    
    If the blend mode is not supported, the closest supported mode is
    chosen.
    
    See also SDL_GetTextureBlendMode()
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    blendMode_c = blendMode
    rc = _LIB.SDL_SetTextureBlendMode(texture_c, blendMode_c)
    return rc

def SDL_SetTextureColorMod(texture, r, g, b):
    """
    ``int SDL_SetTextureColorMod(SDL_Texture *, uint8_t, uint8_t, uint8_t)``
    
    Set an additional color value used in render copy operations.
    
    :param texture: The texture to update.
    :param r: The red color value multiplied into copy operations.
    :param g: The green color value multiplied into copy operations.
    :param b: The blue color value multiplied into copy operations.
    :return: 0 on success, or -1 if the texture is not valid or color
        modulation is not supported.
    
    See also SDL_GetTextureColorMod()
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
    
    Set the priority for the current thread
    """
    priority_c = priority
    rc = _LIB.SDL_SetThreadPriority(priority_c)
    return rc

def SDL_SetWindowBordered(window, bordered):
    """
    ``void SDL_SetWindowBordered(SDL_Window *, SDL_bool)``
    
    Set the border state of a window.
    
    This will add or remove the window's SDL_WINDOW_BORDERLESS flag and
    add or remove the border from the actual window. This is a no-op if
    the window's border already matches the requested state.
    
    :param window: The window of which to change the border state.
    :param bordered: SDL_FALSE to remove border, SDL_TRUE to add border.
    
    You can't change the border state of a fullscreen window.
    
    See also SDL_GetWindowFlags()
    """
    window_c = unbox(window, 'SDL_Window *')
    bordered_c = bordered
    _LIB.SDL_SetWindowBordered(window_c, bordered_c)

def SDL_SetWindowBrightness(window, brightness):
    """
    ``int SDL_SetWindowBrightness(SDL_Window *, float)``
    
    Set the brightness (gamma correction) for a window.
    
    :return: 0 on success, or -1 if setting the brightness isn't
        supported.
    
    See also SDL_GetWindowBrightness()
    """
    window_c = unbox(window, 'SDL_Window *')
    brightness_c = brightness
    rc = _LIB.SDL_SetWindowBrightness(window_c, brightness_c)
    return rc

def SDL_SetWindowData(window, name, userdata):
    """
    ``void * SDL_SetWindowData(SDL_Window *, char const *, void *)``
    
    Associate an arbitrary named pointer with a window.
    
    :param window: The window to associate with the pointer.
    :param name: The name of the pointer.
    :param userdata: The associated pointer.
    :return: The previous value associated with 'name'
    
    The name is case-sensitive.
    
    See also SDL_GetWindowData()
    """
    window_c = unbox(window, 'SDL_Window *')
    name_c = u8(name)
    userdata_c = unbox(userdata, 'void *')
    rc = _LIB.SDL_SetWindowData(window_c, name_c, userdata_c)
    return rc

def SDL_SetWindowDisplayMode(window, mode):
    """
    ``int SDL_SetWindowDisplayMode(SDL_Window *, SDL_DisplayMode const *)``
    
    Set the display mode used when a fullscreen window is visible.
    
    By default the window's dimensions and the desktop format and refresh
    rate are used.
    
    :param window: The window for which the display mode should be set.
    :param mode: The mode to use, or NULL for the default mode.
    :return: 0 on success, or -1 if setting the display mode failed.
    
    See also SDL_GetWindowDisplayMode()
    """
    window_c = unbox(window, 'SDL_Window *')
    mode_c = unbox(mode, 'SDL_DisplayMode const *')
    rc = _LIB.SDL_SetWindowDisplayMode(window_c, mode_c)
    return rc

def SDL_SetWindowFullscreen(window, flags):
    """
    ``int SDL_SetWindowFullscreen(SDL_Window *, uint32_t)``
    
    Set a window's fullscreen state.
    
    :return: 0 on success, or -1 if setting the display mode failed.
    
    See also SDL_SetWindowDisplayMode()
    """
    window_c = unbox(window, 'SDL_Window *')
    flags_c = flags
    rc = _LIB.SDL_SetWindowFullscreen(window_c, flags_c)
    return rc

def SDL_SetWindowGammaRamp(window, red=None, green=None, blue=None):
    """
    ``int SDL_SetWindowGammaRamp(SDL_Window *, uint16_t const *, uint16_t const *, uint16_t const *)``
    
    Set the gamma ramp for a window.
    
    :param window: The window for which the gamma ramp should be set.
    :param red: The translation table for the red channel, or NULL.
    :param green: The translation table for the green channel, or NULL.
    :param blue: The translation table for the blue channel, or NULL.
    :return: 0 on success, or -1 if gamma ramps are unsupported.
    
    Set the gamma translation table for the red, green, and blue channels
    of the video hardware. Each table is an array of 256 16-bit
    quantities, representing a mapping between the input and output for
    that channel. The input is the index into the array, and the output is
    the 16-bit gamma value at that index, scaled to the output color
    precision.
    
    See also SDL_GetWindowGammaRamp()
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
    
    Set a window's input grab mode.
    
    :param window: The window for which the input grab mode should be set.
    :param grabbed: This is SDL_TRUE to grab input, and SDL_FALSE to
        release input.
    
    See also SDL_GetWindowGrab()
    """
    window_c = unbox(window, 'SDL_Window *')
    grabbed_c = grabbed
    _LIB.SDL_SetWindowGrab(window_c, grabbed_c)

def SDL_SetWindowIcon(window, icon):
    """
    ``void SDL_SetWindowIcon(SDL_Window *, SDL_Surface *)``
    
    Set the icon for a window.
    
    :param window: The window for which the icon should be set.
    :param icon: The icon for the window.
    """
    window_c = unbox(window, 'SDL_Window *')
    icon_c = unbox(icon, 'SDL_Surface *')
    _LIB.SDL_SetWindowIcon(window_c, icon_c)

def SDL_SetWindowMaximumSize(window, max_w, max_h):
    """
    ``void SDL_SetWindowMaximumSize(SDL_Window *, int, int)``
    
    Set the maximum size of a window's client area.
    
    :param window: The window to set a new maximum size.
    :param max_w: The maximum width of the window, must be >0
    :param max_h: The maximum height of the window, must be >0
    
    You can't change the maximum size of a fullscreen window, it
    automatically matches the size of the display mode.
    
    See also SDL_GetWindowMaximumSize()
    """
    window_c = unbox(window, 'SDL_Window *')
    max_w_c = max_w
    max_h_c = max_h
    _LIB.SDL_SetWindowMaximumSize(window_c, max_w_c, max_h_c)

def SDL_SetWindowMinimumSize(window, min_w, min_h):
    """
    ``void SDL_SetWindowMinimumSize(SDL_Window *, int, int)``
    
    Set the minimum size of a window's client area.
    
    :param window: The window to set a new minimum size.
    :param min_w: The minimum width of the window, must be >0
    :param min_h: The minimum height of the window, must be >0
    
    You can't change the minimum size of a fullscreen window, it
    automatically matches the size of the display mode.
    
    See also SDL_GetWindowMinimumSize()
    """
    window_c = unbox(window, 'SDL_Window *')
    min_w_c = min_w
    min_h_c = min_h
    _LIB.SDL_SetWindowMinimumSize(window_c, min_w_c, min_h_c)

def SDL_SetWindowPosition(window, x, y):
    """
    ``void SDL_SetWindowPosition(SDL_Window *, int, int)``
    
    Set the position of a window.
    
    :param window: The window to reposition.
    :param x: The x coordinate of the window, SDL_WINDOWPOS_CENTERED, or
        SDL_WINDOWPOS_UNDEFINED.
    :param y: The y coordinate of the window, SDL_WINDOWPOS_CENTERED, or
        SDL_WINDOWPOS_UNDEFINED.
    
    The window coordinate origin is the upper left of the display.
    
    See also SDL_GetWindowPosition()
    """
    window_c = unbox(window, 'SDL_Window *')
    x_c = x
    y_c = y
    _LIB.SDL_SetWindowPosition(window_c, x_c, y_c)

def SDL_SetWindowSize(window, w, h):
    """
    ``void SDL_SetWindowSize(SDL_Window *, int, int)``
    
    Set the size of a window's client area.
    
    :param window: The window to resize.
    :param w: The width of the window, must be >0
    :param h: The height of the window, must be >0
    
    You can't change the size of a fullscreen window, it automatically
    matches the size of the display mode.
    
    See also SDL_GetWindowSize()
    """
    window_c = unbox(window, 'SDL_Window *')
    w_c = w
    h_c = h
    _LIB.SDL_SetWindowSize(window_c, w_c, h_c)

def SDL_SetWindowTitle(window, title):
    """
    ``void SDL_SetWindowTitle(SDL_Window *, char const *)``
    
    Set the title of a window, in UTF-8 format.
    
    See also SDL_GetWindowTitle()
    """
    window_c = unbox(window, 'SDL_Window *')
    title_c = u8(title)
    _LIB.SDL_SetWindowTitle(window_c, title_c)

def SDL_ShowCursor(toggle):
    """
    ``int SDL_ShowCursor(int)``
    
    Toggle whether or not the cursor is shown.
    
    :param toggle: 1 to show the cursor, 0 to hide it, -1 to query the
        current state.
    :return: 1 if the cursor is shown, or 0 if the cursor is hidden.
    """
    toggle_c = toggle
    rc = _LIB.SDL_ShowCursor(toggle_c)
    return rc

def SDL_ShowMessageBox(messageboxdata, buttonid=None):
    """
    ``int SDL_ShowMessageBox(SDL_MessageBoxData const *, int *)``
    
    Create a modal message box.
    
    :param messageboxdata: The SDL_MessageBoxData structure with title,
        text, etc.
    :param buttonid: The pointer to which user id of hit button should be
        copied.
    :return: -1 on error, otherwise 0 and buttonid contains user id of
        button hit or -1 if dialog was closed.
    
    This function should be called on the thread that created the parent
    window, or on the main thread if the messagebox has no parent. It will
    block execution of that thread until the user clicks a button or
    closes the messagebox.
    """
    messageboxdata_c = unbox(messageboxdata, 'SDL_MessageBoxData const *')
    buttonid_c = unbox(buttonid, 'int *')
    rc = _LIB.SDL_ShowMessageBox(messageboxdata_c, buttonid_c)
    if rc == -1: raise SDLError()
    return (rc, buttonid_c[0])

def SDL_ShowSimpleMessageBox(flags, title, message, window):
    """
    ``int SDL_ShowSimpleMessageBox(uint32_t, char const *, char const *, SDL_Window *)``
    
    Create a simple modal message box.
    
    :param flags: SDL_MessageBoxFlags
    :param title: UTF-8 title text
    :param message: UTF-8 message text
    :param window: The parent window, or NULL for no parent
    :return: 0 on success, -1 on error
    
    See also SDL_ShowMessageBox
    """
    flags_c = flags
    title_c = u8(title)
    message_c = u8(message)
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_ShowSimpleMessageBox(flags_c, title_c, message_c, window_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_ShowWindow(window):
    """
    ``void SDL_ShowWindow(SDL_Window *)``
    
    Show a window.
    
    See also SDL_HideWindow()
    """
    window_c = unbox(window, 'SDL_Window *')
    _LIB.SDL_ShowWindow(window_c)

def SDL_SoftStretch(src, srcrect, dst, dstrect):
    """
    ``int SDL_SoftStretch(SDL_Surface *, SDL_Rect const *, SDL_Surface *, SDL_Rect const *)``
    
    Perform a fast, low quality, stretch blit between two surfaces of the
    same pixel format.
    
    This function uses a static buffer, and is not thread-safe.
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
    
    Start accepting Unicode text input events. This function will show the
    on-screen keyboard if supported.
    
    See also SDL_StopTextInput()
    """
    _LIB.SDL_StartTextInput()

def SDL_StopTextInput():
    """
    ``void SDL_StopTextInput(void)``
    
    Stop receiving any text input events. This function will hide the on-
    screen keyboard if supported.
    
    See also SDL_StartTextInput()
    """
    _LIB.SDL_StopTextInput()

def SDL_TLSCreate():
    """
    ``unsigned int SDL_TLSCreate(void)``
    
    Create an identifier that is globally visible to all threads but
    refers to data that is thread-specific.
    
    :return: The newly created thread local storage identifier, or 0 on
        error
    ::
    
       static SDL_SpinLock tls_lock;
       static SDL_TLSID thread_local_storage;
    
    
    
       void SetMyThreadData(void *value)
       {
           if (!thread_local_storage) {
               SDL_AtomicLock(&tls_lock);
               if (!thread_local_storage) {
                   thread_local_storage = SDL_TLSCreate();
               }
               SDL_AtomicUnLock(&tls_lock);
           }
           SDL_TLSSet(thread_local_storage, value);
       }
    
       void *GetMyThreadData(void)
       {
           return SDL_TLSGet(thread_local_storage);
       }
    
    
    See also SDL_TLSGet()
    """
    rc = _LIB.SDL_TLSCreate()
    return rc

def SDL_TLSGet(id):
    """
    ``void * SDL_TLSGet(unsigned int)``
    
    Get the value associated with a thread local storage ID for the
    current thread.
    
    :param id: The thread local storage ID
    :return: The value associated with the ID for the current thread, or
        NULL if no value has been set.
    
    See also SDL_TLSCreate()
    """
    id_c = id
    rc = _LIB.SDL_TLSGet(id_c)
    return rc

def SDL_TLSSet(id, value, destructor):
    """
    ``int SDL_TLSSet(unsigned int, void const *, void SDL_TLSSet(void *))``
    
    Set the value associated with a thread local storage ID for the
    current thread.
    
    :param id: The thread local storage ID
    :param value: The value to associate with the ID for the current
        thread
    :param destructor: A function called when the thread exits, to free
        the value.
    :return: 0 on success, -1 on error
    
    See also SDL_TLSCreate()
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
    
    Get the thread identifier for the current thread.
    """
    rc = _LIB.SDL_ThreadID()
    return rc

def SDL_TryLockMutex(mutex):
    """
    ``int SDL_TryLockMutex(SDL_mutex *)``
    
    Try to lock the mutex
    
    :return: 0, SDL_MUTEX_TIMEDOUT, or -1 on error
    """
    mutex_c = unbox(mutex, 'SDL_mutex *')
    rc = _LIB.SDL_TryLockMutex(mutex_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_UnionRect(A, B, result):
    """
    ``void SDL_UnionRect(SDL_Rect const *, SDL_Rect const *, SDL_Rect *)``
    
    Calculate the union of two rectangles.
    """
    A_c = unbox(A, 'SDL_Rect const *')
    B_c = unbox(B, 'SDL_Rect const *')
    result_c = unbox(result, 'SDL_Rect *')
    _LIB.SDL_UnionRect(A_c, B_c, result_c)

def SDL_UnloadObject(handle):
    """
    ``void SDL_UnloadObject(void *)``
    
    Unload a shared object from memory.
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
    
    See also SDL_LockSurface()
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    _LIB.SDL_UnlockSurface(surface_c)

def SDL_UnlockTexture(texture):
    """
    ``void SDL_UnlockTexture(SDL_Texture *)``
    
    Unlock a texture, uploading the changes to video memory, if needed.
    
    See also SDL_LockTexture()
    """
    texture_c = unbox(texture, 'SDL_Texture *')
    _LIB.SDL_UnlockTexture(texture_c)

def SDL_UpdateTexture(texture, rect, pixels, pitch):
    """
    ``int SDL_UpdateTexture(SDL_Texture *, SDL_Rect const *, void const *, int)``
    
    Update the given texture rectangle with new pixel data.
    
    :param texture: The texture to update
    :param rect: A pointer to the rectangle of pixels to update, or NULL
        to update the entire texture.
    :param pixels: The raw pixel data.
    :param pitch: The number of bytes between rows of pixel data.
    :return: 0 on success, or -1 if the texture is not valid.
    
    This is a fairly slow function.
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
    
    Copy the window surface to the screen.
    
    :return: 0 on success, or -1 on error.
    
    See also SDL_GetWindowSurface()
    """
    window_c = unbox(window, 'SDL_Window *')
    rc = _LIB.SDL_UpdateWindowSurface(window_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_UpdateWindowSurfaceRects(window, rects, numrects):
    """
    ``int SDL_UpdateWindowSurfaceRects(SDL_Window *, SDL_Rect const *, int)``
    
    Copy a number of rectangles on the window surface to the screen.
    
    :return: 0 on success, or -1 on error.
    
    See also SDL_GetWindowSurface()
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
    
    This is the public blit function, SDL_BlitSurface(), and it performs
    rectangle validation and clipping before passing it to SDL_LowerBlit()
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
    
    This is the public scaled blit function, SDL_BlitScaled(), and it
    performs rectangle validation and clipping before passing it to
    SDL_LowerBlitScaled()
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
    
    Initialize the video subsystem, optionally specifying a video driver.
    
    :param driver_name: Initialize a specific driver by name, or NULL for
        the default video driver.
    :return: 0 on success, -1 on error
    
    This function initializes the video subsystem; setting up a connection
    to the window manager, etc, and determines the available display modes
    and pixel formats, but does not initialize a window or graphics mode.
    
    See also SDL_VideoQuit()
    """
    driver_name_c = u8(driver_name)
    rc = _LIB.SDL_VideoInit(driver_name_c)
    if rc == -1: raise SDLError()
    return rc

def SDL_VideoQuit():
    """
    ``void SDL_VideoQuit(void)``
    
    Shuts down the video subsystem.
    
    This function closes all windows, and restores the original video
    mode.
    
    See also SDL_VideoInit()
    """
    _LIB.SDL_VideoQuit()

def SDL_WaitEvent(event):
    """
    ``int SDL_WaitEvent(SDL_Event *)``
    
    Waits indefinitely for the next available event.
    
    :return: 1, or 0 if there was an error while waiting for events.
    :param event: If not NULL, the next event is removed from the queue
        and stored in that area.
    """
    event_c = unbox(event, 'SDL_Event *')
    rc = _LIB.SDL_WaitEvent(event_c)
    return rc

def SDL_WaitEventTimeout(event, timeout):
    """
    ``int SDL_WaitEventTimeout(SDL_Event *, int)``
    
    Waits until the specified timeout (in milliseconds) for the next
    available event.
    
    :return: 1, or 0 if there was an error while waiting for events.
    :param event: If not NULL, the next event is removed from the queue
        and stored in that area.
    :param timeout: The timeout (in milliseconds) to wait for next event.
    """
    event_c = unbox(event, 'SDL_Event *')
    timeout_c = timeout
    rc = _LIB.SDL_WaitEventTimeout(event_c, timeout_c)
    return rc

def SDL_WaitThread(thread, status=None):
    """
    ``void SDL_WaitThread(SDL_Thread *, int *)``
    
    Wait for a thread to finish. Threads that haven't been detached will
    remain (as a "zombie") until this function cleans them up. Not doing
    so is a resource leak.
    
    Once a thread has been cleaned up through this function, the
    SDL_Thread that references it becomes invalid and should not be
    referenced again. As such, only one thread may call SDL_WaitThread()
    on another.
    
    The return code for the thread function is placed in the area pointed
    to by status, if status is not NULL.
    
    You may not wait on a thread that has been used in a call to
    SDL_DetachThread(). Use either that function or this one, but not
    both, or behavior is undefined.
    
    It is safe to pass NULL to this function; it is a no-op.
    """
    thread_c = unbox(thread, 'SDL_Thread *')
    status_c = unbox(status, 'int *')
    _LIB.SDL_WaitThread(thread_c, status_c)
    return status_c[0]

def SDL_WarpMouseInWindow(window, x, y):
    """
    ``void SDL_WarpMouseInWindow(SDL_Window *, int, int)``
    
    Moves the mouse to the given position within the window.
    
    :param window: The window to move the mouse into, or NULL for the
        current mouse focus
    :param x: The x coordinate within the window
    :param y: The y coordinate within the window
    
    This function generates a mouse motion event
    """
    window_c = unbox(window, 'SDL_Window *')
    x_c = x
    y_c = y
    _LIB.SDL_WarpMouseInWindow(window_c, x_c, y_c)

def SDL_WasInit(flags):
    """
    ``uint32_t SDL_WasInit(uint32_t)``
    
    This function returns a mask of the specified subsystems which have
    previously been initialized.
    
    If flags is 0, it returns a mask of all initialized subsystems.
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
    str_c = u8(str)
    rc = _LIB.SDL_atof(str_c)
    return rc

def SDL_atoi(str):
    """
    ``int SDL_atoi(char const *)``
    """
    str_c = u8(str)
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
    name_c = u8(name)
    rc = _LIB.SDL_getenv(name_c)
    return ffi.string(rc).decode('utf-8')

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
    tocode_c = u8(tocode)
    fromcode_c = u8(fromcode)
    rc = _LIB.SDL_iconv_open(tocode_c, fromcode_c)
    return rc

def SDL_iconv_string(tocode, fromcode, inbuf, inbytesleft):
    """
    ``char * SDL_iconv_string(char const *, char const *, char const *, size_t)``
    
    This function converts a string between encodings in one pass,
    returning a string that must be freed with SDL_free() or NULL on
    error.
    """
    tocode_c = u8(tocode)
    fromcode_c = u8(fromcode)
    inbuf_c = u8(inbuf)
    inbytesleft_c = inbytesleft
    rc = _LIB.SDL_iconv_string(tocode_c, fromcode_c, inbuf_c, inbytesleft_c)
    return ffi.string(rc).decode('utf-8')

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
    str_c = u8(str)
    radix_c = radix
    rc = _LIB.SDL_itoa(value_c, str_c, radix_c)
    return ffi.string(rc).decode('utf-8')

def SDL_lltoa(value, str, radix):
    """
    ``char * SDL_lltoa(int64_t, char *, int)``
    """
    value_c = value
    str_c = u8(str)
    radix_c = radix
    rc = _LIB.SDL_lltoa(value_c, str_c, radix_c)
    return ffi.string(rc).decode('utf-8')

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
    str_c = u8(str)
    radix_c = radix
    rc = _LIB.SDL_ltoa(value_c, str_c, radix_c)
    return ffi.string(rc).decode('utf-8')

def SDL_main(argc, argv):
    """
    ``int SDL_main(int, char * *)``
    
    The prototype for the application's main() function
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
    name_c = u8(name)
    value_c = u8(value)
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
    text_c = u8(text)
    maxlen_c = maxlen
    fmt_c = u8(fmt)
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
    text_c = u8(text)
    fmt_c = u8(fmt)
    rc = _LIB.SDL_sscanf(text_c, fmt_c)
    return rc

def SDL_strcasecmp(str1, str2):
    """
    ``int SDL_strcasecmp(char const *, char const *)``
    """
    str1_c = u8(str1)
    str2_c = u8(str2)
    rc = _LIB.SDL_strcasecmp(str1_c, str2_c)
    return rc

def SDL_strchr(str, c):
    """
    ``char * SDL_strchr(char const *, int)``
    """
    str_c = u8(str)
    c_c = c
    rc = _LIB.SDL_strchr(str_c, c_c)
    return ffi.string(rc).decode('utf-8')

def SDL_strcmp(str1, str2):
    """
    ``int SDL_strcmp(char const *, char const *)``
    """
    str1_c = u8(str1)
    str2_c = u8(str2)
    rc = _LIB.SDL_strcmp(str1_c, str2_c)
    return rc

def SDL_strdup(str):
    """
    ``char * SDL_strdup(char const *)``
    """
    str_c = u8(str)
    rc = _LIB.SDL_strdup(str_c)
    return ffi.string(rc).decode('utf-8')

def SDL_strlcat(dst, src, maxlen):
    """
    ``size_t SDL_strlcat(char *, char const *, size_t)``
    """
    dst_c = u8(dst)
    src_c = u8(src)
    maxlen_c = maxlen
    rc = _LIB.SDL_strlcat(dst_c, src_c, maxlen_c)
    return rc

def SDL_strlcpy(dst, src, maxlen):
    """
    ``size_t SDL_strlcpy(char *, char const *, size_t)``
    """
    dst_c = u8(dst)
    src_c = u8(src)
    maxlen_c = maxlen
    rc = _LIB.SDL_strlcpy(dst_c, src_c, maxlen_c)
    return rc

def SDL_strlen(str):
    """
    ``size_t SDL_strlen(char const *)``
    """
    str_c = u8(str)
    rc = _LIB.SDL_strlen(str_c)
    return rc

def SDL_strlwr(str):
    """
    ``char * SDL_strlwr(char *)``
    """
    str_c = u8(str)
    rc = _LIB.SDL_strlwr(str_c)
    return ffi.string(rc).decode('utf-8')

def SDL_strncasecmp(str1, str2, len):
    """
    ``int SDL_strncasecmp(char const *, char const *, size_t)``
    """
    str1_c = u8(str1)
    str2_c = u8(str2)
    len_c = len
    rc = _LIB.SDL_strncasecmp(str1_c, str2_c, len_c)
    return rc

def SDL_strncmp(str1, str2, maxlen):
    """
    ``int SDL_strncmp(char const *, char const *, size_t)``
    """
    str1_c = u8(str1)
    str2_c = u8(str2)
    maxlen_c = maxlen
    rc = _LIB.SDL_strncmp(str1_c, str2_c, maxlen_c)
    return rc

def SDL_strrchr(str, c):
    """
    ``char * SDL_strrchr(char const *, int)``
    """
    str_c = u8(str)
    c_c = c
    rc = _LIB.SDL_strrchr(str_c, c_c)
    return ffi.string(rc).decode('utf-8')

def SDL_strrev(str):
    """
    ``char * SDL_strrev(char *)``
    """
    str_c = u8(str)
    rc = _LIB.SDL_strrev(str_c)
    return ffi.string(rc).decode('utf-8')

def SDL_strstr(haystack, needle):
    """
    ``char * SDL_strstr(char const *, char const *)``
    """
    haystack_c = u8(haystack)
    needle_c = u8(needle)
    rc = _LIB.SDL_strstr(haystack_c, needle_c)
    return ffi.string(rc).decode('utf-8')

def SDL_strtod(str, endp):
    """
    ``double SDL_strtod(char const *, char * *)``
    """
    str_c = u8(str)
    endp_c = unbox(endp, 'char * *')
    rc = _LIB.SDL_strtod(str_c, endp_c)
    return rc

def SDL_strtol(str, endp, base):
    """
    ``long SDL_strtol(char const *, char * *, int)``
    """
    str_c = u8(str)
    endp_c = unbox(endp, 'char * *')
    base_c = base
    rc = _LIB.SDL_strtol(str_c, endp_c, base_c)
    return rc

def SDL_strtoll(str, endp, base):
    """
    ``int64_t SDL_strtoll(char const *, char * *, int)``
    """
    str_c = u8(str)
    endp_c = unbox(endp, 'char * *')
    base_c = base
    rc = _LIB.SDL_strtoll(str_c, endp_c, base_c)
    return rc

def SDL_strtoul(str, endp, base):
    """
    ``unsigned long SDL_strtoul(char const *, char * *, int)``
    """
    str_c = u8(str)
    endp_c = unbox(endp, 'char * *')
    base_c = base
    rc = _LIB.SDL_strtoul(str_c, endp_c, base_c)
    return rc

def SDL_strtoull(str, endp, base):
    """
    ``uint64_t SDL_strtoull(char const *, char * *, int)``
    """
    str_c = u8(str)
    endp_c = unbox(endp, 'char * *')
    base_c = base
    rc = _LIB.SDL_strtoull(str_c, endp_c, base_c)
    return rc

def SDL_strupr(str):
    """
    ``char * SDL_strupr(char *)``
    """
    str_c = u8(str)
    rc = _LIB.SDL_strupr(str_c)
    return ffi.string(rc).decode('utf-8')

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
    str_c = u8(str)
    radix_c = radix
    rc = _LIB.SDL_uitoa(value_c, str_c, radix_c)
    return ffi.string(rc).decode('utf-8')

def SDL_ulltoa(value, str, radix):
    """
    ``char * SDL_ulltoa(uint64_t, char *, int)``
    """
    value_c = value
    str_c = u8(str)
    radix_c = radix
    rc = _LIB.SDL_ulltoa(value_c, str_c, radix_c)
    return ffi.string(rc).decode('utf-8')

def SDL_ultoa(value, str, radix):
    """
    ``char * SDL_ultoa(unsigned long, char *, int)``
    """
    value_c = value
    str_c = u8(str)
    radix_c = radix
    rc = _LIB.SDL_ultoa(value_c, str_c, radix_c)
    return ffi.string(rc).decode('utf-8')

def SDL_utf8strlcpy(dst, src, dst_bytes):
    """
    ``size_t SDL_utf8strlcpy(char *, char const *, size_t)``
    """
    dst_c = u8(dst)
    src_c = u8(src)
    dst_bytes_c = dst_bytes
    rc = _LIB.SDL_utf8strlcpy(dst_c, src_c, dst_bytes_c)
    return rc

def SDL_vsnprintf(text, maxlen, fmt, ap):
    """
    ``int SDL_vsnprintf(char *, size_t, char const *, int32_t)``
    """
    text_c = u8(text)
    maxlen_c = maxlen
    fmt_c = u8(fmt)
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
    RWFromFP = SDL_RWFromFP

class SDL_AudioCVT(Struct):
    """Wrap `SDL_AudioCVT`"""
    @property
    def needed(self): return self.cdata.needed
    @needed.setter
    def needed(self, value): self.cdata.needed = value
    @property
    def src_format(self): return self.cdata.src_format
    @src_format.setter
    def src_format(self, value): self.cdata.src_format = value
    @property
    def dst_format(self): return self.cdata.dst_format
    @dst_format.setter
    def dst_format(self, value): self.cdata.dst_format = value
    @property
    def rate_incr(self): return self.cdata.rate_incr
    @rate_incr.setter
    def rate_incr(self, value): self.cdata.rate_incr = value
    @property
    def buf(self): return self.cdata.buf
    @buf.setter
    def buf(self, value): self.cdata.buf = value
    @property
    def len(self): return self.cdata.len
    @len.setter
    def len(self, value): self.cdata.len = value
    @property
    def len_cvt(self): return self.cdata.len_cvt
    @len_cvt.setter
    def len_cvt(self, value): self.cdata.len_cvt = value
    @property
    def len_mult(self): return self.cdata.len_mult
    @len_mult.setter
    def len_mult(self, value): self.cdata.len_mult = value
    @property
    def len_ratio(self): return self.cdata.len_ratio
    @len_ratio.setter
    def len_ratio(self, value): self.cdata.len_ratio = value
    @property
    def filters(self): return self.cdata.filters
    @filters.setter
    def filters(self, value): self.cdata.filters = value
    @property
    def filter_index(self): return self.cdata.filter_index
    @filter_index.setter
    def filter_index(self, value): self.cdata.filter_index = value
    buildAudioCVT = SDL_BuildAudioCVT
    convertAudio = SDL_ConvertAudio

class SDL_AudioSpec(Struct):
    """Wrap `SDL_AudioSpec`"""
    @property
    def freq(self): return self.cdata.freq
    @freq.setter
    def freq(self, value): self.cdata.freq = value
    @property
    def format(self): return self.cdata.format
    @format.setter
    def format(self, value): self.cdata.format = value
    @property
    def channels(self): return self.cdata.channels
    @channels.setter
    def channels(self, value): self.cdata.channels = value
    @property
    def silence(self): return self.cdata.silence
    @silence.setter
    def silence(self, value): self.cdata.silence = value
    @property
    def samples(self): return self.cdata.samples
    @samples.setter
    def samples(self, value): self.cdata.samples = value
    @property
    def padding(self): return self.cdata.padding
    @padding.setter
    def padding(self, value): self.cdata.padding = value
    @property
    def size(self): return self.cdata.size
    @size.setter
    def size(self, value): self.cdata.size = value
    @property
    def callback(self): return self.cdata.callback
    @callback.setter
    def callback(self, value): self.cdata.callback = value
    @property
    def userdata(self): return self.cdata.userdata
    @userdata.setter
    def userdata(self, value): self.cdata.userdata = value
    openAudio = SDL_OpenAudio

class SDL_Color(Struct):
    """Wrap `SDL_Color`"""
    @property
    def r(self): return self.cdata.r
    @r.setter
    def r(self, value): self.cdata.r = value
    @property
    def g(self): return self.cdata.g
    @g.setter
    def g(self, value): self.cdata.g = value
    @property
    def b(self): return self.cdata.b
    @b.setter
    def b(self, value): self.cdata.b = value
    @property
    def a(self): return self.cdata.a
    @a.setter
    def a(self, value): self.cdata.a = value
    pass

class SDL_CommonEvent(Struct):
    """Wrap `SDL_CommonEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    pass

class SDL_ControllerAxisEvent(Struct):
    """Wrap `SDL_ControllerAxisEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def which(self): return self.cdata.which
    @which.setter
    def which(self, value): self.cdata.which = value
    @property
    def axis(self): return self.cdata.axis
    @axis.setter
    def axis(self, value): self.cdata.axis = value
    @property
    def padding1(self): return self.cdata.padding1
    @padding1.setter
    def padding1(self, value): self.cdata.padding1 = value
    @property
    def padding2(self): return self.cdata.padding2
    @padding2.setter
    def padding2(self, value): self.cdata.padding2 = value
    @property
    def padding3(self): return self.cdata.padding3
    @padding3.setter
    def padding3(self, value): self.cdata.padding3 = value
    @property
    def value(self): return self.cdata.value
    @value.setter
    def value(self, value): self.cdata.value = value
    @property
    def padding4(self): return self.cdata.padding4
    @padding4.setter
    def padding4(self, value): self.cdata.padding4 = value
    pass

class SDL_ControllerButtonEvent(Struct):
    """Wrap `SDL_ControllerButtonEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def which(self): return self.cdata.which
    @which.setter
    def which(self, value): self.cdata.which = value
    @property
    def button(self): return self.cdata.button
    @button.setter
    def button(self, value): self.cdata.button = value
    @property
    def state(self): return self.cdata.state
    @state.setter
    def state(self, value): self.cdata.state = value
    @property
    def padding1(self): return self.cdata.padding1
    @padding1.setter
    def padding1(self, value): self.cdata.padding1 = value
    @property
    def padding2(self): return self.cdata.padding2
    @padding2.setter
    def padding2(self, value): self.cdata.padding2 = value
    pass

class SDL_ControllerDeviceEvent(Struct):
    """Wrap `SDL_ControllerDeviceEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def which(self): return self.cdata.which
    @which.setter
    def which(self, value): self.cdata.which = value
    pass

class SDL_Cursor(Struct):
    """Wrap `SDL_Cursor`"""
    freeCursor = SDL_FreeCursor
    setCursor = SDL_SetCursor

class SDL_DisplayMode(Struct):
    """Wrap `SDL_DisplayMode`"""
    @property
    def format(self): return self.cdata.format
    @format.setter
    def format(self, value): self.cdata.format = value
    @property
    def w(self): return self.cdata.w
    @w.setter
    def w(self, value): self.cdata.w = value
    @property
    def h(self): return self.cdata.h
    @h.setter
    def h(self, value): self.cdata.h = value
    @property
    def refresh_rate(self): return self.cdata.refresh_rate
    @refresh_rate.setter
    def refresh_rate(self, value): self.cdata.refresh_rate = value
    @property
    def driverdata(self): return self.cdata.driverdata
    @driverdata.setter
    def driverdata(self, value): self.cdata.driverdata = value
    pass

class SDL_DollarGestureEvent(Struct):
    """Wrap `SDL_DollarGestureEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def touchId(self): return self.cdata.touchId
    @touchId.setter
    def touchId(self, value): self.cdata.touchId = value
    @property
    def gestureId(self): return self.cdata.gestureId
    @gestureId.setter
    def gestureId(self, value): self.cdata.gestureId = value
    @property
    def numFingers(self): return self.cdata.numFingers
    @numFingers.setter
    def numFingers(self, value): self.cdata.numFingers = value
    @property
    def error(self): return self.cdata.error
    @error.setter
    def error(self, value): self.cdata.error = value
    @property
    def x(self): return self.cdata.x
    @x.setter
    def x(self, value): self.cdata.x = value
    @property
    def y(self): return self.cdata.y
    @y.setter
    def y(self, value): self.cdata.y = value
    pass

class SDL_DropEvent(Struct):
    """Wrap `SDL_DropEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def file(self): return self.cdata.file
    @file.setter
    def file(self, value): self.cdata.file = value
    pass

class SDL_Event(Struct):
    """Wrap `SDL_Event`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def common(self): return self.cdata.common
    @common.setter
    def common(self, value): self.cdata.common = value
    @property
    def window(self): return self.cdata.window
    @window.setter
    def window(self, value): self.cdata.window = value
    @property
    def key(self): return self.cdata.key
    @key.setter
    def key(self, value): self.cdata.key = value
    @property
    def edit(self): return self.cdata.edit
    @edit.setter
    def edit(self, value): self.cdata.edit = value
    @property
    def text(self): return self.cdata.text
    @text.setter
    def text(self, value): self.cdata.text = value
    @property
    def motion(self): return self.cdata.motion
    @motion.setter
    def motion(self, value): self.cdata.motion = value
    @property
    def button(self): return self.cdata.button
    @button.setter
    def button(self, value): self.cdata.button = value
    @property
    def wheel(self): return self.cdata.wheel
    @wheel.setter
    def wheel(self, value): self.cdata.wheel = value
    @property
    def jaxis(self): return self.cdata.jaxis
    @jaxis.setter
    def jaxis(self, value): self.cdata.jaxis = value
    @property
    def jball(self): return self.cdata.jball
    @jball.setter
    def jball(self, value): self.cdata.jball = value
    @property
    def jhat(self): return self.cdata.jhat
    @jhat.setter
    def jhat(self, value): self.cdata.jhat = value
    @property
    def jbutton(self): return self.cdata.jbutton
    @jbutton.setter
    def jbutton(self, value): self.cdata.jbutton = value
    @property
    def jdevice(self): return self.cdata.jdevice
    @jdevice.setter
    def jdevice(self, value): self.cdata.jdevice = value
    @property
    def caxis(self): return self.cdata.caxis
    @caxis.setter
    def caxis(self, value): self.cdata.caxis = value
    @property
    def cbutton(self): return self.cdata.cbutton
    @cbutton.setter
    def cbutton(self, value): self.cdata.cbutton = value
    @property
    def cdevice(self): return self.cdata.cdevice
    @cdevice.setter
    def cdevice(self, value): self.cdata.cdevice = value
    @property
    def quit(self): return self.cdata.quit
    @quit.setter
    def quit(self, value): self.cdata.quit = value
    @property
    def user(self): return self.cdata.user
    @user.setter
    def user(self, value): self.cdata.user = value
    @property
    def syswm(self): return self.cdata.syswm
    @syswm.setter
    def syswm(self, value): self.cdata.syswm = value
    @property
    def tfinger(self): return self.cdata.tfinger
    @tfinger.setter
    def tfinger(self, value): self.cdata.tfinger = value
    @property
    def mgesture(self): return self.cdata.mgesture
    @mgesture.setter
    def mgesture(self, value): self.cdata.mgesture = value
    @property
    def dgesture(self): return self.cdata.dgesture
    @dgesture.setter
    def dgesture(self, value): self.cdata.dgesture = value
    @property
    def drop(self): return self.cdata.drop
    @drop.setter
    def drop(self, value): self.cdata.drop = value
    @property
    def padding(self): return self.cdata.padding
    @padding.setter
    def padding(self, value): self.cdata.padding = value
    peepEvents = SDL_PeepEvents
    pollEvent = SDL_PollEvent
    pushEvent = SDL_PushEvent
    waitEvent = SDL_WaitEvent
    waitEventTimeout = SDL_WaitEventTimeout

class SDL_Finger(Struct):
    """Wrap `SDL_Finger`"""
    @property
    def id(self): return self.cdata.id
    @id.setter
    def id(self, value): self.cdata.id = value
    @property
    def x(self): return self.cdata.x
    @x.setter
    def x(self, value): self.cdata.x = value
    @property
    def y(self): return self.cdata.y
    @y.setter
    def y(self, value): self.cdata.y = value
    @property
    def pressure(self): return self.cdata.pressure
    @pressure.setter
    def pressure(self, value): self.cdata.pressure = value
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
    @property
    def bindType(self): return self.cdata.bindType
    @bindType.setter
    def bindType(self, value): self.cdata.bindType = value
    @property
    def value(self): return self.cdata.value
    @value.setter
    def value(self, value): self.cdata.value = value
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
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def direction(self): return self.cdata.direction
    @direction.setter
    def direction(self, value): self.cdata.direction = value
    @property
    def length(self): return self.cdata.length
    @length.setter
    def length(self, value): self.cdata.length = value
    @property
    def delay(self): return self.cdata.delay
    @delay.setter
    def delay(self, value): self.cdata.delay = value
    @property
    def button(self): return self.cdata.button
    @button.setter
    def button(self, value): self.cdata.button = value
    @property
    def interval(self): return self.cdata.interval
    @interval.setter
    def interval(self, value): self.cdata.interval = value
    @property
    def right_sat(self): return self.cdata.right_sat
    @right_sat.setter
    def right_sat(self, value): self.cdata.right_sat = value
    @property
    def left_sat(self): return self.cdata.left_sat
    @left_sat.setter
    def left_sat(self, value): self.cdata.left_sat = value
    @property
    def right_coeff(self): return self.cdata.right_coeff
    @right_coeff.setter
    def right_coeff(self, value): self.cdata.right_coeff = value
    @property
    def left_coeff(self): return self.cdata.left_coeff
    @left_coeff.setter
    def left_coeff(self, value): self.cdata.left_coeff = value
    @property
    def deadband(self): return self.cdata.deadband
    @deadband.setter
    def deadband(self, value): self.cdata.deadband = value
    @property
    def center(self): return self.cdata.center
    @center.setter
    def center(self, value): self.cdata.center = value
    pass

class SDL_HapticConstant(Struct):
    """Wrap `SDL_HapticConstant`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def direction(self): return self.cdata.direction
    @direction.setter
    def direction(self, value): self.cdata.direction = value
    @property
    def length(self): return self.cdata.length
    @length.setter
    def length(self, value): self.cdata.length = value
    @property
    def delay(self): return self.cdata.delay
    @delay.setter
    def delay(self, value): self.cdata.delay = value
    @property
    def button(self): return self.cdata.button
    @button.setter
    def button(self, value): self.cdata.button = value
    @property
    def interval(self): return self.cdata.interval
    @interval.setter
    def interval(self, value): self.cdata.interval = value
    @property
    def level(self): return self.cdata.level
    @level.setter
    def level(self, value): self.cdata.level = value
    @property
    def attack_length(self): return self.cdata.attack_length
    @attack_length.setter
    def attack_length(self, value): self.cdata.attack_length = value
    @property
    def attack_level(self): return self.cdata.attack_level
    @attack_level.setter
    def attack_level(self, value): self.cdata.attack_level = value
    @property
    def fade_length(self): return self.cdata.fade_length
    @fade_length.setter
    def fade_length(self, value): self.cdata.fade_length = value
    @property
    def fade_level(self): return self.cdata.fade_level
    @fade_level.setter
    def fade_level(self, value): self.cdata.fade_level = value
    pass

class SDL_HapticCustom(Struct):
    """Wrap `SDL_HapticCustom`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def direction(self): return self.cdata.direction
    @direction.setter
    def direction(self, value): self.cdata.direction = value
    @property
    def length(self): return self.cdata.length
    @length.setter
    def length(self, value): self.cdata.length = value
    @property
    def delay(self): return self.cdata.delay
    @delay.setter
    def delay(self, value): self.cdata.delay = value
    @property
    def button(self): return self.cdata.button
    @button.setter
    def button(self, value): self.cdata.button = value
    @property
    def interval(self): return self.cdata.interval
    @interval.setter
    def interval(self, value): self.cdata.interval = value
    @property
    def channels(self): return self.cdata.channels
    @channels.setter
    def channels(self, value): self.cdata.channels = value
    @property
    def period(self): return self.cdata.period
    @period.setter
    def period(self, value): self.cdata.period = value
    @property
    def samples(self): return self.cdata.samples
    @samples.setter
    def samples(self, value): self.cdata.samples = value
    @property
    def data(self): return self.cdata.data
    @data.setter
    def data(self, value): self.cdata.data = value
    @property
    def attack_length(self): return self.cdata.attack_length
    @attack_length.setter
    def attack_length(self, value): self.cdata.attack_length = value
    @property
    def attack_level(self): return self.cdata.attack_level
    @attack_level.setter
    def attack_level(self, value): self.cdata.attack_level = value
    @property
    def fade_length(self): return self.cdata.fade_length
    @fade_length.setter
    def fade_length(self, value): self.cdata.fade_length = value
    @property
    def fade_level(self): return self.cdata.fade_level
    @fade_level.setter
    def fade_level(self, value): self.cdata.fade_level = value
    pass

class SDL_HapticDirection(Struct):
    """Wrap `SDL_HapticDirection`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def dir(self): return self.cdata.dir
    @dir.setter
    def dir(self, value): self.cdata.dir = value
    pass

class SDL_HapticEffect(Struct):
    """Wrap `SDL_HapticEffect`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def constant(self): return self.cdata.constant
    @constant.setter
    def constant(self, value): self.cdata.constant = value
    @property
    def periodic(self): return self.cdata.periodic
    @periodic.setter
    def periodic(self, value): self.cdata.periodic = value
    @property
    def condition(self): return self.cdata.condition
    @condition.setter
    def condition(self, value): self.cdata.condition = value
    @property
    def ramp(self): return self.cdata.ramp
    @ramp.setter
    def ramp(self, value): self.cdata.ramp = value
    @property
    def leftright(self): return self.cdata.leftright
    @leftright.setter
    def leftright(self, value): self.cdata.leftright = value
    @property
    def custom(self): return self.cdata.custom
    @custom.setter
    def custom(self, value): self.cdata.custom = value
    pass

class SDL_HapticLeftRight(Struct):
    """Wrap `SDL_HapticLeftRight`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def length(self): return self.cdata.length
    @length.setter
    def length(self, value): self.cdata.length = value
    @property
    def large_magnitude(self): return self.cdata.large_magnitude
    @large_magnitude.setter
    def large_magnitude(self, value): self.cdata.large_magnitude = value
    @property
    def small_magnitude(self): return self.cdata.small_magnitude
    @small_magnitude.setter
    def small_magnitude(self, value): self.cdata.small_magnitude = value
    pass

class SDL_HapticPeriodic(Struct):
    """Wrap `SDL_HapticPeriodic`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def direction(self): return self.cdata.direction
    @direction.setter
    def direction(self, value): self.cdata.direction = value
    @property
    def length(self): return self.cdata.length
    @length.setter
    def length(self, value): self.cdata.length = value
    @property
    def delay(self): return self.cdata.delay
    @delay.setter
    def delay(self, value): self.cdata.delay = value
    @property
    def button(self): return self.cdata.button
    @button.setter
    def button(self, value): self.cdata.button = value
    @property
    def interval(self): return self.cdata.interval
    @interval.setter
    def interval(self, value): self.cdata.interval = value
    @property
    def period(self): return self.cdata.period
    @period.setter
    def period(self, value): self.cdata.period = value
    @property
    def magnitude(self): return self.cdata.magnitude
    @magnitude.setter
    def magnitude(self, value): self.cdata.magnitude = value
    @property
    def offset(self): return self.cdata.offset
    @offset.setter
    def offset(self, value): self.cdata.offset = value
    @property
    def phase(self): return self.cdata.phase
    @phase.setter
    def phase(self, value): self.cdata.phase = value
    @property
    def attack_length(self): return self.cdata.attack_length
    @attack_length.setter
    def attack_length(self, value): self.cdata.attack_length = value
    @property
    def attack_level(self): return self.cdata.attack_level
    @attack_level.setter
    def attack_level(self, value): self.cdata.attack_level = value
    @property
    def fade_length(self): return self.cdata.fade_length
    @fade_length.setter
    def fade_length(self, value): self.cdata.fade_length = value
    @property
    def fade_level(self): return self.cdata.fade_level
    @fade_level.setter
    def fade_level(self, value): self.cdata.fade_level = value
    pass

class SDL_HapticRamp(Struct):
    """Wrap `SDL_HapticRamp`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def direction(self): return self.cdata.direction
    @direction.setter
    def direction(self, value): self.cdata.direction = value
    @property
    def length(self): return self.cdata.length
    @length.setter
    def length(self, value): self.cdata.length = value
    @property
    def delay(self): return self.cdata.delay
    @delay.setter
    def delay(self, value): self.cdata.delay = value
    @property
    def button(self): return self.cdata.button
    @button.setter
    def button(self, value): self.cdata.button = value
    @property
    def interval(self): return self.cdata.interval
    @interval.setter
    def interval(self, value): self.cdata.interval = value
    @property
    def start(self): return self.cdata.start
    @start.setter
    def start(self, value): self.cdata.start = value
    @property
    def end(self): return self.cdata.end
    @end.setter
    def end(self, value): self.cdata.end = value
    @property
    def attack_length(self): return self.cdata.attack_length
    @attack_length.setter
    def attack_length(self, value): self.cdata.attack_length = value
    @property
    def attack_level(self): return self.cdata.attack_level
    @attack_level.setter
    def attack_level(self, value): self.cdata.attack_level = value
    @property
    def fade_length(self): return self.cdata.fade_length
    @fade_length.setter
    def fade_length(self, value): self.cdata.fade_length = value
    @property
    def fade_level(self): return self.cdata.fade_level
    @fade_level.setter
    def fade_level(self, value): self.cdata.fade_level = value
    pass

class SDL_JoyAxisEvent(Struct):
    """Wrap `SDL_JoyAxisEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def which(self): return self.cdata.which
    @which.setter
    def which(self, value): self.cdata.which = value
    @property
    def axis(self): return self.cdata.axis
    @axis.setter
    def axis(self, value): self.cdata.axis = value
    @property
    def padding1(self): return self.cdata.padding1
    @padding1.setter
    def padding1(self, value): self.cdata.padding1 = value
    @property
    def padding2(self): return self.cdata.padding2
    @padding2.setter
    def padding2(self, value): self.cdata.padding2 = value
    @property
    def padding3(self): return self.cdata.padding3
    @padding3.setter
    def padding3(self, value): self.cdata.padding3 = value
    @property
    def value(self): return self.cdata.value
    @value.setter
    def value(self, value): self.cdata.value = value
    @property
    def padding4(self): return self.cdata.padding4
    @padding4.setter
    def padding4(self, value): self.cdata.padding4 = value
    pass

class SDL_JoyBallEvent(Struct):
    """Wrap `SDL_JoyBallEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def which(self): return self.cdata.which
    @which.setter
    def which(self, value): self.cdata.which = value
    @property
    def ball(self): return self.cdata.ball
    @ball.setter
    def ball(self, value): self.cdata.ball = value
    @property
    def padding1(self): return self.cdata.padding1
    @padding1.setter
    def padding1(self, value): self.cdata.padding1 = value
    @property
    def padding2(self): return self.cdata.padding2
    @padding2.setter
    def padding2(self, value): self.cdata.padding2 = value
    @property
    def padding3(self): return self.cdata.padding3
    @padding3.setter
    def padding3(self, value): self.cdata.padding3 = value
    @property
    def xrel(self): return self.cdata.xrel
    @xrel.setter
    def xrel(self, value): self.cdata.xrel = value
    @property
    def yrel(self): return self.cdata.yrel
    @yrel.setter
    def yrel(self, value): self.cdata.yrel = value
    pass

class SDL_JoyButtonEvent(Struct):
    """Wrap `SDL_JoyButtonEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def which(self): return self.cdata.which
    @which.setter
    def which(self, value): self.cdata.which = value
    @property
    def button(self): return self.cdata.button
    @button.setter
    def button(self, value): self.cdata.button = value
    @property
    def state(self): return self.cdata.state
    @state.setter
    def state(self, value): self.cdata.state = value
    @property
    def padding1(self): return self.cdata.padding1
    @padding1.setter
    def padding1(self, value): self.cdata.padding1 = value
    @property
    def padding2(self): return self.cdata.padding2
    @padding2.setter
    def padding2(self, value): self.cdata.padding2 = value
    pass

class SDL_JoyDeviceEvent(Struct):
    """Wrap `SDL_JoyDeviceEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def which(self): return self.cdata.which
    @which.setter
    def which(self, value): self.cdata.which = value
    pass

class SDL_JoyHatEvent(Struct):
    """Wrap `SDL_JoyHatEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def which(self): return self.cdata.which
    @which.setter
    def which(self, value): self.cdata.which = value
    @property
    def hat(self): return self.cdata.hat
    @hat.setter
    def hat(self, value): self.cdata.hat = value
    @property
    def value(self): return self.cdata.value
    @value.setter
    def value(self, value): self.cdata.value = value
    @property
    def padding1(self): return self.cdata.padding1
    @padding1.setter
    def padding1(self, value): self.cdata.padding1 = value
    @property
    def padding2(self): return self.cdata.padding2
    @padding2.setter
    def padding2(self, value): self.cdata.padding2 = value
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
    @property
    def data(self): return self.cdata.data
    @data.setter
    def data(self, value): self.cdata.data = value
    pass

class SDL_KeyboardEvent(Struct):
    """Wrap `SDL_KeyboardEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def windowID(self): return self.cdata.windowID
    @windowID.setter
    def windowID(self, value): self.cdata.windowID = value
    @property
    def state(self): return self.cdata.state
    @state.setter
    def state(self, value): self.cdata.state = value
    @property
    def repeat(self): return self.cdata.repeat
    @repeat.setter
    def repeat(self, value): self.cdata.repeat = value
    @property
    def padding2(self): return self.cdata.padding2
    @padding2.setter
    def padding2(self, value): self.cdata.padding2 = value
    @property
    def padding3(self): return self.cdata.padding3
    @padding3.setter
    def padding3(self, value): self.cdata.padding3 = value
    @property
    def keysym(self): return self.cdata.keysym
    @keysym.setter
    def keysym(self, value): self.cdata.keysym = value
    pass

class SDL_Keysym(Struct):
    """Wrap `SDL_Keysym`"""
    @property
    def scancode(self): return self.cdata.scancode
    @scancode.setter
    def scancode(self, value): self.cdata.scancode = value
    @property
    def sym(self): return self.cdata.sym
    @sym.setter
    def sym(self, value): self.cdata.sym = value
    @property
    def mod(self): return self.cdata.mod
    @mod.setter
    def mod(self, value): self.cdata.mod = value
    @property
    def unused(self): return self.cdata.unused
    @unused.setter
    def unused(self, value): self.cdata.unused = value
    pass

class SDL_MessageBoxButtonData(Struct):
    """Wrap `SDL_MessageBoxButtonData`"""
    @property
    def flags(self): return self.cdata.flags
    @flags.setter
    def flags(self, value): self.cdata.flags = value
    @property
    def buttonid(self): return self.cdata.buttonid
    @buttonid.setter
    def buttonid(self, value): self.cdata.buttonid = value
    @property
    def text(self): return self.cdata.text
    @text.setter
    def text(self, value): self.cdata.text = value
    pass

class SDL_MessageBoxColor(Struct):
    """Wrap `SDL_MessageBoxColor`"""
    @property
    def r(self): return self.cdata.r
    @r.setter
    def r(self, value): self.cdata.r = value
    @property
    def g(self): return self.cdata.g
    @g.setter
    def g(self, value): self.cdata.g = value
    @property
    def b(self): return self.cdata.b
    @b.setter
    def b(self, value): self.cdata.b = value
    pass

class SDL_MessageBoxColorScheme(Struct):
    """Wrap `SDL_MessageBoxColorScheme`"""
    @property
    def colors(self): return self.cdata.colors
    @colors.setter
    def colors(self, value): self.cdata.colors = value
    pass

class SDL_MessageBoxData(Struct):
    """Wrap `SDL_MessageBoxData`"""
    @property
    def flags(self): return self.cdata.flags
    @flags.setter
    def flags(self, value): self.cdata.flags = value
    @property
    def window(self): return self.cdata.window
    @window.setter
    def window(self, value): self.cdata.window = value
    @property
    def title(self): return self.cdata.title
    @title.setter
    def title(self, value): self.cdata.title = value
    @property
    def message(self): return self.cdata.message
    @message.setter
    def message(self, value): self.cdata.message = value
    @property
    def numbuttons(self): return self.cdata.numbuttons
    @numbuttons.setter
    def numbuttons(self, value): self.cdata.numbuttons = value
    @property
    def buttons(self): return self.cdata.buttons
    @buttons.setter
    def buttons(self, value): self.cdata.buttons = value
    @property
    def colorScheme(self): return self.cdata.colorScheme
    @colorScheme.setter
    def colorScheme(self, value): self.cdata.colorScheme = value
    showMessageBox = SDL_ShowMessageBox

class SDL_MouseButtonEvent(Struct):
    """Wrap `SDL_MouseButtonEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def windowID(self): return self.cdata.windowID
    @windowID.setter
    def windowID(self, value): self.cdata.windowID = value
    @property
    def which(self): return self.cdata.which
    @which.setter
    def which(self, value): self.cdata.which = value
    @property
    def button(self): return self.cdata.button
    @button.setter
    def button(self, value): self.cdata.button = value
    @property
    def state(self): return self.cdata.state
    @state.setter
    def state(self, value): self.cdata.state = value
    @property
    def padding1(self): return self.cdata.padding1
    @padding1.setter
    def padding1(self, value): self.cdata.padding1 = value
    @property
    def padding2(self): return self.cdata.padding2
    @padding2.setter
    def padding2(self, value): self.cdata.padding2 = value
    @property
    def x(self): return self.cdata.x
    @x.setter
    def x(self, value): self.cdata.x = value
    @property
    def y(self): return self.cdata.y
    @y.setter
    def y(self, value): self.cdata.y = value
    pass

class SDL_MouseMotionEvent(Struct):
    """Wrap `SDL_MouseMotionEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def windowID(self): return self.cdata.windowID
    @windowID.setter
    def windowID(self, value): self.cdata.windowID = value
    @property
    def which(self): return self.cdata.which
    @which.setter
    def which(self, value): self.cdata.which = value
    @property
    def state(self): return self.cdata.state
    @state.setter
    def state(self, value): self.cdata.state = value
    @property
    def x(self): return self.cdata.x
    @x.setter
    def x(self, value): self.cdata.x = value
    @property
    def y(self): return self.cdata.y
    @y.setter
    def y(self, value): self.cdata.y = value
    @property
    def xrel(self): return self.cdata.xrel
    @xrel.setter
    def xrel(self, value): self.cdata.xrel = value
    @property
    def yrel(self): return self.cdata.yrel
    @yrel.setter
    def yrel(self, value): self.cdata.yrel = value
    pass

class SDL_MouseWheelEvent(Struct):
    """Wrap `SDL_MouseWheelEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def windowID(self): return self.cdata.windowID
    @windowID.setter
    def windowID(self, value): self.cdata.windowID = value
    @property
    def which(self): return self.cdata.which
    @which.setter
    def which(self, value): self.cdata.which = value
    @property
    def x(self): return self.cdata.x
    @x.setter
    def x(self, value): self.cdata.x = value
    @property
    def y(self): return self.cdata.y
    @y.setter
    def y(self, value): self.cdata.y = value
    pass

class SDL_MultiGestureEvent(Struct):
    """Wrap `SDL_MultiGestureEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def touchId(self): return self.cdata.touchId
    @touchId.setter
    def touchId(self, value): self.cdata.touchId = value
    @property
    def dTheta(self): return self.cdata.dTheta
    @dTheta.setter
    def dTheta(self, value): self.cdata.dTheta = value
    @property
    def dDist(self): return self.cdata.dDist
    @dDist.setter
    def dDist(self, value): self.cdata.dDist = value
    @property
    def x(self): return self.cdata.x
    @x.setter
    def x(self, value): self.cdata.x = value
    @property
    def y(self): return self.cdata.y
    @y.setter
    def y(self, value): self.cdata.y = value
    @property
    def numFingers(self): return self.cdata.numFingers
    @numFingers.setter
    def numFingers(self, value): self.cdata.numFingers = value
    @property
    def padding(self): return self.cdata.padding
    @padding.setter
    def padding(self, value): self.cdata.padding = value
    pass

class SDL_OSEvent(Struct):
    """Wrap `SDL_OSEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    pass

class SDL_Palette(Struct):
    """Wrap `SDL_Palette`"""
    @property
    def ncolors(self): return self.cdata.ncolors
    @ncolors.setter
    def ncolors(self, value): self.cdata.ncolors = value
    @property
    def colors(self): return self.cdata.colors
    @colors.setter
    def colors(self, value): self.cdata.colors = value
    @property
    def version(self): return self.cdata.version
    @version.setter
    def version(self, value): self.cdata.version = value
    @property
    def refcount(self): return self.cdata.refcount
    @refcount.setter
    def refcount(self, value): self.cdata.refcount = value
    freePalette = SDL_FreePalette
    setPaletteColors = SDL_SetPaletteColors

class SDL_PixelFormat(Struct):
    """Wrap `SDL_PixelFormat`"""
    @property
    def format(self): return self.cdata.format
    @format.setter
    def format(self, value): self.cdata.format = value
    @property
    def palette(self): return self.cdata.palette
    @palette.setter
    def palette(self, value): self.cdata.palette = value
    @property
    def BitsPerPixel(self): return self.cdata.BitsPerPixel
    @BitsPerPixel.setter
    def BitsPerPixel(self, value): self.cdata.BitsPerPixel = value
    @property
    def BytesPerPixel(self): return self.cdata.BytesPerPixel
    @BytesPerPixel.setter
    def BytesPerPixel(self, value): self.cdata.BytesPerPixel = value
    @property
    def padding(self): return self.cdata.padding
    @padding.setter
    def padding(self, value): self.cdata.padding = value
    @property
    def Rmask(self): return self.cdata.Rmask
    @Rmask.setter
    def Rmask(self, value): self.cdata.Rmask = value
    @property
    def Gmask(self): return self.cdata.Gmask
    @Gmask.setter
    def Gmask(self, value): self.cdata.Gmask = value
    @property
    def Bmask(self): return self.cdata.Bmask
    @Bmask.setter
    def Bmask(self, value): self.cdata.Bmask = value
    @property
    def Amask(self): return self.cdata.Amask
    @Amask.setter
    def Amask(self, value): self.cdata.Amask = value
    @property
    def Rloss(self): return self.cdata.Rloss
    @Rloss.setter
    def Rloss(self, value): self.cdata.Rloss = value
    @property
    def Gloss(self): return self.cdata.Gloss
    @Gloss.setter
    def Gloss(self, value): self.cdata.Gloss = value
    @property
    def Bloss(self): return self.cdata.Bloss
    @Bloss.setter
    def Bloss(self, value): self.cdata.Bloss = value
    @property
    def Aloss(self): return self.cdata.Aloss
    @Aloss.setter
    def Aloss(self, value): self.cdata.Aloss = value
    @property
    def Rshift(self): return self.cdata.Rshift
    @Rshift.setter
    def Rshift(self, value): self.cdata.Rshift = value
    @property
    def Gshift(self): return self.cdata.Gshift
    @Gshift.setter
    def Gshift(self, value): self.cdata.Gshift = value
    @property
    def Bshift(self): return self.cdata.Bshift
    @Bshift.setter
    def Bshift(self, value): self.cdata.Bshift = value
    @property
    def Ashift(self): return self.cdata.Ashift
    @Ashift.setter
    def Ashift(self, value): self.cdata.Ashift = value
    @property
    def refcount(self): return self.cdata.refcount
    @refcount.setter
    def refcount(self, value): self.cdata.refcount = value
    @property
    def next(self): return self.cdata.next
    @next.setter
    def next(self, value): self.cdata.next = value
    freeFormat = SDL_FreeFormat
    mapRGB = SDL_MapRGB
    mapRGBA = SDL_MapRGBA
    setPixelFormatPalette = SDL_SetPixelFormatPalette

class SDL_Point(Struct):
    """Wrap `SDL_Point`"""
    @property
    def x(self): return self.cdata.x
    @x.setter
    def x(self, value): self.cdata.x = value
    @property
    def y(self): return self.cdata.y
    @y.setter
    def y(self, value): self.cdata.y = value
    enclosePoints = SDL_EnclosePoints

class SDL_QuitEvent(Struct):
    """Wrap `SDL_QuitEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    pass

class SDL_RWops(Struct):
    """Wrap `SDL_RWops`"""
    @property
    def size(self): return self.cdata.size
    @size.setter
    def size(self, value): self.cdata.size = value
    @property
    def seek(self): return self.cdata.seek
    @seek.setter
    def seek(self, value): self.cdata.seek = value
    @property
    def read(self): return self.cdata.read
    @read.setter
    def read(self, value): self.cdata.read = value
    @property
    def write(self): return self.cdata.write
    @write.setter
    def write(self, value): self.cdata.write = value
    @property
    def close(self): return self.cdata.close
    @close.setter
    def close(self, value): self.cdata.close = value
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def hidden(self): return self.cdata.hidden
    @hidden.setter
    def hidden(self, value): self.cdata.hidden = value
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
    @property
    def x(self): return self.cdata.x
    @x.setter
    def x(self, value): self.cdata.x = value
    @property
    def y(self): return self.cdata.y
    @y.setter
    def y(self, value): self.cdata.y = value
    @property
    def w(self): return self.cdata.w
    @w.setter
    def w(self, value): self.cdata.w = value
    @property
    def h(self): return self.cdata.h
    @h.setter
    def h(self, value): self.cdata.h = value
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
    @property
    def name(self): return self.cdata.name
    @name.setter
    def name(self, value): self.cdata.name = value
    @property
    def flags(self): return self.cdata.flags
    @flags.setter
    def flags(self, value): self.cdata.flags = value
    @property
    def num_texture_formats(self): return self.cdata.num_texture_formats
    @num_texture_formats.setter
    def num_texture_formats(self, value): self.cdata.num_texture_formats = value
    @property
    def texture_formats(self): return self.cdata.texture_formats
    @texture_formats.setter
    def texture_formats(self, value): self.cdata.texture_formats = value
    @property
    def max_texture_width(self): return self.cdata.max_texture_width
    @max_texture_width.setter
    def max_texture_width(self, value): self.cdata.max_texture_width = value
    @property
    def max_texture_height(self): return self.cdata.max_texture_height
    @max_texture_height.setter
    def max_texture_height(self, value): self.cdata.max_texture_height = value
    pass

class SDL_Surface(Struct):
    """Wrap `SDL_Surface`"""
    @property
    def flags(self): return self.cdata.flags
    @flags.setter
    def flags(self, value): self.cdata.flags = value
    @property
    def format(self): return self.cdata.format
    @format.setter
    def format(self, value): self.cdata.format = value
    @property
    def w(self): return self.cdata.w
    @w.setter
    def w(self, value): self.cdata.w = value
    @property
    def h(self): return self.cdata.h
    @h.setter
    def h(self, value): self.cdata.h = value
    @property
    def pitch(self): return self.cdata.pitch
    @pitch.setter
    def pitch(self, value): self.cdata.pitch = value
    @property
    def pixels(self): return self.cdata.pixels
    @pixels.setter
    def pixels(self, value): self.cdata.pixels = value
    @property
    def userdata(self): return self.cdata.userdata
    @userdata.setter
    def userdata(self, value): self.cdata.userdata = value
    @property
    def locked(self): return self.cdata.locked
    @locked.setter
    def locked(self, value): self.cdata.locked = value
    @property
    def lock_data(self): return self.cdata.lock_data
    @lock_data.setter
    def lock_data(self, value): self.cdata.lock_data = value
    @property
    def clip_rect(self): return self.cdata.clip_rect
    @clip_rect.setter
    def clip_rect(self, value): self.cdata.clip_rect = value
    @property
    def map(self): return self.cdata.map
    @map.setter
    def map(self, value): self.cdata.map = value
    @property
    def refcount(self): return self.cdata.refcount
    @refcount.setter
    def refcount(self, value): self.cdata.refcount = value
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
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def msg(self): return self.cdata.msg
    @msg.setter
    def msg(self, value): self.cdata.msg = value
    pass

class SDL_SysWMmsg(Struct):
    """Wrap `SDL_SysWMmsg`"""
    pass

class SDL_TextEditingEvent(Struct):
    """Wrap `SDL_TextEditingEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def windowID(self): return self.cdata.windowID
    @windowID.setter
    def windowID(self, value): self.cdata.windowID = value
    @property
    def text(self): return self.cdata.text
    @text.setter
    def text(self, value): self.cdata.text = value
    @property
    def start(self): return self.cdata.start
    @start.setter
    def start(self, value): self.cdata.start = value
    @property
    def length(self): return self.cdata.length
    @length.setter
    def length(self, value): self.cdata.length = value
    pass

class SDL_TextInputEvent(Struct):
    """Wrap `SDL_TextInputEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def windowID(self): return self.cdata.windowID
    @windowID.setter
    def windowID(self, value): self.cdata.windowID = value
    @property
    def text(self): return self.cdata.text
    @text.setter
    def text(self, value): self.cdata.text = value
    pass

class SDL_Texture(Struct):
    """Wrap `SDL_Texture`"""
    destroyTexture = SDL_DestroyTexture
    GL_BindTexture = SDL_GL_BindTexture
    GL_UnbindTexture = SDL_GL_UnbindTexture
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
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def touchId(self): return self.cdata.touchId
    @touchId.setter
    def touchId(self, value): self.cdata.touchId = value
    @property
    def fingerId(self): return self.cdata.fingerId
    @fingerId.setter
    def fingerId(self, value): self.cdata.fingerId = value
    @property
    def x(self): return self.cdata.x
    @x.setter
    def x(self, value): self.cdata.x = value
    @property
    def y(self): return self.cdata.y
    @y.setter
    def y(self, value): self.cdata.y = value
    @property
    def dx(self): return self.cdata.dx
    @dx.setter
    def dx(self, value): self.cdata.dx = value
    @property
    def dy(self): return self.cdata.dy
    @dy.setter
    def dy(self, value): self.cdata.dy = value
    @property
    def pressure(self): return self.cdata.pressure
    @pressure.setter
    def pressure(self, value): self.cdata.pressure = value
    pass

class SDL_UserEvent(Struct):
    """Wrap `SDL_UserEvent`"""
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def windowID(self): return self.cdata.windowID
    @windowID.setter
    def windowID(self, value): self.cdata.windowID = value
    @property
    def code(self): return self.cdata.code
    @code.setter
    def code(self, value): self.cdata.code = value
    @property
    def data1(self): return self.cdata.data1
    @data1.setter
    def data1(self, value): self.cdata.data1 = value
    @property
    def data2(self): return self.cdata.data2
    @data2.setter
    def data2(self, value): self.cdata.data2 = value
    pass

class SDL_Window(Struct):
    """Wrap `SDL_Window`"""
    createRenderer = SDL_CreateRenderer
    destroyWindow = SDL_DestroyWindow
    GL_CreateContext = SDL_GL_CreateContext
    GL_MakeCurrent = SDL_GL_MakeCurrent
    GL_SwapWindow = SDL_GL_SwapWindow
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
    @property
    def type(self): return self.cdata.type
    @type.setter
    def type(self, value): self.cdata.type = value
    @property
    def timestamp(self): return self.cdata.timestamp
    @timestamp.setter
    def timestamp(self, value): self.cdata.timestamp = value
    @property
    def windowID(self): return self.cdata.windowID
    @windowID.setter
    def windowID(self, value): self.cdata.windowID = value
    @property
    def event(self): return self.cdata.event
    @event.setter
    def event(self, value): self.cdata.event = value
    @property
    def padding1(self): return self.cdata.padding1
    @padding1.setter
    def padding1(self, value): self.cdata.padding1 = value
    @property
    def padding2(self): return self.cdata.padding2
    @padding2.setter
    def padding2(self, value): self.cdata.padding2 = value
    @property
    def padding3(self): return self.cdata.padding3
    @padding3.setter
    def padding3(self, value): self.cdata.padding3 = value
    @property
    def data1(self): return self.cdata.data1
    @data1.setter
    def data1(self, value): self.cdata.data1 = value
    @property
    def data2(self): return self.cdata.data2
    @data2.setter
    def data2(self, value): self.cdata.data2 = value
    pass

class SDL_assert_data(Struct):
    """Wrap `SDL_assert_data`"""
    @property
    def always_ignore(self): return self.cdata.always_ignore
    @always_ignore.setter
    def always_ignore(self, value): self.cdata.always_ignore = value
    @property
    def trigger_count(self): return self.cdata.trigger_count
    @trigger_count.setter
    def trigger_count(self, value): self.cdata.trigger_count = value
    @property
    def condition(self): return self.cdata.condition
    @condition.setter
    def condition(self, value): self.cdata.condition = value
    @property
    def filename(self): return self.cdata.filename
    @filename.setter
    def filename(self, value): self.cdata.filename = value
    @property
    def linenum(self): return self.cdata.linenum
    @linenum.setter
    def linenum(self, value): self.cdata.linenum = value
    @property
    def function(self): return self.cdata.function
    @function.setter
    def function(self, value): self.cdata.function = value
    @property
    def next(self): return self.cdata.next
    @next.setter
    def next(self, value): self.cdata.next = value
    reportAssertion = SDL_ReportAssertion

class SDL_atomic_t(Struct):
    """Wrap `SDL_atomic_t`"""
    @property
    def value(self): return self.cdata.value
    @value.setter
    def value(self, value): self.cdata.value = value
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
    @property
    def major(self): return self.cdata.major
    @major.setter
    def major(self, value): self.cdata.major = value
    @property
    def minor(self): return self.cdata.minor
    @minor.setter
    def minor(self, value): self.cdata.minor = value
    @property
    def patch(self): return self.cdata.patch
    @patch.setter
    def patch(self, value): self.cdata.patch = value
    getVersion = SDL_GetVersion

