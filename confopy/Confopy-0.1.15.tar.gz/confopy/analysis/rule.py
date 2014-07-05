# coding: utf-8
'''
File: rule.py
Author: Oliver Zscheyge
Description:
    Rule superclass.
'''

from localizable import Localizable

#class FunctionProvider(object):
#    """Provides a language independent interface to functions operating on
#       a document (metrics, predicates etc.)
#
#    """
#    def __init__(self):
#        self.foo = lambda x: x
#        self.length = len
#
#        # Sentence oriented functions
#        self.has_filler = None
#        self.has_redundancy = None
#        self.has_tautology = None
#        self.has_dead_verbs = None
#        self.has_boosting_adverbs = None
#
#
#class MessageFormat:
#    PAGE = "%page"
#    LINE = "%line"
#    WORD = "%word"
#    SENTENCE  = "%sent"
#    PARAGRAPH = "%para"
#    SECTION   = "%sect"
#
#
#class RuleKind(object):
#    """Kind of a rule.
#    Suitable for masking.
#    """
#
#    UNSPECIFIED = 0 << 0
#
#    # Scope
#    #DOCUMENT    = 1 << 0
#    #SECTION     = 1 << 1
#    #PARAGRAPH   = 1 << 2
#    #SENTENCE    = 1 << 3
#
#    # Level/domain
#    FORM        = 1 << 5
#    LANGUAGE    = 1 << 6
#    CONTENT     = 1 << 7


class Rule(Localizable):
    """Base class to describe rule based knowledge.
    """
    def __init__(self, ID=u"", language=u"", brief=u"", description=u""):
        super(Rule, self).__init__(ID, language, brief, description)

    def evaluate(self, node):
        """Evaluates the rule on a Node.
        Return:
            Bool whether this Rule is satisfied or not.
        """
        return False

#    def __str__(self):
#        return "Rule(%s, %s, %s)" % (self.ID, self.language, self.brief)
#
#    def __repr__(self):
#        return self.__str__()
