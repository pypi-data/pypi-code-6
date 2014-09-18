from Products.CMFCore.utils import getToolByName
from plone.portlets.interfaces import ILocalPortletAssignable
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from zope.component import getUtilitiesFor, getMultiAdapter

from seantis.dir.eventsportlet.events import IEventsPortlet


def update_portlet_schema(context, portlet_interface, attribute, value):
    """
    Helper function to update a schema of an already registered portlet.
    @param context: A Plone context.
    @param portlet_interface: The interface that the portlet implements.
    @param attribute: The name of the attribute to be added as string.
    @param value: The value, the attribute should be initialized with.

    from collective.setuphandlertools

    """
    urltool = getToolByName(context, "portal_url")
    site = urltool.getPortalObject()

    cat = getToolByName(site, 'portal_catalog')
    query = {'object_provides': ILocalPortletAssignable.__identifier__}

    all_brains = cat(**query)
    all_content = [brain.getObject() for brain in all_brains]
    all_content.append(site)
    for content in all_content:
        for manager_name, manager in getUtilitiesFor(IPortletManager,
                                                     context=content):
            mapping = getMultiAdapter((content, manager),
                                      IPortletAssignmentMapping)
            for id, assignment in mapping.items():
                if portlet_interface.providedBy(assignment):
                    try:
                        getattr(assignment, attribute)
                    except AttributeError:
                        setattr(assignment, attribute, value)


def upgrade_1000_to_1001(context):
    # Update existing portlets to the new portlet schema
    update_portlet_schema(context, IEventsPortlet, 'target_blank', False)

    # update js
    getToolByName(context, 'portal_javascripts').cookResources()
