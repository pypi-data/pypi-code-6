#!/usr/bin/env python
"""
    Not much commentary in this example.  It's more of a demo.
"""
import sys
import code
import textwrap
import io
import time
import traceback

sys.path.insert(0, '../')
import untdl

sys.ps1 = '>>> '
sys.ps2 = '... '

WIDTH, HEIGHT = 80, 50
console = untdl.init(WIDTH, HEIGHT, 'Python Interpreter in UNTDL')
console.set_mode('scroll')


class TDLPrint(io.TextIOBase):
    # noinspection PyMissingConstructor
    def __init__(self, fgcolor=(255, 255, 255), bgcolor=(0, 0, 0)):
        self.colors = fgcolor, bgcolor

    def write(self, string):
        old_err.write(string)
        console.set_colors(*self.colors)
        console.write(string)

#sys.stdout = TDLPrint()
sys.stdout = console
sys.stdout.move(0, HEIGHT-1)
old_err = new_err = sys.stderr
# noinspection PyRedeclaration
new_err = TDLPrint((255, 255, 255), (127, 0, 0))


# noinspection PyShadowingBuiltins
def exit():
    raise SystemExit

interpeter = code.InteractiveConsole({'untdl': untdl,
                                      'console': console,
                                      'exit': exit})


def main():
    print()
    print('Python %s' % sys.version)
    print('Press ESC to quit')
    
    buffer = ''
    commands = ['']
    banner = sys.ps1
    cursor = 0
    while 1:
        console.draw_rect(0, HEIGHT-1, None, 1, ' ', (255, 255, 255), (0, 0, 0))
        console.draw_str(0, HEIGHT-1, banner + buffer)
        try:
            console.draw_char(len(banner) + cursor, HEIGHT-1, None, None, (0, 255, 255))
        except untdl.TDLError:
            pass
        untdl.flush()
        
        for event in untdl.event.get():
            if event.type == 'QUIT':
                raise SystemExit()
            if event.type == 'KEYDOWN':
                if event.key == 'ENTER' or event.key == 'KPENTER':
                    sys.stderr = new_err
                    # noinspection PyBroadException
                    try:
                        console.draw_rect(0, HEIGHT-1, None, 1, None, (255, 255, 255), (0, 0, 0))
                        console.scroll(0, -1)
                        if interpeter.push(buffer):
                            banner = sys.ps2
                        else:
                            banner = sys.ps1
                    except SystemExit:
                        raise
                    except:
                        sys.excepthook(*sys.exc_info())
                        banner = sys.ps1
                    finally:
                        sys.stderr = old_err
                        sys.stdout = old_err
                    sys.stdout = console
                    if buffer not in commands:
                        commands.append(buffer)
                    buffer = ''
                elif event.key == 'BACKSPACE':
                    if cursor == 0:
                        continue
                    if buffer[:cursor][-4:] == '    ':
                        buffer = buffer[:cursor-4] + buffer[cursor:]
                        cursor -= 4
                    elif buffer:
                        buffer = buffer[:cursor-1] + buffer[cursor:]
                        cursor -= 1
                elif event.key == 'DELETE':
                    buffer = buffer[:cursor] + buffer[cursor+1:]
                elif event.key == 'LEFT':
                    cursor -= 1
                elif event.key == 'RIGHT':
                    cursor += 1
                elif event.key == 'HOME':
                    cursor = 0
                elif event.key == 'END':
                    cursor = len(buffer)
                elif event.key == 'UP':
                    commands.insert(0, buffer)
                    buffer = commands.pop()
                    cursor = len(buffer)
                elif event.key == 'DOWN':
                    commands.append(buffer)
                    buffer = commands.pop(0)
                    cursor = len(buffer)
                elif event.key == 'TAB':
                    buffer = buffer[:cursor] + '    ' + buffer[cursor:]
                    cursor += 4
                elif event.key == 'ESCAPE':
                    raise SystemExit()
                elif event.char:
                    buffer = buffer[:cursor] + event.char + buffer[cursor:]
                    cursor += 1
                cursor = max(0, min(cursor, len(buffer)))
        time.sleep(.01)

if __name__ == '__main__':
    main()
