from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectMovedEvent
from zope.lifecycleevent.interfaces import ISequence
from Products.CMFCore.interfaces import IFolderish
from Products.ATContentTypes.interfaces.image import IATImage
import urllib, cStringIO
from cStringIO import StringIO
from plone.namedfile.field import NamedBlobImage
from plone import namedfile
import urlparse
import requests, json
from plone.app.imagecropping.at import CroppingUtilsArchetype
import PIL

from zope.annotation.interfaces import IAnnotations
from plone.app.imagecropping import PAI_STORAGE_KEY

def reindexMediaPage(object):
    if hasattr(object, "portal_type"):
        if object.portal_type == "MediaPage" or object.portal_type == "Media Person" or object.portal_type == "MediaLink":
            #print "Reindexing MediaPage"
            object.reindexObject(idxs=['hasMedia'])
            object.reindexObject(idxs=['leadMedia'])
            object.reindexObject(idxs=['getLeadMediaTag'])
            object.reindexObject(idxs=['getLeadImageTag'])

def reindexMedia(object, event):
    """
        reindexes Media catalog indexes on the parent
    """
    if object.id != "whatson":
        #print "Reindexing %s"%object.id
        object.reindexObject(idxs=["hasMedia"])
        object.reindexObject(idxs=["leadMedia"])
        object.reindexObject(idxs=['getLeadMediaTag'])
        object.reindexObject(idxs=['getLeadImageTag'])
        
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
    #print "Media Object was added!"

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
                    try:
                        createThumbnailImage(folder, ob.remoteUrl)
                    except:
                        pass

#
# TRANSLATION AND CROPS
#
def hasCrops(ob):
    #
    # Check if object has crops defined
    #
    annotations = IAnnotations(ob).get(PAI_STORAGE_KEY)
    if annotations != None:
        if 'image_collection' not in annotations.keys():
            return False
        else:
            return True
    else:
        return False

def addCropToTranslation(original, translated):
    # Add crops if original has crops
    if hasCrops(original):
        fieldname = 'image'
        scale = 'collection'
        view = original.restrictedTraverse('@@crop-image')

        box = view._storage['{0:s}_{1:s}'.format(fieldname, scale)]

        # Create new crops
        translated_view = translated.restrictedTraverse('@@crop-image')
        translated_view._crop(fieldname, scale, box)

        # Re-index current crops
        view._crop(fieldname, scale, box)

#
# Event fired when media object is translated
#
def mediaObjectTranslated(ob, event):
    slideshow = None

    language_to_translate = event.language
    original_object = event.object

    #
    # Get type folder content
    # Check if slideshow is present
    #
    brains = original_object.getFolderContents()
    for b in brains:
        if b.id == 'slideshow':
            slideshow = b.getObject()
            break

    # return if no slideshow in folder
    if slideshow == None:
        return

    try:
        # Add translation to sideshow
        slideshow.addTranslation(language_to_translate)
        slideshow_translated = slideshow.getTranslation(language_to_translate)
        slideshow_translated.showinsearch = False

        # Re-index slideshow
        slideshow_translated.reindexObject()
    except:
        # Already translated
        pass

    #
    # Publish translated slideshow
    # Re-index slideshow after publication
    #
    try:
        slideshow_translated.portal_workflow.doActionFor(slideshow_translated, 'publish', comment="Slideshow content automatically published")
        slideshow_translated.reindexObject()
    except:
        # Already published
        pass

    #
    # Translate all content from slideshow
    #
    slideshow_content = slideshow.getFolderContents()
    for item in slideshow_content:
        item_object = item.getObject()
        try:
            item_object.addTranslation(language_to_translate)
            
            # Re-index item after translation
            item_object.reindexObject()

            item_translated = item_object.getTranslation(language_to_translate)
            
            if item_object.portal_type == "Image":
                # Add crops to translated item
                addCropToTranslation(item_object, item_translated)
            
            # Re-index translated item
            if item_translated.portal_type == "MediaPage" or item_translated.portal_type == "Media Person":
                ob.reindexObject(idxs=['hasMedia'])
                ob.reindexObject(idxs=['leadMedia'])
                ob.reindexObject(idxs=['getLeadMediaTag'])
                ob.reindexObject(idxs=['getLeadImageTag'])
            item_translated.reindexObject()
        except:
            # Already translated
            pass

#
# CROPPING
#
def autoCropImage(ob):
    if not hasCrops(ob):
        view = ob.restrictedTraverse('@@crop-image')
        w = ob.width
        h = ob.height

        #
        # Make crop centered
        #
        if w > h:
            delta = w - h
            left = int(delta/2)
            upper = 0
            right = h + left
            lower = h
        else:
            delta = h - w
            left = 0
            upper = int(delta/2)
            right = w
            lower = w + upper

        box = (left, upper, right, lower)

        view._crop(fieldname='image', scale="collection", box=box)
        ob.reindexObject()

#
# Auto crop all images from page slideshow
#
def autoCropImagesFromPage(ob):
    slideshow = None

    # Check if slideshow in folder contents
    brains = ob.getFolderContents()
    for brain in brains:
        if brain.id == 'slideshow':
            slideshow = brain.getObject()
            break

    # Auto crop every image inside slideshow folder
    if slideshow != None:
        slideshow_content = slideshow.getFolderContents()
        for item in slideshow_content:
            item_object = item.getObject()
            if item_object.portal_type == "Image":
                autoCropImage(item_object)
            elif item_object.portal_type == "MediaPage" or item_object.portal_type == "Media Person" or item_object.portal_type == "MediaLink":
                #
                # Object is a page
                # Recursive call to auto crop
                # all images from page inside slideshow
                #
                autoCropImagesFromPage(item_object)
    else:
        # No slideshow folder
        return False

def imageObjectCreated(ob, event):
    #
    # New image is ready
    #
    if ob.portal_type == "Image":
        autoCropImage(ob)
    

def workflowSucceeded(ob, event):
    if ob.portal_type == "MediaPage" or ob.portal_type == "Media Person":
        #print "Media type workflow succeeded"
        if event.action == "publish":
            autoCropImagesFromPage(ob)
            ob.reindexObject(idxs=["hasMedia"])
            ob.reindexObject(idxs=["leadMedia"])
            ob.reindexObject(idxs=['getLeadMediaTag'])
            ob.reindexObject(idxs=['getLeadImageTag'])

