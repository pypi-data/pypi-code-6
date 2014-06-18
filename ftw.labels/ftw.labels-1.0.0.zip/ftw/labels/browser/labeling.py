from Products.Five.browser import BrowserView
from ftw.labels.interfaces import ILabeling


class Labeling(BrowserView):

    def update(self):
        """Update activated labels.
        """
        labeling = ILabeling(self.context)
        activate_labels = self.request.form.get('activate_labels', [])
        labeling.update(activate_labels)
        self.context.reindexObject(idxs=['labels'])
        return self._redirect()

    def _redirect(self):
        response = self.request.RESPONSE
        referer = self.request.get('HTTP_REFERER')
        if referer and referer is not 'localhost':
            response.redirect(referer)
        else:
            response.redirect(self.context.absolute_url())
