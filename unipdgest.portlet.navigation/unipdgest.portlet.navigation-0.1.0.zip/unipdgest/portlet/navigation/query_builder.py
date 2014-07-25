# -*- coding: utf-8 -*-

from zope.interface import implements
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.root import getNavigationRoot
from Products.CMFPlone import utils


class NavtreeQueryBuilder(object):
    """Build a navtree query for accordion portlet
    """
    implements(INavigationQueryBuilder)

    def __init__(self, context, subtree=False):
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')

        # Acquire a custom nav query if available
        customQuery = getattr(context, 'getCustomNavQuery', None)
        if customQuery is not None and utils.safe_callable(customQuery):
            query = customQuery()
        else:
            query = {}

        # Construct the path query

        rootPath = getNavigationRoot(context)
        currentPath = '/'.join(context.getPhysicalPath())

        # If we are above the navigation root, a navtree query would return
        # nothing (since we explicitly start from the root always). Hence,
        # use a regular depth-1 query in this case.

        if subtree:
            query['path'] = {'query': currentPath, 'depth': 2}
        elif not currentPath.startswith(rootPath):
            query['path'] = {'query': rootPath, 'depth': 2}
        else:
            query['path'] = {'query': currentPath, 'navtree': 1, 'depth': 2, }

        topLevel = navtree_properties.getProperty('topLevel', 0)
        if topLevel and topLevel > 0:
            query['path']['navtree_start'] = topLevel + 1

        # XXX: It'd make sense to use 'depth' for bottomLevel, but it doesn't
        # seem to work with EPI.

        # Only list the applicable types
        query['portal_type'] = utils.typesToList(context)

        # Apply the desired sort
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute
            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder

        # Filter on workflow states, if enabled
        if navtree_properties.getProperty('enable_wf_state_filtering', False):
            query['review_state'] = \
                navtree_properties.getProperty('wf_states_to_show', ())

        self.query = query

    def __call__(self):
        return self.query
