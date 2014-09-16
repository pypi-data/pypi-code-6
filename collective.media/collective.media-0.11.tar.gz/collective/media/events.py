
def reindexMedia(object, event):
    """
        reindexes Media catalog indexes on the parent
    """
    if object.id != "whatson":
        print "Reindexing %s"%object.id
        object.reindexObject(idxs=["hasMedia"])
        object.reindexObject(idxs=["leadMedia"])
        print "Finished reindexing %s"%object.id
    
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