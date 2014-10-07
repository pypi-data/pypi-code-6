"""
getkey is a module that defines a single function also called getkey(). it
reads a single keyboard press and returns a string containing the character
pressed if the key pressed is a character. if the key is a special key like
function keys, up arrow, down arrow or backspace, it returns a descriptive
name of the key like 'F11', 'UP', 'DOWN' or 'BACKSPACE'. all names of special
keys are defined in the KEYS variable.
"""


try :
    #windows implementation. try to use it. if import error ecountered,
    #try posix implementation
    import time
    import msvcrt
    
    #special keys to be converted to discriptive names
    KEYS = {b'\x1b':b'ESCAPE',
            b'\x00;':b'F1',
            b'\x00<':b'F2',
            b'\x00=':b'F3',
            b'\x00>':b'F4',
            b'\x00?':b'F5',
            b'\x00@':b'F6',
            b'\x00A':b'F7',
            b'\x00B':b'F8',
            b'\x00C':b'F9',
            b'\x00D':b'F10',
            b'\xe0\x85':b'F11',
            b'\xe0\x86':b'F12',
            b'\xe0R':b'INSERT',
            b'\xe0S':b'DELETE',
            b'\x08':b'BACKSPACE',
            b'\xe0G':b'HOME',
            b'\xe0I':b'PAGEUP',
            b'\xe0Q':b'PAGEDOWN',
            b'\xe0O':b'END',
            b'\xe0H':b'UP',
            b'\xe0P':b'DOWN',
            b'\xe0M':b'RIGHT',
            b'\xe0K':b'LEFT',
            b'\r':b'\n',}
    
    def getkey(timeout=-1):
        """
        gets a single key press from keyboard. returns the character pressed
        if the pressed is a character. if the key is a special key like up or
        down arrow, return a discriptive name of the key. timeout is the
        timeout in deciseconds. if timeout is exceeded, the function returns
        empty string.
        if timeout is negative, wait forever until key is pressed.
        """
        
        timeout /= 10   #convert to deciseconds
        key = b''       #no key in the beginning
        #empty stdin queue
        while msvcrt.kbhit():
            msvcrt.getch()
        #if timeout is valid, delay until key is pressed or timeout
        if timeout >= 0:
            s = time.clock()
            while not msvcrt.kbhit() and time.clock() - s < timeout:
                time.sleep (0.001)
        #if key is pressed, read key
        #if timeout is not valid, block until key pressed
        #if there is timeout and no key pressed, then return empty string
        if msvcrt.kbhit() or timeout < 0:
            key = msvcrt.getch()    #read first character even if blocking
            #read remaining characters in case of multi character key
            while msvcrt.kbhit():
                key = key + msvcrt.getch()
            if key in KEYS:
                key = KEYS[key] #if key is not character, return discription
        return key.decode()
except ImportError:
    #posix implementation.
    import sys, tty, termios
    
    #special keys to be converted to discriptive names
    KEYS = {'\x1b':'ESCAPE',
            '\x1bOP':'F1',
            '\x1bOQ':'F2',
            '\x1bOR':'F3',
            '\x1bOS':'F4',
            '\x1b[15~':'F5',
            '\x1b[17~':'F6',
            '\x1b[18~':'F7',
            '\x1b[19~':'F8',
            '\x1b[20~':'F9',
            '\x1b[21~':'F10',
            '\x1b[23~':'F11',
            '\x1b[24~':'F12',
            '\x1b[2~':'INSERT',
            '\x1b[3~':'DELETE',
            '\x1bOH':'HOME',
            '\x1bOF':'END',
            '\x1b[5~':'PAGEUP',
            '\x1b[6~':'PAGEDOWN',
            '\x7f':'BACKSPACE',
            '\x1b[A':'UP',
            '\x1b[B':'DOWN',
            '\x1b[C':'RIGHT',
            '\x1b[D':'LEFT',
            '\r':'\n',}
    
    def getkey (timeout=-1):
        """
        gets a single key press from keyboard. returns the character pressed
        if the pressed is a character. if the key is a special key like up or
        down arrow, return a discriptive name of the key. timeout is the
        timeout in deciseconds. if timeout is exceeded, the function returns
        empty string.
        if timeout is negative, wait forever until key is pressed.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)    #backup old setting
        tty.setraw(fd)                          #get characters 1 by 1
        new_settings = termios.tcgetattr(fd)    #create new settings
        new_settings[-1][termios.VMIN] = 0      #can receive 0 bytes
        new_settings[-1][termios.VTIME] = timeout   #return after timeout even with no input
        new_settings[3] = new_settings[3] & ~termios.ICANON #canonical mode to enable timeout
        try:
            if timeout >= 0:    #if timeout is valid, apply it
                termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)  #apply new settings
            key = sys.stdin.read(1)     #return after 1 character or timeout
            new_settings[-1][termios.VTIME] = 0 #remove timeout
            termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)  #apply settings
            key += sys.stdin.read() #read all remaining characters
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  #restore old settings
        if key in KEYS:
            key = KEYS[key] #if key is not character, return discription
        return key


