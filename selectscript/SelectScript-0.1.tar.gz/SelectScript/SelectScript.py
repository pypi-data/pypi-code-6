# $ANTLR 3.1.3 Mar 18, 2009 10:09:25 SelectScript.g 2014-02-03 13:11:12

import sys
from antlr3 import *
from antlr3.tree import *
from antlr3.compat import set, frozenset
        
import sys

import antlr3
import antlr3.tree

from SelectExprLexer import SelectExprLexer
from SelectExprParser import SelectExprParser



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
WHERE=60
LT=36
LIST_BEGIN=46
STMT_UPDATE=12
MOD=42
SUB=39
FLOAT=78
DQ=45
NOT=28
AND=21
EOF=-1
CHARACTER=81
TIME=63
AS=61
T__91=91
T__92=92
IN=30
POW=43
SEP=15
POS=8
THIS=62
VAL=6
VAR=5
DIGIT=76
EQ=32
DOT=14
COMMENT=73
SELECT=54
ADD=38
NE=33
INTEGER=77
D=20
E=51
GE=35
LIST_END=47
F=55
G=87
XOR=25
AGE_BEGIN=48
A=18
AS_LIST=65
B=84
C=53
L=52
LINE_COMMENT=74
M=56
STMT_SELECT=11
N=19
FCT=4
O=23
H=59
I=29
J=88
K=89
U=67
T=27
W=58
V=66
Q=86
P=85
AS_VALUE=68
S=50
R=24
LIST=7
TRUE=79
MUL=40
Y=69
PHRASE=83
X=22
AGE_END=49
Z=90
COLON=17
AGE=10
WS=72
NEWLINE=71
SPECIAL=82
AS_SCENE=64
NEG=9
OR=26
SQ=44
ASSIGN=31
GT=37
AS_DICT=70
DIV=41
FROM=57
END=16
FALSE=80
LE=34
STRING=75
RENAME=13

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>", 
    "FCT", "VAR", "VAL", "LIST", "POS", "NEG", "AGE", "STMT_SELECT", "STMT_UPDATE", 
    "RENAME", "DOT", "SEP", "END", "COLON", "A", "N", "D", "AND", "X", "O", 
    "R", "XOR", "OR", "T", "NOT", "I", "IN", "ASSIGN", "EQ", "NE", "LE", 
    "GE", "LT", "GT", "ADD", "SUB", "MUL", "DIV", "MOD", "POW", "SQ", "DQ", 
    "LIST_BEGIN", "LIST_END", "AGE_BEGIN", "AGE_END", "S", "E", "L", "C", 
    "SELECT", "F", "M", "FROM", "W", "H", "WHERE", "AS", "THIS", "TIME", 
    "AS_SCENE", "AS_LIST", "V", "U", "AS_VALUE", "Y", "AS_DICT", "NEWLINE", 
    "WS", "COMMENT", "LINE_COMMENT", "STRING", "DIGIT", "INTEGER", "FLOAT", 
    "TRUE", "FALSE", "CHARACTER", "SPECIAL", "PHRASE", "B", "P", "Q", "G", 
    "J", "K", "Z", "'('", "')'"
]




class SelectScript(TreeParser):
    grammarFileName = "SelectScript.g"
    antlr_version = version_str_to_tuple("3.1.3 Mar 18, 2009 10:09:25")
    antlr_version_str = "3.1.3 Mar 18, 2009 10:09:25"
    tokenNames = tokenNames

    def __init__(self, input, state=None, *args, **kwargs):
        if state is None:
            state = RecognizerSharedState()

        super(SelectScript, self).__init__(input, state, *args, **kwargs)

        self.dfa2 = self.DFA2(
            self, 2,
            eot = self.DFA2_eot,
            eof = self.DFA2_eof,
            min = self.DFA2_min,
            max = self.DFA2_max,
            accept = self.DFA2_accept,
            special = self.DFA2_special,
            transition = self.DFA2_transition
            )

        self.dfa15 = self.DFA15(
            self, 15,
            eot = self.DFA15_eot,
            eof = self.DFA15_eof,
            min = self.DFA15_min,
            max = self.DFA15_max,
            accept = self.DFA15_accept,
            special = self.DFA15_special,
            transition = self.DFA15_transition
            )






                


        

             

    fct_list = {'=' : 'assign', 'in' : 'in',
                'and' : 'and', 'not' : 'not',
                'xor' : 'xor', 'or'  : 'or',
                'lt'  : 'lt',  'le'  : 'le',
                'eq'  : 'eq',  'ne'  : 'ne',
                'ge'  : 'ge',  'gt'  : 'gt' }

    types = {'fct' :0,
             'var' :1,
             'list':2,
             'val' :3,
             'sel' :4,
             'this':5 }
             
    asTypes = {	'dict' :0,
    			'list' :1,
    			'scene':2,
    			'value':3}
    			
    def _fct(self, name, params):
    	return [self.types['fct'], name, params]

    def _var(self, var_name, age=0) :
    	return [self.types['var'], var_name, age]

    def _val(self, value) :
    	return [self.types['val'], value]
    	
    def _list(self, l) :
    	return [self.types['list'], l]
    	
    def _sel(self, s, f, w, a) :
    	return [self.types['sel'], s, f, w, a]
    	
    def _this(self, name='') :
    	return [self.types['this'], name]
    	
    def compile(self, source) :
    	char_stream = antlr3.ANTLRStringStream(source)
    	lexer = SelectExprLexer(char_stream)
    	tokens = antlr3.CommonTokenStream(lexer)
    	parser = SelectExprParser(tokens)
    	r = parser.eval()

    	# this is the root of the AST
    	root = r.tree

    	nodes = antlr3.tree.CommonTreeNodeStream(root)
    	nodes.setTokenStream(tokens)
    	self.__init__(nodes)
    	return self.eval()

    def prettyPrint(self, prog, depth=0):
    	treE = "   "*depth+unichr(9562)+unichr(9552)*2

    	if isinstance(prog[0], list):
    		for stmt in prog:
    			print stmt
    			self.prettyPrint( stmt, depth+1 )
    	
    	elif prog[0] == self.types['fct']:
    		print treE, "func: ", prog[1]
    		for param in prog[2]:
    				self.prettyPrint( param, depth+1 )
    	
    	elif prog[0] == self.types['val']:
    		print treE, "val: ", prog[1]
    		
    	elif prog[0] == self.types['this']:
    		print treE, "this"
    		
    	elif prog[0] == self.types['var']:
    		print treE, "var: ", prog[1]
    		print treE, "age: "
    		treE = "   "*depth+unichr(9568)+unichr(9552)*2
    		self.prettyPrint( prog[2], depth+1 )
    		
    	elif prog[0] == self.types['list']:
    		print treE,"list: ", prog[1]
    		
    	elif prog[0] == self.types['sel']:
    		treE = "   "*depth+unichr(9568)+unichr(9552)*2
    	
    		print treE, 'select: '
    		self.prettyPrint( prog[1], depth+1 )
    		
    		print treE, 'from: '
    		self.prettyPrint( prog[2], depth+1 )
    		
    		print treE, 'where: '
    		self.prettyPrint( prog[3], depth+1 )
    		
    		treE = "   "*depth+unichr(9562)+unichr(9552)*2
    		print treE, 'as: '
    		self.prettyPrint( prog[4], depth+1 )
    		
    	else:
    		print ""



    # $ANTLR start "eval"
    # SelectScript.g:142:1: eval returns [stmt_list] : p= prog ;
    def eval(self, ):

        stmt_list = None

        p = None


        try:
            try:
                # SelectScript.g:142:25: (p= prog )
                # SelectScript.g:143:5: p= prog
                pass 
                self._state.following.append(self.FOLLOW_prog_in_eval83)
                p = self.prog()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    stmt_list = p





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return stmt_list

    # $ANTLR end "eval"


    # $ANTLR start "prog"
    # SelectScript.g:146:1: prog returns [stmt_list] : (stmt= statement )+ ;
    def prog(self, ):

        stmt_list = None

        stmt = None


        stmt_list = []
        try:
            try:
                # SelectScript.g:147:22: ( (stmt= statement )+ )
                # SelectScript.g:148:2: (stmt= statement )+
                pass 
                # SelectScript.g:148:2: (stmt= statement )+
                cnt1 = 0
                while True: #loop1
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if ((FCT <= LA1_0 <= NEG) or LA1_0 == STMT_SELECT or LA1_0 == AND or (XOR <= LA1_0 <= OR) or LA1_0 == NOT or (IN <= LA1_0 <= POW) or LA1_0 == THIS or LA1_0 == 91) :
                        alt1 = 1


                    if alt1 == 1:
                        # SelectScript.g:148:3: stmt= statement
                        pass 
                        self._state.following.append(self.FOLLOW_statement_in_prog105)
                        stmt = self.statement()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            stmt_list.append( stmt )



                    else:
                        if cnt1 >= 1:
                            break #loop1

                        if self._state.backtracking > 0:
                            raise BacktrackingFailed

                        eee = EarlyExitException(1, self.input)
                        raise eee

                    cnt1 += 1




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return stmt_list

    # $ANTLR end "prog"


    # $ANTLR start "statement"
    # SelectScript.g:151:1: statement returns [stmt] : (s= statement_select | e= expr );
    def statement(self, ):

        stmt = None

        s = None

        e = None


        try:
            try:
                # SelectScript.g:151:25: (s= statement_select | e= expr )
                alt2 = 2
                alt2 = self.dfa2.predict(self.input)
                if alt2 == 1:
                    # SelectScript.g:152:2: s= statement_select
                    pass 
                    self._state.following.append(self.FOLLOW_statement_select_in_statement126)
                    s = self.statement_select()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stmt = s



                elif alt2 == 2:
                    # SelectScript.g:153:4: e= expr
                    pass 
                    self._state.following.append(self.FOLLOW_expr_in_statement136)
                    e = self.expr()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stmt = e




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return stmt

    # $ANTLR end "statement"


    # $ANTLR start "statement_select"
    # SelectScript.g:156:1: statement_select returns [selection] : ^( STMT_SELECT s= select_ f= from_ (w= where_ )? (a= as_ )? ) ;
    def statement_select(self, ):

        selection = None

        s = None

        f = None

        w = None

        a = None


        s=[]; f=[]; w=[]; a=self._val(self.asTypes['dict']); 
        try:
            try:
                # SelectScript.g:159:1: ( ^( STMT_SELECT s= select_ f= from_ (w= where_ )? (a= as_ )? ) )
                # SelectScript.g:160:2: ^( STMT_SELECT s= select_ f= from_ (w= where_ )? (a= as_ )? )
                pass 
                self.match(self.input, STMT_SELECT, self.FOLLOW_STMT_SELECT_in_statement_select166)

                self.match(self.input, DOWN, None)
                self._state.following.append(self.FOLLOW_select__in_statement_select170)
                s = self.select_()

                self._state.following.pop()
                self._state.following.append(self.FOLLOW_from__in_statement_select174)
                f = self.from_()

                self._state.following.pop()
                # SelectScript.g:160:34: (w= where_ )?
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if (LA3_0 == WHERE) :
                    alt3 = 1
                if alt3 == 1:
                    # SelectScript.g:160:36: w= where_
                    pass 
                    self._state.following.append(self.FOLLOW_where__in_statement_select180)
                    w = self.where_()

                    self._state.following.pop()



                # SelectScript.g:160:48: (a= as_ )?
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if (LA4_0 == AS) :
                    alt4 = 1
                if alt4 == 1:
                    # SelectScript.g:160:50: a= as_
                    pass 
                    self._state.following.append(self.FOLLOW_as__in_statement_select189)
                    a = self.as_()

                    self._state.following.pop()




                self.match(self.input, UP, None)



                if self._state.backtracking == 0:
                    selection = self._sel(s, f, w, a); 


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return selection

    # $ANTLR end "statement_select"


    # $ANTLR start "select_"
    # SelectScript.g:163:1: select_ returns [types] : ^( SELECT (type= PHRASE | f= function | t= this_ )* ) ;
    def select_(self, ):

        types = None

        type = None
        f = None

        t = None


        types = []
        try:
            try:
                # SelectScript.g:164:19: ( ^( SELECT (type= PHRASE | f= function | t= this_ )* ) )
                # SelectScript.g:165:2: ^( SELECT (type= PHRASE | f= function | t= this_ )* )
                pass 
                self.match(self.input, SELECT, self.FOLLOW_SELECT_in_select_213)

                if self.input.LA(1) == DOWN:
                    self.match(self.input, DOWN, None)
                    # SelectScript.g:166:3: (type= PHRASE | f= function | t= this_ )*
                    while True: #loop5
                        alt5 = 4
                        LA5 = self.input.LA(1)
                        if LA5 == PHRASE:
                            alt5 = 1
                        elif LA5 == FCT:
                            alt5 = 2
                        elif LA5 == THIS:
                            alt5 = 3

                        if alt5 == 1:
                            # SelectScript.g:167:3: type= PHRASE
                            pass 
                            type=self.match(self.input, PHRASE, self.FOLLOW_PHRASE_in_select_224)
                            if self._state.backtracking == 0:
                                types.append( self._fct (type.getText(),  [self._this()] ) ); 



                        elif alt5 == 2:
                            # SelectScript.g:168:5: f= function
                            pass 
                            self._state.following.append(self.FOLLOW_function_in_select_236)
                            f = self.function()

                            self._state.following.pop()
                            if self._state.backtracking == 0:
                                types.append( f ); 



                        elif alt5 == 3:
                            # SelectScript.g:169:5: t= this_
                            pass 
                            self._state.following.append(self.FOLLOW_this__in_select_248)
                            t = self.this_()

                            self._state.following.pop()
                            if self._state.backtracking == 0:
                                types.append( t ); 



                        else:
                            break #loop5

                    self.match(self.input, UP, None)





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return types

    # $ANTLR end "select_"


    # $ANTLR start "from_"
    # SelectScript.g:174:1: from_ returns [env] : ^( FROM (e= expr )+ ) ;
    def from_(self, ):

        env = None

        e = None


        env=[]; 
        try:
            try:
                # SelectScript.g:175:17: ( ^( FROM (e= expr )+ ) )
                # SelectScript.g:176:2: ^( FROM (e= expr )+ )
                pass 
                self.match(self.input, FROM, self.FOLLOW_FROM_in_from_278)

                self.match(self.input, DOWN, None)
                # SelectScript.g:176:9: (e= expr )+
                cnt6 = 0
                while True: #loop6
                    alt6 = 2
                    LA6_0 = self.input.LA(1)

                    if ((FCT <= LA6_0 <= NEG) or LA6_0 == STMT_SELECT or LA6_0 == AND or (XOR <= LA6_0 <= OR) or LA6_0 == NOT or (IN <= LA6_0 <= POW) or LA6_0 == THIS or LA6_0 == 91) :
                        alt6 = 1


                    if alt6 == 1:
                        # SelectScript.g:176:10: e= expr
                        pass 
                        self._state.following.append(self.FOLLOW_expr_in_from_283)
                        e = self.expr()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            env.append(e); 



                    else:
                        if cnt6 >= 1:
                            break #loop6

                        if self._state.backtracking > 0:
                            raise BacktrackingFailed

                        eee = EarlyExitException(6, self.input)
                        raise eee

                    cnt6 += 1

                self.match(self.input, UP, None)




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return env

    # $ANTLR end "from_"


    # $ANTLR start "as_"
    # SelectScript.g:179:1: as_ returns [rep] : ( ^( AS AS_DICT ) | ^( AS AS_LIST ) | ^( AS AS_SCENE ) | ^( AS AS_VALUE ) | ^( AS v= PHRASE ) );
    def as_(self, ):

        rep = None

        v = None

        try:
            try:
                # SelectScript.g:179:19: ( ^( AS AS_DICT ) | ^( AS AS_LIST ) | ^( AS AS_SCENE ) | ^( AS AS_VALUE ) | ^( AS v= PHRASE ) )
                alt7 = 5
                LA7_0 = self.input.LA(1)

                if (LA7_0 == AS) :
                    LA7_1 = self.input.LA(2)

                    if (LA7_1 == 2) :
                        LA7 = self.input.LA(3)
                        if LA7 == AS_DICT:
                            alt7 = 1
                        elif LA7 == AS_LIST:
                            alt7 = 2
                        elif LA7 == AS_SCENE:
                            alt7 = 3
                        elif LA7 == AS_VALUE:
                            alt7 = 4
                        elif LA7 == PHRASE:
                            alt7 = 5
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed

                            nvae = NoViableAltException("", 7, 2, self.input)

                            raise nvae

                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed

                        nvae = NoViableAltException("", 7, 1, self.input)

                        raise nvae

                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed

                    nvae = NoViableAltException("", 7, 0, self.input)

                    raise nvae

                if alt7 == 1:
                    # SelectScript.g:180:2: ^( AS AS_DICT )
                    pass 
                    self.match(self.input, AS, self.FOLLOW_AS_in_as_303)

                    self.match(self.input, DOWN, None)
                    self.match(self.input, AS_DICT, self.FOLLOW_AS_DICT_in_as_305)

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        rep= self._val(self.asTypes['dict']);  



                elif alt7 == 2:
                    # SelectScript.g:181:4: ^( AS AS_LIST )
                    pass 
                    self.match(self.input, AS, self.FOLLOW_AS_in_as_315)

                    self.match(self.input, DOWN, None)
                    self.match(self.input, AS_LIST, self.FOLLOW_AS_LIST_in_as_317)

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        rep= self._val(self.asTypes['list']);  



                elif alt7 == 3:
                    # SelectScript.g:182:4: ^( AS AS_SCENE )
                    pass 
                    self.match(self.input, AS, self.FOLLOW_AS_in_as_327)

                    self.match(self.input, DOWN, None)
                    self.match(self.input, AS_SCENE, self.FOLLOW_AS_SCENE_in_as_329)

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        rep= self._val(self.asTypes['scene']); 



                elif alt7 == 4:
                    # SelectScript.g:183:4: ^( AS AS_VALUE )
                    pass 
                    self.match(self.input, AS, self.FOLLOW_AS_in_as_338)

                    self.match(self.input, DOWN, None)
                    self.match(self.input, AS_VALUE, self.FOLLOW_AS_VALUE_in_as_340)

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        rep= self._val(self.asTypes['value']); 



                elif alt7 == 5:
                    # SelectScript.g:184:4: ^( AS v= PHRASE )
                    pass 
                    self.match(self.input, AS, self.FOLLOW_AS_in_as_350)

                    self.match(self.input, DOWN, None)
                    v=self.match(self.input, PHRASE, self.FOLLOW_PHRASE_in_as_354)

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        rep= self._val(v.getText()); 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return rep

    # $ANTLR end "as_"


    # $ANTLR start "where_"
    # SelectScript.g:187:1: where_ returns [stack] : ^( WHERE e= expr ) ;
    def where_(self, ):

        stack = None

        e = None


        try:
            try:
                # SelectScript.g:187:24: ( ^( WHERE e= expr ) )
                # SelectScript.g:188:2: ^( WHERE e= expr )
                pass 
                self.match(self.input, WHERE, self.FOLLOW_WHERE_in_where_373)

                self.match(self.input, DOWN, None)
                self._state.following.append(self.FOLLOW_expr_in_where_377)
                e = self.expr()

                self._state.following.pop()

                self.match(self.input, UP, None)
                if self._state.backtracking == 0:
                    stack=e 





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return stack

    # $ANTLR end "where_"


    # $ANTLR start "expr"
    # SelectScript.g:191:1: expr returns [val] : (a= assign_expr | l= logic_expr | c= compare_expr | a= arithmetic_expr | a= atom );
    def expr(self, ):

        val = None

        a = None

        l = None

        c = None


        try:
            try:
                # SelectScript.g:191:20: (a= assign_expr | l= logic_expr | c= compare_expr | a= arithmetic_expr | a= atom )
                alt8 = 5
                LA8 = self.input.LA(1)
                if LA8 == ASSIGN:
                    alt8 = 1
                elif LA8 == AND or LA8 == XOR or LA8 == OR or LA8 == NOT:
                    alt8 = 2
                elif LA8 == IN or LA8 == EQ or LA8 == NE or LA8 == LE or LA8 == GE or LA8 == LT or LA8 == GT:
                    alt8 = 3
                elif LA8 == POS or LA8 == NEG or LA8 == ADD or LA8 == SUB or LA8 == MUL or LA8 == DIV or LA8 == MOD or LA8 == POW:
                    alt8 = 4
                elif LA8 == FCT or LA8 == VAR or LA8 == VAL or LA8 == LIST or LA8 == STMT_SELECT or LA8 == THIS or LA8 == 91:
                    alt8 = 5
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed

                    nvae = NoViableAltException("", 8, 0, self.input)

                    raise nvae

                if alt8 == 1:
                    # SelectScript.g:192:2: a= assign_expr
                    pass 
                    self._state.following.append(self.FOLLOW_assign_expr_in_expr399)
                    a = self.assign_expr()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        val = a;



                elif alt8 == 2:
                    # SelectScript.g:193:4: l= logic_expr
                    pass 
                    self._state.following.append(self.FOLLOW_logic_expr_in_expr412)
                    l = self.logic_expr()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        val = l;



                elif alt8 == 3:
                    # SelectScript.g:194:4: c= compare_expr
                    pass 
                    self._state.following.append(self.FOLLOW_compare_expr_in_expr424)
                    c = self.compare_expr()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        val = c;



                elif alt8 == 4:
                    # SelectScript.g:195:4: a= arithmetic_expr
                    pass 
                    self._state.following.append(self.FOLLOW_arithmetic_expr_in_expr435)
                    a = self.arithmetic_expr()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        val = a;



                elif alt8 == 5:
                    # SelectScript.g:196:4: a= atom
                    pass 
                    self._state.following.append(self.FOLLOW_atom_in_expr445)
                    a = self.atom()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        val = a;




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return val

    # $ANTLR end "expr"


    # $ANTLR start "age"
    # SelectScript.g:199:1: age returns [a] : ^( AGE (t= expr )? ) ;
    def age(self, ):

        a = None

        t = None


        a=self._val(0); 
        try:
            try:
                # SelectScript.g:200:25: ( ^( AGE (t= expr )? ) )
                # SelectScript.g:201:2: ^( AGE (t= expr )? )
                pass 
                self.match(self.input, AGE, self.FOLLOW_AGE_in_age469)

                if self.input.LA(1) == DOWN:
                    self.match(self.input, DOWN, None)
                    # SelectScript.g:201:8: (t= expr )?
                    alt9 = 2
                    LA9_0 = self.input.LA(1)

                    if ((FCT <= LA9_0 <= NEG) or LA9_0 == STMT_SELECT or LA9_0 == AND or (XOR <= LA9_0 <= OR) or LA9_0 == NOT or (IN <= LA9_0 <= POW) or LA9_0 == THIS or LA9_0 == 91) :
                        alt9 = 1
                    if alt9 == 1:
                        # SelectScript.g:201:9: t= expr
                        pass 
                        self._state.following.append(self.FOLLOW_expr_in_age474)
                        t = self.expr()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            a=t; 





                    self.match(self.input, UP, None)





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return a

    # $ANTLR end "age"


    # $ANTLR start "assign_expr"
    # SelectScript.g:215:1: assign_expr returns [stack] : ^( ASSIGN v= PHRASE e= expr (a= age )? ) ;
    def assign_expr(self, ):

        stack = None

        v = None
        e = None

        a = None


        a = self._val(0); 
        try:
            try:
                # SelectScript.g:216:27: ( ^( ASSIGN v= PHRASE e= expr (a= age )? ) )
                # SelectScript.g:217:2: ^( ASSIGN v= PHRASE e= expr (a= age )? )
                pass 
                self.match(self.input, ASSIGN, self.FOLLOW_ASSIGN_in_assign_expr509)

                self.match(self.input, DOWN, None)
                v=self.match(self.input, PHRASE, self.FOLLOW_PHRASE_in_assign_expr513)
                self._state.following.append(self.FOLLOW_expr_in_assign_expr517)
                e = self.expr()

                self._state.following.pop()
                # SelectScript.g:217:27: (a= age )?
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == AGE) :
                    alt10 = 1
                if alt10 == 1:
                    # SelectScript.g:217:28: a= age
                    pass 
                    self._state.following.append(self.FOLLOW_age_in_assign_expr522)
                    a = self.age()

                    self._state.following.pop()




                self.match(self.input, UP, None)
                if self._state.backtracking == 0:
                    stack = self._fct( 'assign', [ self._val(v.getText()) , e, a]); 





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return stack

    # $ANTLR end "assign_expr"


    # $ANTLR start "logic_expr"
    # SelectScript.g:220:1: logic_expr returns [stack] : ( ^( OR e1= expr e2= expr ) | ^( XOR e1= expr e2= expr ) | ^( AND e1= expr e2= expr ) | ^( NOT e= expr ) );
    def logic_expr(self, ):

        stack = None

        e1 = None

        e2 = None

        e = None


        try:
            try:
                # SelectScript.g:220:28: ( ^( OR e1= expr e2= expr ) | ^( XOR e1= expr e2= expr ) | ^( AND e1= expr e2= expr ) | ^( NOT e= expr ) )
                alt11 = 4
                LA11 = self.input.LA(1)
                if LA11 == OR:
                    alt11 = 1
                elif LA11 == XOR:
                    alt11 = 2
                elif LA11 == AND:
                    alt11 = 3
                elif LA11 == NOT:
                    alt11 = 4
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed

                    nvae = NoViableAltException("", 11, 0, self.input)

                    raise nvae

                if alt11 == 1:
                    # SelectScript.g:221:2: ^( OR e1= expr e2= expr )
                    pass 
                    self.match(self.input, OR, self.FOLLOW_OR_in_logic_expr543)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_logic_expr547)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_logic_expr551)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('or',  [e1, e2]); 



                elif alt11 == 2:
                    # SelectScript.g:222:4: ^( XOR e1= expr e2= expr )
                    pass 
                    self.match(self.input, XOR, self.FOLLOW_XOR_in_logic_expr561)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_logic_expr565)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_logic_expr569)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('xor', [e1, e2]); 



                elif alt11 == 3:
                    # SelectScript.g:223:4: ^( AND e1= expr e2= expr )
                    pass 
                    self.match(self.input, AND, self.FOLLOW_AND_in_logic_expr580)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_logic_expr584)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_logic_expr588)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('and', [e1, e2]); 



                elif alt11 == 4:
                    # SelectScript.g:224:4: ^( NOT e= expr )
                    pass 
                    self.match(self.input, NOT, self.FOLLOW_NOT_in_logic_expr598)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_logic_expr602)
                    e = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('not', [e] ); 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return stack

    # $ANTLR end "logic_expr"


    # $ANTLR start "compare_expr"
    # SelectScript.g:227:1: compare_expr returns [stack] : ( ^( IN e1= expr e2= expr ) | ^( EQ e1= expr e2= expr ) | ^( NE e1= expr e2= expr ) | ^( GE e1= expr e2= expr ) | ^( GT e1= expr e2= expr ) | ^( LE e1= expr e2= expr ) | ^( LT e1= expr e2= expr ) );
    def compare_expr(self, ):

        stack = None

        e1 = None

        e2 = None


        try:
            try:
                # SelectScript.g:227:29: ( ^( IN e1= expr e2= expr ) | ^( EQ e1= expr e2= expr ) | ^( NE e1= expr e2= expr ) | ^( GE e1= expr e2= expr ) | ^( GT e1= expr e2= expr ) | ^( LE e1= expr e2= expr ) | ^( LT e1= expr e2= expr ) )
                alt12 = 7
                LA12 = self.input.LA(1)
                if LA12 == IN:
                    alt12 = 1
                elif LA12 == EQ:
                    alt12 = 2
                elif LA12 == NE:
                    alt12 = 3
                elif LA12 == GE:
                    alt12 = 4
                elif LA12 == GT:
                    alt12 = 5
                elif LA12 == LE:
                    alt12 = 6
                elif LA12 == LT:
                    alt12 = 7
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed

                    nvae = NoViableAltException("", 12, 0, self.input)

                    raise nvae

                if alt12 == 1:
                    # SelectScript.g:228:2: ^( IN e1= expr e2= expr )
                    pass 
                    self.match(self.input, IN, self.FOLLOW_IN_in_compare_expr623)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr627)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr631)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('in', [e1, e2]); 



                elif alt12 == 2:
                    # SelectScript.g:229:4: ^( EQ e1= expr e2= expr )
                    pass 
                    self.match(self.input, EQ, self.FOLLOW_EQ_in_compare_expr640)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr644)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr648)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('eq', [e1, e2]); 



                elif alt12 == 3:
                    # SelectScript.g:230:4: ^( NE e1= expr e2= expr )
                    pass 
                    self.match(self.input, NE, self.FOLLOW_NE_in_compare_expr657)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr661)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr665)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('ne', [e1, e2]); 



                elif alt12 == 4:
                    # SelectScript.g:231:4: ^( GE e1= expr e2= expr )
                    pass 
                    self.match(self.input, GE, self.FOLLOW_GE_in_compare_expr674)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr678)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr682)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('ge', [e1, e2]); 



                elif alt12 == 5:
                    # SelectScript.g:232:4: ^( GT e1= expr e2= expr )
                    pass 
                    self.match(self.input, GT, self.FOLLOW_GT_in_compare_expr691)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr695)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr699)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('gt', [e1, e2]); 



                elif alt12 == 6:
                    # SelectScript.g:233:4: ^( LE e1= expr e2= expr )
                    pass 
                    self.match(self.input, LE, self.FOLLOW_LE_in_compare_expr708)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr712)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr716)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('le', [e1, e2]); 



                elif alt12 == 7:
                    # SelectScript.g:234:4: ^( LT e1= expr e2= expr )
                    pass 
                    self.match(self.input, LT, self.FOLLOW_LT_in_compare_expr725)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr729)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_compare_expr733)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('lt', [e1, e2]); 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return stack

    # $ANTLR end "compare_expr"


    # $ANTLR start "arithmetic_expr"
    # SelectScript.g:237:1: arithmetic_expr returns [stack] : ( ^( MUL e1= expr e2= expr ) | ^( DIV e1= expr e2= expr ) | ^( MOD e1= expr e2= expr ) | ^( SUB e1= expr e2= expr ) | ^( ADD e1= expr e2= expr ) | ^( POW e1= expr e2= expr ) | ^( NEG e= expr ) | ^( POS e= expr ) );
    def arithmetic_expr(self, ):

        stack = None

        e1 = None

        e2 = None

        e = None


        try:
            try:
                # SelectScript.g:237:32: ( ^( MUL e1= expr e2= expr ) | ^( DIV e1= expr e2= expr ) | ^( MOD e1= expr e2= expr ) | ^( SUB e1= expr e2= expr ) | ^( ADD e1= expr e2= expr ) | ^( POW e1= expr e2= expr ) | ^( NEG e= expr ) | ^( POS e= expr ) )
                alt13 = 8
                LA13 = self.input.LA(1)
                if LA13 == MUL:
                    alt13 = 1
                elif LA13 == DIV:
                    alt13 = 2
                elif LA13 == MOD:
                    alt13 = 3
                elif LA13 == SUB:
                    alt13 = 4
                elif LA13 == ADD:
                    alt13 = 5
                elif LA13 == POW:
                    alt13 = 6
                elif LA13 == NEG:
                    alt13 = 7
                elif LA13 == POS:
                    alt13 = 8
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed

                    nvae = NoViableAltException("", 13, 0, self.input)

                    raise nvae

                if alt13 == 1:
                    # SelectScript.g:238:2: ^( MUL e1= expr e2= expr )
                    pass 
                    self.match(self.input, MUL, self.FOLLOW_MUL_in_arithmetic_expr751)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr755)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr759)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('mul', [e1, e2]); 



                elif alt13 == 2:
                    # SelectScript.g:239:3: ^( DIV e1= expr e2= expr )
                    pass 
                    self.match(self.input, DIV, self.FOLLOW_DIV_in_arithmetic_expr767)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr771)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr775)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('div', [e1, e2]); 



                elif alt13 == 3:
                    # SelectScript.g:240:3: ^( MOD e1= expr e2= expr )
                    pass 
                    self.match(self.input, MOD, self.FOLLOW_MOD_in_arithmetic_expr783)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr787)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr791)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('mod', [e1, e2]); 



                elif alt13 == 4:
                    # SelectScript.g:241:3: ^( SUB e1= expr e2= expr )
                    pass 
                    self.match(self.input, SUB, self.FOLLOW_SUB_in_arithmetic_expr799)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr803)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr807)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('sub', [e1, e2]); 



                elif alt13 == 5:
                    # SelectScript.g:242:3: ^( ADD e1= expr e2= expr )
                    pass 
                    self.match(self.input, ADD, self.FOLLOW_ADD_in_arithmetic_expr815)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr819)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr823)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('add', [e1, e2]); 



                elif alt13 == 6:
                    # SelectScript.g:243:3: ^( POW e1= expr e2= expr )
                    pass 
                    self.match(self.input, POW, self.FOLLOW_POW_in_arithmetic_expr831)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr835)
                    e1 = self.expr()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr839)
                    e2 = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('pow', [e1, e2]); 



                elif alt13 == 7:
                    # SelectScript.g:244:3: ^( NEG e= expr )
                    pass 
                    self.match(self.input, NEG, self.FOLLOW_NEG_in_arithmetic_expr847)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr851)
                    e = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('neg', [e]); 



                elif alt13 == 8:
                    # SelectScript.g:245:3: ^( POS e= expr )
                    pass 
                    self.match(self.input, POS, self.FOLLOW_POS_in_arithmetic_expr861)

                    self.match(self.input, DOWN, None)
                    self._state.following.append(self.FOLLOW_expr_in_arithmetic_expr865)
                    e = self.expr()

                    self._state.following.pop()

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        stack = self._fct('pos', [e]); 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return stack

    # $ANTLR end "arithmetic_expr"


    # $ANTLR start "atom"
    # SelectScript.g:248:1: atom returns [stack] : (val= value | var= variable | fct= function | '(' e= expr ')' | s= statement_select );
    def atom(self, ):

        stack = None

        val = None

        var = None

        fct = None

        e = None

        s = None


        try:
            try:
                # SelectScript.g:248:22: (val= value | var= variable | fct= function | '(' e= expr ')' | s= statement_select )
                alt14 = 5
                LA14 = self.input.LA(1)
                if LA14 == VAL or LA14 == LIST or LA14 == THIS:
                    alt14 = 1
                elif LA14 == VAR:
                    alt14 = 2
                elif LA14 == FCT:
                    alt14 = 3
                elif LA14 == 91:
                    alt14 = 4
                elif LA14 == STMT_SELECT:
                    alt14 = 5
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed

                    nvae = NoViableAltException("", 14, 0, self.input)

                    raise nvae

                if alt14 == 1:
                    # SelectScript.g:249:2: val= value
                    pass 
                    self._state.following.append(self.FOLLOW_value_in_atom888)
                    val = self.value()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stack = val



                elif alt14 == 2:
                    # SelectScript.g:250:4: var= variable
                    pass 
                    self._state.following.append(self.FOLLOW_variable_in_atom903)
                    var = self.variable()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stack = var



                elif alt14 == 3:
                    # SelectScript.g:251:4: fct= function
                    pass 
                    self._state.following.append(self.FOLLOW_function_in_atom916)
                    fct = self.function()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stack = fct



                elif alt14 == 4:
                    # SelectScript.g:252:4: '(' e= expr ')'
                    pass 
                    self.match(self.input, 91, self.FOLLOW_91_in_atom925)
                    self._state.following.append(self.FOLLOW_expr_in_atom929)
                    e = self.expr()

                    self._state.following.pop()
                    self.match(self.input, 92, self.FOLLOW_92_in_atom931)
                    if self._state.backtracking == 0:
                        stack = e  



                elif alt14 == 5:
                    # SelectScript.g:253:4: s= statement_select
                    pass 
                    self._state.following.append(self.FOLLOW_statement_select_in_atom942)
                    s = self.statement_select()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stack = s  




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return stack

    # $ANTLR end "atom"


    # $ANTLR start "value"
    # SelectScript.g:256:1: value returns [val] : ( ^( VAL STRING ) | ^( VAL INTEGER ) | ^( VAL FLOAT ) | ^( VAL TRUE ) | ^( VAL FALSE ) | t= this_ | l= list_ );
    def value(self, ):

        val = None

        STRING1 = None
        INTEGER2 = None
        FLOAT3 = None
        t = None

        l = None


        try:
            try:
                # SelectScript.g:256:21: ( ^( VAL STRING ) | ^( VAL INTEGER ) | ^( VAL FLOAT ) | ^( VAL TRUE ) | ^( VAL FALSE ) | t= this_ | l= list_ )
                alt15 = 7
                alt15 = self.dfa15.predict(self.input)
                if alt15 == 1:
                    # SelectScript.g:257:4: ^( VAL STRING )
                    pass 
                    self.match(self.input, VAL, self.FOLLOW_VAL_in_value962)

                    self.match(self.input, DOWN, None)
                    STRING1=self.match(self.input, STRING, self.FOLLOW_STRING_in_value964)

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        val= self._val( STRING1.getText()[1:-1] ); 



                elif alt15 == 2:
                    # SelectScript.g:258:4: ^( VAL INTEGER )
                    pass 
                    self.match(self.input, VAL, self.FOLLOW_VAL_in_value974)

                    self.match(self.input, DOWN, None)
                    INTEGER2=self.match(self.input, INTEGER, self.FOLLOW_INTEGER_in_value976)

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        val= self._val( int(INTEGER2.getText()) ); 



                elif alt15 == 3:
                    # SelectScript.g:259:4: ^( VAL FLOAT )
                    pass 
                    self.match(self.input, VAL, self.FOLLOW_VAL_in_value987)

                    self.match(self.input, DOWN, None)
                    FLOAT3=self.match(self.input, FLOAT, self.FOLLOW_FLOAT_in_value989)

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        val= self._val( float(FLOAT3.getText()) ); 



                elif alt15 == 4:
                    # SelectScript.g:260:4: ^( VAL TRUE )
                    pass 
                    self.match(self.input, VAL, self.FOLLOW_VAL_in_value999)

                    self.match(self.input, DOWN, None)
                    self.match(self.input, TRUE, self.FOLLOW_TRUE_in_value1001)

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        val= self._val( True  ); 



                elif alt15 == 5:
                    # SelectScript.g:261:4: ^( VAL FALSE )
                    pass 
                    self.match(self.input, VAL, self.FOLLOW_VAL_in_value1011)

                    self.match(self.input, DOWN, None)
                    self.match(self.input, FALSE, self.FOLLOW_FALSE_in_value1013)

                    self.match(self.input, UP, None)
                    if self._state.backtracking == 0:
                        val= self._val( False ); 



                elif alt15 == 6:
                    # SelectScript.g:262:4: t= this_
                    pass 
                    self._state.following.append(self.FOLLOW_this__in_value1024)
                    t = self.this_()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        val=t; 



                elif alt15 == 7:
                    # SelectScript.g:263:4: l= list_
                    pass 
                    self._state.following.append(self.FOLLOW_list__in_value1035)
                    l = self.list_()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        val= self._list(l ) ; 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return val

    # $ANTLR end "value"


    # $ANTLR start "this_"
    # SelectScript.g:266:1: this_ returns [p] : ^( THIS ( PHRASE )? ) ;
    def this_(self, ):

        p = None

        PHRASE4 = None

        p=self._this(); 
        try:
            try:
                # SelectScript.g:267:26: ( ^( THIS ( PHRASE )? ) )
                # SelectScript.g:268:2: ^( THIS ( PHRASE )? )
                pass 
                self.match(self.input, THIS, self.FOLLOW_THIS_in_this_1059)

                if self.input.LA(1) == DOWN:
                    self.match(self.input, DOWN, None)
                    # SelectScript.g:268:9: ( PHRASE )?
                    alt16 = 2
                    LA16_0 = self.input.LA(1)

                    if (LA16_0 == PHRASE) :
                        alt16 = 1
                    if alt16 == 1:
                        # SelectScript.g:268:10: PHRASE
                        pass 
                        PHRASE4=self.match(self.input, PHRASE, self.FOLLOW_PHRASE_in_this_1062)
                        if self._state.backtracking == 0:
                            p=self._this(PHRASE4.getText()); 





                    self.match(self.input, UP, None)





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return p

    # $ANTLR end "this_"


    # $ANTLR start "list_"
    # SelectScript.g:271:1: list_ returns [l] : ^( LIST (e= expr )* ) ;
    def list_(self, ):

        l = None

        e = None


        l = [] 
        try:
            try:
                # SelectScript.g:272:17: ( ^( LIST (e= expr )* ) )
                # SelectScript.g:273:2: ^( LIST (e= expr )* )
                pass 
                self.match(self.input, LIST, self.FOLLOW_LIST_in_list_1086)

                if self.input.LA(1) == DOWN:
                    self.match(self.input, DOWN, None)
                    # SelectScript.g:273:9: (e= expr )*
                    while True: #loop17
                        alt17 = 2
                        LA17_0 = self.input.LA(1)

                        if ((FCT <= LA17_0 <= NEG) or LA17_0 == STMT_SELECT or LA17_0 == AND or (XOR <= LA17_0 <= OR) or LA17_0 == NOT or (IN <= LA17_0 <= POW) or LA17_0 == THIS or LA17_0 == 91) :
                            alt17 = 1


                        if alt17 == 1:
                            # SelectScript.g:273:11: e= expr
                            pass 
                            self._state.following.append(self.FOLLOW_expr_in_list_1092)
                            e = self.expr()

                            self._state.following.pop()
                            if self._state.backtracking == 0:
                                l.append(e); 



                        else:
                            break #loop17

                    self.match(self.input, UP, None)





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return l

    # $ANTLR end "list_"


    # $ANTLR start "variable"
    # SelectScript.g:276:1: variable returns [var] : ^( VAR PHRASE (a= age )? ) ;
    def variable(self, ):

        var = None

        PHRASE5 = None
        a = None


        a = self._val(0); 
        try:
            try:
                # SelectScript.g:277:27: ( ^( VAR PHRASE (a= age )? ) )
                # SelectScript.g:278:2: ^( VAR PHRASE (a= age )? )
                pass 
                self.match(self.input, VAR, self.FOLLOW_VAR_in_variable1116)

                self.match(self.input, DOWN, None)
                PHRASE5=self.match(self.input, PHRASE, self.FOLLOW_PHRASE_in_variable1118)
                # SelectScript.g:278:15: (a= age )?
                alt18 = 2
                LA18_0 = self.input.LA(1)

                if (LA18_0 == AGE) :
                    alt18 = 1
                if alt18 == 1:
                    # SelectScript.g:278:16: a= age
                    pass 
                    self._state.following.append(self.FOLLOW_age_in_variable1123)
                    a = self.age()

                    self._state.following.pop()




                self.match(self.input, UP, None)
                if self._state.backtracking == 0:
                    var = self._var( PHRASE5.getText(), a ); 





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return var

    # $ANTLR end "variable"


    # $ANTLR start "function"
    # SelectScript.g:281:1: function returns [stack] : ^( FCT PHRASE (params= parameter )? ) ;
    def function(self, ):

        stack = None

        PHRASE6 = None
        params = None


        try:
            try:
                # SelectScript.g:281:26: ( ^( FCT PHRASE (params= parameter )? ) )
                # SelectScript.g:282:2: ^( FCT PHRASE (params= parameter )? )
                pass 
                self.match(self.input, FCT, self.FOLLOW_FCT_in_function1143)

                self.match(self.input, DOWN, None)
                PHRASE6=self.match(self.input, PHRASE, self.FOLLOW_PHRASE_in_function1145)
                # SelectScript.g:282:21: (params= parameter )?
                alt19 = 2
                LA19_0 = self.input.LA(1)

                if ((FCT <= LA19_0 <= NEG) or LA19_0 == STMT_SELECT or LA19_0 == AND or (XOR <= LA19_0 <= OR) or LA19_0 == NOT or (IN <= LA19_0 <= POW) or LA19_0 == THIS or LA19_0 == 91) :
                    alt19 = 1
                elif (LA19_0 == 3) :
                    LA19_2 = self.input.LA(2)

                    if (self.synpred48_SelectScript()) :
                        alt19 = 1
                if alt19 == 1:
                    # SelectScript.g:0:0: params= parameter
                    pass 
                    self._state.following.append(self.FOLLOW_parameter_in_function1149)
                    params = self.parameter()

                    self._state.following.pop()




                self.match(self.input, UP, None)
                if self._state.backtracking == 0:
                    stack = self._fct( PHRASE6.getText(), params); 





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return stack

    # $ANTLR end "function"


    # $ANTLR start "parameter"
    # SelectScript.g:286:1: parameter returns [stack] : (e= expr )* ;
    def parameter(self, ):

        stack = None

        e = None


        stack = []
        try:
            try:
                # SelectScript.g:287:19: ( (e= expr )* )
                # SelectScript.g:288:2: (e= expr )*
                pass 
                # SelectScript.g:288:2: (e= expr )*
                while True: #loop20
                    alt20 = 2
                    LA20_0 = self.input.LA(1)

                    if ((FCT <= LA20_0 <= NEG) or LA20_0 == STMT_SELECT or LA20_0 == AND or (XOR <= LA20_0 <= OR) or LA20_0 == NOT or (IN <= LA20_0 <= POW) or LA20_0 == THIS or LA20_0 == 91) :
                        alt20 = 1


                    if alt20 == 1:
                        # SelectScript.g:288:3: e= expr
                        pass 
                        self._state.following.append(self.FOLLOW_expr_in_parameter1175)
                        e = self.expr()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            stack.append(e)



                    else:
                        break #loop20




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return stack

    # $ANTLR end "parameter"

    # $ANTLR start "synpred2_SelectScript"
    def synpred2_SelectScript_fragment(self, ):
        # SelectScript.g:152:2: (s= statement_select )
        # SelectScript.g:152:2: s= statement_select
        pass 
        self._state.following.append(self.FOLLOW_statement_select_in_synpred2_SelectScript126)
        s = self.statement_select()

        self._state.following.pop()


    # $ANTLR end "synpred2_SelectScript"



    # $ANTLR start "synpred48_SelectScript"
    def synpred48_SelectScript_fragment(self, ):
        # SelectScript.g:282:21: (params= parameter )
        # SelectScript.g:282:21: params= parameter
        pass 
        self._state.following.append(self.FOLLOW_parameter_in_synpred48_SelectScript1149)
        params = self.parameter()

        self._state.following.pop()


    # $ANTLR end "synpred48_SelectScript"




    # Delegated rules

    def synpred48_SelectScript(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred48_SelectScript_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred2_SelectScript(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred2_SelectScript_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success



    # lookup tables for DFA #2

    DFA2_eot = DFA.unpack(
        u"\35\uffff"
        )

    DFA2_eof = DFA.unpack(
        u"\35\uffff"
        )

    DFA2_min = DFA.unpack(
        u"\1\4\1\0\33\uffff"
        )

    DFA2_max = DFA.unpack(
        u"\1\133\1\0\33\uffff"
        )

    DFA2_accept = DFA.unpack(
        u"\2\uffff\1\2\31\uffff\1\1"
        )

    DFA2_special = DFA.unpack(
        u"\1\uffff\1\0\33\uffff"
        )

            
    DFA2_transition = [
        DFA.unpack(u"\6\2\1\uffff\1\1\11\uffff\1\2\3\uffff\2\2\1\uffff\1"
        u"\2\1\uffff\16\2\22\uffff\1\2\34\uffff\1\2"),
        DFA.unpack(u"\1\uffff"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]

    # class definition for DFA #2

    class DFA2(DFA):
        pass


        def specialStateTransition(self_, s, input):
            # convince pylint that my self_ magic is ok ;)
            # pylint: disable-msg=E0213

            # pretend we are a member of the recognizer
            # thus semantic predicates can be evaluated
            self = self_.recognizer

            _s = s

            if s == 0: 
                LA2_1 = input.LA(1)

                 
                index2_1 = input.index()
                input.rewind()
                s = -1
                if (self.synpred2_SelectScript()):
                    s = 28

                elif (True):
                    s = 2

                 
                input.seek(index2_1)
                if s >= 0:
                    return s

            if self._state.backtracking >0:
                raise BacktrackingFailed
            nvae = NoViableAltException(self_.getDescription(), 2, _s, input)
            self_.error(nvae)
            raise nvae
    # lookup tables for DFA #15

    DFA15_eot = DFA.unpack(
        u"\12\uffff"
        )

    DFA15_eof = DFA.unpack(
        u"\12\uffff"
        )

    DFA15_min = DFA.unpack(
        u"\1\6\1\2\2\uffff\1\113\5\uffff"
        )

    DFA15_max = DFA.unpack(
        u"\1\76\1\2\2\uffff\1\120\5\uffff"
        )

    DFA15_accept = DFA.unpack(
        u"\2\uffff\1\6\1\7\1\uffff\1\1\1\2\1\3\1\4\1\5"
        )

    DFA15_special = DFA.unpack(
        u"\12\uffff"
        )

            
    DFA15_transition = [
        DFA.unpack(u"\1\1\1\3\66\uffff\1\2"),
        DFA.unpack(u"\1\4"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\5\1\uffff\1\6\1\7\1\10\1\11"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]

    # class definition for DFA #15

    class DFA15(DFA):
        pass


 

    FOLLOW_prog_in_eval83 = frozenset([1])
    FOLLOW_statement_in_prog105 = frozenset([1, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_statement_select_in_statement126 = frozenset([1])
    FOLLOW_expr_in_statement136 = frozenset([1])
    FOLLOW_STMT_SELECT_in_statement_select166 = frozenset([2])
    FOLLOW_select__in_statement_select170 = frozenset([57])
    FOLLOW_from__in_statement_select174 = frozenset([3, 60, 61])
    FOLLOW_where__in_statement_select180 = frozenset([3, 61])
    FOLLOW_as__in_statement_select189 = frozenset([3])
    FOLLOW_SELECT_in_select_213 = frozenset([2])
    FOLLOW_PHRASE_in_select_224 = frozenset([3, 4, 62, 83])
    FOLLOW_function_in_select_236 = frozenset([3, 4, 62, 83])
    FOLLOW_this__in_select_248 = frozenset([3, 4, 62, 83])
    FOLLOW_FROM_in_from_278 = frozenset([2])
    FOLLOW_expr_in_from_283 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_AS_in_as_303 = frozenset([2])
    FOLLOW_AS_DICT_in_as_305 = frozenset([3])
    FOLLOW_AS_in_as_315 = frozenset([2])
    FOLLOW_AS_LIST_in_as_317 = frozenset([3])
    FOLLOW_AS_in_as_327 = frozenset([2])
    FOLLOW_AS_SCENE_in_as_329 = frozenset([3])
    FOLLOW_AS_in_as_338 = frozenset([2])
    FOLLOW_AS_VALUE_in_as_340 = frozenset([3])
    FOLLOW_AS_in_as_350 = frozenset([2])
    FOLLOW_PHRASE_in_as_354 = frozenset([3])
    FOLLOW_WHERE_in_where_373 = frozenset([2])
    FOLLOW_expr_in_where_377 = frozenset([3])
    FOLLOW_assign_expr_in_expr399 = frozenset([1])
    FOLLOW_logic_expr_in_expr412 = frozenset([1])
    FOLLOW_compare_expr_in_expr424 = frozenset([1])
    FOLLOW_arithmetic_expr_in_expr435 = frozenset([1])
    FOLLOW_atom_in_expr445 = frozenset([1])
    FOLLOW_AGE_in_age469 = frozenset([2])
    FOLLOW_expr_in_age474 = frozenset([3])
    FOLLOW_ASSIGN_in_assign_expr509 = frozenset([2])
    FOLLOW_PHRASE_in_assign_expr513 = frozenset([3, 4, 5, 6, 7, 8, 9, 10, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_assign_expr517 = frozenset([3, 10])
    FOLLOW_age_in_assign_expr522 = frozenset([3])
    FOLLOW_OR_in_logic_expr543 = frozenset([2])
    FOLLOW_expr_in_logic_expr547 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_logic_expr551 = frozenset([3])
    FOLLOW_XOR_in_logic_expr561 = frozenset([2])
    FOLLOW_expr_in_logic_expr565 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_logic_expr569 = frozenset([3])
    FOLLOW_AND_in_logic_expr580 = frozenset([2])
    FOLLOW_expr_in_logic_expr584 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_logic_expr588 = frozenset([3])
    FOLLOW_NOT_in_logic_expr598 = frozenset([2])
    FOLLOW_expr_in_logic_expr602 = frozenset([3])
    FOLLOW_IN_in_compare_expr623 = frozenset([2])
    FOLLOW_expr_in_compare_expr627 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_compare_expr631 = frozenset([3])
    FOLLOW_EQ_in_compare_expr640 = frozenset([2])
    FOLLOW_expr_in_compare_expr644 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_compare_expr648 = frozenset([3])
    FOLLOW_NE_in_compare_expr657 = frozenset([2])
    FOLLOW_expr_in_compare_expr661 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_compare_expr665 = frozenset([3])
    FOLLOW_GE_in_compare_expr674 = frozenset([2])
    FOLLOW_expr_in_compare_expr678 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_compare_expr682 = frozenset([3])
    FOLLOW_GT_in_compare_expr691 = frozenset([2])
    FOLLOW_expr_in_compare_expr695 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_compare_expr699 = frozenset([3])
    FOLLOW_LE_in_compare_expr708 = frozenset([2])
    FOLLOW_expr_in_compare_expr712 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_compare_expr716 = frozenset([3])
    FOLLOW_LT_in_compare_expr725 = frozenset([2])
    FOLLOW_expr_in_compare_expr729 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_compare_expr733 = frozenset([3])
    FOLLOW_MUL_in_arithmetic_expr751 = frozenset([2])
    FOLLOW_expr_in_arithmetic_expr755 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_arithmetic_expr759 = frozenset([3])
    FOLLOW_DIV_in_arithmetic_expr767 = frozenset([2])
    FOLLOW_expr_in_arithmetic_expr771 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_arithmetic_expr775 = frozenset([3])
    FOLLOW_MOD_in_arithmetic_expr783 = frozenset([2])
    FOLLOW_expr_in_arithmetic_expr787 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_arithmetic_expr791 = frozenset([3])
    FOLLOW_SUB_in_arithmetic_expr799 = frozenset([2])
    FOLLOW_expr_in_arithmetic_expr803 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_arithmetic_expr807 = frozenset([3])
    FOLLOW_ADD_in_arithmetic_expr815 = frozenset([2])
    FOLLOW_expr_in_arithmetic_expr819 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_arithmetic_expr823 = frozenset([3])
    FOLLOW_POW_in_arithmetic_expr831 = frozenset([2])
    FOLLOW_expr_in_arithmetic_expr835 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_expr_in_arithmetic_expr839 = frozenset([3])
    FOLLOW_NEG_in_arithmetic_expr847 = frozenset([2])
    FOLLOW_expr_in_arithmetic_expr851 = frozenset([3])
    FOLLOW_POS_in_arithmetic_expr861 = frozenset([2])
    FOLLOW_expr_in_arithmetic_expr865 = frozenset([3])
    FOLLOW_value_in_atom888 = frozenset([1])
    FOLLOW_variable_in_atom903 = frozenset([1])
    FOLLOW_function_in_atom916 = frozenset([1])
    FOLLOW_91_in_atom925 = frozenset([4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91, 92])
    FOLLOW_expr_in_atom929 = frozenset([92])
    FOLLOW_92_in_atom931 = frozenset([1])
    FOLLOW_statement_select_in_atom942 = frozenset([1])
    FOLLOW_VAL_in_value962 = frozenset([2])
    FOLLOW_STRING_in_value964 = frozenset([3])
    FOLLOW_VAL_in_value974 = frozenset([2])
    FOLLOW_INTEGER_in_value976 = frozenset([3])
    FOLLOW_VAL_in_value987 = frozenset([2])
    FOLLOW_FLOAT_in_value989 = frozenset([3])
    FOLLOW_VAL_in_value999 = frozenset([2])
    FOLLOW_TRUE_in_value1001 = frozenset([3])
    FOLLOW_VAL_in_value1011 = frozenset([2])
    FOLLOW_FALSE_in_value1013 = frozenset([3])
    FOLLOW_this__in_value1024 = frozenset([1])
    FOLLOW_list__in_value1035 = frozenset([1])
    FOLLOW_THIS_in_this_1059 = frozenset([2])
    FOLLOW_PHRASE_in_this_1062 = frozenset([3])
    FOLLOW_LIST_in_list_1086 = frozenset([2])
    FOLLOW_expr_in_list_1092 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_VAR_in_variable1116 = frozenset([2])
    FOLLOW_PHRASE_in_variable1118 = frozenset([3, 10])
    FOLLOW_age_in_variable1123 = frozenset([3])
    FOLLOW_FCT_in_function1143 = frozenset([2])
    FOLLOW_PHRASE_in_function1145 = frozenset([3, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_parameter_in_function1149 = frozenset([3])
    FOLLOW_expr_in_parameter1175 = frozenset([1, 4, 5, 6, 7, 8, 9, 11, 21, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 62, 91])
    FOLLOW_statement_select_in_synpred2_SelectScript126 = frozenset([1])
    FOLLOW_parameter_in_synpred48_SelectScript1149 = frozenset([1])



       
def main(argv, otherArg=None):
    while True:
        expr = raw_input('>>> ')
        if expr == '':
            break

        scene = SelectScript(None, None)
        code = scene.compile(expr)
        print code
        scene.prettyPrint(code)


if __name__ == '__main__':
    main(sys.argv)
