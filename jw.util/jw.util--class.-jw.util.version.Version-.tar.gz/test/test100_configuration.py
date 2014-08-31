"""
Test configuration module
"""
import io
import os
import tempfile
import unittest

from jw.util import configuration

CONFIG1 = """
level1:
    level2:
        str: string
        int: 1
"""

def test1():
    """
    Test FromString()
    """
    c = configuration.FromString(CONFIG1)
    assert c['level1']

def test2():
    """
    Test FromStream()
    """
    c = configuration.FromStream(io.BytesIO(CONFIG1))
    assert c['level1']

def test3():
    """
    Test FromFile()
    """
    filename = os.path.join(os.path.sep, 'tmp', '%s.tmp' % __name__)
    open(filename, 'w').write(CONFIG1)
    c = configuration.FromFile(filename)
    assert c['level1']
    os.remove(filename)

def test4():
    """
    Test at()
    """
    c = configuration.FromString(CONFIG1)
    assert c.at('level1.level2.str') == 'string'
    assert c.at('level1.level2.int') == 1
    assert c.at('level1.level2.nothing') is None
    assert c.at('level1.level2.nothing', default='none') == 'none'
    assert c.at('level1.level2.nothing', 'none') == 'none'

def test5():
    """
    Test multi-level path access
    """
    c = configuration.FromString(CONFIG1)
    assert c('level1', 'level2', 'str') == 'string'
    assert c('level1', 'level2', 'nothing', default='none') == 'none'

class TestToFile(unittest.TestCase):
    """
    Test configuration.ToFile
    """

    def setUp(self):
        self.filename = tempfile.mktemp()

    def tearDown(self):
        os.remove(self.filename)

    def test1(self):
        configuration.ToFile({'x': 1}, self.filename, False)
        c = configuration.FromFile(self.filename)
        self.assertEqual(c['x'], 1)