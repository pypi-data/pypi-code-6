"""tokenizertools -- Tokenizing iterators that support
__iter__ and __next__ for lexing text files.

class Tokenizer -- Base class.

class RegexTokenizer -- Python re-based tokenizer.

class FlexTokenizer -- Interface to flex-based tokenizer (future).

To use RegexTokenizer, derive your tokenizer class from RegexTokenizer.
Define the class variable 'spec'.  'spec' must be a list of match
specification tuples, in one of these forms:

 * (regular-expression, callable)
 * (regular-expression, (callable, start-state))
 * (regular-expression, (callable, '?'))
 * (regular-expression, callable, [ start-states-list ])
 * (regular-expreesion, (callable, start-state), [ start-states-list ])
 * (regular-expreesion, (callable, '?'), [ start-states-list ])
 
Fixed start-state transitions are specified by putting a hashable (such
as a string) in start-state.  If start-state is absent or None, there is
no transition.  If start-state is '?', then the callable must compute
and return a tuple of (token,state).

Rules are only active when the tokenizer is in one of the start states
listed in start-states-list. The start states list defaults to [0],
the default state.  Start state names can be any hashable, since they
become dictionary keys.  The begin() method can be used to set the
start state from arbitrary code, but should rarely be needed.

The class FlexTokenizer is a place holder for work in progress. Eventually,
the FlexTokenizer class will implement an interface to a flex-based lexer
implemented as a Python C extension.  It goes without saying that this will
increase the complexity of the application build.  The application interface
to the lexer will remain the same, so that a FlexTokenizer can easily be
used as a high performance drop-in replacement for a RegexTokenizer.
"""

# FIXME: Insert license here.

import re
from lookaheadtools import Lexpos
import lookaheadtools

class Tokenizer(object):
    "Base class for Tokenizer iterators."
    def __iter__(self):
        return self
    def next(self):
        return self.__next__() # Python 2.6, 2.7 compatibility
    def __next__(self):
        raise NotImplementedError('Abstract') # Implement lexer here in derived class.
    def begin(self, aState):
        raise NotImplementedError('Abstract') # Implement in derived class.
    def discard(self, c, lexpos):
        "Action taken when discarding characters."
        print 'Discarding:',c,lexpos
    def consume(self, require = None):
        "Guarded form of next(). require(aToken) is a guard predicate."
        t = next(self)
        if require != None:
            assert require(t)
        return t

class TokenizeAhead(lookaheadtools.Lookahead):
    def consume(self, require = None):
        t = next(self)
        if require != None:
            assert require(t)
        return t
    def accept(self, require):
        "Return next token if require(nextToken) returns True, else return None."
        if require(self[0]):
            return next(self)
        return None

class RegexTokenizer(Tokenizer):
    "Tokenizer built upon re module regular expressions."
    # Derive a class from RegexTokenizer, and define the class
    # variable 'spec', which is a list of match specification tuples,
    # one of:
    # (regular-expression, callable)
    # (regular-expreesion, (callable, begin-state))
    # (regular-expreesion, (callable, '?'))
    # (regular-expression, callable, [ start-states-list ])
    # (regular-expreesion, (callable, begin-state), [ start-states-list ])
    # (regular-expreesion, (callable, '?'), [ start-states-list ])
    # Fixed start-state transitions are specified with a fixed begin-state.
    # If begin-state is absent or None, there is no transition.
    # If begin-state is '?', then the callable must compute and return
    # a tuple of (token,state). 
    # The applicable start states list defaults to [0] which means the
    # default state.  Start state names can be any hashable, as they become
    # dictionary keys.
    def __init__(self, anOpenFile, trackingCookie = None):
        self._la = lookaheadtools.LexAhead(anOpenFile, trackingCookie)
        try:
            # Does rules dict exist?
            self.__class__._rulesd
        except AttributeError:
            # No, compile one and cache it.
            self.__class__.compileSpec()
        self.begin(0)
    def begin(self, aState):
        assert aState in self.__class__._rulesd
        self._startState = aState
    @classmethod
    def compileSpec(cls):
        "Compile _rulesd from spec."
        # These two list comprehensions canonicalize each specification
        # tuple into a normalized quadruple.
        # 1. Fill in default start state where required.
        t = [(lambda regex, action, starts=[0]: \
              (regex, action, starts))\
             (*rule) for rule in cls.spec]
        # 2. Fill in state transition information.
        t = [(re.compile(regex),
             action[0] if isinstance(action, tuple) else action,
             action[1] if isinstance(action, tuple) else None,
             starts) \
                 for regex, action, starts in t]
        # Construct the rules dictionary.
        cls._rulesd = dict()
        for cre, action, begin, starts in t:
            for state in starts:
                try:
                    cls._rulesd[state].append((cre,action,begin))
                except KeyError:
                    cls._rulesd[state] = [(cre,action,begin)]
    def __next__(self):
        yytext = '' 
        while yytext == '':
            lexpos = self._la.lexpos
            rule = iter(self.__class__._rulesd[self._startState])
            while True:
                try:
                    cpatt, action, start = next(rule)
                    yytext = self._la.accept_re(cpatt)
                    if yytext != '':
                        break
                except StopIteration:
                    # Discard a character and try again.
                    self.discard(next(self._la), lexpos) # Might raise StopIteration
                    # and if it does, that StopIteration propagates up.
                    break
            if yytext == '':
                # We get here after exhausting all rules and doing a discard.
                continue
            # Found a match.
            if action == None:
                # If the action is None, then simply consume the match.
                tkn = None
            elif start == '?':
                # Make token and compute a new state.
                tkn, start = action(yytext, lexpos)
            else:
                # Make a token. Possibly with transition to constant state.
                tkn = action(yytext, lexpos)
            if start != None:
                self.begin(start)
            if tkn == None:
                # Either action==None, or action returned token==None
                # so clear yytext and search for another match now that
                # any state transitions have been handled.
                yytext = ''
        return tkn

class FlexTokenizer(Tokenizer):
    "Interface to a flex-based tokenizer implemented as a C extension."
    def __init__(self, anOpenFile, trackingCookie = None):
        pass
    def __next__(self):
        raise NotImplementedError('FIXME: To be written. Call lexer here.')

        

