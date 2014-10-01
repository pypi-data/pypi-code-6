from zope.interface import implements, Interface
from zope.component import queryUtility
from Acquisition import aq_base

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from zettwerk.mailtemplates.interfaces import IMessageTemplateUserFilter
from zettwerk.mailtemplates.interfaces import IMessageTemplateUserObjectFilter


class Isend_emailView(Interface):
    """
    send_email view interface
    """


class send_emailView(BrowserView):
    """
    send_email browser view
    """
    implements(Isend_emailView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def portal_groups(self):
        return getToolByName(self.context, 'portal_groups')

    def __call__(self):
        """ do something """
        try:
            targets = self._getMemberTargets()
        except ValueError as e:
            return e.message

        portal_templates = getToolByName(self, 'portal_mail_templates')
        template_id = self.request.get('template', '')

        for member in targets:
            username = member.getUserName()
            portal_templates.sendTemplate(
                template_id, username
                )

        return "sent %s emails" % (len(targets))

    def _getMemberTargets(self):
        """ return the target member objects """
        targets = self._getUserTarget()
        if not targets:
            targets = self._getGroupTargets()

            extra_filter = self.request.get('extra_filter', '')
            if extra_filter:
                extra = queryUtility(IMessageTemplateUserFilter,
                                     name=extra_filter)
                if not extra:
                    raise ValueError(
                        'Invalid extra filter given: %s' % extra
                        )
                targets = extra.filteredMembers(targets)

            extra_object_filters = self.request.get('extra_object_filters', {})
            for object_filter, path in extra_object_filters.items():
                if path:
                    obj = self.context.restrictedTraverse(path)
                    obj_filter = queryUtility(IMessageTemplateUserObjectFilter,
                                              name=object_filter)
                    if not obj_filter:
                        raise ValueError(
                            'Invalid extra obj filter ' \
                                'given: %s' % object_filter
                            )
                    targets = obj_filter.filteredMembers(targets, obj)

        return targets

    def _getUserTarget(self):
        targets = []
        user_id = self.request.get('user_id', '')
        if user_id:
            member = self.portal_membership.getMemberById(user_id)
            if not member:
                raise ValueError('Invalid user_id given: %s' % (user_id))
            targets.append(member)
        return targets

    def _getGroupTargets(self):
        targets = []
        group_id = self.request.get('group_id', '')
        if not group_id:
            targets = self.portal_membership.listMembers()
        else:
            group = self.portal_groups.getGroupById(group_id)
            if not group:
                raise ValueError('Invalid group_id given: %s' % (group_id))
            targets = group.getGroupMembers()

        ## only use top-level members, no members of recursive groups
        return [t for t in targets \
                if not (hasattr(aq_base(t), 'isGroup') and \
                        aq_base(t).isGroup())]
        return targets
