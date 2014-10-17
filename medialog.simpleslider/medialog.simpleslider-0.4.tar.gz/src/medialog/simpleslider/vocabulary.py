from Products.CMFCore.utils import getToolByName
from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory

from plone import api

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('bda.plone.shop')

def format_size(size):
    return "".join(size).split(' ')[0]


def ImageSizeVocabulary(context):
    portal_properties = api.portal.get_tool(name='portal_properties')

    if 'imaging_properties' in portal_properties.objectIds():
        sizes = portal_properties.imaging_properties.getProperty('allowed_sizes')
        sizes += ('original',)
        terms = [ SimpleTerm(value=format_size(pair), token=format_size(pair), title=pair) for pair in sizes ]
        return SimpleVocabulary(terms)
    else:
        return SimpleVocabulary([
            SimpleTerm('mini', 'mini', u'Mini'),
            SimpleTerm('preview', 'preview', u'Preview'),
            SimpleTerm('large', 'large', u'Large'),
            SimpleTerm('original', 'original', u'Original'),
        ])  
      
    return SimpleVocabulary(terms)

directlyProvides(ImageSizeVocabulary, IVocabularyFactory)