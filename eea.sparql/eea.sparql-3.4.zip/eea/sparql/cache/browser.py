""" Browser
"""
from zope import event
from zope.lifecycleevent import ObjectModifiedEvent
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

class CacheView(BrowserView):
    """ Caching for sparql query results
    """
    def __call__(self):
        if "invalidate_cache" in self.request.form:
            event.notify(ObjectModifiedEvent(self.context))
            IStatusMessage(self.request).addStatusMessage("Cache invalidated")
        if "invalidate_last_working_results" in self.request.form:
            self.context.invalidateWorkingResult()
            message = "Last working results invalidated"
            IStatusMessage(self.request).addStatusMessage(message)

        return self.index()
