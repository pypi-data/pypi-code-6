# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from collective.jazzport.interfaces import IJazzportSettings
from collective.jazzport.iterators import AsyncWorkerStreamIterator
from collective.jazzport.utils import ZipExport, ajax_load_url
from plone.registry.interfaces import IRegistry
from zExceptions import NotFound
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.jazzport')


class EnableZipDownloadView(BrowserView):

    def __call__(self):
        context_state = getMultiAdapter(
            (self.context, self.request), name='plone_context_state')
        ob = context_state.canonical_object()

        ob.manage_permission(
            'collective.jazzport: Download Zip',
            ['Anonymous']
        )

        msg = _('Enabled zip download')
        IStatusMessage(self.request).addStatusMessage(msg)

        self.request.response.redirect(ob.absolute_url())
        return u''


class DisableZipDownloadView(BrowserView):

    def __call__(self):
        context_state = getMultiAdapter(
            (self.context, self.request), name='plone_context_state')
        ob = context_state.canonical_object()

        ob.manage_permission(
            'collective.jazzport: Download Zip',
            []
        )

        msg = _('Disabled zip download')
        IStatusMessage(self.request).addStatusMessage(msg)

        self.request.response.redirect(ob.absolute_url())
        return u''


class ZipDownloadView(BrowserView):

    def __call__(self):
        # Get catalog
        pc = getToolByName(self.context, 'portal_catalog')
        if pc is None:
            raise NotFound(self.context, self.__name__, self.request)

        # Get real context (mainly default page's container)
        context_state = getMultiAdapter(
            (self.context, self.request), name='plone_context_state')
        ob = context_state.canonical_object()
        if ob is None:
            raise NotFound(self.context, self.__name__, self.request)

        # Get settings
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IJazzportSettings)

        # Get zipped urls
        query = {
            'path': '/'.join(ob.getPhysicalPath()),
            'portal_type': list(settings.portal_types or []) or None
        }

        urls = sorted([ajax_load_url(brain.getURL()) for brain in pc(query)])
        if not urls:
            raise NotFound(self.context, self.__name__, self.request)

        # Go to zip
        return AsyncWorkerStreamIterator(
            ZipExport('{0:s}.zip'.format(self.context.getId()),
                      urls, cookies=self.request.cookies),
            self.request
        )
