import unittest

from tmplt import render

class TestTmplt(unittest.TestCase):

  def testEmpty(self):
    self.assertEqual('', render('', 'foo'))
    self.assertEqual('', render('', {}))
    self.assertEqual('', render('', []))
    self.assertEqual('', render('', ()))

  def testEmptyTmpl(self):
    self.assertEqual('', render('', {'foo': 'bar'}))
    self.assertEqual('', render('', ['bar']))
    self.assertEqual('', render('', ()))

  def testEmptyData(self):
    self.assertEqual('', render('{{ foo }}', {}))
    self.assertEqual('', render('{{ 0 }}', []))
    self.assertEqual('', render('{{ 0 }}', ()))

  def testStringData(self):
    expected = 'bar bar'
    tmpl = '{{foo}} {{ foo }}'
    self.assertEqual(expected, render(tmpl, {'foo': 'bar'}))
    tmpl = '{{0}} {{ 0 }}'
    self.assertEqual(expected, render(tmpl, ['bar']))
    self.assertEqual(expected, render(tmpl, ('bar',)))

  def testNonStringData(self):
    tmpl = '{{ foo }}'
    self.assertEqual('None', render(tmpl, {'foo': None}))
    self.assertEqual('True', render(tmpl, {'foo': True}))
    self.assertEqual('42', render(tmpl, {'foo': 42}))
    self.assertEqual('3.14', render(tmpl, {'foo': 3.14}))
    self.assertEqual('1j', render(tmpl, {'foo': 1j}))

  def testFunctionData(self):
    def bar(data):
      return data['foo']
    tmpl = '{{ bar }}'
    data = {
      'foo': 'baz',
      'bar': bar
    };
    self.assertEqual('baz', render(tmpl, data))

  def testLambdaData(self):
    tmpl = '{{ bar }}'
    data = {
      'foo': 'baz',
      'bar': lambda data: data['foo']
    };
    self.assertEqual('baz', render(tmpl, data))

  def testNested(self):
    data = {
      'foo': [
        'Hello',
        'Goodbye'
      ],
      'bar': 'World'
    }
    self.assertEqual('Hello, World!', render('{{ foo.0 }}, {{ bar }}!', data))
    self.assertEqual('Goodbye, World!', render('{{ foo.1 }}, {{ bar }}!', data))

  def testNonExistent(self):
    d = {'foo': 'qux'}
    self.assertEqual('qux', render('{{ foo }}', d))
    self.assertEqual('', render('{{ bar }}', d))
    self.assertEqual('', render('{{ foo.bar }}', d))
    l = ['qux']
    self.assertEqual('qux', render('{{ 0 }}', l))
    self.assertEqual('', render('{{ foo }}', l))
    self.assertEqual('', render('{{ 1 }}', l))
    self.assertEqual('', render('{{ 0.1 }}', l))
    t = ('qux',)
    self.assertEqual('qux', render('{{ 0 }}', t))
    self.assertEqual('', render('{{ foo }}', t))
    self.assertEqual('', render('{{ 1 }}', t))
    self.assertEqual('', render('{{ 0.1 }}', t))
