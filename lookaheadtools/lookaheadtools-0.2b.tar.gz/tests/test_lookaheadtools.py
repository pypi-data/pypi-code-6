import lookaheadtools as la
import unittest as ut

file1text = """line 1
 line 22
LINE 3
"""

class TestLookahead(ut.TestCase):
    def setUp(self):
        self.s = 'abcdefghi'
    def test_simpleIteration(self):
        it = iter(self.s)
        li = la.Lookahead(it)
        s2 = ''
        for c in li:
            s2 += c
        self.assertEqual(self.s,s2)
    def test_simpleLookahead(self):
        li = la.Lookahead(iter(self.s))
        self.assertEqual(li[0],'a')
        self.assertEqual(li[1],'b')
        self.assertEqual(li[5],'f')
        self.assertIsNone(li[1000])
        self.assertEqual(next(li),'a')
        self.assertEqual(li[0],'b')
        self.assertEqual(li[5],'g')
    def test_sliceAhead(self):
        li = la.Lookahead(iter(self.s))
        self.assertEqual(next(li),'a')
        self.assertEqual(''.join(li[1:4]),'cde')
        self.assertEqual(li[100:110],[])
    def test_unusual(self):
        t = ([1,2],'abc',9j)
        li = la.Lookahead(iter(t))
        self.assertEqual(next(li),[1,2])
        self.assertEqual(next(li),'abc')
        self.assertEqual(next(li),9j)
        with self.assertRaises(StopIteration):
            next(li)

class TestLinesOf(ut.TestCase):
    def setUp(self):
        self.s1 = 'abc\ndef\nghi'
        self.s2 = self.s1 + '\n'
    def test_LinesOf01(self):
        it = la.LinesOf(self.s1)
        self.assertEqual(next(it),'abc\n')
        self.assertEqual(next(it),'def\n')
        self.assertEqual(next(it),'ghi')
        with self.assertRaises(StopIteration):
            next(it)
    def test_LinesOf02(self):
        it = la.LinesOf(self.s2)
        self.assertEqual(next(it),'abc\n')
        self.assertEqual(next(it),'def\n')
        self.assertEqual(next(it),'ghi\n')
        with self.assertRaises(StopIteration):
            next(it)
    def test_LinesOf03(self):
        it = la.LinesOf(self.s1)
        it2 = la.Lookahead(it)
        self.assertEqual(it2[0],'abc\n')
        self.assertEqual(it2[1],'def\n')
        self.assertEqual(next(it2),'abc\n')
        self.assertEqual(it2[0],'def\n')
        
        
class TestLexPos(ut.TestCase):
    def setUp(self):
        pass
    def test_lexpos1(self):
        lp = la.Lexpos(1,2,3,None)
        self.assertEqual(lp.lineno,1)
        self.assertEqual(lp.colno,2)
        self.assertEqual(lp.charpos,3)
        self.assertIsNone(lp.cookie)
    def test_lexpos2(self):
        lp = la.Lexpos(4,5,6,'aName')
        self.assertEqual(lp.lineno,4)
        self.assertEqual(lp.colno,5)
        self.assertEqual(lp.charpos,6)
        self.assertEqual(lp.cookie,'aName')
        
class TestFileLookahead(ut.TestCase):
    def setUp(self):
        self.testFileName = 'testfile.txt'
        with open(self.testFileName,'w') as f:
            f.write(file1text)
    def test_simple(self):
        with open(self.testFileName) as f:
            it = la.FileLookahead(f,f.name)
            self.assertEqual(it[0],'l')
            self.assertEqual(next(it),'l')
            self.assertEqual(''.join(it[0:3]),'ine')
            self.assertEqual(it.lexpos, la.Lexpos(1,1,1,self.testFileName))
            self.assertEqual(it.curln.rstrip(),file1text.split('\n')[0])
    def test_track01(self):
        with open(self.testFileName) as f:
            it = la.FileLookahead(f,f.name)
            self.assertEqual(it[9],'i')
            self.assertEqual(it.curln,'line 1\n')
            next(it)
            next(it)
            self.assertEqual(it.lexpos.colno, 2)
            while it[0] != '\n':
                next(it)
            self.assertEqual(it.curln,'line 1\n')
            self.assertEqual(it.lexpos.lineno, 1)
            next(it)
            self.assertEqual(it.lexpos.lineno, 2)
            self.assertEqual(it.curln,' line 22\n')
            self.assertEqual(it[1],'l')
            
class TestStringFileLookahead(ut.TestCase):
    def setUp(self):
        pass
    def test_string(self):
        with la.LinesOf('abc\ndef') as g:
            it = la.FileLookahead(g)
            self.assertEqual(it[0],'a')
            self.assertEqual(it[1],'b')
            self.assertEqual(it.curln,'abc\n')
            self.assertEqual(next(it),'a')
            self.assertEqual(next(it),'b')
            self.assertEqual(it.lexpos,la.Lexpos(1,2,2,None))
            self.assertEqual(next(it),'c')
            self.assertEqual(it.curln,'abc\n')
            self.assertEqual(next(it),'\n')
            self.assertEqual(it.curln,'def')
            self.assertEqual(it.lexpos,la.Lexpos(2,0,4,None))
            self.assertEqual(next(it),'d')
            self.assertEqual(next(it),'e')
            self.assertEqual(it[0],'f')
            self.assertEqual(next(it),'f')
            with self.assertRaises(StopIteration):
                next(it)
            
class TestLexahead(ut.TestCase):
    def setUp(self):
        self.testFileName = 'testfile.txt'
        with open(self.testFileName,'w') as f:
            f.write(file1text)
    def test_simple(self):
        with open(self.testFileName) as f:
            it = la.LexAhead(f,f.name)
            self.assertEqual(it[0], 'l')
            it.consume('l')
            self.assertEqual(it[0], 'i')
            self.assertEqual(it.curln, 'line 1\n')
            it.accept_not('',None)
            self.assertEqual(it[0], '\n')
            self.assertEqual(it.curln, 'line 1\n')
            self.assertEqual(it.lexpos,la.Lexpos(1,6,6,self.testFileName))
            self.assertEqual(it.accept(' \n',5),'\n ')
            self.assertEqual(it.accept(set('einl'),None),'line')
    def test_re(self):
        import re
        white = re.compile(r'\s*')
        notWhite = re.compile(r'\S*')
        with open(self.testFileName) as f:
            it = la.LexAhead(f,f.name)
            self.assertEqual(it.accept_re(white),'')
            self.assertEqual(it.accept_re(notWhite),'line')
            it.accept_not('',None)
            self.assertEqual(it.accept_re(white),'\n ')
            self.assertEqual(it.accept_re(notWhite),'line')
    def test_re_lexpos(self):
        import re
        alpha = re.compile(r'[a-zA-Z]+')
        white = re.compile(r'\s*')
        num = re.compile(r'[0-9]+')
        with open(self.testFileName) as f:
            it = la.LexAhead(f,f.name)
            self.assertEqual(it.lexpos,la.Lexpos(1,0,0,'testfile.txt'))
            self.assertEqual(it.accept_re(alpha),'line')
            self.assertEqual(it.lexpos,la.Lexpos(1,4,4,'testfile.txt'))
            it.accept_re(white)
            self.assertEqual(it.accept_re(num),'1')
            self.assertEqual(it.lexpos,la.Lexpos(1,6,6,'testfile.txt'))
            it.accept_re(white)
            self.assertEqual(it.lexpos,la.Lexpos(2,1,8,'testfile.txt'))
    def test_re_stopiter(self):
        pass # FIXME
        

if __name__ == '__main__':
    ut.main()
