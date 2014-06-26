# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from five import grok
from plone import api
from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.directives import dexterity
from Products.CMFCore.interfaces import ISiteRoot
from sc.blog.config import BLOG_BLACKLISTED_TYPES
from sc.blog.content import IBlog
from sc.blog.interfaces import IBlogLayer
from zope.interface import Interface

grok.templatedir('templates')


class View(dexterity.DisplayForm):
    """Default view. Looks like a standard Folder Full View.
    """
    grok.context(IBlog)
    grok.layer(IBlogLayer)
    grok.template('folder_full_view')
    grok.require('zope2.View')

    def get_blog_friendly_types(self):
        """Return the portal types than should be displayed as post entries
        inside a Blog. Some content types (like Blog, File, Folder and Image)
        are excluded by default.

        :returns: a tuple with the names of the portal types
        """
        plone_utils = api.portal.get_tool(name='plone_utils')
        friendly_types = plone_utils.getUserFriendlyTypes()
        blog_types = set(friendly_types) - set(BLOG_BLACKLISTED_TYPES)
        return tuple(blog_types)


class BlogSummaryView(View):
    """Looks like a standard Folder Summary View.
    """
    grok.context(IBlog)
    grok.layer(IBlogLayer)
    grok.name('blog_summary_view')
    grok.template('folder_summary_view')
    grok.require('zope2.View')


class BlogHeader(grok.Viewlet):
    """A viewlet to include a header in the container (Blog) and contained
    (News Article) elements.
    """
    grok.name('sc.blog.blogheader')
    grok.context(Interface)
    grok.layer(IBlogLayer)
    grok.require('zope2.View')
    grok.viewletmanager(IAboveContent)

    def update(self):
        """ check if we are inside a Blog, if its true
            set it into self.blog
        """
        self.context = aq_inner(self.context)
        self.blog = None
        # is context a Blog or inside a Blog?
        for ob in self.context.aq_chain:
            if ISiteRoot.providedBy(ob):
                break
            if IBlog.providedBy(ob):
                self.blog = ob
                break

    def available(self):
        """ return True if we're inside a Blog.
        """
        return bool(self.blog)

    def blog_url(self):
        """ return the blog URL.
        """
        return self.blog.absolute_url()
