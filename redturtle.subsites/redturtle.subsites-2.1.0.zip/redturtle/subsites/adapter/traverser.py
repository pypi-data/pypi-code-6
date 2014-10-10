# -*- coding: utf-8 -*-

from ZPublisher.BaseRequest import DefaultPublishTraverse
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope import interface
from zope.publisher.interfaces import IPublishTraverse
from redturtle.subsites.frontend.browser.interfaces import IFrontendLayer

class NavigationRootTraverser(object):
    """Adapter for the navigation traverser using subsites"""

    interface.implements(IPublishTraverse)
    def __init__(self,context,request):
        self.default = DefaultPublishTraverse(context,request)
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        obj = self.default.publishTraverse(request, name)
        context = self.context
        if IFrontendLayer.providedBy(request) and not INavigationRoot.providedBy(context):
            interface.alsoProvides(context, INavigationRoot)
        elif not IFrontendLayer.providedBy(request) and INavigationRoot.providedBy(context):
            interface.noLongerProvides(context, INavigationRoot)
        return obj
