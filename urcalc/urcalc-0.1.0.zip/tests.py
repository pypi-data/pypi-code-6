#!/usr/bin/env python3

import unittest

from c import C


def c_input(keys, c=None, auto_eq=True, return_c=True):

  if c is None:
    c = C()

  for key in keys:
    c.handle_input(key)

  if auto_eq:
    c.handle_input('=')

  if return_c:
    return c.c

  return c


def o(keys):

  return c_input(keys, auto_eq=False, return_c=False).output.get_text()[0]


def c(keys):

  return c_input(keys)


class CTestCase(unittest.TestCase):

  def test_number_input(self):

    self.assertEqual(o('123'), '123')

    self.assertEqual(o('1.'), '1.')
    self.assertEqual(o('1.2'), '1.2')
    self.assertEqual(o('1.23'), '1.23')

    self.assertEqual(o('1..'), '1.')

    self.assertEqual(o('n'), '-0')
    self.assertEqual(o('nn'), '0')
    self.assertEqual(o('n.12'), '-0.12')

    self.assertEqual(o('1n'), '-1')
    self.assertEqual(o('1nn'), '1')
    self.assertEqual(o('1.23n'), '-1.23')
    self.assertEqual(o('1.23nn'), '1.23')

    self.assertEqual(o(('1', 'backspace')), '0')
    self.assertEqual(o(('1', '.', 'backspace')), '1')
    self.assertEqual(o(('1', '.', '2', 'backspace')), '1.')
    self.assertEqual(o(('1', '.', '2', '3', 'backspace')), '1.2')

    self.assertEqual(o('1C'), '0')
    self.assertEqual(o(('1', 'esc')), '0')

  def test_one_operation(self):

    self.assertEqual(c('3 + 5'), '8')
    self.assertEqual(c('3 - 5'), '-2')
    self.assertEqual(c('3 * 5'), '15')
    self.assertEqual(c('3 / 5'), '0.6')

  def test_order_of_precedence(self):

    self.assertEqual(c('3 + 4 * 5'), '23')
    self.assertEqual(c('3 + 4 * 5 * 2'), '43')

    self.assertEqual(c('6 * 3 + 2'), '20')

    self.assertEqual(c('4 * 5 + 3'), '23')
    self.assertEqual(c('4 * 5 * 2 + 3'), '43')

    self.assertEqual(c('3 + 4 * 5 - 1'), '22')
    self.assertEqual(c('3 + 4 * 5 * 2 - 1'), '42')

    self.assertEqual(c('4 * 5 - 1 + 3'), '22')
    self.assertEqual(c('4 * 5 * 2 - 1 + 3'), '42')

  def test_decimal(self):

    f = '123.456'
    self.assertEqual(c(f), f)
    self.assertEqual(c(f + '*1'), f)

  def test_significant_figures(self):

    FIGURES = C.FIGURES

    f = '0.' + ('0' * (FIGURES - 1)) + '1'
    self.assertEqual(c(f + '*1'), f)

    f = '0.' + ('0' * FIGURES) + '1'
    self.assertEqual(c(f + '*1'), '0')

    f = '1234567899' * 5
    exp = f[:FIGURES - 1] + f[FIGURES] + '0' * (len(f) - FIGURES)
    self.assertEqual(c(f + '+0'), exp)
    self.assertEqual(c(f + '*1'), exp)

    f = '5' * FIGURES
    self.assertEqual(c(f + '*1'), f)

    f = '5' * (FIGURES + 1)
    self.assertEqual(c(f + '*1'), f[:-2] + '60')

    f = '4' * (FIGURES + 1)
    self.assertEqual(c(f + '*1'), f[:-1] + '0')


if __name__ == '__main__':
  unittest.main()
