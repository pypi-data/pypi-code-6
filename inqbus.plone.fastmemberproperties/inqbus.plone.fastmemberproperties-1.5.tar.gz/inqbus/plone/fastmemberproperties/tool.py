from persistent import Persistent
from persistent.dict import PersistentDict
from zope.interface import implements
from zope.component import queryUtility
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

from Products.CMFPlone.utils import safe_unicode

try:
    from Products.membrane.interfaces import IPropertiesProvider
    membrane_supported = True
except:
    membrane_supported = False

from inqbus.plone.fastmemberproperties.interfaces import IFastmemberpropertiesTool

import logging
log = logging.getLogger("inqbus.plone.fastmemberproperties ")



class FastmemberpropertiesTool( Persistent ):
    """ A local utility to cache member properties.
        So that we can provide them very fast even for >> 1000 Members.
    """
    implements(IFastmemberpropertiesTool)

    def __init__(self):
        """ Sets up a local utiltiy
        """
        name = u'fastmemberproperties_tool'
        self.memberproperties = PersistentDict()
        self.portal = getSite()
        acl_userfolder = self.portal.acl_users
        member_objs = acl_userfolder.getUsers()
        for member in member_objs:
            self._register_memberproperties(member)

    def _register_memberproperties(self, member):
        """ Register or update memberproperties in fastmemberproperties_tool
            for a given MemberData object.
        """
        if not member:
            log.error("Error FastmemberpropertiesTool._register_memberproperties(), member is None")
            return
        member_id = member.getId()
        propdict = PersistentDict()
        for id, property in self.portal.portal_memberdata.propertyItems():
            propdict[id] = safe_unicode(member.getProperty(id))
        self.memberproperties[member_id] = propdict
        log.info("Register/Update memberproperties for \"%s\"" % member_id)

    def _unregister_memberproperties(self, member_id):
        """ Unregister memberproperties in fastmemberproperties_tool
            for a given member_id.
        """
        if self.memberproperties.has_key(member_id):
            del self.memberproperties[member_id]
            log.info("Unregister memberproperties for \"%s\"" % member_id)


    def get_all_memberproperties(self):
        """
        """
        log.debug("call FastmemberpropertiesTool.get_all_memberproperties()")
        return self.memberproperties

    def get_properties_for_member(self, memberid=None):
        """
        """
        if memberid and self.memberproperties.has_key(memberid):
            return self.memberproperties[memberid]


def update_memberproperties(obj, event=None):
    """ event handler which take the modified/created member
        and call _register_memberproperties method of
        FastmemberpropertiesTool
    """
    global membrane_supported
    if not obj:
        log.error("update_memberproperties: obj not set!")
        return
    fastmemberproperties_tool = queryUtility(IFastmemberpropertiesTool, 'fastmemberproperties_tool')
    if not fastmemberproperties_tool:
        log.error("fastmemberproperties_tool not found! skip \
                  registristration of member \"%s\"" % obj.getUserName())
        return
    if membrane_supported and IPropertiesProvider.providedBy(obj):
        portal = getSite()
        acl_userfolder = portal.acl_users
        obj = acl_userfolder.getUserById(obj.getUserName())
    fastmemberproperties_tool._register_memberproperties(obj)

def remove_memberproperties(obj, event=None):
    """ event handler which take the removed member
        and call _unregister_memberproperties method of
        FastmemberpropertiesTool
    """
    global membrane_supported
    if not obj:
        log.error("remove_memberproperties: obj not set!")
        return
    if hasattr(obj, 'object'):
        obj = obj.object
    fastmemberproperties_tool = queryUtility(IFastmemberpropertiesTool, 'fastmemberproperties_tool')
    if not fastmemberproperties_tool:
        log.error("fastmemberproperties_tool not found! skip \
                  unregistristration of member \"%s\"" % obj.getUserName())
        return
    member_id = obj.getUserName()
    fastmemberproperties_tool._unregister_memberproperties(member_id)
