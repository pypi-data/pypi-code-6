# -*- coding: utf-8 -*-

from five import grok
from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from sc.blog import _
from zope import schema


class IBlog(form.Schema):
    """A Blog.
    """

    author = schema.TextLine(
        title=_(u'Author'),
        default=u'',
    )

    image = NamedBlobImage(
        title=_(u"Image"),
        required=False,
    )


class Blog(Container):
    """A Blog is a container of News Articles.
    """
    grok.implements(IBlog)


def blog_added(ob, event):
    """ handler for IObjectAddedEvent
        here we revoke "sc.blog: Add Blog" permission and acquisition
        this way Blogs couldn't be added inside Blogs or subobjects
        of Blogs.
    """
    # inside blogs you can't add blogs
    ob.manage_permission("sc.blog: Add Blog")
