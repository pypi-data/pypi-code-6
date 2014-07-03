# coding: utf-8

from confopy.analysis import Rule, Scope
#from confopy.analysis.rule import MessageFormat as MF

class MF(object):
    """docstring for MF"""

    PAGE = u""
    SECTION = u""
    SENTENCE = u""

    def __init__(self, arg):
        super(MF, self).__init__()
        self.arg = arg


RULES = [
  Rule( "Foo"
      , "Bar"
      , Scope.UNSPECIFIED
      , lambda doc, sec, par, sen:
            (not 1 == 2) or (False)
      )

, Rule( "Template"
      , "Template message"
      , 0
      , lambda doc, sec, par, sen:
            (not False) or ()
      )

, Rule( "Subsections"
      , "Section %s has only one subsection or/and lacks an introduction." % MF.SECTION
      , Scope.SECTION | Scope.FORM
      , lambda doc, sec, par, sen:
            (not sec.count_subsections() > 0) or (sec.count_subsections() >= 2 and sec.has_introduction())
      )

, Rule( "Fillers"
      , "Page %s: The sentence \"%s\" contains fillers." % (MF.PAGE, MF.SENTENCE)
      , Scope.SENTENCE | Scope.LANGUAGE
      , lambda doc, sec, par, sen:
            (not sen.has_filler())
      )

, Rule( "Dead Verbs"
      , "Page %s: The sentence \"%s\" contains dead verbs." % (MF.PAGE, MF.SENTENCE)
      , Scope.SENTENCE | Scope.LANGUAGE
      , lambda doc, sec, par, sen:
            (not sen.has_dead_verbs())
      )

, Rule( "Boosting Adverbs"
      , "Page %s: The sentence \"%s\" contains boosting adverbs." % (MF.PAGE, MF.SENTENCE)
      , Scope.SENTENCE | Scope.LANGUAGE
      , lambda doc, sec, par, sen:
            (not sen.has_boosting_adverbs())
      )

, Rule( "Redundancies and Tautologies"
      , "Page %s: The sentence \"%s\" contains a redundancy or tautology." % (MF.PAGE, MF.SENTENCE)
      , Scope.SENTENCE | Scope.LANGUAGE
      , lambda doc, sec, par, sen:
            (not sen.has_redundancy()) and (not sen.has_tautology())
      )
]
