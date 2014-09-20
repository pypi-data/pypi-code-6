"""This is a simple module designed to provide an object oriented interface to the cursor for python.
This depends of User32.dll and hence, Windows.This module is at it's very beginning stage and will mature.
There will be more features coming down the line!This module needs the ctypes module as it's  only dependancy"""
from ctypes import c_int, Structure, c_uint, c_long, c_ulong, pointer
import ctypes
from ctypes import util
class User32_Import_Error(Exception):
    """An error to raise in case we can't import User32"""
class POINT(Structure):
    _fields_ = [("x", c_int),
               ("y", c_int)]
try:
    User32Lib=ctypes.windll.LoadLibrary(ctypes.util.find_library("User32"))
except:
    raise User32_Import_Error("Could not import User32")
class Mouse:
    """This is a class that provides the interface to controlling a windows cursor"""
    def __init__(self):
        """Creates a new Mouse object that can be used in controlling a Windows cursor"""
        self.MOUSEEVENTF_ABSOLUTE=0x8000
        self.MOUSEEVENTF_LEFTDOWN=0x0002
        self.MOUSEEVENTF_LEFTUP=0x0004
        self.MOUSEEVENTF_MIDDLEDOWN=0x0020
        self.MOUSEEVENTF_MIDDLEUP=0x0040
        self.MOUSEEVENTF_MOVE=0x0001
        self.MOUSEEVENTF_RIGHTDOWN=0x0008
        self.MOUSEEVENTF_RIGHTUP=0x0010
        self.MOUSEEVENTF_WHEEL=0x0800
        self.MOUSEEVENTF_XDOWN=0x0080
        self.MOUSEEVENTF_XUP=0x0100
        self.MOUSEEVENTF_HWHEEL=0x01000
        self.mouse_current=int()
    def right_click(self):
        """Presses down and releases right mouse button"""
        self.right_down()
        self.right_up()
    def right_down(self):
        """Holds down right mouse button"""
        User32Lib.mouse_event(self.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    def right_up(self):
        """Releases the right mouse button"""
        User32Lib.mouse_event(self.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    def left_click(self):
        """Left-Clicks the mouse"""
        self.left_down()
        self.left_up()
    def left_down(self):
        """Pushes down the left mouse button"""
        User32Lib.mouse_event(self.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    def left_up(self):
        """Lifts up the left mouse key"""
        User32Lib.mouse_event(self.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    def move_mouse(self, x, y):
        """Moves the mouse to (x, y)"""
        User32Lib.SetCursorPos(x, y)
    def get_mouse_pos(self):
        """Gets the Mouse position and returns a tuple of (x,y) form"""
        self.point=POINT()
        User32Lib.GetCursorPos(ctypes.pointer(self.point))
        return tuple((self.point.x, self.point.y))
