def import_various(context):
    """ setup the thing """
    if context.readDataFile('zettwerk.mailtemplates-various.txt') is None:
        return

    portal = context.getSite()

    if 'portal_mail_templates' in portal:
        portal.portal_mail_templates.setExcludeFromNav(True)

        ## remove our tool from the catalog
        portal.portal_mail_templates.unindexObject()
