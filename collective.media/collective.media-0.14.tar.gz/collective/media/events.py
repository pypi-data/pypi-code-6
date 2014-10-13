from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectMovedEvent
from zope.lifecycleevent.interfaces import ISequence
from Products.CMFCore.interfaces import IFolderish
from Products.ATContentTypes.interfaces.image import IATImage

def reindexMediaPage(object):
    if hasattr(object, "portal_type"):
        if object.portal_type == "MediaPage":
            print "Reindexing MediaPage"
            object.reindexObject(idxs=['hasMedia'])
            object.reindexObject(idxs=['leadMedia'])

def reindexMedia(object, event):
    """
        reindexes Media catalog indexes on the parent
    """
    if object.id != "whatson":
        print "Reindexing %s"%object.id
        object.reindexObject(idxs=["hasMedia"])
        object.reindexObject(idxs=["leadMedia"])
        print "Finished reindexing %s"%object.id
        reindexMediaPage(object.getParentNode())
        
    
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


def mediaObjectTranslated(ob, event):
    print "media object was translated"

    language_to_translate = event.language
    original_object = event.object

    brains = original_object.getFolderContents()
    for b in brains:
        if b.id == 'slideshow':
            slideshow = b.getObject()
            break

    print "translate slideshow folder"
    slideshow.addTranslation(language_to_translate)

    target_object = event.target

    print "translate folder content"
    slideshow_content = slideshow.getFolderContents()
    for item in slideshow_content:
        item_object = item.getObject()
        item_object.addTranslation(language_to_translate)

    """
    if target_object.checkCreationFlag():
        print "Creating the slideshow folder for translated page."

        target_object.invokeFactory(type_name="Folder", id='slideshow', title='slideshow')
        
        print "fetching slideshow folder content"
        folder = target_object['slideshow']
        folder.showinsearch = False

        
        for content in slideshow.getFolderContents():
            print content
            content.addTranslation(language_to_translate)
        
        folder.reindexObject()

        try:
            folder.portal_workflow.doActionFor(folder, "publish", comment="Slideshow content automatically published")
        except:
            pass
    """

