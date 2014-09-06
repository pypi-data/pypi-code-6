# -*- coding: utf-8 -*-

# Soya 3D
# Copyright (C) 2001-2014 Jean-Baptiste LAMY
# http://www.lesfleursdunormal.fr/static/informatique/soya3d/index_en.html

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

RELEASED = 0
PRESSED	 = 1

KEYDOWN = 1
KEYUP = 2

MOUSEMOTION = 3
MOUSEBUTTONDOWN = 4
MOUSEBUTTONUP = 5

JOYAXISMOTION = 6
JOYBUTTONDOWN = 9
JOYBUTTONUP = 10

WINDOW_RESIZED = 11

QUIT = 13


QUERY = -1
IGNORE = 0
DISABLE = 0
ENABLE = 1


# Converted from SDL 2 scancodes :

K_a = "a" #4
K_b = "b" #5
K_c = "c" #6
K_d = "d" #7
K_e = "e" #8
K_f = "f" #9
K_g = "g" #10
K_h = "h" #11
K_i = "i" #12
K_j = "j" #13
K_k = "k" #14
K_l = "l" #15
K_m = "m" #16
K_n = "n" #17
K_o = "o" #18
K_p = "p" #19
K_q = "q" #20
K_r = "r" #21
K_s = "s" #22
K_t = "t" #23
K_u = "u" #24
K_v = "v" #25
K_w = "w" #26
K_x = "x" #27
K_y = "y" #28
K_z = "z" #29

K_1 = "1" #30
K_2 = "2" #31
K_3 = "3" #32
K_4 = "4" #33
K_5 = "5" #34
K_6 = "6" #35
K_7 = "7" #36
K_8 = "8" #37
K_9 = "9" #38
K_0 = "0" #39

K_RETURN = 40
K_ESCAPE = 41
K_BACKSPACE = 42
K_TAB = 43
K_SPACE = 44

K_MINUS = 45
K_EQUALS = 46
K_LEFTBRACKET = 47
K_RIGHTBRACKET = 48
K_BACKSLASH = 49
K_NONUSHASH = 50
K_SEMICOLON = 51
K_APOSTROPHE = 52
K_GRAVE = 53
K_COMMA = 54
K_PERIOD = 55
K_SLASH = 56

K_CAPSLOCK = 57

K_F1 = 58
K_F2 = 59
K_F3 = 60
K_F4 = 61
K_F5 = 62
K_F6 = 63
K_F7 = 64
K_F8 = 65
K_F9 = 66
K_F10 = 67
K_F11 = 68
K_F12 = 69

K_PRINTSCREEN = 70
K_SCROLLLOCK = 71
K_PAUSE = 72
K_INSERT = 73
K_HOME = 74
K_PAGEUP = 75
K_DELETE = 76
K_END = 77
K_PAGEDOWN = 78
K_RIGHT = 79
K_LEFT = 80
K_DOWN = 81
K_UP = 82

K_NUMLOCKCLEAR = 83
K_KP_DIVIDE = 84
K_KP_MULTIPLY = 85
K_KP_MINUS = 86
K_KP_PLUS = 87
K_KP_ENTER = 88
K_KP_1 = 89
K_KP_2 = 90
K_KP_3 = 91
K_KP_4 = 92
K_KP_5 = 93
K_KP_6 = 94
K_KP_7 = 95
K_KP_8 = 96
K_KP_9 = 97
K_KP_0 = 98
K_KP_PERIOD = 99



K_KP_COMMA = 133
K_KP_EQUALSAS400 = 134


K_LCTRL = 224
K_LSHIFT = 225
K_LALT = 226
K_LGUI = 227
K_RCTRL = 228
K_RSHIFT = 229
K_RALT = 230
K_RGUI = 231

K_MODE = 257







MOD_NONE  = 0x0000
MOD_LSHIFT= 0x0001
MOD_RSHIFT= 0x0002
MOD_LCTRL = 0x0040
MOD_RCTRL = 0x0080
MOD_LALT  = 0x0100
MOD_RALT  = 0x0200
MOD_LMETA = 0x0400
MOD_RMETA = 0x0800
MOD_NUM   = 0x1000
MOD_CAPS  = 0x2000
MOD_MODE  = 0x4000
MOD_RESERVED = 0x8000
MOD_CTRL  = MOD_LCTRL  | MOD_RCTRL
MOD_SHIFT = MOD_LSHIFT | MOD_RSHIFT
MOD_ALT   = MOD_LALT   | MOD_RALT
MOD_META  = MOD_LMETA  | MOD_RMETA

BUTTON_LEFT      = 1
BUTTON_MIDDLE    = 2
BUTTON_RIGHT     = 3
BUTTON_WHEELUP   = 4
BUTTON_WHEELDOWN = 5
