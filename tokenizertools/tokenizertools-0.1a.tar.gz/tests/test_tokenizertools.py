import tokenizertools as tt
import lookaheadtools as la
import unittest as ut

file1text = """abc 123
def while 123.456 Ghi789_10
"""

file2text = """abc 123
def "a \\\"string\\\" const" 3.14
"""

file3text = """abc 123
allfloat 456 allowint 789
def
"""

# The Token class used in the test suite.
class Token(object):
    _keywords = {'if':'IF','while':'WHILE','else':'ELSE',
                 'allfloat':'ALLFLOAT','allowint':'ALLOWINT'}
    def __init__(self, tokenType, value, lexpos):
        self.type = tokenType
        self.value = value
        self.lexpos = lexpos
    def __str__(self):
        s = ','.join([str(x) for x in [self.type, self.value, self.lexpos]])
        return s.join(['(',')'])
    def __eq__(self, other):
        # Including lexpos in __eq__() only makes sense because this
        # is used for validation test cases.  In practical applications,
        # token equality would ignore lexical position.
        if other == None: return False
        return self.type == other.type \
            and self.value == other.value \
            and self.lexpos.lineno == other.lexpos.lineno \
            and self.lexpos.colno == other.lexpos.colno \
            and self.lexpos.charpos == other.lexpos.charpos \
            and self.lexpos.cookie == other.lexpos.cookie
    @classmethod
    def typeInt(cls, s, lexpos):
        return cls('INT', int(s), lexpos)
    @classmethod
    def typeFloat(cls, s, lexpos):
        return cls('FLOAT', float(s), lexpos)
    @classmethod
    def typeIdent(cls, s, lexpos):
        # First screen the token text through the keyword dictionary.
        # Anything not found is an identifier.
        try:
            return cls(cls._keywords[s], s, lexpos)
        except KeyError:
            return cls('ID', s, lexpos)
    @classmethod
    def typeStr(cls, s, lexpos):
        # Process escape sequences.
        t = ''
        it = la.Lookahead(iter(s))
        for c in it:
            if c == '\\':
                if it[0] == '"' or it[0] == '\\':
                    c = next(it)
            t += c
        return cls('STR',t,lexpos)
    @classmethod
    def isNum(cls, aToken):
        return aToken.type in frozenset(['INT','FLOAT'])
        
class Lexer01(tt.RegexTokenizer):
    "Trivial lexer."
    spec = [
          (r'[a-zA-Z][a-zA-Z0-9_]*',Token.typeIdent), # idents and keywords
          (r'[0-9]+\.[0-9]+',Token.typeFloat), # floats
          (r'[0-9]+', Token.typeInt), # ints
          (r'\s*',None), # ignore white space
    ]

class Lexer02(tt.RegexTokenizer):
    "Lexer with start state for capturing string literals."
    spec = [
          (r'"', (None, 'str')), # Start string state
          (r'(\\"|[^"])*', Token.typeStr, ['str']), # Pick up str const.
          (r'"', (None, 0), ['str']), # Back to initial state.
          (r'[a-zA-Z][a-zA-Z0-9_]*',Token.typeIdent), # idents and keywords
          (r'[0-9]+\.[0-9]+',Token.typeFloat), # floats
          (r'[0-9]+', Token.typeInt), # ints
          (r'\s*',None), # ignore white space
    ]

def compute_begin(s, lexpos):
    "Lexer action to compute a start state."
    tkn = Token.typeIdent(s, lexpos)
    if tkn.type == 'ALLFLOAT':
        ns = 'allfloat'
    elif tkn.type == 'ALLOWINT':
        ns = 0
    else:
        ns = None
    return tkn,ns

class Lexer03(tt.RegexTokenizer):
    "Lexer with computed start states and a multi-state rule."
    spec = [
          #(r'[a-zA-Z][a-zA-Z0-9_]*',Token.typeIdent), # idents and keywords
          (r'[a-zA-Z][a-zA-Z0-9_]*',(compute_begin,'?'),[0,'allfloat']), # idents and keywords
          (r'[0-9]+\.[0-9]+',Token.typeFloat,[0,'allfloat']), # floats
          (r'[0-9]+', Token.typeInt,[0]), # ints
          (r'[0-9]+', Token.typeFloat,['allfloat']), # float from int
          (r'\s*',None, [0,'allfloat']), # ignore white space
    ]
    
class TestRegex_01(ut.TestCase):
    def setUp(self):
        self.testFileName = 'testfile.txt'
        with open(self.testFileName,'w') as f:
            f.write(file1text)
    def test_simple(self):
        with open(self.testFileName) as f:
            it = Lexer01(f, f.name)
            tkn = next(it)
            self.assertEqual(tkn, Token('ID','abc',tt.Lexpos(1,0,0,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('INT',123,tt.Lexpos(1,4,4,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('ID','def',tt.Lexpos(2,0,8,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('WHILE','while',tt.Lexpos(2,4,12,f.name)))            
            tkn = next(it)
            self.assertEqual(tkn, Token('FLOAT',123.456,tt.Lexpos(2,10,18,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('ID','Ghi789_10',tt.Lexpos(2,18,26,f.name)))
            with self.assertRaises(StopIteration):
                next(it)
    def test_consume(self):
        with open(self.testFileName) as f:
            it = Lexer01(f, f.name)
            tkn = next(it)
            self.assertEqual(tkn, Token('ID','abc',tt.Lexpos(1,0,0,f.name)))
            tkn = it.consume(Token.isNum)
            self.assertEqual(tkn, Token('INT',123,tt.Lexpos(1,4,4,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('ID','def',tt.Lexpos(2,0,8,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('WHILE','while',tt.Lexpos(2,4,12,f.name)))            
            tkn = it.consume(Token.isNum)
            self.assertEqual(tkn, Token('FLOAT',123.456,tt.Lexpos(2,10,18,f.name)))
            with self.assertRaises(AssertionError):
                tkn = it.consume(Token.isNum)
    def test_accept(self):
        with open(self.testFileName) as f:
            it = tt.TokenizeAhead(Lexer01(f,f.name))
            tkn = it.accept(Token.isNum)
            self.assertIsNone(tkn)
            tkn = next(it)
            self.assertEqual(tkn, Token('ID','abc',tt.Lexpos(1,0,0,f.name)))
            tkn = it.accept(Token.isNum)
            self.assertEqual(tkn, Token('INT',123,tt.Lexpos(1,4,4,f.name)))
            tkn = it.consume(lambda t: t.type == 'ID')
            tkn = it.accept(Token.isNum)
            self.assertIsNone(tkn)
            tkn = it.consume(lambda t: t.type == 'WHILE')
            tkn = it.accept(Token.isNum)
            self.assertEqual(tkn, Token('FLOAT',123.456,tt.Lexpos(2,10,18,f.name)))
            
class TestRegex_02(ut.TestCase):
    def setUp(self):
        self.testFileName = 'testfile.txt'
        with open(self.testFileName,'w') as f:
            f.write(file2text)
    def test_states(self):
        with open(self.testFileName) as f:
            it = Lexer02(f, f.name)
            tkn = next(it)
            self.assertEqual(tkn, Token('ID','abc',tt.Lexpos(1,0,0,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('INT',123,tt.Lexpos(1,4,4,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('ID','def',tt.Lexpos(2,0,8,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('STR',r'a "string" const',tt.Lexpos(2,5,13,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('FLOAT',3.14,tt.Lexpos(2,25,33,f.name)))
            with self.assertRaises(StopIteration):
                next(it)

class TestRegex_03(ut.TestCase):
    def setUp(self):
        self.testFileName = 'testfile.txt'
        with open(self.testFileName,'w') as f:
            f.write(file3text)
    def test_computed_states(self):
        with open(self.testFileName) as f:
            it = Lexer03(f, f.name)
            tkn = next(it)
            self.assertEqual(tkn, Token('ID','abc',tt.Lexpos(1,0,0,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('INT',123,tt.Lexpos(1,4,4,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('ALLFLOAT','allfloat',tt.Lexpos(2,0,8,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('FLOAT',456,tt.Lexpos(2,9,17,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('ALLOWINT','allowint',tt.Lexpos(2,13,21,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('INT',789,tt.Lexpos(2,22,30,f.name)))
            tkn = next(it)
            self.assertEqual(tkn, Token('ID','def',tt.Lexpos(3,0,34,f.name)))
            with self.assertRaises(StopIteration):
                next(it)

class TestRegex_04(ut.TestCase):
    def test_inMemoryString(self):
        f = [ln + '\n' for ln in file1text.splitlines()]
    
if __name__ == '__main__':
    ut.main()
