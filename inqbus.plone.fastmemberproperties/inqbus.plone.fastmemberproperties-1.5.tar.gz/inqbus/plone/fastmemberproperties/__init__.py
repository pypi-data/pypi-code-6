from zope.event import notify
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite
from zope.interface import implements
import zope.component.interfaces
from inqbus.plone.fastmemberproperties.interfaces import IMemberWillBeRemovedEvent

import logging
logger = logging.getLogger('inqbus.plone.fastmemberproperties')


class MemberWillBeRemovedEvent(zope.component.interfaces.ObjectEvent):
    """An object has been modified"""
    implements(IMemberWillBeRemovedEvent)
    __module__ = 'zope.app.event.objectevent'

    def __init__(self, object, *descriptions) :
        super(MemberWillBeRemovedEvent, self).__init__(object)
        self.descriptions = descriptions


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    # Monkey patched Products.PlonePAS.plugins.property.ZODBMutablePropertyProvider.setPropertiesForUser, to fire an event on change MemberData onjects.
    from zope.lifecycleevent import ObjectModifiedEvent
    def patched_setPropertiesForUser(self, user, propertysheet):
        # fire a zope event to inform other components:
        notify(ObjectModifiedEvent(user))
        return self.orig_setPropertiesForUser(user, propertysheet)
    from Products.PlonePAS.plugins.property import ZODBMutablePropertyProvider
    ZODBMutablePropertyProvider.orig_setPropertiesForUser = ZODBMutablePropertyProvider.setPropertiesForUser
    ZODBMutablePropertyProvider.setPropertiesForUser = patched_setPropertiesForUser
    logger.info('Monkey patched Products.PlonePAS.plugins.property.ZODBMutablePropertyProvider.setPropertiesForUser, to fire an event on change MemberData onjects!')


    # Monkey patched Products.CMFCore.MembershipTool.MembershipTool.deleteMembers, to fire an event before remove a member.
    def patched_deleteMembers(self, member_ids, delete_memberareas=1,
                      delete_localroles=1, REQUEST=None):
        portal = getSite()
        acl_userfolder = portal.acl_users
        for member_id in member_ids:
            member = acl_userfolder.getUserById(member_id)
            # fire a zope event to inform other components:
            notify(MemberWillBeRemovedEvent(member))
        return self.orig_deleteMembers(member_ids, delete_memberareas,
                      delete_localroles, REQUEST)
    from Products.CMFCore.MembershipTool import MembershipTool
    MembershipTool.orig_deleteMembers = MembershipTool.deleteMembers
    MembershipTool.deleteMembers = patched_deleteMembers
    logger.info('Monkey patched Products.CMFCore.MembershipTool.MembershipTool.deleteMembers, to fire an event before remove a member!')
