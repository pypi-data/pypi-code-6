# Copyright (C) 2014 Yu-Jie Lin
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
from decimal import Decimal, getcontext
from operator import truediv as div
from operator import add, mul, sub

import urwid

__module__ = 'c'
__description__ = 'Simple calculator in terminal using Urwid'
__copyright__ = 'Copyright 2014, Yu Jie Lin'
__license__ = 'MIT License'
__version__ = '0.1.0'
__website__ = 'http://bitbucket.org/livibetter/c'

__author__ = 'Yu-Jie Lin'
__author_email__ = 'livibetter@gmail.com'


OP_MAP = {'+': add, '-': sub, '*': mul, '/': div}
RE = re.compile('\s+')
LAYOUT = '''
 C   7   8   9   +
<--  4   5   6   -
+/-  1   2   3   *
OFF  0   .   =   /
'''
LAYOUT = tuple(filter(
  None,
  (tuple(filter(None, RE.split(line))) for line in LAYOUT.split('\n'))
))
PALETTE = [
  (None, 'dark green', 'default'),
  ('focus', 'light red', 'default'),
  ('output', 'light blue', 'default'),
]


class CBigText(urwid.BigText):

  _selectable = True


class CButton(urwid.Button):

  def __init__(self, label, on_press=None):

    w = CBigText(label, urwid.HalfBlock5x4Font())
    self._label = w
    w = urwid.AttrMap(w, None, 'focus')
    w = urwid.Padding(w, align='center', width='clip')
    w = urwid.Filler(w, valign='middle', bottom=1)
    w = urwid.BoxAdapter(w, height=5)
    urwid.WidgetWrap.__init__(self, w)

    if on_press:
      urwid.connect_signal(self, 'click', on_press)

    self.set_label(label)


class C():

  FIGURES = 17  # significant figures
  FMT = '%d.%df' % (FIGURES, FIGURES)

  def __init__(self):

    output = urwid.BigText('', urwid.HalfBlock5x4Font())
    self.output = output
    top_row = urwid.Padding(output, align='right', width='clip')
    top_row = urwid.AttrMap(top_row, 'output')
    top_row = urwid.Filler(top_row, top=1)
    top_row = urwid.BoxAdapter(top_row, height=5)

    _btn = lambda btn: CButton(btn, on_press=self.button_keypress)
    _row = lambda btn: _btn(btn) if btn != '---' else urwid.Text('')
    rows = [urwid.Columns(map(_row, row)) for row in LAYOUT]

    self.widget = urwid.Filler(urwid.Pile([top_row] + rows))

    self.reset(reset_c=True, reset=True, reset_p=True)
    self.update_output()

  def reset(self, reset_c=False, reset=False, reset_p=False):

    if reset_c:
      self.c = '0'    # current number
    if reset:
      self.n = None   # last number
      self.o = None   # operator
    if reset_p:       # order of precedence
      self.np = None  # number
      self.op = None  # operator

  def update_output(self):

    self.output.set_text(self.c)

  def handle_input(self, key):

    if isinstance(key, tuple) and key[0].startswith('mouse'):
      return False

    if '0' <= key <= '9':
      self.c = key if self.c == '0' else self.c + key
    elif key == '.':
      if '.' not in self.c:
        self.c += key
    elif key in ('n', '+/-'):
      self.c = self.c[1:] if self.c.startswith('-') else '-' + self.c
    elif key in '+-*/':
      if self.n is None:
        self.n = self.c
        self.o = key
      else:
        if key in ('+', '-'):
          if self.op:
            self.np = self.do_op(self.op, self.np, self.c)
            self.n = self.do_op(self.o, self.n, self.np)
            self.o = key
            self.reset(reset_p=True)
          elif self.o:
            self.n = self.do_op(self.o, self.n, self.c)
            self.o = key
          else:
            self.n = self.do_op(key, self.n, self.c)
        else:
          if self.op:
            self.np = self.do_op(self.op, self.np, self.c)
            self.op = key
          elif self.o in ('+', '-'):
            self.np = self.c
            self.op = key
          else:
            self.n = self.do_op(key, self.n, self.c)
      self.c = '0'
    elif key == '=':
      if self.op:
        self.c = self.do_op(self.op, self.np, self.c)
        self.reset(reset_p=True)
      if self.o:
        self.c = self.do_op(self.o, self.n, self.c)
      self.reset(reset=True)
    elif key in ('backspace', '<--'):
      self.c = self.c[:-1]
      if not self.c:
        self.c = '0'
    elif key in ('esc', 'C'):
      self.reset(reset_c=True, reset=True, reset_p=True)
    elif key in ('q', 'Q', 'OFF'):
      raise urwid.ExitMainLoop()

    self.update_output()
    return True

  def button_keypress(self, button):

    self.handle_input(button.get_label())

  @classmethod
  def f(cls, n):

    return (format(n, cls.FMT)).rstrip('0').rstrip('.')

  @classmethod
  def do_op(cls, op, a, b):

    getcontext().prec = cls.FIGURES
    return cls.f(OP_MAP[op](Decimal(a), Decimal(b)))


def main():

  c = C()
  loop = urwid.MainLoop(c.widget, PALETTE, unhandled_input=c.handle_input)
  loop.run()


if __name__ == '__main__':
  main()
