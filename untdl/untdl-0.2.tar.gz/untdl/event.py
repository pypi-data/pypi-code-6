"""
    This module handles user input.
    
    To handle user input you will likely want to use the L{event.get} function
    or create a subclass of L{event.App}.
     - L{event.get} iterates over recent events.
     - L{event.App} passes events to the overridable methods: ev_* and key_*.
    
    But there are other options such as L{event.keyWait} and L{event.isWindowClosed}.
    
    A few event attributes are actually string constants.
    Here's a reference for those:
     - L{Event.type}
     
       'QUIT', 'KEYDOWN', 'KEYUP', 'MOUSEDOWN', 'MOUSEUP', or 'MOUSEMOTION.'
       
     - L{MouseButtonEvent.button} (found in L{MouseDown} and L{MouseUp} events)
     
       'LEFT', 'MIDDLE', 'RIGHT', 'SCROLLUP', 'SCROLLDOWN'
       
     - L{KeyEvent.key} (found in L{KeyDown} and L{KeyUp} events)
     
       'NONE', 'ESCAPE', 'BACKSPACE', 'TAB', 'ENTER', 'SHIFT', 'CONTROL',
       'ALT', 'PAUSE', 'CAPSLOCK', 'PAGEUP', 'PAGEDOWN', 'END', 'HOME', 'UP',
       'LEFT', 'RIGHT', 'DOWN', 'PRINTSCREEN', 'INSERT', 'DELETE', 'LWIN',
       'RWIN', 'APPS', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
       'KP0', 'KP1', 'KP2', 'KP3', 'KP4', 'KP5', 'KP6', 'KP7', 'KP8', 'KP9',
       'KPADD', 'KPSUB', 'KPDIV', 'KPMUL', 'KPDEC', 'KPENTER', 'F1', 'F2',
       'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
       'NUMLOCK', 'SCROLLLOCK', 'SPACE', 'CHAR'
"""

import time
# import ctypes

# noinspection PyProtectedMember
from .__tcod import _lib, _Mouse, _Key
from . import __tcod as _tcod
import untdl as _tdl

_eventQueue = []
_pushedEvents = []

_mouse_l = 0
_mouse_m = 0
_mouse_r = 0

# this interprets the constants from libtcod and makes a key -> keyname dictionary


def _parse_key_names(module):
    """
    returns a dictionary mapping of human readable key names to their keycodes
    this parses constants with the names of K_* and makes code=name pairs
    this is for KeyEvent.key variable and that enables things like:
    if (event.key == 'PAGEUP'):
    """
    _key_names = {}
    for attr in dir(module):  # from the modules variables
        if attr[:2] == 'K_':  # get the K_* constants
            _key_names[getattr(_tcod, attr)] = attr[2:]  # and make CODE=NAME pairs
    return _key_names


_keyNames = _parse_key_names(_tcod)


class Event(object):
    """Base Event class.
    
    You can easily subclass this to make your own events.  Be sure to set
    the class attribute L{Event.type} for it to be passed to a custom L{App}
    ev_* method."""
    __slots__ = ('__weakref__',)
    type = None
    """String constant representing the type of event.
    
    The L{App} ev_* methods depend on this attribute.
    
    Can be: 'QUIT', 'KEYDOWN', 'KEYUP', 'MOUSEDOWN', 'MOUSEUP', or 'MOUSEMOTION.'
    """

    def __repr__(self):
        """List an events public attributes when printed.
        """
        attr_dict = {}
        for var_name in dir(self):
            if '_' == var_name[0]:
                continue
            attr_dict[var_name] = self.__getattribute__(var_name)
        return '%s Event %s' % (self.__class__.__name__, repr(attr_dict))


class Quit(Event):
    """Fired when the window is closed by the user.
    """
    __slots__ = ()
    type = 'QUIT'


class KeyEvent(Event):
    __slots__ = ('key', 'char', 'keychar', 'shift', 'alt', 'control',
                 'leftAlt', 'leftCtrl', 'rightAlt', 'rightCtrl')

    def __init__(self, key, char, l_alt, l_ctrl, r_alt, r_ctrl, shift):
        # Convert keycodes into string, but use string if passed
        self.key = key if isinstance(key, str) else _keyNames[key]
        """Human readable names of the key pressed.
        Non special characters will show up as 'CHAR'.
        
        Can be one of
        'NONE', 'ESCAPE', 'BACKSPACE', 'TAB', 'ENTER', 'SHIFT', 'CONTROL',
        'ALT', 'PAUSE', 'CAPSLOCK', 'PAGEUP', 'PAGEDOWN', 'END', 'HOME', 'UP',
        'LEFT', 'RIGHT', 'DOWN', 'PRINTSCREEN', 'INSERT', 'DELETE', 'LWIN',
        'RWIN', 'APPS', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'KP0', 'KP1', 'KP2', 'KP3', 'KP4', 'KP5', 'KP6', 'KP7', 'KP8', 'KP9',
        'KPADD', 'KPSUB', 'KPDIV', 'KPMUL', 'KPDEC', 'KPENTER', 'F1', 'F2',
        'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
        'NUMLOCK', 'SCROLLLOCK', 'SPACE', 'CHAR'
        
        For the actual character instead of 'CHAR' use L{keychar}.
        @type: string"""
        char = char if isinstance(char, str) else char.decode()
        self.char = char.replace('\x00', '')  # change null to empty string
        """A single character string of the letter or symbol pressed.
        
        Special characters like delete and return are not cross-platform.
        L{key} or L{keychar} should be used instead for special keys.
        Characters are also case sensitive.
        @type: string"""
        # get the best out of self.key and self.char
        self.keychar = self.char if self.key == 'CHAR' else self.key
        """Similar to L{key} but returns a case sensitive letter or symbol
        instead of 'CHAR'.
        
        This variable makes available the widest variety of symbols and should
        be used for key-mappings or anywhere where a narrower sample of keys
        isn't needed.
        """
        self.leftAlt = bool(l_alt)
        """@type: boolean"""
        self.rightAlt = bool(r_alt)
        """@type: boolean"""
        self.leftCtrl = bool(l_ctrl)
        """@type: boolean"""
        self.rightCtrl = bool(r_ctrl)
        """@type: boolean"""
        self.shift = bool(shift)
        """True if shift was held down during this event.
        @type: boolean"""
        self.alt = bool(l_alt or r_alt)
        """True if alt was held down during this event.
        @type: boolean"""
        self.control = bool(l_ctrl or r_ctrl)
        """True if control was held down during this event.
        @type: boolean"""


class KeyDown(KeyEvent):
    """Fired when the user presses a key on the keyboard or a key repeats.
    """
    __slots__ = ()
    type = 'KEYDOWN'


class KeyUp(KeyEvent):
    """Fired when the user releases a key on the keyboard.
    """
    __slots__ = ()
    type = 'KEYUP'


_mouseNames = {1: 'LEFT', 2: 'MIDDLE', 3: 'RIGHT', 4: 'SCROLLUP', 5: 'SCROLLDOWN'}


class MouseButtonEvent(Event):
    __slots__ = ('button', 'pos', 'cell')

    def __init__(self, button, pos, cell):
        self.button = _mouseNames[button]
        """Can be one of
        'LEFT', 'MIDDLE', 'RIGHT', 'SCROLLUP', 'SCROLLDOWN'
        @type: string"""
        self.pos = pos
        """(x, y) position of the mouse on the screen
        @type: (int, int)"""
        self.cell = cell
        """(x, y) position of the mouse snapped to a cell on the root console
        @type: (int, int)"""


class MouseDown(MouseButtonEvent):
    """Fired when a mouse button is pressed."""
    __slots__ = ()
    type = 'MOUSEDOWN'


class MouseUp(MouseButtonEvent):
    """Fired when a mouse button is released."""
    __slots__ = ()
    type = 'MOUSEUP'


class MouseMotion(Event):
    """Fired when the mouse is moved."""
    __slots__ = ('pos', 'motion', 'cell', 'cellmotion')
    type = 'MOUSEMOTION'

    def __init__(self, pos, cell, motion, cellmotion):
        self.pos = pos
        """(x, y) position of the mouse on the screen.
        type: (int, int)"""
        self.cell = cell
        """(x, y) position of the mouse snapped to a cell on the root console.
        type: (int, int)"""
        self.motion = motion
        """(x, y) motion of the mouse on the screen.
        type: (int, int)"""
        self.cellmotion = cellmotion
        """(x, y) motion of the mouse moving over cells on the root console.
        type: (int, int)"""


# noinspection PyPep8Naming,PyMethodMayBeStatic,PyAttributeOutsideInit
class App(object):
    """
    Application framework.
    
     - ev_*: Events are passed to methods based on their L{Event.type} attribute.
       If an event type is 'KEYDOWN' the ev_KEYDOWN method will be called
       with the event instance as a parameter.
    
     - key_*: When a key is pressed another method will be called based on the
       L{KeyEvent.key} attribute.  For example the 'ENTER' key will call key_ENTER
       with the associated L{KeyDown} event as its parameter.
       
     - L{update}: This method is called every loop.  It is passed a single
       parameter detailing the time in seconds since the last update
       (often known as deltaTime.)
       
       You may want to call drawing routines in this method followed by
       L{untdl.flush}.
    """
    __slots__ = ('__running', '__prevTime')

    def ev_QUIT(self, event):
        """Unless overridden this method raises a SystemExit exception closing
        the program."""
        raise SystemExit()

    def ev_KEYDOWN(self, event):
        """Override this method to handle a L{KeyDown} event."""

    def ev_KEYUP(self, event):
        """Override this method to handle a L{KeyUp} event."""

    def ev_MOUSEDOWN(self, event):
        """Override this method to handle a L{MouseDown} event."""

    def ev_MOUSEUP(self, event):
        """Override this method to handle a L{MouseUp} event."""

    def ev_MOUSEMOTION(self, event):
        """Override this method to handle a L{MouseMotion} event."""

    def update(self, delta_time):
        """Override this method to handle per frame logic and drawing.
        
        @type delta_time: float
        @param delta_time: This parameter tells the amount of time passed since
                          the last call measured in seconds as a floating point
                          number.
                          
                          You can use this variable to make your program
                          frame rate independent.
                          Use this parameter to adjust the speed of motion,
                          timers, and other game logic.
        """
        pass

    def suspend(self):
        """When called the App will begin to return control to where
        L{App.run} was called.
        
        Some further events are processed and the L{App.update} method will be
        called one last time before exiting
        (unless suspended during a call to L{App.update}.)
        """
        self.__running = False

    def run(self):
        """Delegate control over to this App instance.  This function will
        process all events and send them to the special methods ev_* and key_*.
        
        A call to L{App.suspend} will return the control flow back to where
        this function is called.  And then the App can be run again.
        But a single App instance can not be run multiple times simultaneously.
        """
        if getattr(self, '_App__running', False):
            raise _tdl.TDLError('An App can not be run multiple times simultaneously')
        self.__running = True
        while self.__running:
            self.run_once()

    def run_once(self):
        """Pump events to this App instance and then return.
        
        This works in the way described in L{App.run} except it immediately
        returns after the first L{update} call.
        
        Having multiple L{App} instances and selectively calling run_once on
        them is a decent way to create a state machine.
        """
        if not hasattr(self, '_App__prevTime'):
            self.__prevTime = time.clock()  # initiate __prevTime
        for event in get():
            if event.type:  # exclude custom events with a blank type variable
                # call the ev_* methods
                method = 'ev_%s' % event.type  # ev_TYPE
                getattr(self, method)(event)
            if event.type == 'KEYDOWN':
                # call the key_* methods
                method = 'key_%s' % event.key  # key_KEYNAME
                if hasattr(self, method):  # silently exclude undefined methods
                    getattr(self, method)(event)
        new_time = time.clock()
        self.update(new_time - self.__prevTime)
        self.__prevTime = new_time
        #_tdl.flush()


def _process_events():
    """Flushes the event queue from libtcod into the global list _eventQueue"""
    global _mouse_l, _mouse_m, _mouse_r, _eventsflushed, _pushedEvents
    _eventsflushed = True
    events = _pushedEvents  # get events from event.push
    _pushedEvents = []  # then clear the pushed events queue

    mouse = _Mouse()
    lib_key = _Key()
    while 1:
        lib_event = _lib.TCOD_sys_check_for_event(_tcod.TCOD_EVENT_ANY, lib_key, mouse)
        if not lib_event:  # no more events from libtcod
            break

        #if mouse.dx or mouse.dy:
        if lib_event & _tcod.TCOD_EVENT_MOUSE_MOVE:
            events.append(MouseMotion(*mouse.motion))

        mouse_pos = ((mouse.x, mouse.y), (mouse.cx, mouse.cy))

        for old_state, new_state, released, button in zip((_mouse_l, _mouse_m, _mouse_r),
                                                          mouse.button, mouse.button_pressed, (1, 2, 3)):
            if released:
                if not old_state:
                    events.append(MouseDown(button, *mouse_pos))
                events.append(MouseUp(button, *mouse_pos))
                if new_state:
                    events.append(MouseDown(button, *mouse_pos))
            elif new_state and not old_state:
                events.append(MouseDown(button, *mouse_pos))

        if mouse.wheel_up:
            events.append(MouseDown(4, *mouse_pos))
        if mouse.wheel_down:
            events.append(MouseDown(5, *mouse_pos))

        _mouse_l = mouse.lbutton
        _mouse_m = mouse.mbutton
        _mouse_r = mouse.rbutton

        if lib_key.vk == _tcod.K_NONE:
            break
        if lib_key.pressed:
            keyevent = KeyDown
        else:
            keyevent = KeyUp
        events.append(keyevent(*tuple(lib_key)))

    if _lib.TCOD_console_is_window_closed():
        events.append(Quit())

    _eventQueue.extend(events)


def get():
    """Flushes the event queue and returns the list of events.
    
    This function returns L{Event} objects that can be identified by their
    type attribute or their class.
    
    @rtype: iterator
    @return: Returns an iterable of objects derived from L{Event} or anything
             put in a L{push} call.  If the iterator is deleted or otherwise
             interrupted before finishing the excess items are preserved for the
             next call.
    """

    def event_generator():
        while _eventQueue:
            # if there is an interruption the rest of the events stay untouched
            # this means you can break out of a event.get loop without losing
            # the leftover events
            yield (_eventQueue.pop(0))
        raise StopIteration()

    _process_events()
    return event_generator()


def push(event):
    """Push an event into the event buffer.
    
    @type event: L{Event}-like object
    @param event: The event will be available on the next call to L{event.get}.
                  An event pushed in the middle of a L{get} will not show until
                  the next time L{get} called preventing push related
                  infinite loops.
    """
    _pushedEvents.append(event)


def key_wait():
    """Waits until the user presses a key.
    Then returns a L{KeyDown} event.
    
    Key events will repeat if held down.
    
    A click to close the window will be converted into an Alt+F4 KeyDown event.
    
    @rtype: L{KeyDown}
    """
    while 1:
        for event in get():
            if event.type == 'KEYDOWN':
                return event
            if event.type == 'QUIT':
                # convert QUIT into alt+F4
                return KeyDown('F4', '', True, False, True, False, False)
        time.sleep(.001)


def set_key_repeat(delay=500, interval=0):
    """Change or disable key repeat.
    
    @type delay: int
    @param delay: Milliseconds before a held key begins to repeat.
    
                  Key repeat can be disabled entirely by setting a delay of zero.
    
    @type interval: int
    @param interval: Milliseconds between key repeats.
    
                     An interval of zero will repeat every frame.
    """
    _lib.TCOD_console_set_keyboard_repeat(delay, interval)


def is_window_closed():
    """Returns True if the exit button on the window has been clicked and
    stays True afterwards.
    
    @rtype: boolean
    """
    return _lib.TCOD_console_is_window_closed()


__all__ = [_var for _var in locals().keys() if _var[0] != '_' and _var not in ['time', 'ctypes']]
