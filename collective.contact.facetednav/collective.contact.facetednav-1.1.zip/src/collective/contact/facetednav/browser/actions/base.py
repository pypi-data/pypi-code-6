from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase


class BatchActionBase(ViewletBase):
    index = ViewPageTemplateFile('batchaction.pt')
    klass = 'context'
    onclick = None
    name = None
    weight = 1000

    def available(self):
        return True


class ActionBase(ViewletBase):
    index = ViewPageTemplateFile('action.pt')
    klass = None
    onclick = None
    icon = None
    name = None
    weight = 1000

    def available(self):
        return True