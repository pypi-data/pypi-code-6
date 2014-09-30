# SDL2's SDL_image bindings for pysdl2-cffi.

import cffi

import _sdl.cdefs
import _sdl.lib

ffi = cffi.FFI()
ffi.include(_sdl.cdefs.ffi)

# SDL_image uses SDL_SetError / SDL_GetError for error reporting.

ffi.cdef("""

extern const SDL_version * IMG_Linked_Version(void);

typedef enum
{
    IMG_INIT_JPG = 0x00000001,
    IMG_INIT_PNG = 0x00000002,
    IMG_INIT_TIF = 0x00000004,
    IMG_INIT_WEBP = 0x00000008
} IMG_InitFlags;

extern int IMG_Init(int flags);

extern void IMG_Quit(void);

extern SDL_Surface * IMG_LoadTyped_RW(SDL_RWops *src, int freesrc, const char *type);

extern SDL_Surface * IMG_Load(const char *file);
extern SDL_Surface * IMG_Load_RW(SDL_RWops *src, int freesrc);

extern SDL_Texture * IMG_LoadTexture(SDL_Renderer *renderer, const char *file);
extern SDL_Texture * IMG_LoadTexture_RW(SDL_Renderer *renderer, SDL_RWops *src, int freesrc);
extern SDL_Texture * IMG_LoadTextureTyped_RW(SDL_Renderer *renderer, SDL_RWops *src, int freesrc, const char *type);

extern int IMG_isICO(SDL_RWops *src);
extern int IMG_isCUR(SDL_RWops *src);
extern int IMG_isBMP(SDL_RWops *src);
extern int IMG_isGIF(SDL_RWops *src);
extern int IMG_isJPG(SDL_RWops *src);
extern int IMG_isLBM(SDL_RWops *src);
extern int IMG_isPCX(SDL_RWops *src);
extern int IMG_isPNG(SDL_RWops *src);
extern int IMG_isPNM(SDL_RWops *src);
extern int IMG_isTIF(SDL_RWops *src);
extern int IMG_isXCF(SDL_RWops *src);
extern int IMG_isXPM(SDL_RWops *src);
extern int IMG_isXV(SDL_RWops *src);
extern int IMG_isWEBP(SDL_RWops *src);

extern SDL_Surface * IMG_LoadICO_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadCUR_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadBMP_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadGIF_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadJPG_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadLBM_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadPCX_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadPNG_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadPNM_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadTGA_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadTIF_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadXCF_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadXPM_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadXV_RW(SDL_RWops *src);
extern SDL_Surface * IMG_LoadWEBP_RW(SDL_RWops *src);

extern SDL_Surface * IMG_ReadXPMFromArray(char **xpm);

extern int IMG_SavePNG(SDL_Surface *surface, const char *file);
extern int IMG_SavePNG_RW(SDL_Surface *surface, SDL_RWops *dst, int freedst);
""")

IMG_GetError = _sdl.lib.SDL_GetError
IMG_SetError = _sdl.lib.SDL_SetError
