# $ANTLR 3.1.3 Mar 18, 2009 10:09:25 SelectExpr.g 2014-02-03 13:11:11

import sys
from antlr3 import *
from antlr3.compat import set, frozenset

from antlr3.tree import *

        
import antlr3
import antlr3.tree
from SelectExprLexer import SelectExprLexer



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
LT=36
STMT_UPDATE=12
MOD=42
LIST_BEGIN=46
DQ=45
NOT=28
EOF=-1
CHARACTER=81
T__91=91
T__92=92
POW=43
POS=8
THIS=62
VAL=6
VAR=5
EQ=32
COMMENT=73
SELECT=54
NE=33
D=20
E=51
GE=35
LIST_END=47
F=55
G=87
A=18
AS_LIST=65
B=84
C=53
L=52
LINE_COMMENT=74
M=56
N=19
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
S=50
AS_VALUE=68
R=24
LIST=7
MUL=40
Y=69
X=22
Z=90
WS=72
SPECIAL=82
OR=26
GT=37
END=16
FROM=57
FALSE=80
RENAME=13
WHERE=60
SUB=39
FLOAT=78
AND=21
AS=61
TIME=63
IN=30
SEP=15
DIGIT=76
DOT=14
ADD=38
INTEGER=77
XOR=25
AGE_BEGIN=48
STMT_SELECT=11
FCT=4
TRUE=79
PHRASE=83
AGE_END=49
COLON=17
AGE=10
NEWLINE=71
NEG=9
AS_SCENE=64
ASSIGN=31
SQ=44
AS_DICT=70
DIV=41
LE=34
STRING=75

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




class SelectExprParser(Parser):
    grammarFileName = "SelectExpr.g"
    antlr_version = version_str_to_tuple("3.1.3 Mar 18, 2009 10:09:25")
    antlr_version_str = "3.1.3 Mar 18, 2009 10:09:25"
    tokenNames = tokenNames

    def __init__(self, input, state=None, *args, **kwargs):
        if state is None:
            state = RecognizerSharedState()

        super(SelectExprParser, self).__init__(input, state, *args, **kwargs)

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

        self.dfa10 = self.DFA10(
            self, 10,
            eot = self.DFA10_eot,
            eof = self.DFA10_eof,
            min = self.DFA10_min,
            max = self.DFA10_max,
            accept = self.DFA10_accept,
            special = self.DFA10_special,
            transition = self.DFA10_transition
            )






        self._adaptor = None
        self.adaptor = CommonTreeAdaptor()
                


        
    def getTreeAdaptor(self):
        return self._adaptor

    def setTreeAdaptor(self, adaptor):
        self._adaptor = adaptor

    adaptor = property(getTreeAdaptor, setTreeAdaptor)


    class eval_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.eval_return, self).__init__()

            self.tree = None




    # $ANTLR start "eval"
    # SelectExpr.g:139:1: eval : prog ;
    def eval(self, ):

        retval = self.eval_return()
        retval.start = self.input.LT(1)

        root_0 = None

        prog1 = None



        try:
            try:
                # SelectExpr.g:139:6: ( prog )
                # SelectExpr.g:139:8: prog
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_prog_in_eval1249)
                prog1 = self.prog()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, prog1.tree)



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "eval"

    class prog_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.prog_return, self).__init__()

            self.tree = None




    # $ANTLR start "prog"
    # SelectExpr.g:142:1: prog : ( statement )+ ;
    def prog(self, ):

        retval = self.prog_return()
        retval.start = self.input.LT(1)

        root_0 = None

        statement2 = None



        try:
            try:
                # SelectExpr.g:142:6: ( ( statement )+ )
                # SelectExpr.g:142:8: ( statement )+
                pass 
                root_0 = self._adaptor.nil()

                # SelectExpr.g:142:8: ( statement )+
                cnt1 = 0
                while True: #loop1
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if (LA1_0 == END or LA1_0 == NOT or (ADD <= LA1_0 <= SUB) or LA1_0 == LIST_BEGIN or LA1_0 == SELECT or LA1_0 == THIS or LA1_0 == STRING or (INTEGER <= LA1_0 <= FALSE) or LA1_0 == PHRASE or LA1_0 == 91) :
                        alt1 = 1


                    if alt1 == 1:
                        # SelectExpr.g:0:0: statement
                        pass 
                        self._state.following.append(self.FOLLOW_statement_in_prog1259)
                        statement2 = self.statement()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, statement2.tree)


                    else:
                        if cnt1 >= 1:
                            break #loop1

                        if self._state.backtracking > 0:
                            raise BacktrackingFailed

                        eee = EarlyExitException(1, self.input)
                        raise eee

                    cnt1 += 1



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "prog"

    class statement_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.statement_return, self).__init__()

            self.tree = None




    # $ANTLR start "statement"
    # SelectExpr.g:145:1: statement : ( statement_select END | expr END | END );
    def statement(self, ):

        retval = self.statement_return()
        retval.start = self.input.LT(1)

        root_0 = None

        END4 = None
        END6 = None
        END7 = None
        statement_select3 = None

        expr5 = None


        END4_tree = None
        END6_tree = None
        END7_tree = None

        try:
            try:
                # SelectExpr.g:145:11: ( statement_select END | expr END | END )
                alt2 = 3
                alt2 = self.dfa2.predict(self.input)
                if alt2 == 1:
                    # SelectExpr.g:145:13: statement_select END
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_statement_select_in_statement1269)
                    statement_select3 = self.statement_select()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, statement_select3.tree)
                    END4=self.match(self.input, END, self.FOLLOW_END_in_statement1271)


                elif alt2 == 2:
                    # SelectExpr.g:146:4: expr END
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_expr_in_statement1277)
                    expr5 = self.expr()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, expr5.tree)
                    END6=self.match(self.input, END, self.FOLLOW_END_in_statement1279)


                elif alt2 == 3:
                    # SelectExpr.g:147:4: END
                    pass 
                    root_0 = self._adaptor.nil()

                    END7=self.match(self.input, END, self.FOLLOW_END_in_statement1285)


                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "statement"

    class statement_select_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.statement_select_return, self).__init__()

            self.tree = None




    # $ANTLR start "statement_select"
    # SelectExpr.g:150:1: statement_select : select_ from_ ( where_ )? ( as_ )? -> ^( STMT_SELECT select_ from_ ( where_ )? ( as_ )? ) ;
    def statement_select(self, ):

        retval = self.statement_select_return()
        retval.start = self.input.LT(1)

        root_0 = None

        select_8 = None

        from_9 = None

        where_10 = None

        as_11 = None


        stream_select_ = RewriteRuleSubtreeStream(self._adaptor, "rule select_")
        stream_where_ = RewriteRuleSubtreeStream(self._adaptor, "rule where_")
        stream_as_ = RewriteRuleSubtreeStream(self._adaptor, "rule as_")
        stream_from_ = RewriteRuleSubtreeStream(self._adaptor, "rule from_")
        try:
            try:
                # SelectExpr.g:150:18: ( select_ from_ ( where_ )? ( as_ )? -> ^( STMT_SELECT select_ from_ ( where_ )? ( as_ )? ) )
                # SelectExpr.g:151:2: select_ from_ ( where_ )? ( as_ )?
                pass 
                self._state.following.append(self.FOLLOW_select__in_statement_select1296)
                select_8 = self.select_()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    stream_select_.add(select_8.tree)
                self._state.following.append(self.FOLLOW_from__in_statement_select1298)
                from_9 = self.from_()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    stream_from_.add(from_9.tree)
                # SelectExpr.g:151:16: ( where_ )?
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if (LA3_0 == WHERE) :
                    LA3_1 = self.input.LA(2)

                    if (self.synpred4_SelectExpr()) :
                        alt3 = 1
                if alt3 == 1:
                    # SelectExpr.g:151:17: where_
                    pass 
                    self._state.following.append(self.FOLLOW_where__in_statement_select1301)
                    where_10 = self.where_()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stream_where_.add(where_10.tree)



                # SelectExpr.g:151:26: ( as_ )?
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if (LA4_0 == AS) :
                    LA4_1 = self.input.LA(2)

                    if (self.synpred5_SelectExpr()) :
                        alt4 = 1
                if alt4 == 1:
                    # SelectExpr.g:151:27: as_
                    pass 
                    self._state.following.append(self.FOLLOW_as__in_statement_select1306)
                    as_11 = self.as_()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stream_as_.add(as_11.tree)




                # AST Rewrite
                # elements: where_, as_, select_, from_
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                if self._state.backtracking == 0:

                    retval.tree = root_0

                    if retval is not None:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                    else:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                    root_0 = self._adaptor.nil()
                    # 151:33: -> ^( STMT_SELECT select_ from_ ( where_ )? ( as_ )? )
                    # SelectExpr.g:151:37: ^( STMT_SELECT select_ from_ ( where_ )? ( as_ )? )
                    root_1 = self._adaptor.nil()
                    root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(STMT_SELECT, "STMT_SELECT"), root_1)

                    self._adaptor.addChild(root_1, stream_select_.nextTree())
                    self._adaptor.addChild(root_1, stream_from_.nextTree())
                    # SelectExpr.g:151:65: ( where_ )?
                    if stream_where_.hasNext():
                        self._adaptor.addChild(root_1, stream_where_.nextTree())


                    stream_where_.reset();
                    # SelectExpr.g:151:75: ( as_ )?
                    if stream_as_.hasNext():
                        self._adaptor.addChild(root_1, stream_as_.nextTree())


                    stream_as_.reset();

                    self._adaptor.addChild(root_0, root_1)



                    retval.tree = root_0



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "statement_select"

    class select__return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.select__return, self).__init__()

            self.tree = None




    # $ANTLR start "select_"
    # SelectExpr.g:154:1: select_ : SELECT ( MUL | ( ( PHRASE | function | this_ ) ( SEP ( PHRASE | function | this_ ) )* ) ) ;
    def select_(self, ):

        retval = self.select__return()
        retval.start = self.input.LT(1)

        root_0 = None

        SELECT12 = None
        MUL13 = None
        PHRASE14 = None
        SEP17 = None
        PHRASE18 = None
        function15 = None

        this_16 = None

        function19 = None

        this_20 = None


        SELECT12_tree = None
        MUL13_tree = None
        PHRASE14_tree = None
        SEP17_tree = None
        PHRASE18_tree = None

        try:
            try:
                # SelectExpr.g:154:9: ( SELECT ( MUL | ( ( PHRASE | function | this_ ) ( SEP ( PHRASE | function | this_ ) )* ) ) )
                # SelectExpr.g:154:11: SELECT ( MUL | ( ( PHRASE | function | this_ ) ( SEP ( PHRASE | function | this_ ) )* ) )
                pass 
                root_0 = self._adaptor.nil()

                SELECT12=self.match(self.input, SELECT, self.FOLLOW_SELECT_in_select_1339)
                if self._state.backtracking == 0:

                    SELECT12_tree = self._adaptor.createWithPayload(SELECT12)
                    root_0 = self._adaptor.becomeRoot(SELECT12_tree, root_0)

                # SelectExpr.g:154:19: ( MUL | ( ( PHRASE | function | this_ ) ( SEP ( PHRASE | function | this_ ) )* ) )
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if (LA8_0 == MUL) :
                    alt8 = 1
                elif (LA8_0 == THIS or LA8_0 == PHRASE) :
                    alt8 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed

                    nvae = NoViableAltException("", 8, 0, self.input)

                    raise nvae

                if alt8 == 1:
                    # SelectExpr.g:154:20: MUL
                    pass 
                    MUL13=self.match(self.input, MUL, self.FOLLOW_MUL_in_select_1343)


                elif alt8 == 2:
                    # SelectExpr.g:154:27: ( ( PHRASE | function | this_ ) ( SEP ( PHRASE | function | this_ ) )* )
                    pass 
                    # SelectExpr.g:154:27: ( ( PHRASE | function | this_ ) ( SEP ( PHRASE | function | this_ ) )* )
                    # SelectExpr.g:154:28: ( PHRASE | function | this_ ) ( SEP ( PHRASE | function | this_ ) )*
                    pass 
                    # SelectExpr.g:154:28: ( PHRASE | function | this_ )
                    alt5 = 3
                    LA5_0 = self.input.LA(1)

                    if (LA5_0 == PHRASE) :
                        LA5 = self.input.LA(2)
                        if LA5 == 91:
                            alt5 = 2
                        elif LA5 == DOT:
                            alt5 = 3
                        elif LA5 == SEP or LA5 == FROM:
                            alt5 = 1
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed

                            nvae = NoViableAltException("", 5, 1, self.input)

                            raise nvae

                    elif (LA5_0 == THIS) :
                        alt5 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed

                        nvae = NoViableAltException("", 5, 0, self.input)

                        raise nvae

                    if alt5 == 1:
                        # SelectExpr.g:154:29: PHRASE
                        pass 
                        PHRASE14=self.match(self.input, PHRASE, self.FOLLOW_PHRASE_in_select_1350)
                        if self._state.backtracking == 0:

                            PHRASE14_tree = self._adaptor.createWithPayload(PHRASE14)
                            self._adaptor.addChild(root_0, PHRASE14_tree)



                    elif alt5 == 2:
                        # SelectExpr.g:154:38: function
                        pass 
                        self._state.following.append(self.FOLLOW_function_in_select_1354)
                        function15 = self.function()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, function15.tree)


                    elif alt5 == 3:
                        # SelectExpr.g:154:49: this_
                        pass 
                        self._state.following.append(self.FOLLOW_this__in_select_1358)
                        this_16 = self.this_()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, this_16.tree)



                    # SelectExpr.g:154:56: ( SEP ( PHRASE | function | this_ ) )*
                    while True: #loop7
                        alt7 = 2
                        LA7_0 = self.input.LA(1)

                        if (LA7_0 == SEP) :
                            alt7 = 1


                        if alt7 == 1:
                            # SelectExpr.g:154:57: SEP ( PHRASE | function | this_ )
                            pass 
                            SEP17=self.match(self.input, SEP, self.FOLLOW_SEP_in_select_1362)
                            # SelectExpr.g:154:62: ( PHRASE | function | this_ )
                            alt6 = 3
                            LA6_0 = self.input.LA(1)

                            if (LA6_0 == PHRASE) :
                                LA6 = self.input.LA(2)
                                if LA6 == 91:
                                    alt6 = 2
                                elif LA6 == DOT:
                                    alt6 = 3
                                elif LA6 == SEP or LA6 == FROM:
                                    alt6 = 1
                                else:
                                    if self._state.backtracking > 0:
                                        raise BacktrackingFailed

                                    nvae = NoViableAltException("", 6, 1, self.input)

                                    raise nvae

                            elif (LA6_0 == THIS) :
                                alt6 = 3
                            else:
                                if self._state.backtracking > 0:
                                    raise BacktrackingFailed

                                nvae = NoViableAltException("", 6, 0, self.input)

                                raise nvae

                            if alt6 == 1:
                                # SelectExpr.g:154:63: PHRASE
                                pass 
                                PHRASE18=self.match(self.input, PHRASE, self.FOLLOW_PHRASE_in_select_1366)
                                if self._state.backtracking == 0:

                                    PHRASE18_tree = self._adaptor.createWithPayload(PHRASE18)
                                    self._adaptor.addChild(root_0, PHRASE18_tree)



                            elif alt6 == 2:
                                # SelectExpr.g:154:72: function
                                pass 
                                self._state.following.append(self.FOLLOW_function_in_select_1370)
                                function19 = self.function()

                                self._state.following.pop()
                                if self._state.backtracking == 0:
                                    self._adaptor.addChild(root_0, function19.tree)


                            elif alt6 == 3:
                                # SelectExpr.g:154:83: this_
                                pass 
                                self._state.following.append(self.FOLLOW_this__in_select_1374)
                                this_20 = self.this_()

                                self._state.following.pop()
                                if self._state.backtracking == 0:
                                    self._adaptor.addChild(root_0, this_20.tree)





                        else:
                            break #loop7









                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "select_"

    class from__return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.from__return, self).__init__()

            self.tree = None




    # $ANTLR start "from_"
    # SelectExpr.g:157:1: from_ : FROM expr ( SEP expr )* ;
    def from_(self, ):

        retval = self.from__return()
        retval.start = self.input.LT(1)

        root_0 = None

        FROM21 = None
        SEP23 = None
        expr22 = None

        expr24 = None


        FROM21_tree = None
        SEP23_tree = None

        try:
            try:
                # SelectExpr.g:157:7: ( FROM expr ( SEP expr )* )
                # SelectExpr.g:157:9: FROM expr ( SEP expr )*
                pass 
                root_0 = self._adaptor.nil()

                FROM21=self.match(self.input, FROM, self.FOLLOW_FROM_in_from_1390)
                if self._state.backtracking == 0:

                    FROM21_tree = self._adaptor.createWithPayload(FROM21)
                    root_0 = self._adaptor.becomeRoot(FROM21_tree, root_0)

                self._state.following.append(self.FOLLOW_expr_in_from_1393)
                expr22 = self.expr()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, expr22.tree)
                # SelectExpr.g:157:20: ( SEP expr )*
                while True: #loop9
                    alt9 = 2
                    LA9_0 = self.input.LA(1)

                    if (LA9_0 == SEP) :
                        LA9_2 = self.input.LA(2)

                        if (self.synpred12_SelectExpr()) :
                            alt9 = 1




                    if alt9 == 1:
                        # SelectExpr.g:157:21: SEP expr
                        pass 
                        SEP23=self.match(self.input, SEP, self.FOLLOW_SEP_in_from_1396)
                        self._state.following.append(self.FOLLOW_expr_in_from_1399)
                        expr24 = self.expr()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, expr24.tree)


                    else:
                        break #loop9



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "from_"

    class where__return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.where__return, self).__init__()

            self.tree = None




    # $ANTLR start "where_"
    # SelectExpr.g:160:1: where_ : WHERE expr ;
    def where_(self, ):

        retval = self.where__return()
        retval.start = self.input.LT(1)

        root_0 = None

        WHERE25 = None
        expr26 = None


        WHERE25_tree = None

        try:
            try:
                # SelectExpr.g:160:8: ( WHERE expr )
                # SelectExpr.g:160:10: WHERE expr
                pass 
                root_0 = self._adaptor.nil()

                WHERE25=self.match(self.input, WHERE, self.FOLLOW_WHERE_in_where_1410)
                if self._state.backtracking == 0:

                    WHERE25_tree = self._adaptor.createWithPayload(WHERE25)
                    root_0 = self._adaptor.becomeRoot(WHERE25_tree, root_0)

                self._state.following.append(self.FOLLOW_expr_in_where_1413)
                expr26 = self.expr()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, expr26.tree)



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "where_"

    class as__return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.as__return, self).__init__()

            self.tree = None




    # $ANTLR start "as_"
    # SelectExpr.g:163:1: as_ : AS ( AS_SCENE | AS_LIST | AS_VALUE | AS_DICT | PHRASE ) ;
    def as_(self, ):

        retval = self.as__return()
        retval.start = self.input.LT(1)

        root_0 = None

        AS27 = None
        set28 = None

        AS27_tree = None
        set28_tree = None

        try:
            try:
                # SelectExpr.g:163:5: ( AS ( AS_SCENE | AS_LIST | AS_VALUE | AS_DICT | PHRASE ) )
                # SelectExpr.g:163:7: AS ( AS_SCENE | AS_LIST | AS_VALUE | AS_DICT | PHRASE )
                pass 
                root_0 = self._adaptor.nil()

                AS27=self.match(self.input, AS, self.FOLLOW_AS_in_as_1422)
                if self._state.backtracking == 0:

                    AS27_tree = self._adaptor.createWithPayload(AS27)
                    root_0 = self._adaptor.becomeRoot(AS27_tree, root_0)

                set28 = self.input.LT(1)
                if (AS_SCENE <= self.input.LA(1) <= AS_LIST) or self.input.LA(1) == AS_VALUE or self.input.LA(1) == AS_DICT or self.input.LA(1) == PHRASE:
                    self.input.consume()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set28))
                    self._state.errorRecovery = False

                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed

                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "as_"

    class expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "expr"
    # SelectExpr.g:166:1: expr : ( assign_expr | logic_expr );
    def expr(self, ):

        retval = self.expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        assign_expr29 = None

        logic_expr30 = None



        try:
            try:
                # SelectExpr.g:166:6: ( assign_expr | logic_expr )
                alt10 = 2
                alt10 = self.dfa10.predict(self.input)
                if alt10 == 1:
                    # SelectExpr.g:166:8: assign_expr
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_assign_expr_in_expr1452)
                    assign_expr29 = self.assign_expr()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, assign_expr29.tree)


                elif alt10 == 2:
                    # SelectExpr.g:167:4: logic_expr
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_logic_expr_in_expr1458)
                    logic_expr30 = self.logic_expr()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, logic_expr30.tree)


                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "expr"

    class assign_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.assign_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "assign_expr"
    # SelectExpr.g:169:1: assign_expr : PHRASE ( age )? ASSIGN expr -> ^( ASSIGN PHRASE expr ( age )? ) ;
    def assign_expr(self, ):

        retval = self.assign_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        PHRASE31 = None
        ASSIGN33 = None
        age32 = None

        expr34 = None


        PHRASE31_tree = None
        ASSIGN33_tree = None
        stream_PHRASE = RewriteRuleTokenStream(self._adaptor, "token PHRASE")
        stream_ASSIGN = RewriteRuleTokenStream(self._adaptor, "token ASSIGN")
        stream_age = RewriteRuleSubtreeStream(self._adaptor, "rule age")
        stream_expr = RewriteRuleSubtreeStream(self._adaptor, "rule expr")
        try:
            try:
                # SelectExpr.g:169:13: ( PHRASE ( age )? ASSIGN expr -> ^( ASSIGN PHRASE expr ( age )? ) )
                # SelectExpr.g:169:15: PHRASE ( age )? ASSIGN expr
                pass 
                PHRASE31=self.match(self.input, PHRASE, self.FOLLOW_PHRASE_in_assign_expr1466) 
                if self._state.backtracking == 0:
                    stream_PHRASE.add(PHRASE31)
                # SelectExpr.g:169:22: ( age )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == AGE_BEGIN) :
                    alt11 = 1
                if alt11 == 1:
                    # SelectExpr.g:169:23: age
                    pass 
                    self._state.following.append(self.FOLLOW_age_in_assign_expr1469)
                    age32 = self.age()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stream_age.add(age32.tree)



                ASSIGN33=self.match(self.input, ASSIGN, self.FOLLOW_ASSIGN_in_assign_expr1473) 
                if self._state.backtracking == 0:
                    stream_ASSIGN.add(ASSIGN33)
                self._state.following.append(self.FOLLOW_expr_in_assign_expr1475)
                expr34 = self.expr()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    stream_expr.add(expr34.tree)

                # AST Rewrite
                # elements: expr, ASSIGN, age, PHRASE
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                if self._state.backtracking == 0:

                    retval.tree = root_0

                    if retval is not None:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                    else:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                    root_0 = self._adaptor.nil()
                    # 169:41: -> ^( ASSIGN PHRASE expr ( age )? )
                    # SelectExpr.g:169:44: ^( ASSIGN PHRASE expr ( age )? )
                    root_1 = self._adaptor.nil()
                    root_1 = self._adaptor.becomeRoot(stream_ASSIGN.nextNode(), root_1)

                    self._adaptor.addChild(root_1, stream_PHRASE.nextNode())
                    self._adaptor.addChild(root_1, stream_expr.nextTree())
                    # SelectExpr.g:169:65: ( age )?
                    if stream_age.hasNext():
                        self._adaptor.addChild(root_1, stream_age.nextTree())


                    stream_age.reset();

                    self._adaptor.addChild(root_0, root_1)



                    retval.tree = root_0



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "assign_expr"

    class logic_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.logic_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "logic_expr"
    # SelectExpr.g:171:1: logic_expr : logic_or ;
    def logic_expr(self, ):

        retval = self.logic_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        logic_or35 = None



        try:
            try:
                # SelectExpr.g:171:12: ( logic_or )
                # SelectExpr.g:171:14: logic_or
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_logic_or_in_logic_expr1498)
                logic_or35 = self.logic_or()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, logic_or35.tree)



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "logic_expr"

    class logic_or_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.logic_or_return, self).__init__()

            self.tree = None




    # $ANTLR start "logic_or"
    # SelectExpr.g:172:1: logic_or : logic_xor ( OR logic_xor )* ;
    def logic_or(self, ):

        retval = self.logic_or_return()
        retval.start = self.input.LT(1)

        root_0 = None

        OR37 = None
        logic_xor36 = None

        logic_xor38 = None


        OR37_tree = None

        try:
            try:
                # SelectExpr.g:172:11: ( logic_xor ( OR logic_xor )* )
                # SelectExpr.g:172:13: logic_xor ( OR logic_xor )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_logic_xor_in_logic_or1507)
                logic_xor36 = self.logic_xor()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, logic_xor36.tree)
                # SelectExpr.g:172:23: ( OR logic_xor )*
                while True: #loop12
                    alt12 = 2
                    LA12_0 = self.input.LA(1)

                    if (LA12_0 == OR) :
                        LA12_2 = self.input.LA(2)

                        if (self.synpred19_SelectExpr()) :
                            alt12 = 1




                    if alt12 == 1:
                        # SelectExpr.g:172:24: OR logic_xor
                        pass 
                        OR37=self.match(self.input, OR, self.FOLLOW_OR_in_logic_or1510)
                        if self._state.backtracking == 0:

                            OR37_tree = self._adaptor.createWithPayload(OR37)
                            root_0 = self._adaptor.becomeRoot(OR37_tree, root_0)

                        self._state.following.append(self.FOLLOW_logic_xor_in_logic_or1514)
                        logic_xor38 = self.logic_xor()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, logic_xor38.tree)


                    else:
                        break #loop12



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "logic_or"

    class logic_xor_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.logic_xor_return, self).__init__()

            self.tree = None




    # $ANTLR start "logic_xor"
    # SelectExpr.g:173:1: logic_xor : logic_and ( XOR logic_and )* ;
    def logic_xor(self, ):

        retval = self.logic_xor_return()
        retval.start = self.input.LT(1)

        root_0 = None

        XOR40 = None
        logic_and39 = None

        logic_and41 = None


        XOR40_tree = None

        try:
            try:
                # SelectExpr.g:173:11: ( logic_and ( XOR logic_and )* )
                # SelectExpr.g:173:13: logic_and ( XOR logic_and )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_logic_and_in_logic_xor1524)
                logic_and39 = self.logic_and()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, logic_and39.tree)
                # SelectExpr.g:173:23: ( XOR logic_and )*
                while True: #loop13
                    alt13 = 2
                    LA13_0 = self.input.LA(1)

                    if (LA13_0 == XOR) :
                        LA13_2 = self.input.LA(2)

                        if (self.synpred20_SelectExpr()) :
                            alt13 = 1




                    if alt13 == 1:
                        # SelectExpr.g:173:24: XOR logic_and
                        pass 
                        XOR40=self.match(self.input, XOR, self.FOLLOW_XOR_in_logic_xor1527)
                        if self._state.backtracking == 0:

                            XOR40_tree = self._adaptor.createWithPayload(XOR40)
                            root_0 = self._adaptor.becomeRoot(XOR40_tree, root_0)

                        self._state.following.append(self.FOLLOW_logic_and_in_logic_xor1530)
                        logic_and41 = self.logic_and()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, logic_and41.tree)


                    else:
                        break #loop13



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "logic_xor"

    class logic_and_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.logic_and_return, self).__init__()

            self.tree = None




    # $ANTLR start "logic_and"
    # SelectExpr.g:174:1: logic_and : logic_not ( AND logic_not )* ;
    def logic_and(self, ):

        retval = self.logic_and_return()
        retval.start = self.input.LT(1)

        root_0 = None

        AND43 = None
        logic_not42 = None

        logic_not44 = None


        AND43_tree = None

        try:
            try:
                # SelectExpr.g:174:11: ( logic_not ( AND logic_not )* )
                # SelectExpr.g:174:13: logic_not ( AND logic_not )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_logic_not_in_logic_and1540)
                logic_not42 = self.logic_not()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, logic_not42.tree)
                # SelectExpr.g:174:23: ( AND logic_not )*
                while True: #loop14
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if (LA14_0 == AND) :
                        LA14_2 = self.input.LA(2)

                        if (self.synpred21_SelectExpr()) :
                            alt14 = 1




                    if alt14 == 1:
                        # SelectExpr.g:174:24: AND logic_not
                        pass 
                        AND43=self.match(self.input, AND, self.FOLLOW_AND_in_logic_and1543)
                        if self._state.backtracking == 0:

                            AND43_tree = self._adaptor.createWithPayload(AND43)
                            root_0 = self._adaptor.becomeRoot(AND43_tree, root_0)

                        self._state.following.append(self.FOLLOW_logic_not_in_logic_and1546)
                        logic_not44 = self.logic_not()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, logic_not44.tree)


                    else:
                        break #loop14



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "logic_and"

    class logic_not_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.logic_not_return, self).__init__()

            self.tree = None




    # $ANTLR start "logic_not"
    # SelectExpr.g:175:1: logic_not : ( NOT )? compare_expr ;
    def logic_not(self, ):

        retval = self.logic_not_return()
        retval.start = self.input.LT(1)

        root_0 = None

        NOT45 = None
        compare_expr46 = None


        NOT45_tree = None

        try:
            try:
                # SelectExpr.g:175:11: ( ( NOT )? compare_expr )
                # SelectExpr.g:175:13: ( NOT )? compare_expr
                pass 
                root_0 = self._adaptor.nil()

                # SelectExpr.g:175:13: ( NOT )?
                alt15 = 2
                LA15_0 = self.input.LA(1)

                if (LA15_0 == NOT) :
                    alt15 = 1
                if alt15 == 1:
                    # SelectExpr.g:175:14: NOT
                    pass 
                    NOT45=self.match(self.input, NOT, self.FOLLOW_NOT_in_logic_not1557)
                    if self._state.backtracking == 0:

                        NOT45_tree = self._adaptor.createWithPayload(NOT45)
                        root_0 = self._adaptor.becomeRoot(NOT45_tree, root_0)




                self._state.following.append(self.FOLLOW_compare_expr_in_logic_not1562)
                compare_expr46 = self.compare_expr()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, compare_expr46.tree)



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "logic_not"

    class compare_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.compare_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "compare_expr"
    # SelectExpr.g:177:1: compare_expr : compare_in ;
    def compare_expr(self, ):

        retval = self.compare_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        compare_in47 = None



        try:
            try:
                # SelectExpr.g:177:14: ( compare_in )
                # SelectExpr.g:177:16: compare_in
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_compare_in_in_compare_expr1571)
                compare_in47 = self.compare_in()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, compare_in47.tree)



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "compare_expr"

    class compare_in_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.compare_in_return, self).__init__()

            self.tree = None




    # $ANTLR start "compare_in"
    # SelectExpr.g:178:1: compare_in : compare_eq ( IN atom )* ;
    def compare_in(self, ):

        retval = self.compare_in_return()
        retval.start = self.input.LT(1)

        root_0 = None

        IN49 = None
        compare_eq48 = None

        atom50 = None


        IN49_tree = None

        try:
            try:
                # SelectExpr.g:178:12: ( compare_eq ( IN atom )* )
                # SelectExpr.g:178:14: compare_eq ( IN atom )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_compare_eq_in_compare_in1579)
                compare_eq48 = self.compare_eq()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, compare_eq48.tree)
                # SelectExpr.g:178:25: ( IN atom )*
                while True: #loop16
                    alt16 = 2
                    LA16_0 = self.input.LA(1)

                    if (LA16_0 == IN) :
                        LA16_2 = self.input.LA(2)

                        if (self.synpred23_SelectExpr()) :
                            alt16 = 1




                    if alt16 == 1:
                        # SelectExpr.g:178:26: IN atom
                        pass 
                        IN49=self.match(self.input, IN, self.FOLLOW_IN_in_compare_in1582)
                        if self._state.backtracking == 0:

                            IN49_tree = self._adaptor.createWithPayload(IN49)
                            root_0 = self._adaptor.becomeRoot(IN49_tree, root_0)

                        self._state.following.append(self.FOLLOW_atom_in_compare_in1585)
                        atom50 = self.atom()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, atom50.tree)


                    else:
                        break #loop16



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "compare_in"

    class compare_eq_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.compare_eq_return, self).__init__()

            self.tree = None




    # $ANTLR start "compare_eq"
    # SelectExpr.g:179:1: compare_eq : compare_ne ( EQ compare_ne )* ;
    def compare_eq(self, ):

        retval = self.compare_eq_return()
        retval.start = self.input.LT(1)

        root_0 = None

        EQ52 = None
        compare_ne51 = None

        compare_ne53 = None


        EQ52_tree = None

        try:
            try:
                # SelectExpr.g:179:12: ( compare_ne ( EQ compare_ne )* )
                # SelectExpr.g:179:14: compare_ne ( EQ compare_ne )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_compare_ne_in_compare_eq1595)
                compare_ne51 = self.compare_ne()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, compare_ne51.tree)
                # SelectExpr.g:179:25: ( EQ compare_ne )*
                while True: #loop17
                    alt17 = 2
                    LA17_0 = self.input.LA(1)

                    if (LA17_0 == EQ) :
                        LA17_2 = self.input.LA(2)

                        if (self.synpred24_SelectExpr()) :
                            alt17 = 1




                    if alt17 == 1:
                        # SelectExpr.g:179:26: EQ compare_ne
                        pass 
                        EQ52=self.match(self.input, EQ, self.FOLLOW_EQ_in_compare_eq1598)
                        if self._state.backtracking == 0:

                            EQ52_tree = self._adaptor.createWithPayload(EQ52)
                            root_0 = self._adaptor.becomeRoot(EQ52_tree, root_0)

                        self._state.following.append(self.FOLLOW_compare_ne_in_compare_eq1601)
                        compare_ne53 = self.compare_ne()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, compare_ne53.tree)


                    else:
                        break #loop17



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "compare_eq"

    class compare_ne_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.compare_ne_return, self).__init__()

            self.tree = None




    # $ANTLR start "compare_ne"
    # SelectExpr.g:180:1: compare_ne : compare_ge ( NE compare_ge )* ;
    def compare_ne(self, ):

        retval = self.compare_ne_return()
        retval.start = self.input.LT(1)

        root_0 = None

        NE55 = None
        compare_ge54 = None

        compare_ge56 = None


        NE55_tree = None

        try:
            try:
                # SelectExpr.g:180:12: ( compare_ge ( NE compare_ge )* )
                # SelectExpr.g:180:14: compare_ge ( NE compare_ge )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_compare_ge_in_compare_ne1611)
                compare_ge54 = self.compare_ge()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, compare_ge54.tree)
                # SelectExpr.g:180:25: ( NE compare_ge )*
                while True: #loop18
                    alt18 = 2
                    LA18_0 = self.input.LA(1)

                    if (LA18_0 == NE) :
                        LA18_2 = self.input.LA(2)

                        if (self.synpred25_SelectExpr()) :
                            alt18 = 1




                    if alt18 == 1:
                        # SelectExpr.g:180:26: NE compare_ge
                        pass 
                        NE55=self.match(self.input, NE, self.FOLLOW_NE_in_compare_ne1614)
                        if self._state.backtracking == 0:

                            NE55_tree = self._adaptor.createWithPayload(NE55)
                            root_0 = self._adaptor.becomeRoot(NE55_tree, root_0)

                        self._state.following.append(self.FOLLOW_compare_ge_in_compare_ne1617)
                        compare_ge56 = self.compare_ge()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, compare_ge56.tree)


                    else:
                        break #loop18



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "compare_ne"

    class compare_ge_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.compare_ge_return, self).__init__()

            self.tree = None




    # $ANTLR start "compare_ge"
    # SelectExpr.g:181:1: compare_ge : compare_gt ( GE compare_gt )* ;
    def compare_ge(self, ):

        retval = self.compare_ge_return()
        retval.start = self.input.LT(1)

        root_0 = None

        GE58 = None
        compare_gt57 = None

        compare_gt59 = None


        GE58_tree = None

        try:
            try:
                # SelectExpr.g:181:12: ( compare_gt ( GE compare_gt )* )
                # SelectExpr.g:181:14: compare_gt ( GE compare_gt )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_compare_gt_in_compare_ge1627)
                compare_gt57 = self.compare_gt()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, compare_gt57.tree)
                # SelectExpr.g:181:25: ( GE compare_gt )*
                while True: #loop19
                    alt19 = 2
                    LA19_0 = self.input.LA(1)

                    if (LA19_0 == GE) :
                        LA19_2 = self.input.LA(2)

                        if (self.synpred26_SelectExpr()) :
                            alt19 = 1




                    if alt19 == 1:
                        # SelectExpr.g:181:26: GE compare_gt
                        pass 
                        GE58=self.match(self.input, GE, self.FOLLOW_GE_in_compare_ge1630)
                        if self._state.backtracking == 0:

                            GE58_tree = self._adaptor.createWithPayload(GE58)
                            root_0 = self._adaptor.becomeRoot(GE58_tree, root_0)

                        self._state.following.append(self.FOLLOW_compare_gt_in_compare_ge1633)
                        compare_gt59 = self.compare_gt()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, compare_gt59.tree)


                    else:
                        break #loop19



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "compare_ge"

    class compare_gt_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.compare_gt_return, self).__init__()

            self.tree = None




    # $ANTLR start "compare_gt"
    # SelectExpr.g:182:1: compare_gt : compare_le ( GT compare_le )* ;
    def compare_gt(self, ):

        retval = self.compare_gt_return()
        retval.start = self.input.LT(1)

        root_0 = None

        GT61 = None
        compare_le60 = None

        compare_le62 = None


        GT61_tree = None

        try:
            try:
                # SelectExpr.g:182:12: ( compare_le ( GT compare_le )* )
                # SelectExpr.g:182:14: compare_le ( GT compare_le )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_compare_le_in_compare_gt1643)
                compare_le60 = self.compare_le()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, compare_le60.tree)
                # SelectExpr.g:182:25: ( GT compare_le )*
                while True: #loop20
                    alt20 = 2
                    LA20_0 = self.input.LA(1)

                    if (LA20_0 == GT) :
                        LA20_2 = self.input.LA(2)

                        if (self.synpred27_SelectExpr()) :
                            alt20 = 1




                    if alt20 == 1:
                        # SelectExpr.g:182:26: GT compare_le
                        pass 
                        GT61=self.match(self.input, GT, self.FOLLOW_GT_in_compare_gt1646)
                        if self._state.backtracking == 0:

                            GT61_tree = self._adaptor.createWithPayload(GT61)
                            root_0 = self._adaptor.becomeRoot(GT61_tree, root_0)

                        self._state.following.append(self.FOLLOW_compare_le_in_compare_gt1649)
                        compare_le62 = self.compare_le()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, compare_le62.tree)


                    else:
                        break #loop20



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "compare_gt"

    class compare_le_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.compare_le_return, self).__init__()

            self.tree = None




    # $ANTLR start "compare_le"
    # SelectExpr.g:183:1: compare_le : compare_lt ( LE compare_lt )* ;
    def compare_le(self, ):

        retval = self.compare_le_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LE64 = None
        compare_lt63 = None

        compare_lt65 = None


        LE64_tree = None

        try:
            try:
                # SelectExpr.g:183:12: ( compare_lt ( LE compare_lt )* )
                # SelectExpr.g:183:14: compare_lt ( LE compare_lt )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_compare_lt_in_compare_le1659)
                compare_lt63 = self.compare_lt()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, compare_lt63.tree)
                # SelectExpr.g:183:25: ( LE compare_lt )*
                while True: #loop21
                    alt21 = 2
                    LA21_0 = self.input.LA(1)

                    if (LA21_0 == LE) :
                        LA21_2 = self.input.LA(2)

                        if (self.synpred28_SelectExpr()) :
                            alt21 = 1




                    if alt21 == 1:
                        # SelectExpr.g:183:26: LE compare_lt
                        pass 
                        LE64=self.match(self.input, LE, self.FOLLOW_LE_in_compare_le1662)
                        if self._state.backtracking == 0:

                            LE64_tree = self._adaptor.createWithPayload(LE64)
                            root_0 = self._adaptor.becomeRoot(LE64_tree, root_0)

                        self._state.following.append(self.FOLLOW_compare_lt_in_compare_le1665)
                        compare_lt65 = self.compare_lt()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, compare_lt65.tree)


                    else:
                        break #loop21



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "compare_le"

    class compare_lt_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.compare_lt_return, self).__init__()

            self.tree = None




    # $ANTLR start "compare_lt"
    # SelectExpr.g:184:1: compare_lt : arithmetic_expr ( LT arithmetic_expr )* ;
    def compare_lt(self, ):

        retval = self.compare_lt_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LT67 = None
        arithmetic_expr66 = None

        arithmetic_expr68 = None


        LT67_tree = None

        try:
            try:
                # SelectExpr.g:184:12: ( arithmetic_expr ( LT arithmetic_expr )* )
                # SelectExpr.g:184:14: arithmetic_expr ( LT arithmetic_expr )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_arithmetic_expr_in_compare_lt1675)
                arithmetic_expr66 = self.arithmetic_expr()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, arithmetic_expr66.tree)
                # SelectExpr.g:184:30: ( LT arithmetic_expr )*
                while True: #loop22
                    alt22 = 2
                    LA22_0 = self.input.LA(1)

                    if (LA22_0 == LT) :
                        LA22_2 = self.input.LA(2)

                        if (self.synpred29_SelectExpr()) :
                            alt22 = 1




                    if alt22 == 1:
                        # SelectExpr.g:184:31: LT arithmetic_expr
                        pass 
                        LT67=self.match(self.input, LT, self.FOLLOW_LT_in_compare_lt1678)
                        if self._state.backtracking == 0:

                            LT67_tree = self._adaptor.createWithPayload(LT67)
                            root_0 = self._adaptor.becomeRoot(LT67_tree, root_0)

                        self._state.following.append(self.FOLLOW_arithmetic_expr_in_compare_lt1681)
                        arithmetic_expr68 = self.arithmetic_expr()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, arithmetic_expr68.tree)


                    else:
                        break #loop22



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "compare_lt"

    class arithmetic_expr_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.arithmetic_expr_return, self).__init__()

            self.tree = None




    # $ANTLR start "arithmetic_expr"
    # SelectExpr.g:186:1: arithmetic_expr : arithmetic_sub_add ;
    def arithmetic_expr(self, ):

        retval = self.arithmetic_expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        arithmetic_sub_add69 = None



        try:
            try:
                # SelectExpr.g:186:17: ( arithmetic_sub_add )
                # SelectExpr.g:186:19: arithmetic_sub_add
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_arithmetic_sub_add_in_arithmetic_expr1692)
                arithmetic_sub_add69 = self.arithmetic_sub_add()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, arithmetic_sub_add69.tree)



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "arithmetic_expr"

    class arithmetic_sub_add_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.arithmetic_sub_add_return, self).__init__()

            self.tree = None




    # $ANTLR start "arithmetic_sub_add"
    # SelectExpr.g:187:1: arithmetic_sub_add : arithmetic_mul_div_mod ( ( SUB | ADD ) arithmetic_mul_div_mod )* ;
    def arithmetic_sub_add(self, ):

        retval = self.arithmetic_sub_add_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SUB71 = None
        ADD72 = None
        arithmetic_mul_div_mod70 = None

        arithmetic_mul_div_mod73 = None


        SUB71_tree = None
        ADD72_tree = None

        try:
            try:
                # SelectExpr.g:187:20: ( arithmetic_mul_div_mod ( ( SUB | ADD ) arithmetic_mul_div_mod )* )
                # SelectExpr.g:187:22: arithmetic_mul_div_mod ( ( SUB | ADD ) arithmetic_mul_div_mod )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_arithmetic_mul_div_mod_in_arithmetic_sub_add1700)
                arithmetic_mul_div_mod70 = self.arithmetic_mul_div_mod()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, arithmetic_mul_div_mod70.tree)
                # SelectExpr.g:187:45: ( ( SUB | ADD ) arithmetic_mul_div_mod )*
                while True: #loop24
                    alt24 = 2
                    LA24_0 = self.input.LA(1)

                    if (LA24_0 == SUB) :
                        LA24_2 = self.input.LA(2)

                        if (self.synpred31_SelectExpr()) :
                            alt24 = 1


                    elif (LA24_0 == ADD) :
                        LA24_3 = self.input.LA(2)

                        if (self.synpred31_SelectExpr()) :
                            alt24 = 1




                    if alt24 == 1:
                        # SelectExpr.g:187:46: ( SUB | ADD ) arithmetic_mul_div_mod
                        pass 
                        # SelectExpr.g:187:46: ( SUB | ADD )
                        alt23 = 2
                        LA23_0 = self.input.LA(1)

                        if (LA23_0 == SUB) :
                            alt23 = 1
                        elif (LA23_0 == ADD) :
                            alt23 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed

                            nvae = NoViableAltException("", 23, 0, self.input)

                            raise nvae

                        if alt23 == 1:
                            # SelectExpr.g:187:47: SUB
                            pass 
                            SUB71=self.match(self.input, SUB, self.FOLLOW_SUB_in_arithmetic_sub_add1704)
                            if self._state.backtracking == 0:

                                SUB71_tree = self._adaptor.createWithPayload(SUB71)
                                root_0 = self._adaptor.becomeRoot(SUB71_tree, root_0)



                        elif alt23 == 2:
                            # SelectExpr.g:187:52: ADD
                            pass 
                            ADD72=self.match(self.input, ADD, self.FOLLOW_ADD_in_arithmetic_sub_add1707)
                            if self._state.backtracking == 0:

                                ADD72_tree = self._adaptor.createWithPayload(ADD72)
                                root_0 = self._adaptor.becomeRoot(ADD72_tree, root_0)




                        self._state.following.append(self.FOLLOW_arithmetic_mul_div_mod_in_arithmetic_sub_add1711)
                        arithmetic_mul_div_mod73 = self.arithmetic_mul_div_mod()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, arithmetic_mul_div_mod73.tree)


                    else:
                        break #loop24



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "arithmetic_sub_add"

    class arithmetic_mul_div_mod_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.arithmetic_mul_div_mod_return, self).__init__()

            self.tree = None




    # $ANTLR start "arithmetic_mul_div_mod"
    # SelectExpr.g:188:1: arithmetic_mul_div_mod : arithmetic_pow ( ( MUL | DIV | MOD ) arithmetic_pow )* ;
    def arithmetic_mul_div_mod(self, ):

        retval = self.arithmetic_mul_div_mod_return()
        retval.start = self.input.LT(1)

        root_0 = None

        MUL75 = None
        DIV76 = None
        MOD77 = None
        arithmetic_pow74 = None

        arithmetic_pow78 = None


        MUL75_tree = None
        DIV76_tree = None
        MOD77_tree = None

        try:
            try:
                # SelectExpr.g:188:24: ( arithmetic_pow ( ( MUL | DIV | MOD ) arithmetic_pow )* )
                # SelectExpr.g:188:26: arithmetic_pow ( ( MUL | DIV | MOD ) arithmetic_pow )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_arithmetic_pow_in_arithmetic_mul_div_mod1721)
                arithmetic_pow74 = self.arithmetic_pow()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, arithmetic_pow74.tree)
                # SelectExpr.g:188:41: ( ( MUL | DIV | MOD ) arithmetic_pow )*
                while True: #loop26
                    alt26 = 2
                    LA26 = self.input.LA(1)
                    if LA26 == MUL:
                        LA26_2 = self.input.LA(2)

                        if (self.synpred34_SelectExpr()) :
                            alt26 = 1


                    elif LA26 == DIV:
                        LA26_3 = self.input.LA(2)

                        if (self.synpred34_SelectExpr()) :
                            alt26 = 1


                    elif LA26 == MOD:
                        LA26_4 = self.input.LA(2)

                        if (self.synpred34_SelectExpr()) :
                            alt26 = 1



                    if alt26 == 1:
                        # SelectExpr.g:188:42: ( MUL | DIV | MOD ) arithmetic_pow
                        pass 
                        # SelectExpr.g:188:42: ( MUL | DIV | MOD )
                        alt25 = 3
                        LA25 = self.input.LA(1)
                        if LA25 == MUL:
                            alt25 = 1
                        elif LA25 == DIV:
                            alt25 = 2
                        elif LA25 == MOD:
                            alt25 = 3
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed

                            nvae = NoViableAltException("", 25, 0, self.input)

                            raise nvae

                        if alt25 == 1:
                            # SelectExpr.g:188:43: MUL
                            pass 
                            MUL75=self.match(self.input, MUL, self.FOLLOW_MUL_in_arithmetic_mul_div_mod1725)
                            if self._state.backtracking == 0:

                                MUL75_tree = self._adaptor.createWithPayload(MUL75)
                                root_0 = self._adaptor.becomeRoot(MUL75_tree, root_0)



                        elif alt25 == 2:
                            # SelectExpr.g:188:50: DIV
                            pass 
                            DIV76=self.match(self.input, DIV, self.FOLLOW_DIV_in_arithmetic_mul_div_mod1730)
                            if self._state.backtracking == 0:

                                DIV76_tree = self._adaptor.createWithPayload(DIV76)
                                root_0 = self._adaptor.becomeRoot(DIV76_tree, root_0)



                        elif alt25 == 3:
                            # SelectExpr.g:188:57: MOD
                            pass 
                            MOD77=self.match(self.input, MOD, self.FOLLOW_MOD_in_arithmetic_mul_div_mod1735)
                            if self._state.backtracking == 0:

                                MOD77_tree = self._adaptor.createWithPayload(MOD77)
                                root_0 = self._adaptor.becomeRoot(MOD77_tree, root_0)




                        self._state.following.append(self.FOLLOW_arithmetic_pow_in_arithmetic_mul_div_mod1739)
                        arithmetic_pow78 = self.arithmetic_pow()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, arithmetic_pow78.tree)


                    else:
                        break #loop26



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "arithmetic_mul_div_mod"

    class arithmetic_pow_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.arithmetic_pow_return, self).__init__()

            self.tree = None




    # $ANTLR start "arithmetic_pow"
    # SelectExpr.g:189:1: arithmetic_pow : arithmetic_unary ( POW arithmetic_unary )* ;
    def arithmetic_pow(self, ):

        retval = self.arithmetic_pow_return()
        retval.start = self.input.LT(1)

        root_0 = None

        POW80 = None
        arithmetic_unary79 = None

        arithmetic_unary81 = None


        POW80_tree = None

        try:
            try:
                # SelectExpr.g:189:16: ( arithmetic_unary ( POW arithmetic_unary )* )
                # SelectExpr.g:189:18: arithmetic_unary ( POW arithmetic_unary )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_arithmetic_unary_in_arithmetic_pow1749)
                arithmetic_unary79 = self.arithmetic_unary()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, arithmetic_unary79.tree)
                # SelectExpr.g:189:35: ( POW arithmetic_unary )*
                while True: #loop27
                    alt27 = 2
                    LA27_0 = self.input.LA(1)

                    if (LA27_0 == POW) :
                        LA27_2 = self.input.LA(2)

                        if (self.synpred35_SelectExpr()) :
                            alt27 = 1




                    if alt27 == 1:
                        # SelectExpr.g:189:36: POW arithmetic_unary
                        pass 
                        POW80=self.match(self.input, POW, self.FOLLOW_POW_in_arithmetic_pow1752)
                        if self._state.backtracking == 0:

                            POW80_tree = self._adaptor.createWithPayload(POW80)
                            root_0 = self._adaptor.becomeRoot(POW80_tree, root_0)

                        self._state.following.append(self.FOLLOW_arithmetic_unary_in_arithmetic_pow1755)
                        arithmetic_unary81 = self.arithmetic_unary()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, arithmetic_unary81.tree)


                    else:
                        break #loop27



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "arithmetic_pow"

    class arithmetic_unary_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.arithmetic_unary_return, self).__init__()

            self.tree = None




    # $ANTLR start "arithmetic_unary"
    # SelectExpr.g:190:1: arithmetic_unary : ( SUB atom -> ^( NEG atom ) | ADD atom -> ^( POS atom ) | atom );
    def arithmetic_unary(self, ):

        retval = self.arithmetic_unary_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SUB82 = None
        ADD84 = None
        atom83 = None

        atom85 = None

        atom86 = None


        SUB82_tree = None
        ADD84_tree = None
        stream_SUB = RewriteRuleTokenStream(self._adaptor, "token SUB")
        stream_ADD = RewriteRuleTokenStream(self._adaptor, "token ADD")
        stream_atom = RewriteRuleSubtreeStream(self._adaptor, "rule atom")
        try:
            try:
                # SelectExpr.g:190:18: ( SUB atom -> ^( NEG atom ) | ADD atom -> ^( POS atom ) | atom )
                alt28 = 3
                LA28 = self.input.LA(1)
                if LA28 == SUB:
                    alt28 = 1
                elif LA28 == ADD:
                    alt28 = 2
                elif LA28 == LIST_BEGIN or LA28 == SELECT or LA28 == THIS or LA28 == STRING or LA28 == INTEGER or LA28 == FLOAT or LA28 == TRUE or LA28 == FALSE or LA28 == PHRASE or LA28 == 91:
                    alt28 = 3
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed

                    nvae = NoViableAltException("", 28, 0, self.input)

                    raise nvae

                if alt28 == 1:
                    # SelectExpr.g:191:2: SUB atom
                    pass 
                    SUB82=self.match(self.input, SUB, self.FOLLOW_SUB_in_arithmetic_unary1766) 
                    if self._state.backtracking == 0:
                        stream_SUB.add(SUB82)
                    self._state.following.append(self.FOLLOW_atom_in_arithmetic_unary1768)
                    atom83 = self.atom()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stream_atom.add(atom83.tree)

                    # AST Rewrite
                    # elements: atom
                    # token labels: 
                    # rule labels: retval
                    # token list labels: 
                    # rule list labels: 
                    # wildcard labels: 
                    if self._state.backtracking == 0:

                        retval.tree = root_0

                        if retval is not None:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                        else:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                        root_0 = self._adaptor.nil()
                        # 191:11: -> ^( NEG atom )
                        # SelectExpr.g:191:14: ^( NEG atom )
                        root_1 = self._adaptor.nil()
                        root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(NEG, "NEG"), root_1)

                        self._adaptor.addChild(root_1, stream_atom.nextTree())

                        self._adaptor.addChild(root_0, root_1)



                        retval.tree = root_0


                elif alt28 == 2:
                    # SelectExpr.g:192:5: ADD atom
                    pass 
                    ADD84=self.match(self.input, ADD, self.FOLLOW_ADD_in_arithmetic_unary1782) 
                    if self._state.backtracking == 0:
                        stream_ADD.add(ADD84)
                    self._state.following.append(self.FOLLOW_atom_in_arithmetic_unary1784)
                    atom85 = self.atom()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stream_atom.add(atom85.tree)

                    # AST Rewrite
                    # elements: atom
                    # token labels: 
                    # rule labels: retval
                    # token list labels: 
                    # rule list labels: 
                    # wildcard labels: 
                    if self._state.backtracking == 0:

                        retval.tree = root_0

                        if retval is not None:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                        else:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                        root_0 = self._adaptor.nil()
                        # 192:14: -> ^( POS atom )
                        # SelectExpr.g:192:17: ^( POS atom )
                        root_1 = self._adaptor.nil()
                        root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(POS, "POS"), root_1)

                        self._adaptor.addChild(root_1, stream_atom.nextTree())

                        self._adaptor.addChild(root_0, root_1)



                        retval.tree = root_0


                elif alt28 == 3:
                    # SelectExpr.g:193:5: atom
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_atom_in_arithmetic_unary1798)
                    atom86 = self.atom()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, atom86.tree)


                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "arithmetic_unary"

    class atom_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.atom_return, self).__init__()

            self.tree = None




    # $ANTLR start "atom"
    # SelectExpr.g:196:1: atom : ( value | variable | function | '(' expr ')' | statement_select );
    def atom(self, ):

        retval = self.atom_return()
        retval.start = self.input.LT(1)

        root_0 = None

        char_literal90 = None
        char_literal92 = None
        value87 = None

        variable88 = None

        function89 = None

        expr91 = None

        statement_select93 = None


        char_literal90_tree = None
        char_literal92_tree = None

        try:
            try:
                # SelectExpr.g:197:2: ( value | variable | function | '(' expr ')' | statement_select )
                alt29 = 5
                LA29 = self.input.LA(1)
                if LA29 == LIST_BEGIN or LA29 == THIS or LA29 == STRING or LA29 == INTEGER or LA29 == FLOAT or LA29 == TRUE or LA29 == FALSE:
                    alt29 = 1
                elif LA29 == PHRASE:
                    LA29 = self.input.LA(2)
                    if LA29 == DOT:
                        alt29 = 1
                    elif LA29 == 91:
                        alt29 = 3
                    elif LA29 == EOF or LA29 == SEP or LA29 == END or LA29 == AND or LA29 == XOR or LA29 == OR or LA29 == IN or LA29 == EQ or LA29 == NE or LA29 == LE or LA29 == GE or LA29 == LT or LA29 == GT or LA29 == ADD or LA29 == SUB or LA29 == MUL or LA29 == DIV or LA29 == MOD or LA29 == POW or LA29 == LIST_END or LA29 == AGE_BEGIN or LA29 == AGE_END or LA29 == WHERE or LA29 == AS or LA29 == 92:
                        alt29 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed

                        nvae = NoViableAltException("", 29, 2, self.input)

                        raise nvae

                elif LA29 == 91:
                    alt29 = 4
                elif LA29 == SELECT:
                    alt29 = 5
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed

                    nvae = NoViableAltException("", 29, 0, self.input)

                    raise nvae

                if alt29 == 1:
                    # SelectExpr.g:197:4: value
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_value_in_atom1809)
                    value87 = self.value()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, value87.tree)


                elif alt29 == 2:
                    # SelectExpr.g:198:4: variable
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_variable_in_atom1814)
                    variable88 = self.variable()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, variable88.tree)


                elif alt29 == 3:
                    # SelectExpr.g:199:4: function
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_function_in_atom1819)
                    function89 = self.function()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, function89.tree)


                elif alt29 == 4:
                    # SelectExpr.g:200:4: '(' expr ')'
                    pass 
                    root_0 = self._adaptor.nil()

                    char_literal90=self.match(self.input, 91, self.FOLLOW_91_in_atom1824)
                    self._state.following.append(self.FOLLOW_expr_in_atom1827)
                    expr91 = self.expr()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, expr91.tree)
                    char_literal92=self.match(self.input, 92, self.FOLLOW_92_in_atom1829)


                elif alt29 == 5:
                    # SelectExpr.g:201:4: statement_select
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_statement_select_in_atom1835)
                    statement_select93 = self.statement_select()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, statement_select93.tree)


                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "atom"

    class function_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.function_return, self).__init__()

            self.tree = None




    # $ANTLR start "function"
    # SelectExpr.g:204:1: function : PHRASE '(' ( parameter )? ')' -> ^( FCT PHRASE ( parameter )? ) ;
    def function(self, ):

        retval = self.function_return()
        retval.start = self.input.LT(1)

        root_0 = None

        PHRASE94 = None
        char_literal95 = None
        char_literal97 = None
        parameter96 = None


        PHRASE94_tree = None
        char_literal95_tree = None
        char_literal97_tree = None
        stream_92 = RewriteRuleTokenStream(self._adaptor, "token 92")
        stream_91 = RewriteRuleTokenStream(self._adaptor, "token 91")
        stream_PHRASE = RewriteRuleTokenStream(self._adaptor, "token PHRASE")
        stream_parameter = RewriteRuleSubtreeStream(self._adaptor, "rule parameter")
        try:
            try:
                # SelectExpr.g:204:10: ( PHRASE '(' ( parameter )? ')' -> ^( FCT PHRASE ( parameter )? ) )
                # SelectExpr.g:204:12: PHRASE '(' ( parameter )? ')'
                pass 
                PHRASE94=self.match(self.input, PHRASE, self.FOLLOW_PHRASE_in_function1844) 
                if self._state.backtracking == 0:
                    stream_PHRASE.add(PHRASE94)
                char_literal95=self.match(self.input, 91, self.FOLLOW_91_in_function1846) 
                if self._state.backtracking == 0:
                    stream_91.add(char_literal95)
                # SelectExpr.g:204:23: ( parameter )?
                alt30 = 2
                LA30_0 = self.input.LA(1)

                if (LA30_0 == NOT or (ADD <= LA30_0 <= SUB) or LA30_0 == LIST_BEGIN or LA30_0 == SELECT or LA30_0 == THIS or LA30_0 == STRING or (INTEGER <= LA30_0 <= FALSE) or LA30_0 == PHRASE or LA30_0 == 91) :
                    alt30 = 1
                if alt30 == 1:
                    # SelectExpr.g:0:0: parameter
                    pass 
                    self._state.following.append(self.FOLLOW_parameter_in_function1848)
                    parameter96 = self.parameter()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stream_parameter.add(parameter96.tree)



                char_literal97=self.match(self.input, 92, self.FOLLOW_92_in_function1851) 
                if self._state.backtracking == 0:
                    stream_92.add(char_literal97)

                # AST Rewrite
                # elements: parameter, PHRASE
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                if self._state.backtracking == 0:

                    retval.tree = root_0

                    if retval is not None:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                    else:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                    root_0 = self._adaptor.nil()
                    # 204:38: -> ^( FCT PHRASE ( parameter )? )
                    # SelectExpr.g:204:41: ^( FCT PHRASE ( parameter )? )
                    root_1 = self._adaptor.nil()
                    root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(FCT, "FCT"), root_1)

                    self._adaptor.addChild(root_1, stream_PHRASE.nextNode())
                    # SelectExpr.g:204:54: ( parameter )?
                    if stream_parameter.hasNext():
                        self._adaptor.addChild(root_1, stream_parameter.nextTree())


                    stream_parameter.reset();

                    self._adaptor.addChild(root_0, root_1)



                    retval.tree = root_0



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "function"

    class parameter_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.parameter_return, self).__init__()

            self.tree = None




    # $ANTLR start "parameter"
    # SelectExpr.g:207:1: parameter : expr ( SEP expr )* ;
    def parameter(self, ):

        retval = self.parameter_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SEP99 = None
        expr98 = None

        expr100 = None


        SEP99_tree = None

        try:
            try:
                # SelectExpr.g:207:11: ( expr ( SEP expr )* )
                # SelectExpr.g:207:13: expr ( SEP expr )*
                pass 
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_expr_in_parameter1871)
                expr98 = self.expr()

                self._state.following.pop()
                if self._state.backtracking == 0:
                    self._adaptor.addChild(root_0, expr98.tree)
                # SelectExpr.g:207:18: ( SEP expr )*
                while True: #loop31
                    alt31 = 2
                    LA31_0 = self.input.LA(1)

                    if (LA31_0 == SEP) :
                        alt31 = 1


                    if alt31 == 1:
                        # SelectExpr.g:207:19: SEP expr
                        pass 
                        SEP99=self.match(self.input, SEP, self.FOLLOW_SEP_in_parameter1874)
                        self._state.following.append(self.FOLLOW_expr_in_parameter1877)
                        expr100 = self.expr()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            self._adaptor.addChild(root_0, expr100.tree)


                    else:
                        break #loop31



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "parameter"

    class variable_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.variable_return, self).__init__()

            self.tree = None




    # $ANTLR start "variable"
    # SelectExpr.g:210:1: variable : PHRASE ( age )? -> ^( VAR PHRASE ( age )? ) ;
    def variable(self, ):

        retval = self.variable_return()
        retval.start = self.input.LT(1)

        root_0 = None

        PHRASE101 = None
        age102 = None


        PHRASE101_tree = None
        stream_PHRASE = RewriteRuleTokenStream(self._adaptor, "token PHRASE")
        stream_age = RewriteRuleSubtreeStream(self._adaptor, "rule age")
        try:
            try:
                # SelectExpr.g:210:10: ( PHRASE ( age )? -> ^( VAR PHRASE ( age )? ) )
                # SelectExpr.g:210:12: PHRASE ( age )?
                pass 
                PHRASE101=self.match(self.input, PHRASE, self.FOLLOW_PHRASE_in_variable1888) 
                if self._state.backtracking == 0:
                    stream_PHRASE.add(PHRASE101)
                # SelectExpr.g:210:19: ( age )?
                alt32 = 2
                LA32_0 = self.input.LA(1)

                if (LA32_0 == AGE_BEGIN) :
                    alt32 = 1
                if alt32 == 1:
                    # SelectExpr.g:210:20: age
                    pass 
                    self._state.following.append(self.FOLLOW_age_in_variable1891)
                    age102 = self.age()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stream_age.add(age102.tree)




                # AST Rewrite
                # elements: age, PHRASE
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                if self._state.backtracking == 0:

                    retval.tree = root_0

                    if retval is not None:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                    else:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                    root_0 = self._adaptor.nil()
                    # 210:26: -> ^( VAR PHRASE ( age )? )
                    # SelectExpr.g:210:29: ^( VAR PHRASE ( age )? )
                    root_1 = self._adaptor.nil()
                    root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(VAR, "VAR"), root_1)

                    self._adaptor.addChild(root_1, stream_PHRASE.nextNode())
                    # SelectExpr.g:210:42: ( age )?
                    if stream_age.hasNext():
                        self._adaptor.addChild(root_1, stream_age.nextTree())


                    stream_age.reset();

                    self._adaptor.addChild(root_0, root_1)



                    retval.tree = root_0



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "variable"

    class age_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.age_return, self).__init__()

            self.tree = None




    # $ANTLR start "age"
    # SelectExpr.g:213:1: age : AGE_BEGIN ( expr )? AGE_END -> ^( AGE ( expr )? ) ;
    def age(self, ):

        retval = self.age_return()
        retval.start = self.input.LT(1)

        root_0 = None

        AGE_BEGIN103 = None
        AGE_END105 = None
        expr104 = None


        AGE_BEGIN103_tree = None
        AGE_END105_tree = None
        stream_AGE_BEGIN = RewriteRuleTokenStream(self._adaptor, "token AGE_BEGIN")
        stream_AGE_END = RewriteRuleTokenStream(self._adaptor, "token AGE_END")
        stream_expr = RewriteRuleSubtreeStream(self._adaptor, "rule expr")
        try:
            try:
                # SelectExpr.g:213:5: ( AGE_BEGIN ( expr )? AGE_END -> ^( AGE ( expr )? ) )
                # SelectExpr.g:213:7: AGE_BEGIN ( expr )? AGE_END
                pass 
                AGE_BEGIN103=self.match(self.input, AGE_BEGIN, self.FOLLOW_AGE_BEGIN_in_age1915) 
                if self._state.backtracking == 0:
                    stream_AGE_BEGIN.add(AGE_BEGIN103)
                # SelectExpr.g:213:17: ( expr )?
                alt33 = 2
                LA33_0 = self.input.LA(1)

                if (LA33_0 == NOT or (ADD <= LA33_0 <= SUB) or LA33_0 == LIST_BEGIN or LA33_0 == SELECT or LA33_0 == THIS or LA33_0 == STRING or (INTEGER <= LA33_0 <= FALSE) or LA33_0 == PHRASE or LA33_0 == 91) :
                    alt33 = 1
                if alt33 == 1:
                    # SelectExpr.g:0:0: expr
                    pass 
                    self._state.following.append(self.FOLLOW_expr_in_age1917)
                    expr104 = self.expr()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stream_expr.add(expr104.tree)



                AGE_END105=self.match(self.input, AGE_END, self.FOLLOW_AGE_END_in_age1920) 
                if self._state.backtracking == 0:
                    stream_AGE_END.add(AGE_END105)

                # AST Rewrite
                # elements: expr
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                if self._state.backtracking == 0:

                    retval.tree = root_0

                    if retval is not None:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                    else:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                    root_0 = self._adaptor.nil()
                    # 213:31: -> ^( AGE ( expr )? )
                    # SelectExpr.g:213:34: ^( AGE ( expr )? )
                    root_1 = self._adaptor.nil()
                    root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(AGE, "AGE"), root_1)

                    # SelectExpr.g:213:40: ( expr )?
                    if stream_expr.hasNext():
                        self._adaptor.addChild(root_1, stream_expr.nextTree())


                    stream_expr.reset();

                    self._adaptor.addChild(root_0, root_1)



                    retval.tree = root_0



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "age"

    class value_return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.value_return, self).__init__()

            self.tree = None




    # $ANTLR start "value"
    # SelectExpr.g:216:1: value : ( STRING -> ^( VAL STRING ) | FLOAT -> ^( VAL FLOAT ) | INTEGER -> ^( VAL INTEGER ) | TRUE -> ^( VAL TRUE ) | FALSE -> ^( VAL FALSE ) | this_ | list_ );
    def value(self, ):

        retval = self.value_return()
        retval.start = self.input.LT(1)

        root_0 = None

        STRING106 = None
        FLOAT107 = None
        INTEGER108 = None
        TRUE109 = None
        FALSE110 = None
        this_111 = None

        list_112 = None


        STRING106_tree = None
        FLOAT107_tree = None
        INTEGER108_tree = None
        TRUE109_tree = None
        FALSE110_tree = None
        stream_INTEGER = RewriteRuleTokenStream(self._adaptor, "token INTEGER")
        stream_FLOAT = RewriteRuleTokenStream(self._adaptor, "token FLOAT")
        stream_FALSE = RewriteRuleTokenStream(self._adaptor, "token FALSE")
        stream_TRUE = RewriteRuleTokenStream(self._adaptor, "token TRUE")
        stream_STRING = RewriteRuleTokenStream(self._adaptor, "token STRING")

        try:
            try:
                # SelectExpr.g:216:7: ( STRING -> ^( VAL STRING ) | FLOAT -> ^( VAL FLOAT ) | INTEGER -> ^( VAL INTEGER ) | TRUE -> ^( VAL TRUE ) | FALSE -> ^( VAL FALSE ) | this_ | list_ )
                alt34 = 7
                LA34 = self.input.LA(1)
                if LA34 == STRING:
                    alt34 = 1
                elif LA34 == FLOAT:
                    alt34 = 2
                elif LA34 == INTEGER:
                    alt34 = 3
                elif LA34 == TRUE:
                    alt34 = 4
                elif LA34 == FALSE:
                    alt34 = 5
                elif LA34 == THIS or LA34 == PHRASE:
                    alt34 = 6
                elif LA34 == LIST_BEGIN:
                    alt34 = 7
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed

                    nvae = NoViableAltException("", 34, 0, self.input)

                    raise nvae

                if alt34 == 1:
                    # SelectExpr.g:216:9: STRING
                    pass 
                    STRING106=self.match(self.input, STRING, self.FOLLOW_STRING_in_value1938) 
                    if self._state.backtracking == 0:
                        stream_STRING.add(STRING106)

                    # AST Rewrite
                    # elements: STRING
                    # token labels: 
                    # rule labels: retval
                    # token list labels: 
                    # rule list labels: 
                    # wildcard labels: 
                    if self._state.backtracking == 0:

                        retval.tree = root_0

                        if retval is not None:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                        else:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                        root_0 = self._adaptor.nil()
                        # 216:17: -> ^( VAL STRING )
                        # SelectExpr.g:216:20: ^( VAL STRING )
                        root_1 = self._adaptor.nil()
                        root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(VAL, "VAL"), root_1)

                        self._adaptor.addChild(root_1, stream_STRING.nextNode())

                        self._adaptor.addChild(root_0, root_1)



                        retval.tree = root_0


                elif alt34 == 2:
                    # SelectExpr.g:217:4: FLOAT
                    pass 
                    FLOAT107=self.match(self.input, FLOAT, self.FOLLOW_FLOAT_in_value1952) 
                    if self._state.backtracking == 0:
                        stream_FLOAT.add(FLOAT107)

                    # AST Rewrite
                    # elements: FLOAT
                    # token labels: 
                    # rule labels: retval
                    # token list labels: 
                    # rule list labels: 
                    # wildcard labels: 
                    if self._state.backtracking == 0:

                        retval.tree = root_0

                        if retval is not None:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                        else:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                        root_0 = self._adaptor.nil()
                        # 217:11: -> ^( VAL FLOAT )
                        # SelectExpr.g:217:14: ^( VAL FLOAT )
                        root_1 = self._adaptor.nil()
                        root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(VAL, "VAL"), root_1)

                        self._adaptor.addChild(root_1, stream_FLOAT.nextNode())

                        self._adaptor.addChild(root_0, root_1)



                        retval.tree = root_0


                elif alt34 == 3:
                    # SelectExpr.g:218:4: INTEGER
                    pass 
                    INTEGER108=self.match(self.input, INTEGER, self.FOLLOW_INTEGER_in_value1966) 
                    if self._state.backtracking == 0:
                        stream_INTEGER.add(INTEGER108)

                    # AST Rewrite
                    # elements: INTEGER
                    # token labels: 
                    # rule labels: retval
                    # token list labels: 
                    # rule list labels: 
                    # wildcard labels: 
                    if self._state.backtracking == 0:

                        retval.tree = root_0

                        if retval is not None:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                        else:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                        root_0 = self._adaptor.nil()
                        # 218:12: -> ^( VAL INTEGER )
                        # SelectExpr.g:218:15: ^( VAL INTEGER )
                        root_1 = self._adaptor.nil()
                        root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(VAL, "VAL"), root_1)

                        self._adaptor.addChild(root_1, stream_INTEGER.nextNode())

                        self._adaptor.addChild(root_0, root_1)



                        retval.tree = root_0


                elif alt34 == 4:
                    # SelectExpr.g:219:4: TRUE
                    pass 
                    TRUE109=self.match(self.input, TRUE, self.FOLLOW_TRUE_in_value1979) 
                    if self._state.backtracking == 0:
                        stream_TRUE.add(TRUE109)

                    # AST Rewrite
                    # elements: TRUE
                    # token labels: 
                    # rule labels: retval
                    # token list labels: 
                    # rule list labels: 
                    # wildcard labels: 
                    if self._state.backtracking == 0:

                        retval.tree = root_0

                        if retval is not None:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                        else:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                        root_0 = self._adaptor.nil()
                        # 219:10: -> ^( VAL TRUE )
                        # SelectExpr.g:219:13: ^( VAL TRUE )
                        root_1 = self._adaptor.nil()
                        root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(VAL, "VAL"), root_1)

                        self._adaptor.addChild(root_1, stream_TRUE.nextNode())

                        self._adaptor.addChild(root_0, root_1)



                        retval.tree = root_0


                elif alt34 == 5:
                    # SelectExpr.g:220:4: FALSE
                    pass 
                    FALSE110=self.match(self.input, FALSE, self.FOLLOW_FALSE_in_value1993) 
                    if self._state.backtracking == 0:
                        stream_FALSE.add(FALSE110)

                    # AST Rewrite
                    # elements: FALSE
                    # token labels: 
                    # rule labels: retval
                    # token list labels: 
                    # rule list labels: 
                    # wildcard labels: 
                    if self._state.backtracking == 0:

                        retval.tree = root_0

                        if retval is not None:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                        else:
                            stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                        root_0 = self._adaptor.nil()
                        # 220:11: -> ^( VAL FALSE )
                        # SelectExpr.g:220:14: ^( VAL FALSE )
                        root_1 = self._adaptor.nil()
                        root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(VAL, "VAL"), root_1)

                        self._adaptor.addChild(root_1, stream_FALSE.nextNode())

                        self._adaptor.addChild(root_0, root_1)



                        retval.tree = root_0


                elif alt34 == 6:
                    # SelectExpr.g:221:4: this_
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_this__in_value2007)
                    this_111 = self.this_()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, this_111.tree)


                elif alt34 == 7:
                    # SelectExpr.g:222:4: list_
                    pass 
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_list__in_value2012)
                    list_112 = self.list_()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        self._adaptor.addChild(root_0, list_112.tree)


                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "value"

    class this__return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.this__return, self).__init__()

            self.tree = None




    # $ANTLR start "this_"
    # SelectExpr.g:225:1: this_ : ( PHRASE DOT )? THIS -> ^( THIS ( PHRASE )? ) ;
    def this_(self, ):

        retval = self.this__return()
        retval.start = self.input.LT(1)

        root_0 = None

        PHRASE113 = None
        DOT114 = None
        THIS115 = None

        PHRASE113_tree = None
        DOT114_tree = None
        THIS115_tree = None
        stream_DOT = RewriteRuleTokenStream(self._adaptor, "token DOT")
        stream_PHRASE = RewriteRuleTokenStream(self._adaptor, "token PHRASE")
        stream_THIS = RewriteRuleTokenStream(self._adaptor, "token THIS")

        try:
            try:
                # SelectExpr.g:225:7: ( ( PHRASE DOT )? THIS -> ^( THIS ( PHRASE )? ) )
                # SelectExpr.g:225:9: ( PHRASE DOT )? THIS
                pass 
                # SelectExpr.g:225:9: ( PHRASE DOT )?
                alt35 = 2
                LA35_0 = self.input.LA(1)

                if (LA35_0 == PHRASE) :
                    alt35 = 1
                if alt35 == 1:
                    # SelectExpr.g:225:10: PHRASE DOT
                    pass 
                    PHRASE113=self.match(self.input, PHRASE, self.FOLLOW_PHRASE_in_this_2023) 
                    if self._state.backtracking == 0:
                        stream_PHRASE.add(PHRASE113)
                    DOT114=self.match(self.input, DOT, self.FOLLOW_DOT_in_this_2025) 
                    if self._state.backtracking == 0:
                        stream_DOT.add(DOT114)



                THIS115=self.match(self.input, THIS, self.FOLLOW_THIS_in_this_2029) 
                if self._state.backtracking == 0:
                    stream_THIS.add(THIS115)

                # AST Rewrite
                # elements: THIS, PHRASE
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                if self._state.backtracking == 0:

                    retval.tree = root_0

                    if retval is not None:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                    else:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                    root_0 = self._adaptor.nil()
                    # 225:29: -> ^( THIS ( PHRASE )? )
                    # SelectExpr.g:225:32: ^( THIS ( PHRASE )? )
                    root_1 = self._adaptor.nil()
                    root_1 = self._adaptor.becomeRoot(stream_THIS.nextNode(), root_1)

                    # SelectExpr.g:225:39: ( PHRASE )?
                    if stream_PHRASE.hasNext():
                        self._adaptor.addChild(root_1, stream_PHRASE.nextNode())


                    stream_PHRASE.reset();

                    self._adaptor.addChild(root_0, root_1)



                    retval.tree = root_0



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "this_"

    class list__return(ParserRuleReturnScope):
        def __init__(self):
            super(SelectExprParser.list__return, self).__init__()

            self.tree = None




    # $ANTLR start "list_"
    # SelectExpr.g:228:1: list_ : LIST_BEGIN ( ( expr )? ( SEP expr )* ) LIST_END -> ^( LIST ( expr )* ) ;
    def list_(self, ):

        retval = self.list__return()
        retval.start = self.input.LT(1)

        root_0 = None

        LIST_BEGIN116 = None
        SEP118 = None
        LIST_END120 = None
        expr117 = None

        expr119 = None


        LIST_BEGIN116_tree = None
        SEP118_tree = None
        LIST_END120_tree = None
        stream_LIST_END = RewriteRuleTokenStream(self._adaptor, "token LIST_END")
        stream_SEP = RewriteRuleTokenStream(self._adaptor, "token SEP")
        stream_LIST_BEGIN = RewriteRuleTokenStream(self._adaptor, "token LIST_BEGIN")
        stream_expr = RewriteRuleSubtreeStream(self._adaptor, "rule expr")
        try:
            try:
                # SelectExpr.g:228:7: ( LIST_BEGIN ( ( expr )? ( SEP expr )* ) LIST_END -> ^( LIST ( expr )* ) )
                # SelectExpr.g:228:10: LIST_BEGIN ( ( expr )? ( SEP expr )* ) LIST_END
                pass 
                LIST_BEGIN116=self.match(self.input, LIST_BEGIN, self.FOLLOW_LIST_BEGIN_in_list_2050) 
                if self._state.backtracking == 0:
                    stream_LIST_BEGIN.add(LIST_BEGIN116)
                # SelectExpr.g:228:21: ( ( expr )? ( SEP expr )* )
                # SelectExpr.g:228:23: ( expr )? ( SEP expr )*
                pass 
                # SelectExpr.g:228:23: ( expr )?
                alt36 = 2
                LA36_0 = self.input.LA(1)

                if (LA36_0 == NOT or (ADD <= LA36_0 <= SUB) or LA36_0 == LIST_BEGIN or LA36_0 == SELECT or LA36_0 == THIS or LA36_0 == STRING or (INTEGER <= LA36_0 <= FALSE) or LA36_0 == PHRASE or LA36_0 == 91) :
                    alt36 = 1
                if alt36 == 1:
                    # SelectExpr.g:0:0: expr
                    pass 
                    self._state.following.append(self.FOLLOW_expr_in_list_2054)
                    expr117 = self.expr()

                    self._state.following.pop()
                    if self._state.backtracking == 0:
                        stream_expr.add(expr117.tree)



                # SelectExpr.g:228:29: ( SEP expr )*
                while True: #loop37
                    alt37 = 2
                    LA37_0 = self.input.LA(1)

                    if (LA37_0 == SEP) :
                        alt37 = 1


                    if alt37 == 1:
                        # SelectExpr.g:228:30: SEP expr
                        pass 
                        SEP118=self.match(self.input, SEP, self.FOLLOW_SEP_in_list_2058) 
                        if self._state.backtracking == 0:
                            stream_SEP.add(SEP118)
                        self._state.following.append(self.FOLLOW_expr_in_list_2060)
                        expr119 = self.expr()

                        self._state.following.pop()
                        if self._state.backtracking == 0:
                            stream_expr.add(expr119.tree)


                    else:
                        break #loop37



                LIST_END120=self.match(self.input, LIST_END, self.FOLLOW_LIST_END_in_list_2066) 
                if self._state.backtracking == 0:
                    stream_LIST_END.add(LIST_END120)

                # AST Rewrite
                # elements: expr
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 
                # wildcard labels: 
                if self._state.backtracking == 0:

                    retval.tree = root_0

                    if retval is not None:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                    else:
                        stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                    root_0 = self._adaptor.nil()
                    # 228:52: -> ^( LIST ( expr )* )
                    # SelectExpr.g:228:55: ^( LIST ( expr )* )
                    root_1 = self._adaptor.nil()
                    root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(LIST, "LIST"), root_1)

                    # SelectExpr.g:228:62: ( expr )*
                    while stream_expr.hasNext():
                        self._adaptor.addChild(root_1, stream_expr.nextTree())


                    stream_expr.reset();

                    self._adaptor.addChild(root_0, root_1)



                    retval.tree = root_0



                retval.stop = self.input.LT(-1)

                if self._state.backtracking == 0:

                    retval.tree = self._adaptor.rulePostProcessing(root_0)
                    self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "list_"

    # $ANTLR start "synpred2_SelectExpr"
    def synpred2_SelectExpr_fragment(self, ):
        # SelectExpr.g:145:13: ( statement_select END )
        # SelectExpr.g:145:13: statement_select END
        pass 
        self._state.following.append(self.FOLLOW_statement_select_in_synpred2_SelectExpr1269)
        self.statement_select()

        self._state.following.pop()
        self.match(self.input, END, self.FOLLOW_END_in_synpred2_SelectExpr1271)


    # $ANTLR end "synpred2_SelectExpr"



    # $ANTLR start "synpred3_SelectExpr"
    def synpred3_SelectExpr_fragment(self, ):
        # SelectExpr.g:146:4: ( expr END )
        # SelectExpr.g:146:4: expr END
        pass 
        self._state.following.append(self.FOLLOW_expr_in_synpred3_SelectExpr1277)
        self.expr()

        self._state.following.pop()
        self.match(self.input, END, self.FOLLOW_END_in_synpred3_SelectExpr1279)


    # $ANTLR end "synpred3_SelectExpr"



    # $ANTLR start "synpred4_SelectExpr"
    def synpred4_SelectExpr_fragment(self, ):
        # SelectExpr.g:151:17: ( where_ )
        # SelectExpr.g:151:17: where_
        pass 
        self._state.following.append(self.FOLLOW_where__in_synpred4_SelectExpr1301)
        self.where_()

        self._state.following.pop()


    # $ANTLR end "synpred4_SelectExpr"



    # $ANTLR start "synpred5_SelectExpr"
    def synpred5_SelectExpr_fragment(self, ):
        # SelectExpr.g:151:27: ( as_ )
        # SelectExpr.g:151:27: as_
        pass 
        self._state.following.append(self.FOLLOW_as__in_synpred5_SelectExpr1306)
        self.as_()

        self._state.following.pop()


    # $ANTLR end "synpred5_SelectExpr"



    # $ANTLR start "synpred12_SelectExpr"
    def synpred12_SelectExpr_fragment(self, ):
        # SelectExpr.g:157:21: ( SEP expr )
        # SelectExpr.g:157:21: SEP expr
        pass 
        self.match(self.input, SEP, self.FOLLOW_SEP_in_synpred12_SelectExpr1396)
        self._state.following.append(self.FOLLOW_expr_in_synpred12_SelectExpr1399)
        self.expr()

        self._state.following.pop()


    # $ANTLR end "synpred12_SelectExpr"



    # $ANTLR start "synpred17_SelectExpr"
    def synpred17_SelectExpr_fragment(self, ):
        # SelectExpr.g:166:8: ( assign_expr )
        # SelectExpr.g:166:8: assign_expr
        pass 
        self._state.following.append(self.FOLLOW_assign_expr_in_synpred17_SelectExpr1452)
        self.assign_expr()

        self._state.following.pop()


    # $ANTLR end "synpred17_SelectExpr"



    # $ANTLR start "synpred19_SelectExpr"
    def synpred19_SelectExpr_fragment(self, ):
        # SelectExpr.g:172:24: ( OR logic_xor )
        # SelectExpr.g:172:24: OR logic_xor
        pass 
        self.match(self.input, OR, self.FOLLOW_OR_in_synpred19_SelectExpr1510)
        self._state.following.append(self.FOLLOW_logic_xor_in_synpred19_SelectExpr1514)
        self.logic_xor()

        self._state.following.pop()


    # $ANTLR end "synpred19_SelectExpr"



    # $ANTLR start "synpred20_SelectExpr"
    def synpred20_SelectExpr_fragment(self, ):
        # SelectExpr.g:173:24: ( XOR logic_and )
        # SelectExpr.g:173:24: XOR logic_and
        pass 
        self.match(self.input, XOR, self.FOLLOW_XOR_in_synpred20_SelectExpr1527)
        self._state.following.append(self.FOLLOW_logic_and_in_synpred20_SelectExpr1530)
        self.logic_and()

        self._state.following.pop()


    # $ANTLR end "synpred20_SelectExpr"



    # $ANTLR start "synpred21_SelectExpr"
    def synpred21_SelectExpr_fragment(self, ):
        # SelectExpr.g:174:24: ( AND logic_not )
        # SelectExpr.g:174:24: AND logic_not
        pass 
        self.match(self.input, AND, self.FOLLOW_AND_in_synpred21_SelectExpr1543)
        self._state.following.append(self.FOLLOW_logic_not_in_synpred21_SelectExpr1546)
        self.logic_not()

        self._state.following.pop()


    # $ANTLR end "synpred21_SelectExpr"



    # $ANTLR start "synpred23_SelectExpr"
    def synpred23_SelectExpr_fragment(self, ):
        # SelectExpr.g:178:26: ( IN atom )
        # SelectExpr.g:178:26: IN atom
        pass 
        self.match(self.input, IN, self.FOLLOW_IN_in_synpred23_SelectExpr1582)
        self._state.following.append(self.FOLLOW_atom_in_synpred23_SelectExpr1585)
        self.atom()

        self._state.following.pop()


    # $ANTLR end "synpred23_SelectExpr"



    # $ANTLR start "synpred24_SelectExpr"
    def synpred24_SelectExpr_fragment(self, ):
        # SelectExpr.g:179:26: ( EQ compare_ne )
        # SelectExpr.g:179:26: EQ compare_ne
        pass 
        self.match(self.input, EQ, self.FOLLOW_EQ_in_synpred24_SelectExpr1598)
        self._state.following.append(self.FOLLOW_compare_ne_in_synpred24_SelectExpr1601)
        self.compare_ne()

        self._state.following.pop()


    # $ANTLR end "synpred24_SelectExpr"



    # $ANTLR start "synpred25_SelectExpr"
    def synpred25_SelectExpr_fragment(self, ):
        # SelectExpr.g:180:26: ( NE compare_ge )
        # SelectExpr.g:180:26: NE compare_ge
        pass 
        self.match(self.input, NE, self.FOLLOW_NE_in_synpred25_SelectExpr1614)
        self._state.following.append(self.FOLLOW_compare_ge_in_synpred25_SelectExpr1617)
        self.compare_ge()

        self._state.following.pop()


    # $ANTLR end "synpred25_SelectExpr"



    # $ANTLR start "synpred26_SelectExpr"
    def synpred26_SelectExpr_fragment(self, ):
        # SelectExpr.g:181:26: ( GE compare_gt )
        # SelectExpr.g:181:26: GE compare_gt
        pass 
        self.match(self.input, GE, self.FOLLOW_GE_in_synpred26_SelectExpr1630)
        self._state.following.append(self.FOLLOW_compare_gt_in_synpred26_SelectExpr1633)
        self.compare_gt()

        self._state.following.pop()


    # $ANTLR end "synpred26_SelectExpr"



    # $ANTLR start "synpred27_SelectExpr"
    def synpred27_SelectExpr_fragment(self, ):
        # SelectExpr.g:182:26: ( GT compare_le )
        # SelectExpr.g:182:26: GT compare_le
        pass 
        self.match(self.input, GT, self.FOLLOW_GT_in_synpred27_SelectExpr1646)
        self._state.following.append(self.FOLLOW_compare_le_in_synpred27_SelectExpr1649)
        self.compare_le()

        self._state.following.pop()


    # $ANTLR end "synpred27_SelectExpr"



    # $ANTLR start "synpred28_SelectExpr"
    def synpred28_SelectExpr_fragment(self, ):
        # SelectExpr.g:183:26: ( LE compare_lt )
        # SelectExpr.g:183:26: LE compare_lt
        pass 
        self.match(self.input, LE, self.FOLLOW_LE_in_synpred28_SelectExpr1662)
        self._state.following.append(self.FOLLOW_compare_lt_in_synpred28_SelectExpr1665)
        self.compare_lt()

        self._state.following.pop()


    # $ANTLR end "synpred28_SelectExpr"



    # $ANTLR start "synpred29_SelectExpr"
    def synpred29_SelectExpr_fragment(self, ):
        # SelectExpr.g:184:31: ( LT arithmetic_expr )
        # SelectExpr.g:184:31: LT arithmetic_expr
        pass 
        self.match(self.input, LT, self.FOLLOW_LT_in_synpred29_SelectExpr1678)
        self._state.following.append(self.FOLLOW_arithmetic_expr_in_synpred29_SelectExpr1681)
        self.arithmetic_expr()

        self._state.following.pop()


    # $ANTLR end "synpred29_SelectExpr"



    # $ANTLR start "synpred31_SelectExpr"
    def synpred31_SelectExpr_fragment(self, ):
        # SelectExpr.g:187:46: ( ( SUB | ADD ) arithmetic_mul_div_mod )
        # SelectExpr.g:187:46: ( SUB | ADD ) arithmetic_mul_div_mod
        pass 
        if (ADD <= self.input.LA(1) <= SUB):
            self.input.consume()
            self._state.errorRecovery = False

        else:
            if self._state.backtracking > 0:
                raise BacktrackingFailed

            mse = MismatchedSetException(None, self.input)
            raise mse


        self._state.following.append(self.FOLLOW_arithmetic_mul_div_mod_in_synpred31_SelectExpr1711)
        self.arithmetic_mul_div_mod()

        self._state.following.pop()


    # $ANTLR end "synpred31_SelectExpr"



    # $ANTLR start "synpred34_SelectExpr"
    def synpred34_SelectExpr_fragment(self, ):
        # SelectExpr.g:188:42: ( ( MUL | DIV | MOD ) arithmetic_pow )
        # SelectExpr.g:188:42: ( MUL | DIV | MOD ) arithmetic_pow
        pass 
        if (MUL <= self.input.LA(1) <= MOD):
            self.input.consume()
            self._state.errorRecovery = False

        else:
            if self._state.backtracking > 0:
                raise BacktrackingFailed

            mse = MismatchedSetException(None, self.input)
            raise mse


        self._state.following.append(self.FOLLOW_arithmetic_pow_in_synpred34_SelectExpr1739)
        self.arithmetic_pow()

        self._state.following.pop()


    # $ANTLR end "synpred34_SelectExpr"



    # $ANTLR start "synpred35_SelectExpr"
    def synpred35_SelectExpr_fragment(self, ):
        # SelectExpr.g:189:36: ( POW arithmetic_unary )
        # SelectExpr.g:189:36: POW arithmetic_unary
        pass 
        self.match(self.input, POW, self.FOLLOW_POW_in_synpred35_SelectExpr1752)
        self._state.following.append(self.FOLLOW_arithmetic_unary_in_synpred35_SelectExpr1755)
        self.arithmetic_unary()

        self._state.following.pop()


    # $ANTLR end "synpred35_SelectExpr"




    # Delegated rules

    def synpred35_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred35_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred29_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred29_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred19_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred19_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred12_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred12_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred21_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred21_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred26_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred26_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred4_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred4_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred17_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred17_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred34_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred34_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred28_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred28_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred27_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred27_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred5_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred5_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred24_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred24_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred23_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred23_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred31_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred31_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred2_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred2_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred3_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred3_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred25_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred25_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred20_SelectExpr(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred20_SelectExpr_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success



    # lookup tables for DFA #2

    DFA2_eot = DFA.unpack(
        u"\20\uffff"
        )

    DFA2_eof = DFA.unpack(
        u"\20\uffff"
        )

    DFA2_min = DFA.unpack(
        u"\1\20\1\0\16\uffff"
        )

    DFA2_max = DFA.unpack(
        u"\1\133\1\0\16\uffff"
        )

    DFA2_accept = DFA.unpack(
        u"\2\uffff\1\2\13\uffff\1\3\1\1"
        )

    DFA2_special = DFA.unpack(
        u"\1\uffff\1\0\16\uffff"
        )

            
    DFA2_transition = [
        DFA.unpack(u"\1\16\13\uffff\1\2\11\uffff\2\2\6\uffff\1\2\7\uffff"
        u"\1\1\7\uffff\1\2\14\uffff\1\2\1\uffff\4\2\2\uffff\1\2\7\uffff\1"
        u"\2"),
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
                if (self.synpred2_SelectExpr()):
                    s = 15

                elif (self.synpred3_SelectExpr()):
                    s = 2

                 
                input.seek(index2_1)
                if s >= 0:
                    return s

            if self._state.backtracking >0:
                raise BacktrackingFailed
            nvae = NoViableAltException(self_.getDescription(), 2, _s, input)
            self_.error(nvae)
            raise nvae
    # lookup tables for DFA #10

    DFA10_eot = DFA.unpack(
        u"\17\uffff"
        )

    DFA10_eof = DFA.unpack(
        u"\17\uffff"
        )

    DFA10_min = DFA.unpack(
        u"\1\34\1\0\15\uffff"
        )

    DFA10_max = DFA.unpack(
        u"\1\133\1\0\15\uffff"
        )

    DFA10_accept = DFA.unpack(
        u"\2\uffff\1\2\13\uffff\1\1"
        )

    DFA10_special = DFA.unpack(
        u"\1\uffff\1\0\15\uffff"
        )

            
    DFA10_transition = [
        DFA.unpack(u"\1\2\11\uffff\2\2\6\uffff\1\2\7\uffff\1\2\7\uffff\1"
        u"\2\14\uffff\1\2\1\uffff\4\2\2\uffff\1\1\7\uffff\1\2"),
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
        DFA.unpack(u"")
    ]

    # class definition for DFA #10

    class DFA10(DFA):
        pass


        def specialStateTransition(self_, s, input):
            # convince pylint that my self_ magic is ok ;)
            # pylint: disable-msg=E0213

            # pretend we are a member of the recognizer
            # thus semantic predicates can be evaluated
            self = self_.recognizer

            _s = s

            if s == 0: 
                LA10_1 = input.LA(1)

                 
                index10_1 = input.index()
                input.rewind()
                s = -1
                if (self.synpred17_SelectExpr()):
                    s = 14

                elif (True):
                    s = 2

                 
                input.seek(index10_1)
                if s >= 0:
                    return s

            if self._state.backtracking >0:
                raise BacktrackingFailed
            nvae = NoViableAltException(self_.getDescription(), 10, _s, input)
            self_.error(nvae)
            raise nvae
 

    FOLLOW_prog_in_eval1249 = frozenset([1])
    FOLLOW_statement_in_prog1259 = frozenset([1, 16, 28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_statement_select_in_statement1269 = frozenset([16])
    FOLLOW_END_in_statement1271 = frozenset([1])
    FOLLOW_expr_in_statement1277 = frozenset([16])
    FOLLOW_END_in_statement1279 = frozenset([1])
    FOLLOW_END_in_statement1285 = frozenset([1])
    FOLLOW_select__in_statement_select1296 = frozenset([57])
    FOLLOW_from__in_statement_select1298 = frozenset([1, 60, 61])
    FOLLOW_where__in_statement_select1301 = frozenset([1, 61])
    FOLLOW_as__in_statement_select1306 = frozenset([1])
    FOLLOW_SELECT_in_select_1339 = frozenset([40, 62, 83])
    FOLLOW_MUL_in_select_1343 = frozenset([1])
    FOLLOW_PHRASE_in_select_1350 = frozenset([1, 15])
    FOLLOW_function_in_select_1354 = frozenset([1, 15])
    FOLLOW_this__in_select_1358 = frozenset([1, 15])
    FOLLOW_SEP_in_select_1362 = frozenset([62, 83])
    FOLLOW_PHRASE_in_select_1366 = frozenset([1, 15])
    FOLLOW_function_in_select_1370 = frozenset([1, 15])
    FOLLOW_this__in_select_1374 = frozenset([1, 15])
    FOLLOW_FROM_in_from_1390 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_expr_in_from_1393 = frozenset([1, 15])
    FOLLOW_SEP_in_from_1396 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_expr_in_from_1399 = frozenset([1, 15])
    FOLLOW_WHERE_in_where_1410 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_expr_in_where_1413 = frozenset([1])
    FOLLOW_AS_in_as_1422 = frozenset([64, 65, 68, 70, 83])
    FOLLOW_set_in_as_1425 = frozenset([1])
    FOLLOW_assign_expr_in_expr1452 = frozenset([1])
    FOLLOW_logic_expr_in_expr1458 = frozenset([1])
    FOLLOW_PHRASE_in_assign_expr1466 = frozenset([31, 48])
    FOLLOW_age_in_assign_expr1469 = frozenset([31])
    FOLLOW_ASSIGN_in_assign_expr1473 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_expr_in_assign_expr1475 = frozenset([1])
    FOLLOW_logic_or_in_logic_expr1498 = frozenset([1])
    FOLLOW_logic_xor_in_logic_or1507 = frozenset([1, 26])
    FOLLOW_OR_in_logic_or1510 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_logic_xor_in_logic_or1514 = frozenset([1, 26])
    FOLLOW_logic_and_in_logic_xor1524 = frozenset([1, 25])
    FOLLOW_XOR_in_logic_xor1527 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_logic_and_in_logic_xor1530 = frozenset([1, 25])
    FOLLOW_logic_not_in_logic_and1540 = frozenset([1, 21])
    FOLLOW_AND_in_logic_and1543 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_logic_not_in_logic_and1546 = frozenset([1, 21])
    FOLLOW_NOT_in_logic_not1557 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_compare_expr_in_logic_not1562 = frozenset([1])
    FOLLOW_compare_in_in_compare_expr1571 = frozenset([1])
    FOLLOW_compare_eq_in_compare_in1579 = frozenset([1, 30])
    FOLLOW_IN_in_compare_in1582 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_atom_in_compare_in1585 = frozenset([1, 30])
    FOLLOW_compare_ne_in_compare_eq1595 = frozenset([1, 32])
    FOLLOW_EQ_in_compare_eq1598 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_compare_ne_in_compare_eq1601 = frozenset([1, 32])
    FOLLOW_compare_ge_in_compare_ne1611 = frozenset([1, 33])
    FOLLOW_NE_in_compare_ne1614 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_compare_ge_in_compare_ne1617 = frozenset([1, 33])
    FOLLOW_compare_gt_in_compare_ge1627 = frozenset([1, 35])
    FOLLOW_GE_in_compare_ge1630 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_compare_gt_in_compare_ge1633 = frozenset([1, 35])
    FOLLOW_compare_le_in_compare_gt1643 = frozenset([1, 37])
    FOLLOW_GT_in_compare_gt1646 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_compare_le_in_compare_gt1649 = frozenset([1, 37])
    FOLLOW_compare_lt_in_compare_le1659 = frozenset([1, 34])
    FOLLOW_LE_in_compare_le1662 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_compare_lt_in_compare_le1665 = frozenset([1, 34])
    FOLLOW_arithmetic_expr_in_compare_lt1675 = frozenset([1, 36])
    FOLLOW_LT_in_compare_lt1678 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_arithmetic_expr_in_compare_lt1681 = frozenset([1, 36])
    FOLLOW_arithmetic_sub_add_in_arithmetic_expr1692 = frozenset([1])
    FOLLOW_arithmetic_mul_div_mod_in_arithmetic_sub_add1700 = frozenset([1, 38, 39])
    FOLLOW_SUB_in_arithmetic_sub_add1704 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_ADD_in_arithmetic_sub_add1707 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_arithmetic_mul_div_mod_in_arithmetic_sub_add1711 = frozenset([1, 38, 39])
    FOLLOW_arithmetic_pow_in_arithmetic_mul_div_mod1721 = frozenset([1, 40, 41, 42])
    FOLLOW_MUL_in_arithmetic_mul_div_mod1725 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_DIV_in_arithmetic_mul_div_mod1730 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_MOD_in_arithmetic_mul_div_mod1735 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_arithmetic_pow_in_arithmetic_mul_div_mod1739 = frozenset([1, 40, 41, 42])
    FOLLOW_arithmetic_unary_in_arithmetic_pow1749 = frozenset([1, 43])
    FOLLOW_POW_in_arithmetic_pow1752 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_arithmetic_unary_in_arithmetic_pow1755 = frozenset([1, 43])
    FOLLOW_SUB_in_arithmetic_unary1766 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_atom_in_arithmetic_unary1768 = frozenset([1])
    FOLLOW_ADD_in_arithmetic_unary1782 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_atom_in_arithmetic_unary1784 = frozenset([1])
    FOLLOW_atom_in_arithmetic_unary1798 = frozenset([1])
    FOLLOW_value_in_atom1809 = frozenset([1])
    FOLLOW_variable_in_atom1814 = frozenset([1])
    FOLLOW_function_in_atom1819 = frozenset([1])
    FOLLOW_91_in_atom1824 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_expr_in_atom1827 = frozenset([92])
    FOLLOW_92_in_atom1829 = frozenset([1])
    FOLLOW_statement_select_in_atom1835 = frozenset([1])
    FOLLOW_PHRASE_in_function1844 = frozenset([91])
    FOLLOW_91_in_function1846 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91, 92])
    FOLLOW_parameter_in_function1848 = frozenset([92])
    FOLLOW_92_in_function1851 = frozenset([1])
    FOLLOW_expr_in_parameter1871 = frozenset([1, 15])
    FOLLOW_SEP_in_parameter1874 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_expr_in_parameter1877 = frozenset([1, 15])
    FOLLOW_PHRASE_in_variable1888 = frozenset([1, 48])
    FOLLOW_age_in_variable1891 = frozenset([1])
    FOLLOW_AGE_BEGIN_in_age1915 = frozenset([28, 38, 39, 46, 49, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_expr_in_age1917 = frozenset([49])
    FOLLOW_AGE_END_in_age1920 = frozenset([1])
    FOLLOW_STRING_in_value1938 = frozenset([1])
    FOLLOW_FLOAT_in_value1952 = frozenset([1])
    FOLLOW_INTEGER_in_value1966 = frozenset([1])
    FOLLOW_TRUE_in_value1979 = frozenset([1])
    FOLLOW_FALSE_in_value1993 = frozenset([1])
    FOLLOW_this__in_value2007 = frozenset([1])
    FOLLOW_list__in_value2012 = frozenset([1])
    FOLLOW_PHRASE_in_this_2023 = frozenset([14])
    FOLLOW_DOT_in_this_2025 = frozenset([62])
    FOLLOW_THIS_in_this_2029 = frozenset([1])
    FOLLOW_LIST_BEGIN_in_list_2050 = frozenset([15, 28, 38, 39, 46, 47, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_expr_in_list_2054 = frozenset([15, 47])
    FOLLOW_SEP_in_list_2058 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_expr_in_list_2060 = frozenset([15, 47])
    FOLLOW_LIST_END_in_list_2066 = frozenset([1])
    FOLLOW_statement_select_in_synpred2_SelectExpr1269 = frozenset([16])
    FOLLOW_END_in_synpred2_SelectExpr1271 = frozenset([1])
    FOLLOW_expr_in_synpred3_SelectExpr1277 = frozenset([16])
    FOLLOW_END_in_synpred3_SelectExpr1279 = frozenset([1])
    FOLLOW_where__in_synpred4_SelectExpr1301 = frozenset([1])
    FOLLOW_as__in_synpred5_SelectExpr1306 = frozenset([1])
    FOLLOW_SEP_in_synpred12_SelectExpr1396 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_expr_in_synpred12_SelectExpr1399 = frozenset([1])
    FOLLOW_assign_expr_in_synpred17_SelectExpr1452 = frozenset([1])
    FOLLOW_OR_in_synpred19_SelectExpr1510 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_logic_xor_in_synpred19_SelectExpr1514 = frozenset([1])
    FOLLOW_XOR_in_synpred20_SelectExpr1527 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_logic_and_in_synpred20_SelectExpr1530 = frozenset([1])
    FOLLOW_AND_in_synpred21_SelectExpr1543 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_logic_not_in_synpred21_SelectExpr1546 = frozenset([1])
    FOLLOW_IN_in_synpred23_SelectExpr1582 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_atom_in_synpred23_SelectExpr1585 = frozenset([1])
    FOLLOW_EQ_in_synpred24_SelectExpr1598 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_compare_ne_in_synpred24_SelectExpr1601 = frozenset([1])
    FOLLOW_NE_in_synpred25_SelectExpr1614 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_compare_ge_in_synpred25_SelectExpr1617 = frozenset([1])
    FOLLOW_GE_in_synpred26_SelectExpr1630 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_compare_gt_in_synpred26_SelectExpr1633 = frozenset([1])
    FOLLOW_GT_in_synpred27_SelectExpr1646 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_compare_le_in_synpred27_SelectExpr1649 = frozenset([1])
    FOLLOW_LE_in_synpred28_SelectExpr1662 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_compare_lt_in_synpred28_SelectExpr1665 = frozenset([1])
    FOLLOW_LT_in_synpred29_SelectExpr1678 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_arithmetic_expr_in_synpred29_SelectExpr1681 = frozenset([1])
    FOLLOW_set_in_synpred31_SelectExpr1703 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_arithmetic_mul_div_mod_in_synpred31_SelectExpr1711 = frozenset([1])
    FOLLOW_set_in_synpred34_SelectExpr1724 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_arithmetic_pow_in_synpred34_SelectExpr1739 = frozenset([1])
    FOLLOW_POW_in_synpred35_SelectExpr1752 = frozenset([28, 38, 39, 46, 54, 62, 75, 77, 78, 79, 80, 83, 91])
    FOLLOW_arithmetic_unary_in_synpred35_SelectExpr1755 = frozenset([1])



       
def main(argv, otherArg=None):
	while True:
		Expr = ""
		while True:
			expr = raw_input('>>> ')
			if expr == 'run':
				break
			else:
				Expr += expr
		char_stream = antlr3.ANTLRStringStream(Expr)
		lexer = SelectExprLexer(char_stream)
		tokens = antlr3.CommonTokenStream(lexer)
		parser = SceneExprParser(tokens)
		print parser.eval()


if __name__ == '__main__':
    main(sys.argv)
