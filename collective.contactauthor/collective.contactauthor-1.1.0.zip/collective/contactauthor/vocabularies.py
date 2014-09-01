# -*- coding: utf-8 -*-

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    # Plone 4.1
    from zope.schema.interfaces import IVocabularyFactory

from collective.contactauthor import messageFactory as _
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


class SecurityLevelVocabulary(object):
    """Vocabulary factory with anonymous access security levels
    """
    implements( IVocabularyFactory )

    def __call__(self, context):
        
        terms = [SimpleTerm(u'anon-with-captcha', u'anon-with-captcha', _(u'Anonymous, with captcha protection')),
                 SimpleTerm(u'free-for-all', u'free-for-all', _(u'Free for Anonymous, with no protection (WARNING)')),
                 SimpleTerm(u'authenticated-only', u'authenticated-only', _(u'No Anonymous access (Plone default)')),
                 ]
        return SimpleVocabulary(terms)


securityLevelVocabularyFactory = SecurityLevelVocabulary()
