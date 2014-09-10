from plone.app.contentrules.handlers import execute
from zope.app.component.hooks import getSite


def unsubscribed(event):
    # The object added event executes too early for Archetypes objects.
    # We need to delay execution until we receive a subsequent IObjectInitializedEvent
    portal = getSite()
    execute(portal, event)


def confirmed(event):
    """When a subscription has been confirmed, execute rules assigned to channel folder.
    """
    portal = getSite()
    execute(portal, event)
