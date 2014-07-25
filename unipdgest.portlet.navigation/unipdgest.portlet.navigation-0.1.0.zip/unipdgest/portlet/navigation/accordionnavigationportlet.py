# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.portlets.portlets.navigation import AddForm as BaseAddForm
from plone.app.portlets.portlets.navigation import Assignment as BaseAssignment
from plone.app.portlets.portlets.navigation import EditForm as BaseEditForm
from plone.app.portlets.portlets.navigation import INavigationPortlet
from plone.app.portlets.portlets.navigation import Renderer as BaseRenderer
from plone.memoize.instance import memoize
from unipdgest.portlet.navigation import _
from unipdgest.portlet.navigation.query_builder import NavtreeQueryBuilder
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements


class IAccordionNavigationPortlet(INavigationPortlet):
    """Accordion navigation portlet"""


class Assignment(BaseAssignment):

    implements(IAccordionNavigationPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        if self.name:
            return _('accordion_navigation_with_title',
                     default=u'Accordion navigation: $title',
                     mapping={'title': self.name})
        return _(u'Accordion navigation')


SKIP_FIELDS = ('topLevel', 'includeTop', 'currentFolderOnly')


class Renderer(BaseRenderer):

    render = ViewPageTemplateFile('accordion_navigation.pt')
    recurse = ViewPageTemplateFile('accordion_navigation_recurse.pt')

    @memoize
    def getNavTree(self, _marker=None):
        if _marker is None:
            _marker = []
        context = aq_inner(self.context)
        queryBuilder = NavtreeQueryBuilder(self.getNavRoot())
        strategy = getMultiAdapter((context, self.data), INavtreeStrategy)
        tree = buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)
        tree = self._expandFolderTree(tree, queryBuilder, strategy)
        return tree

    def _findNode(self, tree, path):
        """Get the reference to the section of the tree identified by the path"""
        for item in tree['children']:
             if path.startswith(item['path']):
                 return self._findNode(item, path)
        return tree

    def _minifyTree(self, tree, path):
        """Clean al uneeded elements, keep focus on te context"""
        if tree:
            if tree[0]['path']==path:
                return tree[0]['children']
            return self._minifyTree(tree[0]['children'], path)
        return tree

    def _expandFolderTree(self, tree, queryBuilder, strategy):
        """Add a subtree to the current tree"""
        context = aq_inner(self.context)
        nav_root = self.getNavRoot()
        portal = getToolByName(context, 'portal_url').getPortalObject()
        nav_root_path = '/'.join(nav_root.getPhysicalPath())
        context_path = '/'.join(context.getPhysicalPath())
        if context_path.startswith(nav_root_path) and \
                len(context.getPhysicalPath()) - len(portal.getPhysicalPath()) > 2:
            queryBuilder = NavtreeQueryBuilder(context, subtree=True)
            subtree = buildFolderTree(context, obj=context,
                                      query=queryBuilder(),
                                      strategy=strategy)
            subtree = self._minifyTree(subtree['children'], context_path)
            tree_node = self._findNode(tree, context_path)
            # now place the subtree inside the tree
            tree_node['children'] = subtree
        return tree


class AddForm(BaseAddForm):
    form_fields = form.Fields(IAccordionNavigationPortlet)
    form_fields = form_fields.omit(*SKIP_FIELDS)
    form_fields['root'].custom_widget = UberSelectionWidget

    def create(self, data):
        return Assignment(name=data.get('name', ""),
                          root=data.get('root', ""),
                          currentFolderOnly=False,
                          includeTop=False,
                          topLevel=0,
                          bottomLevel=data.get('bottomLevel', 0))


class EditForm(BaseEditForm):
    form_fields = form.Fields(IAccordionNavigationPortlet)
    form_fields = form_fields.omit(*SKIP_FIELDS)
    form_fields['root'].custom_widget = UberSelectionWidget
