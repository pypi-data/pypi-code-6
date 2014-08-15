from ftw.profilehook.interfaces import IProfileHook
from Products.CMFCore.utils import getToolByName
from zope.component import queryAdapter
import re


def profile_imported(event):
    if not event.full_import:
        return

    profile = re.sub('^profile-', '', event.profile_id)
    site = getToolByName(event.tool, 'portal_url').getPortalObject()
    hook = queryAdapter(site, IProfileHook, name=profile)
    if hook:
        hook(site)
