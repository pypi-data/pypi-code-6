# -*- coding: utf-8 -*-
from Acquisition import aq_base
from interlegis.intranetmodelo.departments.interfaces import IDepartment
from five import grok
from plone import api

grok.templatedir('templates')


class View (grok.View):
    """ Default view for Department content type
    """

    grok.context(IDepartment)

    def group(self):
        """Return the a group associated with this Department.

        :returns: A Group for this Department
        :rtype: GroupData object
        :raises:
            ValueError
        """
        group_id = self.context.title
        group = api.group.get(groupname=group_id)
        return group

    def department_members(self):
        """Returns the titles (or fullnames) for all Group Members

        :returns: A list of titles (for groups) or fullnames (for members)
        :rtype: list
        :raises:
            ValueError
        """
        group = self.group()
        members = api.user.get_users(group=group)
        members_list = []
        for member in members:
            if hasattr(aq_base(member), 'getGroupId'):
                title = '{0} (Group)'.format(member.getGroupId())
            else:
                title = member.getProperty('fullname')
            members_list.append(title)
        members_list.sort()
        return members_list
