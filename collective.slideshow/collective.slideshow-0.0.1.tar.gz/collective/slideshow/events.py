# Handling Events


def objectAddedEvent(ob, event):
	print "object added"
	if ob.portal_type != "Folder":
		if 'slideshow' not in ob.objectIds():
			ob.invokeFactory(type_name="Folder", id="slideshow", title="slideshow")

			folder = ob['slideshow']
			folder.showinsearch = False

			folder.reindexObject()

			try:
				folder.portal_workflow.doActionFor(folder, "publish", comment="Slideshow content automatically published")
			except:
				pass
				