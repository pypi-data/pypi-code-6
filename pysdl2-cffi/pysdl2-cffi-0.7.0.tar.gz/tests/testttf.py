# Use sdl.ttf to show some text.
#
# Daniel Holth <dholth@fastmail.fm>, 2014

import sys
import sdl
import sdl.ttf
import sdl.image
import time

def main():
    phrase = sys.argv[2]
    sdl.ttf.init()
    font = sdl.ttf.openFont(sys.argv[1], 72)
    rc = font.sizeUTF8(phrase)
    size = rc[1:]
    print(phrase)
    print(size)

    sdl.image.init(sdl.image.INIT_PNG)

    sdl.init(sdl.INIT_VIDEO)
    window = sdl.createWindow(phrase,
            sdl.WINDOWPOS_UNDEFINED, sdl.WINDOWPOS_UNDEFINED,
            size[0] + 20, size[1] + 20,
            sdl.WINDOW_SHOWN)
    renderer = sdl.createRenderer(window, -1, 0)
    renderer.setRenderDrawColor(0xff,0xff,0xff,0xff)
    renderer.renderClear()
    text = font.renderUTF8_Blended(phrase, sdl.Color((0,0,0,0xff)).cdata[0])
    texture = renderer.createTextureFromSurface(text)
    # None means copy the whole texture:
    renderer.renderCopy(texture, None, (10,10,size[0],size[1]))
    renderer.renderPresent()

    time.sleep(10)

    text.freeSurface()
    texture.destroyTexture()
    renderer.destroyRenderer()
    window.destroyWindow()


if __name__ == "__main__":
    main()
