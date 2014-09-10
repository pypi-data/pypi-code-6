from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IE10Mode(common.ViewletBase):
    
    template = ViewPageTemplateFile('ie10mode.pt')
    
    steps = ['plone.portlet.static.Static', 'portal_factory', 'atct_edit']

    def index(self):
        if  set(self.request.steps).intersection(set(self.steps)):
            return self.template()
        return ''