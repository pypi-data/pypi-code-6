# Automatically generated wrappers.
# Override by adding wrappers to helpers.py.
from .dso import ffi, _LIB
from .structs import unbox, Struct
from _sdl.structs import u8, SDLError
from _sdl.autohelpers import SDL_Surface, SDL_version

def TTF_ByteSwappedUNICODE(swapped):
    """
    ``void TTF_ByteSwappedUNICODE(int)``
    """
    swapped_c = swapped
    _LIB.TTF_ByteSwappedUNICODE(swapped_c)

def TTF_CloseFont(font):
    """
    ``void TTF_CloseFont(TTF_Font *)``
    """
    font_c = unbox(font, 'TTF_Font *')
    _LIB.TTF_CloseFont(font_c)

def TTF_FontAscent(font):
    """
    ``int TTF_FontAscent(TTF_Font const *)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    rc = _LIB.TTF_FontAscent(font_c)
    return rc

def TTF_FontDescent(font):
    """
    ``int TTF_FontDescent(TTF_Font const *)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    rc = _LIB.TTF_FontDescent(font_c)
    return rc

def TTF_FontFaceFamilyName(font):
    """
    ``char * TTF_FontFaceFamilyName(TTF_Font const *)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    rc = _LIB.TTF_FontFaceFamilyName(font_c)
    return ffi.string(rc).decode('utf-8')

def TTF_FontFaceIsFixedWidth(font):
    """
    ``int TTF_FontFaceIsFixedWidth(TTF_Font const *)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    rc = _LIB.TTF_FontFaceIsFixedWidth(font_c)
    return rc

def TTF_FontFaceStyleName(font):
    """
    ``char * TTF_FontFaceStyleName(TTF_Font const *)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    rc = _LIB.TTF_FontFaceStyleName(font_c)
    return ffi.string(rc).decode('utf-8')

def TTF_FontFaces(font):
    """
    ``long TTF_FontFaces(TTF_Font const *)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    rc = _LIB.TTF_FontFaces(font_c)
    return rc

def TTF_FontHeight(font):
    """
    ``int TTF_FontHeight(TTF_Font const *)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    rc = _LIB.TTF_FontHeight(font_c)
    return rc

def TTF_FontLineSkip(font):
    """
    ``int TTF_FontLineSkip(TTF_Font const *)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    rc = _LIB.TTF_FontLineSkip(font_c)
    return rc

def TTF_GetFontHinting(font):
    """
    ``int TTF_GetFontHinting(TTF_Font const *)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    rc = _LIB.TTF_GetFontHinting(font_c)
    return rc

def TTF_GetFontKerning(font):
    """
    ``int TTF_GetFontKerning(TTF_Font const *)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    rc = _LIB.TTF_GetFontKerning(font_c)
    return rc

def TTF_GetFontKerningSize(font, prev_index, index):
    """
    ``int TTF_GetFontKerningSize(TTF_Font *, int, int)``
    """
    font_c = unbox(font, 'TTF_Font *')
    prev_index_c = prev_index
    index_c = index
    rc = _LIB.TTF_GetFontKerningSize(font_c, prev_index_c, index_c)
    return rc

def TTF_GetFontOutline(font):
    """
    ``int TTF_GetFontOutline(TTF_Font const *)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    rc = _LIB.TTF_GetFontOutline(font_c)
    return rc

def TTF_GetFontStyle(font):
    """
    ``int TTF_GetFontStyle(TTF_Font const *)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    rc = _LIB.TTF_GetFontStyle(font_c)
    return rc

def TTF_GlyphIsProvided(font, ch):
    """
    ``int TTF_GlyphIsProvided(TTF_Font const *, uint16_t)``
    """
    font_c = unbox(font, 'TTF_Font const *')
    ch_c = ch
    rc = _LIB.TTF_GlyphIsProvided(font_c, ch_c)
    return rc

def TTF_GlyphMetrics(font, ch, minx=None, maxx=None, miny=None, maxy=None, advance=None):
    """
    ``int TTF_GlyphMetrics(TTF_Font *, uint16_t, int *, int *, int *, int *, int *)``
    """
    font_c = unbox(font, 'TTF_Font *')
    ch_c = ch
    minx_c = unbox(minx, 'int *')
    maxx_c = unbox(maxx, 'int *')
    miny_c = unbox(miny, 'int *')
    maxy_c = unbox(maxy, 'int *')
    advance_c = unbox(advance, 'int *')
    rc = _LIB.TTF_GlyphMetrics(font_c, ch_c, minx_c, maxx_c, miny_c, maxy_c, advance_c)
    return (rc, minx_c[0], maxx_c[0], miny_c[0], maxy_c[0], advance_c[0])

def TTF_Init():
    """
    ``int TTF_Init(void)``
    """
    rc = _LIB.TTF_Init()
    if rc == -1: raise SDLError()
    return rc

def TTF_Linked_Version():
    """
    ``SDL_version const * TTF_Linked_Version(void)``
    """
    rc = _LIB.TTF_Linked_Version()
    return SDL_version(rc)

def TTF_OpenFont(file, ptsize):
    """
    ``TTF_Font * TTF_OpenFont(char const *, int)``
    """
    file_c = u8(file)
    ptsize_c = ptsize
    rc = _LIB.TTF_OpenFont(file_c, ptsize_c)
    if rc == ffi.NULL: raise SDLError()
    return TTF_Font(rc)

def TTF_OpenFontIndex(file, ptsize, index):
    """
    ``TTF_Font * TTF_OpenFontIndex(char const *, int, long)``
    """
    file_c = u8(file)
    ptsize_c = ptsize
    index_c = index
    rc = _LIB.TTF_OpenFontIndex(file_c, ptsize_c, index_c)
    if rc == ffi.NULL: raise SDLError()
    return TTF_Font(rc)

def TTF_OpenFontIndexRW(src, freesrc, ptsize, index):
    """
    ``TTF_Font * TTF_OpenFontIndexRW(SDL_RWops *, int, int, long)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    freesrc_c = freesrc
    ptsize_c = ptsize
    index_c = index
    rc = _LIB.TTF_OpenFontIndexRW(src_c, freesrc_c, ptsize_c, index_c)
    if rc == ffi.NULL: raise SDLError()
    return TTF_Font(rc)

def TTF_OpenFontRW(src, freesrc, ptsize):
    """
    ``TTF_Font * TTF_OpenFontRW(SDL_RWops *, int, int)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    freesrc_c = freesrc
    ptsize_c = ptsize
    rc = _LIB.TTF_OpenFontRW(src_c, freesrc_c, ptsize_c)
    if rc == ffi.NULL: raise SDLError()
    return TTF_Font(rc)

def TTF_Quit():
    """
    ``void TTF_Quit(void)``
    """
    _LIB.TTF_Quit()

def TTF_RenderGlyph_Blended(font, ch, fg):
    """
    ``SDL_Surface * TTF_RenderGlyph_Blended(TTF_Font *, uint16_t, SDL_Color)``
    """
    font_c = unbox(font, 'TTF_Font *')
    ch_c = ch
    fg_c = unbox(fg, 'SDL_Color')
    rc = _LIB.TTF_RenderGlyph_Blended(font_c, ch_c, fg_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderGlyph_Shaded(font, ch, fg, bg):
    """
    ``SDL_Surface * TTF_RenderGlyph_Shaded(TTF_Font *, uint16_t, SDL_Color, SDL_Color)``
    """
    font_c = unbox(font, 'TTF_Font *')
    ch_c = ch
    fg_c = unbox(fg, 'SDL_Color')
    bg_c = unbox(bg, 'SDL_Color')
    rc = _LIB.TTF_RenderGlyph_Shaded(font_c, ch_c, fg_c, bg_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderGlyph_Solid(font, ch, fg):
    """
    ``SDL_Surface * TTF_RenderGlyph_Solid(TTF_Font *, uint16_t, SDL_Color)``
    """
    font_c = unbox(font, 'TTF_Font *')
    ch_c = ch
    fg_c = unbox(fg, 'SDL_Color')
    rc = _LIB.TTF_RenderGlyph_Solid(font_c, ch_c, fg_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderText_Blended(font, text, fg):
    """
    ``SDL_Surface * TTF_RenderText_Blended(TTF_Font *, char const *, SDL_Color)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = u8(text)
    fg_c = unbox(fg, 'SDL_Color')
    rc = _LIB.TTF_RenderText_Blended(font_c, text_c, fg_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderText_Blended_Wrapped(font, text, fg, wrapLength):
    """
    ``SDL_Surface * TTF_RenderText_Blended_Wrapped(TTF_Font *, char const *, SDL_Color, uint32_t)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = u8(text)
    fg_c = unbox(fg, 'SDL_Color')
    wrapLength_c = wrapLength
    rc = _LIB.TTF_RenderText_Blended_Wrapped(font_c, text_c, fg_c, wrapLength_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderText_Shaded(font, text, fg, bg):
    """
    ``SDL_Surface * TTF_RenderText_Shaded(TTF_Font *, char const *, SDL_Color, SDL_Color)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = u8(text)
    fg_c = unbox(fg, 'SDL_Color')
    bg_c = unbox(bg, 'SDL_Color')
    rc = _LIB.TTF_RenderText_Shaded(font_c, text_c, fg_c, bg_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderText_Solid(font, text, fg):
    """
    ``SDL_Surface * TTF_RenderText_Solid(TTF_Font *, char const *, SDL_Color)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = u8(text)
    fg_c = unbox(fg, 'SDL_Color')
    rc = _LIB.TTF_RenderText_Solid(font_c, text_c, fg_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderUNICODE_Blended(font, text, fg):
    """
    ``SDL_Surface * TTF_RenderUNICODE_Blended(TTF_Font *, uint16_t const *, SDL_Color)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = unbox(text, 'uint16_t const *')
    fg_c = unbox(fg, 'SDL_Color')
    rc = _LIB.TTF_RenderUNICODE_Blended(font_c, text_c, fg_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderUNICODE_Blended_Wrapped(font, text, fg, wrapLength):
    """
    ``SDL_Surface * TTF_RenderUNICODE_Blended_Wrapped(TTF_Font *, uint16_t const *, SDL_Color, uint32_t)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = unbox(text, 'uint16_t const *')
    fg_c = unbox(fg, 'SDL_Color')
    wrapLength_c = wrapLength
    rc = _LIB.TTF_RenderUNICODE_Blended_Wrapped(font_c, text_c, fg_c, wrapLength_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderUNICODE_Shaded(font, text, fg, bg):
    """
    ``SDL_Surface * TTF_RenderUNICODE_Shaded(TTF_Font *, uint16_t const *, SDL_Color, SDL_Color)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = unbox(text, 'uint16_t const *')
    fg_c = unbox(fg, 'SDL_Color')
    bg_c = unbox(bg, 'SDL_Color')
    rc = _LIB.TTF_RenderUNICODE_Shaded(font_c, text_c, fg_c, bg_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderUNICODE_Solid(font, text, fg):
    """
    ``SDL_Surface * TTF_RenderUNICODE_Solid(TTF_Font *, uint16_t const *, SDL_Color)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = unbox(text, 'uint16_t const *')
    fg_c = unbox(fg, 'SDL_Color')
    rc = _LIB.TTF_RenderUNICODE_Solid(font_c, text_c, fg_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderUTF8_Blended(font, text, fg):
    """
    ``SDL_Surface * TTF_RenderUTF8_Blended(TTF_Font *, char const *, SDL_Color)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = u8(text)
    fg_c = unbox(fg, 'SDL_Color')
    rc = _LIB.TTF_RenderUTF8_Blended(font_c, text_c, fg_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderUTF8_Blended_Wrapped(font, text, fg, wrapLength):
    """
    ``SDL_Surface * TTF_RenderUTF8_Blended_Wrapped(TTF_Font *, char const *, SDL_Color, uint32_t)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = u8(text)
    fg_c = unbox(fg, 'SDL_Color')
    wrapLength_c = wrapLength
    rc = _LIB.TTF_RenderUTF8_Blended_Wrapped(font_c, text_c, fg_c, wrapLength_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderUTF8_Shaded(font, text, fg, bg):
    """
    ``SDL_Surface * TTF_RenderUTF8_Shaded(TTF_Font *, char const *, SDL_Color, SDL_Color)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = u8(text)
    fg_c = unbox(fg, 'SDL_Color')
    bg_c = unbox(bg, 'SDL_Color')
    rc = _LIB.TTF_RenderUTF8_Shaded(font_c, text_c, fg_c, bg_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_RenderUTF8_Solid(font, text, fg):
    """
    ``SDL_Surface * TTF_RenderUTF8_Solid(TTF_Font *, char const *, SDL_Color)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = u8(text)
    fg_c = unbox(fg, 'SDL_Color')
    rc = _LIB.TTF_RenderUTF8_Solid(font_c, text_c, fg_c)
    if rc == ffi.NULL: raise SDLError()
    return SDL_Surface(rc)

def TTF_SetFontHinting(font, hinting):
    """
    ``void TTF_SetFontHinting(TTF_Font *, int)``
    """
    font_c = unbox(font, 'TTF_Font *')
    hinting_c = hinting
    _LIB.TTF_SetFontHinting(font_c, hinting_c)

def TTF_SetFontKerning(font, allowed):
    """
    ``void TTF_SetFontKerning(TTF_Font *, int)``
    """
    font_c = unbox(font, 'TTF_Font *')
    allowed_c = allowed
    _LIB.TTF_SetFontKerning(font_c, allowed_c)

def TTF_SetFontOutline(font, outline):
    """
    ``void TTF_SetFontOutline(TTF_Font *, int)``
    """
    font_c = unbox(font, 'TTF_Font *')
    outline_c = outline
    _LIB.TTF_SetFontOutline(font_c, outline_c)

def TTF_SetFontStyle(font, style):
    """
    ``void TTF_SetFontStyle(TTF_Font *, int)``
    """
    font_c = unbox(font, 'TTF_Font *')
    style_c = style
    _LIB.TTF_SetFontStyle(font_c, style_c)

def TTF_SizeText(font, text, w=None, h=None):
    """
    ``int TTF_SizeText(TTF_Font *, char const *, int *, int *)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = u8(text)
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    rc = _LIB.TTF_SizeText(font_c, text_c, w_c, h_c)
    return (rc, w_c[0], h_c[0])

def TTF_SizeUNICODE(font, text=None, w=None, h=None):
    """
    ``int TTF_SizeUNICODE(TTF_Font *, uint16_t const *, int *, int *)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = unbox(text, 'uint16_t const *')
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    rc = _LIB.TTF_SizeUNICODE(font_c, text_c, w_c, h_c)
    return (rc, text_c[0], w_c[0], h_c[0])

def TTF_SizeUTF8(font, text, w=None, h=None):
    """
    ``int TTF_SizeUTF8(TTF_Font *, char const *, int *, int *)``
    """
    font_c = unbox(font, 'TTF_Font *')
    text_c = u8(text)
    w_c = unbox(w, 'int *')
    h_c = unbox(h, 'int *')
    rc = _LIB.TTF_SizeUTF8(font_c, text_c, w_c, h_c)
    return (rc, w_c[0], h_c[0])

def TTF_WasInit():
    """
    ``int TTF_WasInit(void)``
    """
    rc = _LIB.TTF_WasInit()
    return rc

class TTF_Font(Struct):
    """Wrap `TTF_Font`"""
    closeFont = TTF_CloseFont
    fontAscent = TTF_FontAscent
    fontDescent = TTF_FontDescent
    fontFaceFamilyName = TTF_FontFaceFamilyName
    fontFaceIsFixedWidth = TTF_FontFaceIsFixedWidth
    fontFaceStyleName = TTF_FontFaceStyleName
    fontFaces = TTF_FontFaces
    fontHeight = TTF_FontHeight
    fontLineSkip = TTF_FontLineSkip
    getFontHinting = TTF_GetFontHinting
    getFontKerning = TTF_GetFontKerning
    getFontKerningSize = TTF_GetFontKerningSize
    getFontOutline = TTF_GetFontOutline
    getFontStyle = TTF_GetFontStyle
    glyphIsProvided = TTF_GlyphIsProvided
    glyphMetrics = TTF_GlyphMetrics
    renderGlyph_Blended = TTF_RenderGlyph_Blended
    renderGlyph_Shaded = TTF_RenderGlyph_Shaded
    renderGlyph_Solid = TTF_RenderGlyph_Solid
    renderText_Blended = TTF_RenderText_Blended
    renderText_Blended_Wrapped = TTF_RenderText_Blended_Wrapped
    renderText_Shaded = TTF_RenderText_Shaded
    renderText_Solid = TTF_RenderText_Solid
    renderUNICODE_Blended = TTF_RenderUNICODE_Blended
    renderUNICODE_Blended_Wrapped = TTF_RenderUNICODE_Blended_Wrapped
    renderUNICODE_Shaded = TTF_RenderUNICODE_Shaded
    renderUNICODE_Solid = TTF_RenderUNICODE_Solid
    renderUTF8_Blended = TTF_RenderUTF8_Blended
    renderUTF8_Blended_Wrapped = TTF_RenderUTF8_Blended_Wrapped
    renderUTF8_Shaded = TTF_RenderUTF8_Shaded
    renderUTF8_Solid = TTF_RenderUTF8_Solid
    setFontHinting = TTF_SetFontHinting
    setFontKerning = TTF_SetFontKerning
    setFontOutline = TTF_SetFontOutline
    setFontStyle = TTF_SetFontStyle
    sizeText = TTF_SizeText
    sizeUNICODE = TTF_SizeUNICODE
    sizeUTF8 = TTF_SizeUTF8

