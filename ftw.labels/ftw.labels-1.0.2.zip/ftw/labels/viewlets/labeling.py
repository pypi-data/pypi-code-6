from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from ftw.labels.interfaces import ILabeling
from ftw.labels.interfaces import ILabelSupport
from Products.CMFCore.utils import getToolByName


class LabelingViewlet(ViewletBase):

    index = ViewPageTemplateFile('labeling.pt')

    @property
    def available(self):
        if not self.available_labels:
            return False
        if 'portal_factory' in self.context.absolute_url():
            return False
        if not ILabelSupport.providedBy(self.context):
            return False
        if not tuple(self.available_labels):
            return False
        return True

    @property
    def active_labels(self):
        return ILabeling(self.context).active_labels()

    @property
    def available_labels(self):
        return ILabeling(self.context).available_labels()

    @property
    def can_edit(self):
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.checkPermission('ftw.labels: Change Labels', self.context)
