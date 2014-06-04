from Products.CMFCore.utils import getToolByName


def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(
        'profile-zettwerk.mailtemplates:uninstall'
    )

    cp_tool = getToolByName(portal, 'portal_controlpanel')
    cp_tool.unregisterConfiglet('zettwerkmailtemplates')

    if 'portal_mail_templates' in portal:
        portal.manage_delObjects(['portal_mail_templates'])

    return "Ran all uninstall steps."
