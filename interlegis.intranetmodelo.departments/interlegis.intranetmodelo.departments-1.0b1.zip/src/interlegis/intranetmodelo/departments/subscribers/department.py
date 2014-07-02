# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from five import grok
from interlegis.intranetmodelo.departments.config import PROJECTNAME
from interlegis.intranetmodelo.departments.interfaces import IDepartment
from plone import api
from zope.lifecycleevent.interfaces import IObjectAddedEvent

import logging


logger = logging.getLogger(PROJECTNAME)


@grok.subscribe(IObjectAddedEvent)
def fix_department_groups(event, obj=None):
    """ Fix groups
    """
    if not obj:
        obj = event.object

    if not IDepartment.providedBy(obj):  # Not a department
        return

    parent = aq_parent(obj)

    if IDepartment.providedBy(parent):
        # Implement subgroups
        group_id = obj.title
        group = api.group.get(groupname=group_id)
        parent_group_id = parent.title
        parent_group = api.group.get(groupname=parent_group_id)
        members = api.user.get_users(group=parent_group)
        if group not in members:
            portal_groups = api.portal.get_tool('portal_groups')
            portal_groups.addPrincipalToGroup(group_id, parent_group_id)
            logger.info('Group {0} added as member to group {1}'.format(
                group_id,
                parent_group_id)
            )
