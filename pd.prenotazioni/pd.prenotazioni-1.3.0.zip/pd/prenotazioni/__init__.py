"""Main product initializer
"""
from App.config import getConfiguration
from Products.Archetypes import atapi
from Products.CMFCore import utils
from logging import getLogger, FileHandler, Formatter
from pd.prenotazioni import config
from rg.prenotazioni.content.prenotazione import PrenotazioneSchema
from zope.i18nmessageid import MessageFactory


prenotazioniMessageFactory = MessageFactory('pd.prenotazioni')
prenotazioniLogger = getLogger('pd.prenotazioni')
prenotazioniFileLogger = getLogger('pd.prenotazioni.file')


def init_handler():
    '''
    Protect the namespace
    '''
    if prenotazioniFileLogger.handlers:
        return
    product_config = getattr(getConfiguration(), 'product_config', {})
    config = product_config.get('pd.prenotazioni', {})
    logfile = config.get('logfile')
    if not logfile:
        return
    hdlr = FileHandler(logfile)
    formatter = Formatter('%(asctime)s %(levelname)s %(message)s',
                          "%Y-%m-%d %H:%M:%S")
    hdlr.setFormatter(formatter)
    prenotazioniFileLogger.addHandler(hdlr)

init_handler()


def initialize(context):
    """Initializer called when used as a Zope 2 product.

    This is referenced from configure.zcml. Regstrations as a "Zope 2 product"
    is necessary for GenericSetup profiles to work, for example.

    Here, we call the Archetypes machinery to register our content types
    with Zope and the CMF.
    """

    # Retrieve the content types that have been registered with Archetypes
    # This happens when the content type is imported and the registerType()
    # call in the content type's module is invoked. Actually, this happens
    # during ZCML processing, but we do it here again to be explicit. Of
    # course, even if we import the module several times, it is only run
    # once.

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    # Now initialize all these content types. The initialization process takes
    # care of registering low-level Zope 2 factories, including the relevant
    # add-permission. These are listed in config.py. We use different
    # permissions for each content type to allow maximum flexibility of who
    # can add which content types, where. The roles are set up in rolemap.xml
    # in the GenericSetup profile.

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit(
            '%s: %s' % (
                config.PROJECTNAME, atype.portal_type),
            content_types=(atype,),
            permission=config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors=(constructor,),
        ).initialize(context)
    PrenotazioneSchema['email'].required = False
    PrenotazioneSchema['gate'].searchable = False
    PrenotazioneSchema['location'].searchable = False
    PrenotazioneSchema['subject'].searchable = False
