import serial

LUMINANCE_100 = b'\x01'
LUMINANCE_75 = b'\x02'
LUMINANCE_50 = b'\x03'
LUMINANCE_25 = b'\x04'
BACKSPACE = b'\x08'
TAB = b'\x09'
LF = b'\x0a'
CLEAR = b'\x0c'
CR = b'\x0d'
NORMAL_WRITE = b'\x11'
SCROLL_WRITE = b'\x12'

CURSOR = {
    'on': b'\x13',
    'off': b'\x14',
    'flash': b'\x15',
}
CURSOR_TYPE = {
    'underline': b'\x16',
    'block': b'\x17',
    'inverse': b'\x18',
}
USER_CHAR = b'\x1a'
ESCAPE = b'\x1c'

RASPBERRY_PI = '/dev/ttyAMA0'

class VFD(object):
    def __init__(self, serial_path):
        self.serial = serial.Serial(serial_path, baudrate=9600, timeout=1)
        self._cursor = 'off'
        self._cursor_type = 'underline'
        self.serial.write(CURSOR[self._cursor])
        self.serial.write(CURSOR_TYPE[self._cursor_type])
        self.clear()

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, c):
        self.serial.write(CURSOR[self.cursor[c]])
        self._cursor = c

    @property
    def cursor_type(self):
        return self._cursor_type

    @cursor_type.setter
    def cursor_type(self, ct):
        self.serial.write(CURSOR_TYPE[ct])
        self._cursor_type = ct

    def write(self, message):
        self.serial.write(message.encode('ascii'))
        return self

    def clear(self):
        self.serial.write(CLEAR)
        return self

    def scroll_write(self):
        self.serial.write(SCROLL_WRITE)
        return self

    def normal_write(self):
        self.serial.write(NORMAL_WRITE)
        return self

    def backspace(self):
        self.serial.write(BACKSPACE)
        return self

    def tab(self):
        self.serial.write(TAB)
        return self

    def escape(self):
        self.serial.write(ESCAPE)
        return self
