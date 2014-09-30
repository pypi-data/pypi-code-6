# SDL2's SDL_ttf bindings for pysdl2-cffi.

import cffi

import _sdl.cdefs

ffi = cffi.FFI()
ffi.include(_sdl.cdefs.ffi)

ffi.cdef("""
extern  const SDL_version *  TTF_Linked_Version(void);
extern  void  TTF_ByteSwappedUNICODE(int swapped);
typedef struct _TTF_Font TTF_Font;
extern  int  TTF_Init(void);
extern  TTF_Font *  TTF_OpenFont(const char *file, int ptsize);
extern  TTF_Font *  TTF_OpenFontIndex(const char *file, int ptsize, long index);
extern  TTF_Font *  TTF_OpenFontRW(SDL_RWops *src, int freesrc, int ptsize);
extern  TTF_Font *  TTF_OpenFontIndexRW(SDL_RWops *src, int freesrc, int ptsize, long index);
extern  int  TTF_GetFontStyle(const TTF_Font *font);
extern  void  TTF_SetFontStyle(TTF_Font *font, int style);
extern  int  TTF_GetFontOutline(const TTF_Font *font);
extern  void  TTF_SetFontOutline(TTF_Font *font, int outline);
extern  int  TTF_GetFontHinting(const TTF_Font *font);
extern  void  TTF_SetFontHinting(TTF_Font *font, int hinting);
extern  int  TTF_FontHeight(const TTF_Font *font);
extern  int  TTF_FontAscent(const TTF_Font *font);
extern  int  TTF_FontDescent(const TTF_Font *font);
extern  int  TTF_FontLineSkip(const TTF_Font *font);
extern  int  TTF_GetFontKerning(const TTF_Font *font);
extern  void  TTF_SetFontKerning(TTF_Font *font, int allowed);
extern  long  TTF_FontFaces(const TTF_Font *font);
extern  int  TTF_FontFaceIsFixedWidth(const TTF_Font *font);
extern  char *  TTF_FontFaceFamilyName(const TTF_Font *font);
extern  char *  TTF_FontFaceStyleName(const TTF_Font *font);
extern  int  TTF_GlyphIsProvided(const TTF_Font *font, Uint16 ch);
extern  int  TTF_GlyphMetrics(TTF_Font *font, Uint16 ch,
                     int *minx, int *maxx,
                                     int *miny, int *maxy, int *advance);
extern  int  TTF_SizeText(TTF_Font *font, const char *text, int *w, int *h);
extern  int  TTF_SizeUTF8(TTF_Font *font, const char *text, int *w, int *h);
extern  int  TTF_SizeUNICODE(TTF_Font *font, const Uint16 *text, int *w, int *h);
extern  SDL_Surface *  TTF_RenderText_Solid(TTF_Font *font,
                const char *text, SDL_Color fg);
extern  SDL_Surface *  TTF_RenderUTF8_Solid(TTF_Font *font,
                const char *text, SDL_Color fg);
extern  SDL_Surface *  TTF_RenderUNICODE_Solid(TTF_Font *font,
                const Uint16 *text, SDL_Color fg);
extern  SDL_Surface *  TTF_RenderGlyph_Solid(TTF_Font *font,
                    Uint16 ch, SDL_Color fg);
extern  SDL_Surface *  TTF_RenderText_Shaded(TTF_Font *font,
                const char *text, SDL_Color fg, SDL_Color bg);
extern  SDL_Surface *  TTF_RenderUTF8_Shaded(TTF_Font *font,
                const char *text, SDL_Color fg, SDL_Color bg);
extern  SDL_Surface *  TTF_RenderUNICODE_Shaded(TTF_Font *font,
                const Uint16 *text, SDL_Color fg, SDL_Color bg);
extern  SDL_Surface *  TTF_RenderGlyph_Shaded(TTF_Font *font,
                Uint16 ch, SDL_Color fg, SDL_Color bg);
extern  SDL_Surface *  TTF_RenderText_Blended(TTF_Font *font,
                const char *text, SDL_Color fg);
extern  SDL_Surface *  TTF_RenderUTF8_Blended(TTF_Font *font,
                const char *text, SDL_Color fg);
extern  SDL_Surface *  TTF_RenderUNICODE_Blended(TTF_Font *font,
                const Uint16 *text, SDL_Color fg);
extern  SDL_Surface *  TTF_RenderText_Blended_Wrapped(TTF_Font *font,
                const char *text, SDL_Color fg, Uint32 wrapLength);
extern  SDL_Surface *  TTF_RenderUTF8_Blended_Wrapped(TTF_Font *font,
                const char *text, SDL_Color fg, Uint32 wrapLength);
extern  SDL_Surface *  TTF_RenderUNICODE_Blended_Wrapped(TTF_Font *font,
                const Uint16 *text, SDL_Color fg, Uint32 wrapLength);
extern  SDL_Surface *  TTF_RenderGlyph_Blended(TTF_Font *font,
                        Uint16 ch, SDL_Color fg);
extern  void  TTF_CloseFont(TTF_Font *font);
extern  void  TTF_Quit(void);
extern  int  TTF_WasInit(void);
extern  int TTF_GetFontKerningSize(TTF_Font *font, int prev_index, int index);
""")
