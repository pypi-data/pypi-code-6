from plone.memoize.instance import memoize
from zope.i18n import translate

from Acquisition import aq_base
from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.controlpanel.form import ControlPanelView

from .. import ESI_VERSION

class OverviewControlPanel(ControlPanelView):

    template = ViewPageTemplateFile('overview.pt')

    def __call__(self):
        self.request.set('disable_border', 1)
        return self.template()

    @memoize
    def cptool(self):
        return getToolByName(aq_inner(self.context), 'portal_controlpanel')

    @memoize
    def migration(self):
        return getToolByName(aq_inner(self.context), 'portal_migration')

    @memoize
    def core_versions(self):
        return self.migration().coreVersions()

    def version_overview(self):
        versions=[]
        
        versions.append(ESI_VERSION)
        versions.append('Plone ' + self.migration().getInstanceVersion())
        
        core_versions = self.core_versions()
        for v in ('CMF', 'Zope', 'Python'):
            versions.append(v + ' ' + core_versions.get(v))
        pil = core_versions.get('PIL', None)
        if pil is not None:
            versions.append('PIL ' + pil)
        return versions

    @memoize
    def is_dev_mode(self):
        qi = getToolByName(aq_inner(self.context), 'portal_quickinstaller')
        return qi.isDevelopmentMode()

    def upgrade_warning(self):
        mt = getToolByName(aq_inner(self.context), 'portal_migration')
        return mt.needUpgrading()

    def mailhost_warning(self):
        mailhost = getToolByName(aq_inner(self.context), 'MailHost', None)
        if mailhost is None:
            return True
        mailhost = getattr(aq_base(mailhost), 'smtp_host', None)
        email = getattr(aq_inner(self.context), 'email_from_address', None)
        if mailhost and email:
            return False
        return True

    def pil(self):
        return 'PIL' in self.core_versions()

