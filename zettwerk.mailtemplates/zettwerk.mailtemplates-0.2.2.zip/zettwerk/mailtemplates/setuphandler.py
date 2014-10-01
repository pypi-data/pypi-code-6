def import_various(context):
    """ setup the thing """
    if context.readDataFile('zettwerk.mailtemplates-various.txt') is None:
        return

    portal = context.getSite()
    TOOL_TITLE = 'Zettwerk Mailtemplates'

    if 'portal_mail_templates' in portal:
        ## remove our tool from the catalog
        tool = portal.portal_mail_templates

        first_install = tool.title != TOOL_TITLE
        tool.unindexObject()

        tool.title = TOOL_TITLE

        ## also add an example template on first install
        if first_install:
            tool.invokeFactory('Template',
                               'hello-world',
                               templateId='hello-world',
                               title='Hello World',
                               description='''
Dear %(fullname)s,

Hello world from %(portal_name)s

Your username is: %(username)s
Please visit the page at: %(portal_url)s

Thank you!''')
