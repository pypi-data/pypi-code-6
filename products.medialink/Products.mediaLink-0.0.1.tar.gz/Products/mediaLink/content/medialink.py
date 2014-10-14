"""Definition of the MediaLink content type
"""

from zope.interface import implements
import urlparse
from urllib import quote

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import event
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import schemata
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import StringField
from Products.CMFCore.permissions import ModifyPortalContent, View
from Products.Archetypes.atapi import CalendarWidget
from Products.Archetypes.atapi import StringWidget
from Products.ATContentTypes import ATCTMessageFactory as _
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View

# -*- Message Factory Imported Here -*-

from Products.mediaLink.interfaces import IMediaLink
from Products.mediaLink.config import PROJECTNAME

MediaLinkSchema = folder.ATFolderSchema.copy() + document.ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    StringField('remoteUrl',
        required=True,
        searchable=True,
        primary=False,
        default="http://",
        # either mailto, absolute url or relative url
        validators=(),
        widget=StringWidget(
            description='',
            label=_(u'label_url', default=u'URL'),
            maxlength='511',
            )),
))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

MediaLinkSchema['title'].storage = atapi.AnnotationStorage()
MediaLinkSchema['description'].storage = atapi.AnnotationStorage()
MediaLinkSchema['text'].storage = atapi.AnnotationStorage()



schemata.finalizeATCTSchema(
    MediaLinkSchema,
    folderish=True,
    moveDiscussion=False
)

class MediaLink(folder.ATFolder):
    """Folderish Page"""
    implements(IMediaLink)

    meta_type = "MediaLink"
    schema = MediaLinkSchema
    schema['relatedItems'].widget.visible['edit'] = 'visible'

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    text = atapi.ATFieldProperty('text')

    security = ClassSecurityInfo()

    security.declareProtected(ModifyPortalContent, 'setRemoteUrl')

    def setRemoteUrl(self, value, **kwargs):
        """remute url mutator

        Use urlparse to sanify the url
        Also see http://dev.plone.org/plone/ticket/3296
        """
        if value:
            value = urlparse.urlunparse(urlparse.urlparse(value))
        self.getField('remoteUrl').set(self, value, **kwargs)

    security.declareProtected(View, 'remote_url')
    def remote_url(self):
        """CMF compatibility method
        """
        return self.getRemoteUrl()

    security.declarePrivate('cmf_edit')
    def cmf_edit(self, remote_url=None, **kwargs):
        if not remote_url:
            remote_url = kwargs.get('remote_url', None)
        self.update(remoteUrl=remote_url, **kwargs)

    security.declareProtected(View, 'getRemoteUrl')
    def getRemoteUrl(self):
        """Sanitize output
        """
        value = self.Schema()['remoteUrl'].get(self)
        if not value: value = ''  # ensure we have a string
        return quote(value, safe='?$#@/:=+;$,&%')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(MediaLink, PROJECTNAME)


