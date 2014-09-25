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


"""@adapter(IFolderish, IObjectModifiedEvent)
def objecModified(context, event):
    print "[object modified]"
    #plone_object = context.getParentNode()
    #if plone_object.portal_type == "MediaPage":
    #    context.getParentNode().reindexObject(idxs=['hasMedia'])
    #    context.getParentNode().reindexObject(idxs=['leadMedia'])
"""
"""@adapter(IATImage, IObjectModifiedEvent)
def imageObjectModified(context, event):
    print "#### Image modified"

@adapter(IATImage, IObjectMovedEvent)
def objectMoved(context, event):
    print "object moved"

@adapter(IATImage, ISequence)
def sequenceEvent(context, event):
    print "sequence"
"""
    
