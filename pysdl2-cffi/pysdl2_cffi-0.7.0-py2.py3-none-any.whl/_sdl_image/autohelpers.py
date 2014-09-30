# Automatically generated wrappers.
# Override by adding wrappers to helpers.py.
from .dso import ffi, _LIB
from .structs import unbox
from _sdl.structs import SDLError, u8
from _sdl.autohelpers import SDL_Surface, SDL_Texture, SDL_version

def IMG_Init(flags):
    """
    ``int IMG_Init(int)``
    """
    flags_c = flags
    rc = _LIB.IMG_Init(flags_c)
    return rc

def IMG_Linked_Version():
    """
    ``SDL_version const * IMG_Linked_Version(void)``
    """
    rc = _LIB.IMG_Linked_Version()
    return SDL_version(rc)

def IMG_Load(file):
    """
    ``SDL_Surface * IMG_Load(char const *)``
    """
    file_c = u8(file)
    rc = _LIB.IMG_Load(file_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadBMP_RW(src):
    """
    ``SDL_Surface * IMG_LoadBMP_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadBMP_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadCUR_RW(src):
    """
    ``SDL_Surface * IMG_LoadCUR_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadCUR_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadGIF_RW(src):
    """
    ``SDL_Surface * IMG_LoadGIF_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadGIF_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadICO_RW(src):
    """
    ``SDL_Surface * IMG_LoadICO_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadICO_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadJPG_RW(src):
    """
    ``SDL_Surface * IMG_LoadJPG_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadJPG_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadLBM_RW(src):
    """
    ``SDL_Surface * IMG_LoadLBM_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadLBM_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadPCX_RW(src):
    """
    ``SDL_Surface * IMG_LoadPCX_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadPCX_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadPNG_RW(src):
    """
    ``SDL_Surface * IMG_LoadPNG_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadPNG_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadPNM_RW(src):
    """
    ``SDL_Surface * IMG_LoadPNM_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadPNM_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadTGA_RW(src):
    """
    ``SDL_Surface * IMG_LoadTGA_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadTGA_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadTIF_RW(src):
    """
    ``SDL_Surface * IMG_LoadTIF_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadTIF_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadTexture(renderer, file):
    """
    ``SDL_Texture * IMG_LoadTexture(SDL_Renderer *, char const *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    file_c = u8(file)
    rc = _LIB.IMG_LoadTexture(renderer_c, file_c)
    return SDL_Texture(rc)

def IMG_LoadTextureTyped_RW(renderer, src, freesrc, type):
    """
    ``SDL_Texture * IMG_LoadTextureTyped_RW(SDL_Renderer *, SDL_RWops *, int, char const *)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    src_c = unbox(src, 'SDL_RWops *')
    freesrc_c = freesrc
    type_c = u8(type)
    rc = _LIB.IMG_LoadTextureTyped_RW(renderer_c, src_c, freesrc_c, type_c)
    return SDL_Texture(rc)

def IMG_LoadTexture_RW(renderer, src, freesrc):
    """
    ``SDL_Texture * IMG_LoadTexture_RW(SDL_Renderer *, SDL_RWops *, int)``
    """
    renderer_c = unbox(renderer, 'SDL_Renderer *')
    src_c = unbox(src, 'SDL_RWops *')
    freesrc_c = freesrc
    rc = _LIB.IMG_LoadTexture_RW(renderer_c, src_c, freesrc_c)
    return SDL_Texture(rc)

def IMG_LoadTyped_RW(src, freesrc, type):
    """
    ``SDL_Surface * IMG_LoadTyped_RW(SDL_RWops *, int, char const *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    freesrc_c = freesrc
    type_c = u8(type)
    rc = _LIB.IMG_LoadTyped_RW(src_c, freesrc_c, type_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadWEBP_RW(src):
    """
    ``SDL_Surface * IMG_LoadWEBP_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadWEBP_RW(src_c)
    return SDL_Surface(rc)

def IMG_LoadXCF_RW(src):
    """
    ``SDL_Surface * IMG_LoadXCF_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadXCF_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadXPM_RW(src):
    """
    ``SDL_Surface * IMG_LoadXPM_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadXPM_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_LoadXV_RW(src):
    """
    ``SDL_Surface * IMG_LoadXV_RW(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_LoadXV_RW(src_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_Load_RW(src, freesrc):
    """
    ``SDL_Surface * IMG_Load_RW(SDL_RWops *, int)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    freesrc_c = freesrc
    rc = _LIB.IMG_Load_RW(src_c, freesrc_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_Quit():
    """
    ``void IMG_Quit(void)``
    """
    _LIB.IMG_Quit()

def IMG_ReadXPMFromArray(xpm):
    """
    ``SDL_Surface * IMG_ReadXPMFromArray(char * *)``
    """
    xpm_c = unbox(xpm, 'char * *')
    rc = _LIB.IMG_ReadXPMFromArray(xpm_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def IMG_SavePNG(surface, file):
    """
    ``int IMG_SavePNG(SDL_Surface *, char const *)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    file_c = u8(file)
    rc = _LIB.IMG_SavePNG(surface_c, file_c)
    return rc

def IMG_SavePNG_RW(surface, dst, freedst):
    """
    ``int IMG_SavePNG_RW(SDL_Surface *, SDL_RWops *, int)``
    """
    surface_c = unbox(surface, 'SDL_Surface *')
    dst_c = unbox(dst, 'SDL_RWops *')
    freedst_c = freedst
    rc = _LIB.IMG_SavePNG_RW(surface_c, dst_c, freedst_c)
    return rc

def IMG_isBMP(src):
    """
    ``int IMG_isBMP(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isBMP(src_c)
    return rc

def IMG_isCUR(src):
    """
    ``int IMG_isCUR(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isCUR(src_c)
    return rc

def IMG_isGIF(src):
    """
    ``int IMG_isGIF(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isGIF(src_c)
    return rc

def IMG_isICO(src):
    """
    ``int IMG_isICO(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isICO(src_c)
    return rc

def IMG_isJPG(src):
    """
    ``int IMG_isJPG(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isJPG(src_c)
    return rc

def IMG_isLBM(src):
    """
    ``int IMG_isLBM(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isLBM(src_c)
    return rc

def IMG_isPCX(src):
    """
    ``int IMG_isPCX(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isPCX(src_c)
    return rc

def IMG_isPNG(src):
    """
    ``int IMG_isPNG(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isPNG(src_c)
    return rc

def IMG_isPNM(src):
    """
    ``int IMG_isPNM(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isPNM(src_c)
    return rc

def IMG_isTIF(src):
    """
    ``int IMG_isTIF(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isTIF(src_c)
    return rc

def IMG_isWEBP(src):
    """
    ``int IMG_isWEBP(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isWEBP(src_c)
    return rc

def IMG_isXCF(src):
    """
    ``int IMG_isXCF(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isXCF(src_c)
    return rc

def IMG_isXPM(src):
    """
    ``int IMG_isXPM(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isXPM(src_c)
    return rc

def IMG_isXV(src):
    """
    ``int IMG_isXV(SDL_RWops *)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    rc = _LIB.IMG_isXV(src_c)
    return rc

IMG_INIT_JPG = _LIB.IMG_INIT_JPG
IMG_INIT_PNG = _LIB.IMG_INIT_PNG
IMG_INIT_TIF = _LIB.IMG_INIT_TIF
IMG_INIT_WEBP = _LIB.IMG_INIT_WEBP

