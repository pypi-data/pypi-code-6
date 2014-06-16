from zope.interface import implements
from zope.viewlet.interfaces import IViewletManager
from zope.viewlet.manager import ConditionalViewletManager

from collective.contact.facetednav.browser.view import ACTIONS_ENABLED_KEY


class IBatchActions(IViewletManager):
    pass


class BatchActionsViewletManager(ConditionalViewletManager):
    implements(IBatchActions)


class IActions(IViewletManager):
    pass


class ActionsViewletManager(ConditionalViewletManager):
    implements(IActions)

    def available(self):
        return self.request[ACTIONS_ENABLED_KEY]