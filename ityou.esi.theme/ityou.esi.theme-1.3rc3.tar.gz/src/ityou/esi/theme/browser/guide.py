# -*- coding: utf-8 -*-
import logging
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from ityou.jsonapi.json.json_utils import JsonApiUtils
ju = JsonApiUtils()

guide = {}
try:
    # --- ESI GUIDED TOUR --------------------------
    from ityou.esi.theme.guides import GUIDE
    guide.update(GUIDE)

    # --- DUMMY BOOTSTRAPTOUR -----------------------
    GUIDE = {'dummy': {'element':'dummy', 'title':'Dummy', 'content':'Dummy Inhalte', 'placement':''}}
    guide.update(GUIDE)

    # --- Weitere Tours -----------------------------
    # from ityou.follow.guides import GUIDE
    # guide.update(GUIDE)
    from ityou.astream.guides import GUIDE
    guide.update(GUIDE)

except:
    logging.warn('Could not load all guides - Loaded guides: %s' % str(guide.keys()) )



class GuideView(BrowserView):
    """View which calls template for guided tour.
    """
    
    def __call__(self):
        """
        """
        context = aq_inner(self.context)
        page = context.REQUEST.get('p')

        if page:
            if guide.has_key(page):
                return ju._json_response( context,  guide[page] )
            else:
                error = {
                    'error': 'Wrong Page Id', 
                    'error-message': "Please enter a correct Page Id. Available Page Ids: %s" % str(guide.keys())
                }
        else:
            error = {
                'error': 'No Page Id', 
                'error-message': "Please enter a Page Id i.e. @@guide?p=message"
            }
        return ju._json_response( context, error )




