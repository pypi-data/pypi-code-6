# -*- coding: utf-8 -*-
from rg.prenotazioni.browser.prenotazione_add import IAddForm
from zope.interface.declarations import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


class RequirableBookingFieldsVocabulary(object):
    implements(IVocabularyFactory)

    static_voc = SimpleVocabulary(
        [
            SimpleTerm(
                field,
                field,
                IAddForm[field].title
            )
            for field
            in (
                'email',
                'mobile',
                'phone',
                'subject',
                'agency',
            )
        ]
    )

    def __call__(self, context):
        '''
        Return all the gates defined in the PrenotazioniFolder
        '''
        return self.static_voc

RequirableBookingFieldsVocabularyFactory = RequirableBookingFieldsVocabulary()
