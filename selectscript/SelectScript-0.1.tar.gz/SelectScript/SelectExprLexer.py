# $ANTLR 3.1.3 Mar 18, 2009 10:09:25 SelectExpr.g 2014-02-03 13:11:11

import sys
from antlr3 import *
from antlr3.compat import set, frozenset


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


class SelectExprLexer(Lexer):

    grammarFileName = "SelectExpr.g"
    antlr_version = version_str_to_tuple("3.1.3 Mar 18, 2009 10:09:25")
    antlr_version_str = "3.1.3 Mar 18, 2009 10:09:25"

    def __init__(self, input=None, state=None):
        if state is None:
            state = RecognizerSharedState()
        super(SelectExprLexer, self).__init__(input, state)


        self.dfa20 = self.DFA20(
            self, 20,
            eot = self.DFA20_eot,
            eof = self.DFA20_eof,
            min = self.DFA20_min,
            max = self.DFA20_max,
            accept = self.DFA20_accept,
            special = self.DFA20_special,
            transition = self.DFA20_transition
            )






    # $ANTLR start "T__91"
    def mT__91(self, ):

        try:
            _type = T__91
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:7:7: ( '(' )
            # SelectExpr.g:7:9: '('
            pass 
            self.match(40)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "T__91"



    # $ANTLR start "T__92"
    def mT__92(self, ):

        try:
            _type = T__92
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:8:7: ( ')' )
            # SelectExpr.g:8:9: ')'
            pass 
            self.match(41)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "T__92"



    # $ANTLR start "DOT"
    def mDOT(self, ):

        try:
            _type = DOT
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:55:5: ( '.' )
            # SelectExpr.g:55:7: '.'
            pass 
            self.match(46)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DOT"



    # $ANTLR start "SEP"
    def mSEP(self, ):

        try:
            _type = SEP
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:56:5: ( ',' )
            # SelectExpr.g:56:7: ','
            pass 
            self.match(44)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SEP"



    # $ANTLR start "END"
    def mEND(self, ):

        try:
            _type = END
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:57:5: ( ';' )
            # SelectExpr.g:57:7: ';'
            pass 
            self.match(59)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "END"



    # $ANTLR start "COLON"
    def mCOLON(self, ):

        try:
            _type = COLON
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:58:7: ( ':' )
            # SelectExpr.g:58:9: ':'
            pass 
            self.match(58)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COLON"



    # $ANTLR start "AND"
    def mAND(self, ):

        try:
            _type = AND
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:60:5: ( A N D )
            # SelectExpr.g:60:7: A N D
            pass 
            self.mA()
            self.mN()
            self.mD()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AND"



    # $ANTLR start "XOR"
    def mXOR(self, ):

        try:
            _type = XOR
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:61:5: ( X O R )
            # SelectExpr.g:61:7: X O R
            pass 
            self.mX()
            self.mO()
            self.mR()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "XOR"



    # $ANTLR start "OR"
    def mOR(self, ):

        try:
            _type = OR
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:62:5: ( O R )
            # SelectExpr.g:62:7: O R
            pass 
            self.mO()
            self.mR()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "OR"



    # $ANTLR start "NOT"
    def mNOT(self, ):

        try:
            _type = NOT
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:63:5: ( N O T )
            # SelectExpr.g:63:7: N O T
            pass 
            self.mN()
            self.mO()
            self.mT()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NOT"



    # $ANTLR start "IN"
    def mIN(self, ):

        try:
            _type = IN
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:64:5: ( I N )
            # SelectExpr.g:64:7: I N
            pass 
            self.mI()
            self.mN()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "IN"



    # $ANTLR start "ASSIGN"
    def mASSIGN(self, ):

        try:
            _type = ASSIGN
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:66:8: ( '=' )
            # SelectExpr.g:66:11: '='
            pass 
            self.match(61)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ASSIGN"



    # $ANTLR start "EQ"
    def mEQ(self, ):

        try:
            _type = EQ
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:68:4: ( '==' )
            # SelectExpr.g:68:6: '=='
            pass 
            self.match("==")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EQ"



    # $ANTLR start "NE"
    def mNE(self, ):

        try:
            _type = NE
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:69:4: ( '!=' )
            # SelectExpr.g:69:6: '!='
            pass 
            self.match("!=")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NE"



    # $ANTLR start "LE"
    def mLE(self, ):

        try:
            _type = LE
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:70:4: ( '<=' )
            # SelectExpr.g:70:6: '<='
            pass 
            self.match("<=")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LE"



    # $ANTLR start "GE"
    def mGE(self, ):

        try:
            _type = GE
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:71:4: ( '>=' )
            # SelectExpr.g:71:6: '>='
            pass 
            self.match(">=")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "GE"



    # $ANTLR start "LT"
    def mLT(self, ):

        try:
            _type = LT
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:72:4: ( '<' )
            # SelectExpr.g:72:7: '<'
            pass 
            self.match(60)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LT"



    # $ANTLR start "GT"
    def mGT(self, ):

        try:
            _type = GT
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:73:4: ( '>' )
            # SelectExpr.g:73:7: '>'
            pass 
            self.match(62)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "GT"



    # $ANTLR start "ADD"
    def mADD(self, ):

        try:
            _type = ADD
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:75:5: ( '+' )
            # SelectExpr.g:75:7: '+'
            pass 
            self.match(43)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ADD"



    # $ANTLR start "SUB"
    def mSUB(self, ):

        try:
            _type = SUB
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:76:5: ( '-' )
            # SelectExpr.g:76:7: '-'
            pass 
            self.match(45)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SUB"



    # $ANTLR start "MUL"
    def mMUL(self, ):

        try:
            _type = MUL
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:77:5: ( '*' )
            # SelectExpr.g:77:7: '*'
            pass 
            self.match(42)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "MUL"



    # $ANTLR start "DIV"
    def mDIV(self, ):

        try:
            _type = DIV
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:78:5: ( '/' )
            # SelectExpr.g:78:7: '/'
            pass 
            self.match(47)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DIV"



    # $ANTLR start "MOD"
    def mMOD(self, ):

        try:
            _type = MOD
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:79:5: ( '%' )
            # SelectExpr.g:79:7: '%'
            pass 
            self.match(37)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "MOD"



    # $ANTLR start "POW"
    def mPOW(self, ):

        try:
            _type = POW
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:80:5: ( '^' )
            # SelectExpr.g:80:7: '^'
            pass 
            self.match(94)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "POW"



    # $ANTLR start "SQ"
    def mSQ(self, ):

        try:
            _type = SQ
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:82:4: ( '\\'' )
            # SelectExpr.g:82:6: '\\''
            pass 
            self.match(39)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SQ"



    # $ANTLR start "DQ"
    def mDQ(self, ):

        try:
            _type = DQ
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:83:4: ( '\\\"' )
            # SelectExpr.g:83:6: '\\\"'
            pass 
            self.match(34)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DQ"



    # $ANTLR start "LIST_BEGIN"
    def mLIST_BEGIN(self, ):

        try:
            _type = LIST_BEGIN
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:85:12: ( '[' )
            # SelectExpr.g:85:14: '['
            pass 
            self.match(91)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LIST_BEGIN"



    # $ANTLR start "LIST_END"
    def mLIST_END(self, ):

        try:
            _type = LIST_END
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:86:12: ( ']' )
            # SelectExpr.g:86:14: ']'
            pass 
            self.match(93)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LIST_END"



    # $ANTLR start "AGE_BEGIN"
    def mAGE_BEGIN(self, ):

        try:
            _type = AGE_BEGIN
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:88:11: ( '{' )
            # SelectExpr.g:88:13: '{'
            pass 
            self.match(123)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AGE_BEGIN"



    # $ANTLR start "AGE_END"
    def mAGE_END(self, ):

        try:
            _type = AGE_END
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:89:11: ( '}' )
            # SelectExpr.g:89:13: '}'
            pass 
            self.match(125)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AGE_END"



    # $ANTLR start "SELECT"
    def mSELECT(self, ):

        try:
            _type = SELECT
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:91:8: ( S E L E C T )
            # SelectExpr.g:91:10: S E L E C T
            pass 
            self.mS()
            self.mE()
            self.mL()
            self.mE()
            self.mC()
            self.mT()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SELECT"



    # $ANTLR start "FROM"
    def mFROM(self, ):

        try:
            _type = FROM
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:92:8: ( F R O M )
            # SelectExpr.g:92:10: F R O M
            pass 
            self.mF()
            self.mR()
            self.mO()
            self.mM()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "FROM"



    # $ANTLR start "WHERE"
    def mWHERE(self, ):

        try:
            _type = WHERE
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:93:8: ( W H E R E )
            # SelectExpr.g:93:10: W H E R E
            pass 
            self.mW()
            self.mH()
            self.mE()
            self.mR()
            self.mE()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "WHERE"



    # $ANTLR start "AS"
    def mAS(self, ):

        try:
            _type = AS
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:94:8: ( A S )
            # SelectExpr.g:94:10: A S
            pass 
            self.mA()
            self.mS()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AS"



    # $ANTLR start "THIS"
    def mTHIS(self, ):

        try:
            _type = THIS
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:95:8: ( T H I S )
            # SelectExpr.g:95:10: T H I S
            pass 
            self.mT()
            self.mH()
            self.mI()
            self.mS()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "THIS"



    # $ANTLR start "TIME"
    def mTIME(self, ):

        try:
            _type = TIME
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:96:8: ( T I M E )
            # SelectExpr.g:96:10: T I M E
            pass 
            self.mT()
            self.mI()
            self.mM()
            self.mE()



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "TIME"



    # $ANTLR start "AS_SCENE"
    def mAS_SCENE(self, ):

        try:
            _type = AS_SCENE
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:98:9: ( S ( C E N E )? )
            # SelectExpr.g:98:11: S ( C E N E )?
            pass 
            self.mS()
            # SelectExpr.g:98:13: ( C E N E )?
            alt1 = 2
            LA1_0 = self.input.LA(1)

            if (LA1_0 == 67 or LA1_0 == 99) :
                alt1 = 1
            if alt1 == 1:
                # SelectExpr.g:98:14: C E N E
                pass 
                self.mC()
                self.mE()
                self.mN()
                self.mE()






            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AS_SCENE"



    # $ANTLR start "AS_LIST"
    def mAS_LIST(self, ):

        try:
            _type = AS_LIST
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:99:9: ( L ( I S T )? )
            # SelectExpr.g:99:11: L ( I S T )?
            pass 
            self.mL()
            # SelectExpr.g:99:13: ( I S T )?
            alt2 = 2
            LA2_0 = self.input.LA(1)

            if (LA2_0 == 73 or LA2_0 == 105) :
                alt2 = 1
            if alt2 == 1:
                # SelectExpr.g:99:14: I S T
                pass 
                self.mI()
                self.mS()
                self.mT()






            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AS_LIST"



    # $ANTLR start "AS_VALUE"
    def mAS_VALUE(self, ):

        try:
            _type = AS_VALUE
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:100:9: ( V ( A L ( U E )? )? )
            # SelectExpr.g:100:11: V ( A L ( U E )? )?
            pass 
            self.mV()
            # SelectExpr.g:100:13: ( A L ( U E )? )?
            alt4 = 2
            LA4_0 = self.input.LA(1)

            if (LA4_0 == 65 or LA4_0 == 97) :
                alt4 = 1
            if alt4 == 1:
                # SelectExpr.g:100:14: A L ( U E )?
                pass 
                self.mA()
                self.mL()
                # SelectExpr.g:100:18: ( U E )?
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if (LA3_0 == 85 or LA3_0 == 117) :
                    alt3 = 1
                if alt3 == 1:
                    # SelectExpr.g:100:19: U E
                    pass 
                    self.mU()
                    self.mE()









            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AS_VALUE"



    # $ANTLR start "AS_DICT"
    def mAS_DICT(self, ):

        try:
            _type = AS_DICT
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:101:9: ( D ( I C T ( I O N A R Y )? ) )
            # SelectExpr.g:101:11: D ( I C T ( I O N A R Y )? )
            pass 
            self.mD()
            # SelectExpr.g:101:13: ( I C T ( I O N A R Y )? )
            # SelectExpr.g:101:14: I C T ( I O N A R Y )?
            pass 
            self.mI()
            self.mC()
            self.mT()
            # SelectExpr.g:101:20: ( I O N A R Y )?
            alt5 = 2
            LA5_0 = self.input.LA(1)

            if (LA5_0 == 73 or LA5_0 == 105) :
                alt5 = 1
            if alt5 == 1:
                # SelectExpr.g:101:21: I O N A R Y
                pass 
                self.mI()
                self.mO()
                self.mN()
                self.mA()
                self.mR()
                self.mY()









            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AS_DICT"



    # $ANTLR start "NEWLINE"
    def mNEWLINE(self, ):

        try:
            _type = NEWLINE
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:103:9: ( ( ( '\\r' )? '\\n' ) )
            # SelectExpr.g:103:11: ( ( '\\r' )? '\\n' )
            pass 
            # SelectExpr.g:103:11: ( ( '\\r' )? '\\n' )
            # SelectExpr.g:103:12: ( '\\r' )? '\\n'
            pass 
            # SelectExpr.g:103:12: ( '\\r' )?
            alt6 = 2
            LA6_0 = self.input.LA(1)

            if (LA6_0 == 13) :
                alt6 = 1
            if alt6 == 1:
                # SelectExpr.g:103:12: '\\r'
                pass 
                self.match(13)



            self.match(10)



            #action start
            self.skip()
            #action end



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NEWLINE"



    # $ANTLR start "WS"
    def mWS(self, ):

        try:
            _type = WS
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:104:4: ( ( ' ' | '\\t' | '\\n' | '\\r' )+ )
            # SelectExpr.g:104:6: ( ' ' | '\\t' | '\\n' | '\\r' )+
            pass 
            # SelectExpr.g:104:6: ( ' ' | '\\t' | '\\n' | '\\r' )+
            cnt7 = 0
            while True: #loop7
                alt7 = 2
                LA7_0 = self.input.LA(1)

                if ((9 <= LA7_0 <= 10) or LA7_0 == 13 or LA7_0 == 32) :
                    alt7 = 1


                if alt7 == 1:
                    # SelectExpr.g:
                    pass 
                    if (9 <= self.input.LA(1) <= 10) or self.input.LA(1) == 13 or self.input.LA(1) == 32:
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse



                else:
                    if cnt7 >= 1:
                        break #loop7

                    eee = EarlyExitException(7, self.input)
                    raise eee

                cnt7 += 1
            #action start
            self.skip()
            #action end



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "WS"



    # $ANTLR start "COMMENT"
    def mCOMMENT(self, ):

        try:
            _type = COMMENT
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:106:9: ( '/*' ( . )* '*/' )
            # SelectExpr.g:106:11: '/*' ( . )* '*/'
            pass 
            self.match("/*")
            # SelectExpr.g:106:16: ( . )*
            while True: #loop8
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if (LA8_0 == 42) :
                    LA8_1 = self.input.LA(2)

                    if (LA8_1 == 47) :
                        alt8 = 2
                    elif ((0 <= LA8_1 <= 46) or (48 <= LA8_1 <= 65535)) :
                        alt8 = 1


                elif ((0 <= LA8_0 <= 41) or (43 <= LA8_0 <= 65535)) :
                    alt8 = 1


                if alt8 == 1:
                    # SelectExpr.g:106:16: .
                    pass 
                    self.matchAny()


                else:
                    break #loop8
            self.match("*/")
            #action start
            _channel=HIDDEN;
            #action end



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COMMENT"



    # $ANTLR start "LINE_COMMENT"
    def mLINE_COMMENT(self, ):

        try:
            _type = LINE_COMMENT
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:107:14: ( '//' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n' )
            # SelectExpr.g:107:16: '//' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n'
            pass 
            self.match("//")
            # SelectExpr.g:107:21: (~ ( '\\n' | '\\r' ) )*
            while True: #loop9
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if ((0 <= LA9_0 <= 9) or (11 <= LA9_0 <= 12) or (14 <= LA9_0 <= 65535)) :
                    alt9 = 1


                if alt9 == 1:
                    # SelectExpr.g:107:21: ~ ( '\\n' | '\\r' )
                    pass 
                    if (0 <= self.input.LA(1) <= 9) or (11 <= self.input.LA(1) <= 12) or (14 <= self.input.LA(1) <= 65535):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse



                else:
                    break #loop9
            # SelectExpr.g:107:35: ( '\\r' )?
            alt10 = 2
            LA10_0 = self.input.LA(1)

            if (LA10_0 == 13) :
                alt10 = 1
            if alt10 == 1:
                # SelectExpr.g:107:35: '\\r'
                pass 
                self.match(13)



            self.match(10)
            #action start
            _channel=HIDDEN;
            #action end



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LINE_COMMENT"



    # $ANTLR start "STRING"
    def mSTRING(self, ):

        try:
            _type = STRING
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:109:9: ( DQ (~ ( DQ ) )* DQ | SQ (~ ( SQ ) )* SQ )
            alt13 = 2
            LA13_0 = self.input.LA(1)

            if (LA13_0 == 34) :
                alt13 = 1
            elif (LA13_0 == 39) :
                alt13 = 2
            else:
                nvae = NoViableAltException("", 13, 0, self.input)

                raise nvae

            if alt13 == 1:
                # SelectExpr.g:109:11: DQ (~ ( DQ ) )* DQ
                pass 
                self.mDQ()
                # SelectExpr.g:109:14: (~ ( DQ ) )*
                while True: #loop11
                    alt11 = 2
                    LA11_0 = self.input.LA(1)

                    if ((0 <= LA11_0 <= 33) or (35 <= LA11_0 <= 65535)) :
                        alt11 = 1


                    if alt11 == 1:
                        # SelectExpr.g:109:15: ~ ( DQ )
                        pass 
                        if (0 <= self.input.LA(1) <= 33) or (35 <= self.input.LA(1) <= 65535):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse



                    else:
                        break #loop11
                self.mDQ()


            elif alt13 == 2:
                # SelectExpr.g:109:28: SQ (~ ( SQ ) )* SQ
                pass 
                self.mSQ()
                # SelectExpr.g:109:31: (~ ( SQ ) )*
                while True: #loop12
                    alt12 = 2
                    LA12_0 = self.input.LA(1)

                    if ((0 <= LA12_0 <= 38) or (40 <= LA12_0 <= 65535)) :
                        alt12 = 1


                    if alt12 == 1:
                        # SelectExpr.g:109:32: ~ ( SQ )
                        pass 
                        if (0 <= self.input.LA(1) <= 38) or (40 <= self.input.LA(1) <= 65535):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse



                    else:
                        break #loop12
                self.mSQ()


            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "STRING"



    # $ANTLR start "INTEGER"
    def mINTEGER(self, ):

        try:
            _type = INTEGER
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:110:9: ( ( DIGIT )+ )
            # SelectExpr.g:110:11: ( DIGIT )+
            pass 
            # SelectExpr.g:110:11: ( DIGIT )+
            cnt14 = 0
            while True: #loop14
                alt14 = 2
                LA14_0 = self.input.LA(1)

                if ((48 <= LA14_0 <= 57)) :
                    alt14 = 1


                if alt14 == 1:
                    # SelectExpr.g:110:11: DIGIT
                    pass 
                    self.mDIGIT()


                else:
                    if cnt14 >= 1:
                        break #loop14

                    eee = EarlyExitException(14, self.input)
                    raise eee

                cnt14 += 1



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "INTEGER"



    # $ANTLR start "FLOAT"
    def mFLOAT(self, ):

        try:
            _type = FLOAT
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:111:8: ( ( DIGIT )* DOT ( DIGIT )* )
            # SelectExpr.g:111:10: ( DIGIT )* DOT ( DIGIT )*
            pass 
            # SelectExpr.g:111:10: ( DIGIT )*
            while True: #loop15
                alt15 = 2
                LA15_0 = self.input.LA(1)

                if ((48 <= LA15_0 <= 57)) :
                    alt15 = 1


                if alt15 == 1:
                    # SelectExpr.g:111:10: DIGIT
                    pass 
                    self.mDIGIT()


                else:
                    break #loop15
            self.mDOT()
            # SelectExpr.g:111:21: ( DIGIT )*
            while True: #loop16
                alt16 = 2
                LA16_0 = self.input.LA(1)

                if ((48 <= LA16_0 <= 57)) :
                    alt16 = 1


                if alt16 == 1:
                    # SelectExpr.g:111:21: DIGIT
                    pass 
                    self.mDIGIT()


                else:
                    break #loop16



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "FLOAT"



    # $ANTLR start "TRUE"
    def mTRUE(self, ):

        try:
            _type = TRUE
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:112:7: ( ( 'T' | 't' ) ( ( 'R' | 'r' ) ( 'U' | 'u' ) ( 'E' | 'e' ) )? )
            # SelectExpr.g:112:9: ( 'T' | 't' ) ( ( 'R' | 'r' ) ( 'U' | 'u' ) ( 'E' | 'e' ) )?
            pass 
            if self.input.LA(1) == 84 or self.input.LA(1) == 116:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse

            # SelectExpr.g:112:19: ( ( 'R' | 'r' ) ( 'U' | 'u' ) ( 'E' | 'e' ) )?
            alt17 = 2
            LA17_0 = self.input.LA(1)

            if (LA17_0 == 82 or LA17_0 == 114) :
                alt17 = 1
            if alt17 == 1:
                # SelectExpr.g:112:20: ( 'R' | 'r' ) ( 'U' | 'u' ) ( 'E' | 'e' )
                pass 
                if self.input.LA(1) == 82 or self.input.LA(1) == 114:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse

                if self.input.LA(1) == 85 or self.input.LA(1) == 117:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse

                if self.input.LA(1) == 69 or self.input.LA(1) == 101:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse







            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "TRUE"



    # $ANTLR start "FALSE"
    def mFALSE(self, ):

        try:
            _type = FALSE
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:113:8: ( ( 'F' | 'f' ) ( ( 'A' | 'a' ) ( 'L' | 'l' ) ( 'S' | 's' ) ( 'E' | 'e' ) )? )
            # SelectExpr.g:113:10: ( 'F' | 'f' ) ( ( 'A' | 'a' ) ( 'L' | 'l' ) ( 'S' | 's' ) ( 'E' | 'e' ) )?
            pass 
            if self.input.LA(1) == 70 or self.input.LA(1) == 102:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse

            # SelectExpr.g:113:20: ( ( 'A' | 'a' ) ( 'L' | 'l' ) ( 'S' | 's' ) ( 'E' | 'e' ) )?
            alt18 = 2
            LA18_0 = self.input.LA(1)

            if (LA18_0 == 65 or LA18_0 == 97) :
                alt18 = 1
            if alt18 == 1:
                # SelectExpr.g:113:21: ( 'A' | 'a' ) ( 'L' | 'l' ) ( 'S' | 's' ) ( 'E' | 'e' )
                pass 
                if self.input.LA(1) == 65 or self.input.LA(1) == 97:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse

                if self.input.LA(1) == 76 or self.input.LA(1) == 108:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse

                if self.input.LA(1) == 83 or self.input.LA(1) == 115:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse

                if self.input.LA(1) == 69 or self.input.LA(1) == 101:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse







            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "FALSE"



    # $ANTLR start "PHRASE"
    def mPHRASE(self, ):

        try:
            _type = PHRASE
            _channel = DEFAULT_CHANNEL

            # SelectExpr.g:115:8: ( ( CHARACTER | SPECIAL ) ( DIGIT | CHARACTER | SPECIAL )* )
            # SelectExpr.g:115:10: ( CHARACTER | SPECIAL ) ( DIGIT | CHARACTER | SPECIAL )*
            pass 
            if (65 <= self.input.LA(1) <= 90) or self.input.LA(1) == 95 or (97 <= self.input.LA(1) <= 122):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse

            # SelectExpr.g:115:32: ( DIGIT | CHARACTER | SPECIAL )*
            while True: #loop19
                alt19 = 2
                LA19_0 = self.input.LA(1)

                if ((48 <= LA19_0 <= 57) or (65 <= LA19_0 <= 90) or LA19_0 == 95 or (97 <= LA19_0 <= 122)) :
                    alt19 = 1


                if alt19 == 1:
                    # SelectExpr.g:
                    pass 
                    if (48 <= self.input.LA(1) <= 57) or (65 <= self.input.LA(1) <= 90) or self.input.LA(1) == 95 or (97 <= self.input.LA(1) <= 122):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse



                else:
                    break #loop19



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PHRASE"



    # $ANTLR start "DIGIT"
    def mDIGIT(self, ):

        try:
            # SelectExpr.g:117:20: ( '0' .. '9' )
            # SelectExpr.g:117:22: '0' .. '9'
            pass 
            self.matchRange(48, 57)




        finally:

            pass

    # $ANTLR end "DIGIT"



    # $ANTLR start "CHARACTER"
    def mCHARACTER(self, ):

        try:
            # SelectExpr.g:118:20: ( ( 'a' .. 'z' | 'A' .. 'Z' ) )
            # SelectExpr.g:118:22: ( 'a' .. 'z' | 'A' .. 'Z' )
            pass 
            if (65 <= self.input.LA(1) <= 90) or (97 <= self.input.LA(1) <= 122):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "CHARACTER"



    # $ANTLR start "SPECIAL"
    def mSPECIAL(self, ):

        try:
            # SelectExpr.g:119:20: ( '_' )
            # SelectExpr.g:119:22: '_'
            pass 
            self.match(95)




        finally:

            pass

    # $ANTLR end "SPECIAL"



    # $ANTLR start "A"
    def mA(self, ):

        try:
            # SelectExpr.g:121:12: ( ( 'A' | 'a' ) )
            # SelectExpr.g:121:14: ( 'A' | 'a' )
            pass 
            if self.input.LA(1) == 65 or self.input.LA(1) == 97:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "A"



    # $ANTLR start "N"
    def mN(self, ):

        try:
            # SelectExpr.g:121:12: ( ( 'N' | 'n' ) )
            # SelectExpr.g:121:14: ( 'N' | 'n' )
            pass 
            if self.input.LA(1) == 78 or self.input.LA(1) == 110:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "N"



    # $ANTLR start "B"
    def mB(self, ):

        try:
            # SelectExpr.g:122:12: ( ( 'B' | 'b' ) )
            # SelectExpr.g:122:14: ( 'B' | 'b' )
            pass 
            if self.input.LA(1) == 66 or self.input.LA(1) == 98:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "B"



    # $ANTLR start "O"
    def mO(self, ):

        try:
            # SelectExpr.g:122:12: ( ( 'O' | 'o' ) )
            # SelectExpr.g:122:14: ( 'O' | 'o' )
            pass 
            if self.input.LA(1) == 79 or self.input.LA(1) == 111:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "O"



    # $ANTLR start "C"
    def mC(self, ):

        try:
            # SelectExpr.g:123:12: ( ( 'C' | 'c' ) )
            # SelectExpr.g:123:14: ( 'C' | 'c' )
            pass 
            if self.input.LA(1) == 67 or self.input.LA(1) == 99:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "C"



    # $ANTLR start "P"
    def mP(self, ):

        try:
            # SelectExpr.g:123:12: ( ( 'P' | 'p' ) )
            # SelectExpr.g:123:14: ( 'P' | 'p' )
            pass 
            if self.input.LA(1) == 80 or self.input.LA(1) == 112:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "P"



    # $ANTLR start "D"
    def mD(self, ):

        try:
            # SelectExpr.g:124:12: ( ( 'D' | 'd' ) )
            # SelectExpr.g:124:14: ( 'D' | 'd' )
            pass 
            if self.input.LA(1) == 68 or self.input.LA(1) == 100:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "D"



    # $ANTLR start "Q"
    def mQ(self, ):

        try:
            # SelectExpr.g:124:12: ( ( 'Q' | 'q' ) )
            # SelectExpr.g:124:14: ( 'Q' | 'q' )
            pass 
            if self.input.LA(1) == 81 or self.input.LA(1) == 113:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "Q"



    # $ANTLR start "E"
    def mE(self, ):

        try:
            # SelectExpr.g:125:12: ( ( 'E' | 'e' ) )
            # SelectExpr.g:125:14: ( 'E' | 'e' )
            pass 
            if self.input.LA(1) == 69 or self.input.LA(1) == 101:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "E"



    # $ANTLR start "R"
    def mR(self, ):

        try:
            # SelectExpr.g:125:12: ( ( 'R' | 'r' ) )
            # SelectExpr.g:125:14: ( 'R' | 'r' )
            pass 
            if self.input.LA(1) == 82 or self.input.LA(1) == 114:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "R"



    # $ANTLR start "F"
    def mF(self, ):

        try:
            # SelectExpr.g:126:12: ( ( 'F' | 'f' ) )
            # SelectExpr.g:126:14: ( 'F' | 'f' )
            pass 
            if self.input.LA(1) == 70 or self.input.LA(1) == 102:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "F"



    # $ANTLR start "S"
    def mS(self, ):

        try:
            # SelectExpr.g:126:12: ( ( 'S' | 's' ) )
            # SelectExpr.g:126:14: ( 'S' | 's' )
            pass 
            if self.input.LA(1) == 83 or self.input.LA(1) == 115:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "S"



    # $ANTLR start "G"
    def mG(self, ):

        try:
            # SelectExpr.g:127:12: ( ( 'G' | 'g' ) )
            # SelectExpr.g:127:14: ( 'G' | 'g' )
            pass 
            if self.input.LA(1) == 71 or self.input.LA(1) == 103:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "G"



    # $ANTLR start "T"
    def mT(self, ):

        try:
            # SelectExpr.g:127:12: ( ( 'T' | 't' ) )
            # SelectExpr.g:127:14: ( 'T' | 't' )
            pass 
            if self.input.LA(1) == 84 or self.input.LA(1) == 116:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "T"



    # $ANTLR start "H"
    def mH(self, ):

        try:
            # SelectExpr.g:128:12: ( ( 'H' | 'h' ) )
            # SelectExpr.g:128:14: ( 'H' | 'h' )
            pass 
            if self.input.LA(1) == 72 or self.input.LA(1) == 104:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "H"



    # $ANTLR start "U"
    def mU(self, ):

        try:
            # SelectExpr.g:128:12: ( ( 'U' | 'u' ) )
            # SelectExpr.g:128:14: ( 'U' | 'u' )
            pass 
            if self.input.LA(1) == 85 or self.input.LA(1) == 117:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "U"



    # $ANTLR start "I"
    def mI(self, ):

        try:
            # SelectExpr.g:129:12: ( ( 'I' | 'i' ) )
            # SelectExpr.g:129:14: ( 'I' | 'i' )
            pass 
            if self.input.LA(1) == 73 or self.input.LA(1) == 105:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "I"



    # $ANTLR start "V"
    def mV(self, ):

        try:
            # SelectExpr.g:129:12: ( ( 'V' | 'v' ) )
            # SelectExpr.g:129:14: ( 'V' | 'v' )
            pass 
            if self.input.LA(1) == 86 or self.input.LA(1) == 118:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "V"



    # $ANTLR start "J"
    def mJ(self, ):

        try:
            # SelectExpr.g:130:12: ( ( 'J' | 'j' ) )
            # SelectExpr.g:130:14: ( 'J' | 'j' )
            pass 
            if self.input.LA(1) == 74 or self.input.LA(1) == 106:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "J"



    # $ANTLR start "W"
    def mW(self, ):

        try:
            # SelectExpr.g:130:12: ( ( 'W' | 'w' ) )
            # SelectExpr.g:130:14: ( 'W' | 'w' )
            pass 
            if self.input.LA(1) == 87 or self.input.LA(1) == 119:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "W"



    # $ANTLR start "K"
    def mK(self, ):

        try:
            # SelectExpr.g:131:12: ( ( 'K' | 'k' ) )
            # SelectExpr.g:131:14: ( 'K' | 'k' )
            pass 
            if self.input.LA(1) == 75 or self.input.LA(1) == 107:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "K"



    # $ANTLR start "X"
    def mX(self, ):

        try:
            # SelectExpr.g:131:12: ( ( 'X' | 'x' ) )
            # SelectExpr.g:131:14: ( 'X' | 'x' )
            pass 
            if self.input.LA(1) == 88 or self.input.LA(1) == 120:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "X"



    # $ANTLR start "L"
    def mL(self, ):

        try:
            # SelectExpr.g:132:12: ( ( 'L' | 'l' ) )
            # SelectExpr.g:132:14: ( 'L' | 'l' )
            pass 
            if self.input.LA(1) == 76 or self.input.LA(1) == 108:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "L"



    # $ANTLR start "Y"
    def mY(self, ):

        try:
            # SelectExpr.g:132:12: ( ( 'Y' | 'y' ) )
            # SelectExpr.g:132:14: ( 'Y' | 'y' )
            pass 
            if self.input.LA(1) == 89 or self.input.LA(1) == 121:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "Y"



    # $ANTLR start "M"
    def mM(self, ):

        try:
            # SelectExpr.g:133:12: ( ( 'M' | 'm' ) )
            # SelectExpr.g:133:14: ( 'M' | 'm' )
            pass 
            if self.input.LA(1) == 77 or self.input.LA(1) == 109:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "M"



    # $ANTLR start "Z"
    def mZ(self, ):

        try:
            # SelectExpr.g:133:12: ( ( 'Z' | 'z' ) )
            # SelectExpr.g:133:14: ( 'Z' | 'z' )
            pass 
            if self.input.LA(1) == 90 or self.input.LA(1) == 122:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "Z"



    def mTokens(self):
        # SelectExpr.g:1:8: ( T__91 | T__92 | DOT | SEP | END | COLON | AND | XOR | OR | NOT | IN | ASSIGN | EQ | NE | LE | GE | LT | GT | ADD | SUB | MUL | DIV | MOD | POW | SQ | DQ | LIST_BEGIN | LIST_END | AGE_BEGIN | AGE_END | SELECT | FROM | WHERE | AS | THIS | TIME | AS_SCENE | AS_LIST | AS_VALUE | AS_DICT | NEWLINE | WS | COMMENT | LINE_COMMENT | STRING | INTEGER | FLOAT | TRUE | FALSE | PHRASE )
        alt20 = 50
        alt20 = self.dfa20.predict(self.input)
        if alt20 == 1:
            # SelectExpr.g:1:10: T__91
            pass 
            self.mT__91()


        elif alt20 == 2:
            # SelectExpr.g:1:16: T__92
            pass 
            self.mT__92()


        elif alt20 == 3:
            # SelectExpr.g:1:22: DOT
            pass 
            self.mDOT()


        elif alt20 == 4:
            # SelectExpr.g:1:26: SEP
            pass 
            self.mSEP()


        elif alt20 == 5:
            # SelectExpr.g:1:30: END
            pass 
            self.mEND()


        elif alt20 == 6:
            # SelectExpr.g:1:34: COLON
            pass 
            self.mCOLON()


        elif alt20 == 7:
            # SelectExpr.g:1:40: AND
            pass 
            self.mAND()


        elif alt20 == 8:
            # SelectExpr.g:1:44: XOR
            pass 
            self.mXOR()


        elif alt20 == 9:
            # SelectExpr.g:1:48: OR
            pass 
            self.mOR()


        elif alt20 == 10:
            # SelectExpr.g:1:51: NOT
            pass 
            self.mNOT()


        elif alt20 == 11:
            # SelectExpr.g:1:55: IN
            pass 
            self.mIN()


        elif alt20 == 12:
            # SelectExpr.g:1:58: ASSIGN
            pass 
            self.mASSIGN()


        elif alt20 == 13:
            # SelectExpr.g:1:65: EQ
            pass 
            self.mEQ()


        elif alt20 == 14:
            # SelectExpr.g:1:68: NE
            pass 
            self.mNE()


        elif alt20 == 15:
            # SelectExpr.g:1:71: LE
            pass 
            self.mLE()


        elif alt20 == 16:
            # SelectExpr.g:1:74: GE
            pass 
            self.mGE()


        elif alt20 == 17:
            # SelectExpr.g:1:77: LT
            pass 
            self.mLT()


        elif alt20 == 18:
            # SelectExpr.g:1:80: GT
            pass 
            self.mGT()


        elif alt20 == 19:
            # SelectExpr.g:1:83: ADD
            pass 
            self.mADD()


        elif alt20 == 20:
            # SelectExpr.g:1:87: SUB
            pass 
            self.mSUB()


        elif alt20 == 21:
            # SelectExpr.g:1:91: MUL
            pass 
            self.mMUL()


        elif alt20 == 22:
            # SelectExpr.g:1:95: DIV
            pass 
            self.mDIV()


        elif alt20 == 23:
            # SelectExpr.g:1:99: MOD
            pass 
            self.mMOD()


        elif alt20 == 24:
            # SelectExpr.g:1:103: POW
            pass 
            self.mPOW()


        elif alt20 == 25:
            # SelectExpr.g:1:107: SQ
            pass 
            self.mSQ()


        elif alt20 == 26:
            # SelectExpr.g:1:110: DQ
            pass 
            self.mDQ()


        elif alt20 == 27:
            # SelectExpr.g:1:113: LIST_BEGIN
            pass 
            self.mLIST_BEGIN()


        elif alt20 == 28:
            # SelectExpr.g:1:124: LIST_END
            pass 
            self.mLIST_END()


        elif alt20 == 29:
            # SelectExpr.g:1:133: AGE_BEGIN
            pass 
            self.mAGE_BEGIN()


        elif alt20 == 30:
            # SelectExpr.g:1:143: AGE_END
            pass 
            self.mAGE_END()


        elif alt20 == 31:
            # SelectExpr.g:1:151: SELECT
            pass 
            self.mSELECT()


        elif alt20 == 32:
            # SelectExpr.g:1:158: FROM
            pass 
            self.mFROM()


        elif alt20 == 33:
            # SelectExpr.g:1:163: WHERE
            pass 
            self.mWHERE()


        elif alt20 == 34:
            # SelectExpr.g:1:169: AS
            pass 
            self.mAS()


        elif alt20 == 35:
            # SelectExpr.g:1:172: THIS
            pass 
            self.mTHIS()


        elif alt20 == 36:
            # SelectExpr.g:1:177: TIME
            pass 
            self.mTIME()


        elif alt20 == 37:
            # SelectExpr.g:1:182: AS_SCENE
            pass 
            self.mAS_SCENE()


        elif alt20 == 38:
            # SelectExpr.g:1:191: AS_LIST
            pass 
            self.mAS_LIST()


        elif alt20 == 39:
            # SelectExpr.g:1:199: AS_VALUE
            pass 
            self.mAS_VALUE()


        elif alt20 == 40:
            # SelectExpr.g:1:208: AS_DICT
            pass 
            self.mAS_DICT()


        elif alt20 == 41:
            # SelectExpr.g:1:216: NEWLINE
            pass 
            self.mNEWLINE()


        elif alt20 == 42:
            # SelectExpr.g:1:224: WS
            pass 
            self.mWS()


        elif alt20 == 43:
            # SelectExpr.g:1:227: COMMENT
            pass 
            self.mCOMMENT()


        elif alt20 == 44:
            # SelectExpr.g:1:235: LINE_COMMENT
            pass 
            self.mLINE_COMMENT()


        elif alt20 == 45:
            # SelectExpr.g:1:248: STRING
            pass 
            self.mSTRING()


        elif alt20 == 46:
            # SelectExpr.g:1:255: INTEGER
            pass 
            self.mINTEGER()


        elif alt20 == 47:
            # SelectExpr.g:1:263: FLOAT
            pass 
            self.mFLOAT()


        elif alt20 == 48:
            # SelectExpr.g:1:269: TRUE
            pass 
            self.mTRUE()


        elif alt20 == 49:
            # SelectExpr.g:1:274: FALSE
            pass 
            self.mFALSE()


        elif alt20 == 50:
            # SelectExpr.g:1:280: PHRASE
            pass 
            self.mPHRASE()







    # lookup tables for DFA #20

    DFA20_eot = DFA.unpack(
        u"\3\uffff\1\50\3\uffff\5\47\1\61\1\uffff\1\63\1\65\3\uffff\1\70"
        u"\2\uffff\1\71\1\73\4\uffff\1\74\1\77\1\47\1\103\1\107\1\111\1\47"
        u"\1\45\1\114\1\uffff\1\115\3\uffff\1\47\1\117\1\47\1\121\1\47\1"
        u"\123\15\uffff\2\47\1\uffff\3\47\1\uffff\3\47\1\uffff\1\47\1\uffff"
        u"\2\47\2\uffff\1\137\1\uffff\1\140\1\uffff\1\141\1\uffff\11\47\1"
        u"\111\1\47\3\uffff\2\47\1\157\2\47\1\162\1\103\1\163\1\107\1\47"
        u"\1\165\1\47\1\74\1\uffff\1\77\1\170\2\uffff\1\111\1\uffff\1\47"
        u"\1\172\1\uffff\1\47\1\uffff\3\47\1\165"
        )

    DFA20_eof = DFA.unpack(
        u"\177\uffff"
        )

    DFA20_min = DFA.unpack(
        u"\1\11\2\uffff\1\60\3\uffff\1\116\1\117\1\122\1\117\1\116\1\75\1"
        u"\uffff\2\75\3\uffff\1\52\2\uffff\2\0\4\uffff\2\60\1\110\3\60\1"
        u"\111\1\12\1\11\1\uffff\1\56\3\uffff\1\104\1\60\1\122\1\60\1\124"
        u"\1\60\15\uffff\1\114\1\105\1\uffff\1\117\1\114\1\105\1\uffff\1"
        u"\115\1\125\1\111\1\uffff\1\123\1\uffff\1\114\1\103\2\uffff\1\60"
        u"\1\uffff\1\60\1\uffff\1\60\1\uffff\1\105\1\116\1\115\1\123\1\122"
        u"\2\105\1\123\1\124\1\60\1\124\3\uffff\1\103\1\105\1\60\2\105\4"
        u"\60\1\105\1\60\1\124\1\60\1\uffff\2\60\2\uffff\1\60\1\uffff\1\117"
        u"\1\60\1\uffff\1\116\1\uffff\1\101\1\122\1\131\1\60"
        )

    DFA20_max = DFA.unpack(
        u"\1\175\2\uffff\1\71\3\uffff\1\163\1\157\1\162\1\157\1\156\1\75"
        u"\1\uffff\2\75\3\uffff\1\57\2\uffff\2\uffff\4\uffff\2\172\1\150"
        u"\3\172\1\151\1\12\1\40\1\uffff\1\71\3\uffff\1\144\1\172\1\162\1"
        u"\172\1\164\1\172\15\uffff\1\154\1\145\1\uffff\1\157\1\154\1\145"
        u"\1\uffff\1\155\1\165\1\151\1\uffff\1\163\1\uffff\1\154\1\143\2"
        u"\uffff\1\172\1\uffff\1\172\1\uffff\1\172\1\uffff\1\145\1\156\1"
        u"\155\1\163\1\162\2\145\1\163\1\164\1\172\1\164\3\uffff\1\143\1"
        u"\145\1\172\2\145\4\172\1\145\1\172\1\164\1\172\1\uffff\2\172\2"
        u"\uffff\1\172\1\uffff\1\157\1\172\1\uffff\1\156\1\uffff\1\141\1"
        u"\162\1\171\1\172"
        )

    DFA20_accept = DFA.unpack(
        u"\1\uffff\1\1\1\2\1\uffff\1\4\1\5\1\6\6\uffff\1\16\2\uffff\1\23"
        u"\1\24\1\25\1\uffff\1\27\1\30\2\uffff\1\33\1\34\1\35\1\36\11\uffff"
        u"\1\52\1\uffff\1\62\1\3\1\57\6\uffff\1\15\1\14\1\17\1\21\1\20\1"
        u"\22\1\53\1\54\1\26\1\31\1\55\1\32\1\45\2\uffff\1\61\3\uffff\1\60"
        u"\3\uffff\1\46\1\uffff\1\47\2\uffff\1\51\1\56\1\uffff\1\42\1\uffff"
        u"\1\11\1\uffff\1\13\13\uffff\1\7\1\10\1\12\15\uffff\1\40\2\uffff"
        u"\1\44\1\43\1\uffff\1\50\2\uffff\1\41\1\uffff\1\37\4\uffff"
        )

    DFA20_special = DFA.unpack(
        u"\26\uffff\1\1\1\0\147\uffff"
        )

            
    DFA20_transition = [
        DFA.unpack(u"\1\45\1\44\2\uffff\1\43\22\uffff\1\45\1\15\1\27\2\uffff"
        u"\1\24\1\uffff\1\26\1\1\1\2\1\22\1\20\1\4\1\21\1\3\1\23\12\46\1"
        u"\6\1\5\1\16\1\14\1\17\2\uffff\1\7\2\47\1\42\1\47\1\35\2\47\1\13"
        u"\2\47\1\40\1\47\1\12\1\11\3\47\1\34\1\37\1\47\1\41\1\36\1\10\2"
        u"\47\1\30\1\uffff\1\31\1\25\1\47\1\uffff\1\7\2\47\1\42\1\47\1\35"
        u"\2\47\1\13\2\47\1\40\1\47\1\12\1\11\3\47\1\34\1\37\1\47\1\41\1"
        u"\36\1\10\2\47\1\32\1\uffff\1\33"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\12\51"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\52\4\uffff\1\53\32\uffff\1\52\4\uffff\1\53"),
        DFA.unpack(u"\1\54\37\uffff\1\54"),
        DFA.unpack(u"\1\55\37\uffff\1\55"),
        DFA.unpack(u"\1\56\37\uffff\1\56"),
        DFA.unpack(u"\1\57\37\uffff\1\57"),
        DFA.unpack(u"\1\60"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\62"),
        DFA.unpack(u"\1\64"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\66\4\uffff\1\67"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\0\72"),
        DFA.unpack(u"\0\72"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\12\47\7\uffff\2\47\1\76\1\47\1\75\25\47\4\uffff\1"
        u"\47\1\uffff\2\47\1\76\1\47\1\75\25\47"),
        DFA.unpack(u"\12\47\7\uffff\1\101\20\47\1\100\10\47\4\uffff\1\47"
        u"\1\uffff\1\101\20\47\1\100\10\47"),
        DFA.unpack(u"\1\102\37\uffff\1\102"),
        DFA.unpack(u"\12\47\7\uffff\7\47\1\106\1\104\10\47\1\105\10\47\4"
        u"\uffff\1\47\1\uffff\7\47\1\106\1\104\10\47\1\105\10\47"),
        DFA.unpack(u"\12\47\7\uffff\10\47\1\110\21\47\4\uffff\1\47\1\uffff"
        u"\10\47\1\110\21\47"),
        DFA.unpack(u"\12\47\7\uffff\1\112\31\47\4\uffff\1\47\1\uffff\1\112"
        u"\31\47"),
        DFA.unpack(u"\1\113\37\uffff\1\113"),
        DFA.unpack(u"\1\44"),
        DFA.unpack(u"\2\45\2\uffff\1\45\22\uffff\1\45"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\51\1\uffff\12\46"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\116\37\uffff\1\116"),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u"\1\120\37\uffff\1\120"),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u"\1\122\37\uffff\1\122"),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
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
        DFA.unpack(u"\1\124\37\uffff\1\124"),
        DFA.unpack(u"\1\125\37\uffff\1\125"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\126\37\uffff\1\126"),
        DFA.unpack(u"\1\127\37\uffff\1\127"),
        DFA.unpack(u"\1\130\37\uffff\1\130"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\131\37\uffff\1\131"),
        DFA.unpack(u"\1\132\37\uffff\1\132"),
        DFA.unpack(u"\1\133\37\uffff\1\133"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\134\37\uffff\1\134"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\135\37\uffff\1\135"),
        DFA.unpack(u"\1\136\37\uffff\1\136"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u""),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u""),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\142\37\uffff\1\142"),
        DFA.unpack(u"\1\143\37\uffff\1\143"),
        DFA.unpack(u"\1\144\37\uffff\1\144"),
        DFA.unpack(u"\1\145\37\uffff\1\145"),
        DFA.unpack(u"\1\146\37\uffff\1\146"),
        DFA.unpack(u"\1\147\37\uffff\1\147"),
        DFA.unpack(u"\1\150\37\uffff\1\150"),
        DFA.unpack(u"\1\151\37\uffff\1\151"),
        DFA.unpack(u"\1\152\37\uffff\1\152"),
        DFA.unpack(u"\12\47\7\uffff\24\47\1\153\5\47\4\uffff\1\47\1\uffff"
        u"\24\47\1\153\5\47"),
        DFA.unpack(u"\1\154\37\uffff\1\154"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\155\37\uffff\1\155"),
        DFA.unpack(u"\1\156\37\uffff\1\156"),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u"\1\160\37\uffff\1\160"),
        DFA.unpack(u"\1\161\37\uffff\1\161"),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u"\1\164\37\uffff\1\164"),
        DFA.unpack(u"\12\47\7\uffff\10\47\1\166\21\47\4\uffff\1\47\1\uffff"
        u"\10\47\1\166\21\47"),
        DFA.unpack(u"\1\167\37\uffff\1\167"),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u""),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\171\37\uffff\1\171"),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\173\37\uffff\1\173"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\174\37\uffff\1\174"),
        DFA.unpack(u"\1\175\37\uffff\1\175"),
        DFA.unpack(u"\1\176\37\uffff\1\176"),
        DFA.unpack(u"\12\47\7\uffff\32\47\4\uffff\1\47\1\uffff\32\47")
    ]

    # class definition for DFA #20

    class DFA20(DFA):
        pass


        def specialStateTransition(self_, s, input):
            # convince pylint that my self_ magic is ok ;)
            # pylint: disable-msg=E0213

            # pretend we are a member of the recognizer
            # thus semantic predicates can be evaluated
            self = self_.recognizer

            _s = s

            if s == 0: 
                LA20_23 = input.LA(1)

                s = -1
                if ((0 <= LA20_23 <= 65535)):
                    s = 58

                else:
                    s = 59

                if s >= 0:
                    return s
            elif s == 1: 
                LA20_22 = input.LA(1)

                s = -1
                if ((0 <= LA20_22 <= 65535)):
                    s = 58

                else:
                    s = 57

                if s >= 0:
                    return s

            nvae = NoViableAltException(self_.getDescription(), 20, _s, input)
            self_.error(nvae)
            raise nvae
 



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import LexerMain
    main = LexerMain(SelectExprLexer)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)
