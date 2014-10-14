from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectMovedEvent
from zope.lifecycleevent.interfaces import ISequence
from Products.CMFCore.interfaces import IFolderish
from Products.ATContentTypes.interfaces.image import IATImage
import urllib, cStringIO
from plone.namedfile.field import NamedBlobImage
from plone import namedfile
import urlparse
import requests, json

def reindexMediaPage(object):
    if hasattr(object, "portal_type"):
        if object.portal_type == "MediaPage":
            #print "Reindexing MediaPage"
            object.reindexObject(idxs=['hasMedia'])
            object.reindexObject(idxs=['leadMedia'])

def reindexMedia(object, event):
    """
        reindexes Media catalog indexes on the parent
    """
    if object.id != "whatson":
        #print "Reindexing %s"%object.id
        object.reindexObject(idxs=["hasMedia"])
        object.reindexObject(idxs=["leadMedia"])
        #print "Finished reindexing %s"%object.id
        reindexMediaPage(object.getParentNode())
        

def getYoutubeOrVimeoID(link):
    if "youtube.com" in link:
        url_data = urlparse.urlparse(link)
        query = urlparse.parse_qs(url_data.query)
        video_id = query["v"][0]

        video_thumbnail_url = "http://img.youtube.com/vi/"+video_id+"/maxresdefault.jpg"

        return video_id, video_thumbnail_url
    elif "vimeo.com" in link:
        video_id = urlparse.urlparse(link).path.lstrip("/")
        data = requests.get('http://vimeo.com/api/v2/video/'+video_id+'.json').json()

        video_thumbnail_url = data[0]["thumbnail_large"]
        return video_id, video_thumbnail_url
    else:
        return False
  
def createThumbnailImage(folder, link):
    video_id, video_thumbnail_url = getYoutubeOrVimeoID(link)

    if video_id != False:
        folder.invokeFactory(type_name="Image", id=video_id, title=link)
        image = folder[video_id]
        file_data = urllib.urlopen(video_thumbnail_url).read()
        image.setImage(file_data)
        image.reindexObject()

def mediaObjectAdded(ob, event):
    #
    # Event that is triggred when a MediaPage is created
    # Create a folder slideshow for the new MediaPage
    #
    print "Media Object was added!"

    if 'slideshow' not in ob.objectIds():
        if not ob.checkCreationFlag():
            print "Creating the slideshow folder."
            ob.invokeFactory(type_name="Folder", id='slideshow', title='slideshow')
            
            folder = ob['slideshow']
            folder.showinsearch = False
            
            folder.reindexObject()
            try:
                folder.portal_workflow.doActionFor(folder, "publish", comment="Slideshow content automatically published") 
            except:
                pass

            if hasattr(ob, "portal_type"):
                    if ob.portal_type == "MediaLink":
                        createThumbnailImage(folder, ob.remoteUrl)


def mediaObjectTranslated(ob, event):
    #print "media object was translated"

    slideshow = None

    language_to_translate = event.language
    original_object = event.object

    brains = original_object.getFolderContents()
    for b in brains:
        if b.id == 'slideshow':
            slideshow = b.getObject()
            break

    if slideshow == None:
        return

    #print "translate slideshow folder"
    slideshow.addTranslation(language_to_translate)

    target_object = event.target

    #print "translate folder content"
    slideshow_content = slideshow.getFolderContents()
    for item in slideshow_content:
        item_object = item.getObject()
        item_object.addTranslation(language_to_translate)

