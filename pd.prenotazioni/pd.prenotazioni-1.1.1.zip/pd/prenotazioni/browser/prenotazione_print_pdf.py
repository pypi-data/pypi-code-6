# -*- coding: utf-8 -*-
from pd.prenotazioni import prenotazioniMessageFactory as _
from plone.memoize.view import memoize
from rg.prenotazioni.browser.prenotazione_print import PrenotazionePrint


class PrenotazionePrintPDF(PrenotazionePrint):
    '''
    This is a view to proxy autorizzazione
    '''
    title = _("booking_receipt", "Booking receipt")

    footer_text = "Comune di Padova - Sistema di prenotazione unico"

    @property
    @memoize
    def rml_options(self):
        '''
        Return the options for this prenotazione
        '''
        return {'prenotazione': self.prenotazione,
                'logo': ''
                }
