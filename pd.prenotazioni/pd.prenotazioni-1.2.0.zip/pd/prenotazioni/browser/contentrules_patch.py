# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.assignments import ManageAssignments
from plone.app.contentrules.rule import get_assignments
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.engine.interfaces import IRuleAssignmentManager
from zope.component import getUtility


class PatchedManageAssignments(ManageAssignments):
    """ Fix the behaviour described here:
    https://stackoverflow.com/questions/17615994/unassigning-content-rule-throws-traceback-error-in-plone-4-2  # noqa
    """
    def __call__(self):
        """
        """
        request = aq_inner(self.request)
        form = request.form

        if not 'form.button.Delete' in form:
            return super(PatchedManageAssignments, self).__call__()

        context = aq_inner(self.context)
        assignable = IRuleAssignmentManager(context)
        storage = getUtility(IRuleStorage)
        status = IStatusMessage(self.request)
        rule_ids = form.get('rule_ids', ())
        path = '/'.join(context.getPhysicalPath())

        for r in rule_ids:
            del assignable[r]
            assignments = get_assignments(storage[r])
            if path in assignments:
                get_assignments(storage[r]).remove(path, None)
        status.addStatusMessage(_(u"Assignments deleted."), type='info')
        return self.template()
