# -*- coding: utf-8 -*-
from five import grok
from interlegis.portalmodelo.policy.config import DEFAULT_CONTENT
from interlegis.portalmodelo.policy.config import IMAGE
from interlegis.portalmodelo.policy.config import PROJECTNAME
from interlegis.portalmodelo.policy.config import SITE_STRUCTURE
from plone import api
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool import interfaces as qi
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implements

import logging

logger = logging.getLogger(PROJECTNAME)


class HiddenProducts(grok.GlobalUtility):

    grok.implements(qi.INonInstallable)
    grok.provides(qi.INonInstallable)
    grok.name(PROJECTNAME)

    def getNonInstallableProducts(self):
        return [
            u'Products.Ploneboard'
            u'Products.windowZ'
        ]


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'interlegis.portalmodelo.policy.upgrades.v2000:default'
            u'Products.Ploneboard:default'
            u'Products.Ploneboard:intranet'
            u'Products.Ploneboard:ploneboard'
            u'Products.Ploneboard:uninstall'
            u'Products.Ploneboard:zbasicboard'
            u'Products.Ploneboard:zlotsofposts'
            u'Products.windowZ:default'
        ]


# XXX: we should found a way to avoid creating default content on first place
def delete_default_content(site):
    """Delete content created at Plone's installation.
    """
    logger.info(u'Apagando conteúdo padrão do Plone')
    for item in DEFAULT_CONTENT:
        if hasattr(site, item):
            api.content.delete(site[item])
            logger.debug(u'    {0} apagado'.format(item))


# XXX: we should found a way to avoid creating default portlets on first place
def delete_default_portlets(site):
    """Delete default portlets created at Plone's installation.
    """
    def get_assignment(column):
        assert column in [u'left', u'right']
        name = u'plone.{0}column'.format(column)
        manager = getUtility(IPortletManager, name=name, context=site)
        return getMultiAdapter((site, manager), IPortletAssignmentMapping)

    logger.info(u'Apagando portlets padrão do Plone')
    for column in [u'left', u'right']:
        assignment = get_assignment(column)
        for portlet in assignment.keys():
            del assignment[portlet]
            logger.debug(u'    {0} apagado'.format(portlet))


def constrain_types(folder, addable_types):
    """Constrain addable types in folder.
    """
    folder.setConstrainTypesMode(True)
    folder.setImmediatelyAddableTypes(addable_types)
    folder.setLocallyAllowedTypes(addable_types)


def create_site_structure(root, structure):
    """Create and publish new site structure as defined in config.py."""
    for item in structure:
        id = item['id']
        title = item['title']
        description = item.get('description', u'')
        if id not in root:
            if 'creators' not in item:
                item['creators'] = (u'Programa Interlegis', )
            obj = api.content.create(root, **item)
            # publish private content
            if api.content.get_state(obj) == 'private':
                api.content.transition(obj, 'publish')
            elif obj.portal_type == 'PloneboardForum':
                api.content.transition(obj, 'make_freeforall')
            # constrain types in folder?
            if '_addable_types' in item:
                constrain_types(obj, item['_addable_types'])
            # the content has more content inside? create it
            if '_children' in item:
                create_site_structure(obj, item['_children'])
            # add an image to all news items
            if obj.portal_type == 'News Item':
                obj.setImage(IMAGE)
            # XXX: workaround for https://github.com/plone/plone.api/issues/99
            obj.setTitle(title)
            obj.setDescription(description)
            obj.reindexObject()
            logger.debug(u'    {0} criado e publicado'.format(title))
        else:
            logger.debug(u'    pulando {0}; conteúdo existente'.format(title))


def setup_csvdata_permissions(portal):
    """CSVData content type is allowed **only** within its own folder
    """
    permission = 'interlegis.portalmodelo.transparency: Add CSVData'
    roles = ('Manager', 'Site Administrator', 'Owner', 'Contributor')
    folder = portal['transparencia']
    folder.manage_permission(
        permission,
        roles=roles
    )
    logger.debug(u'Permissoes ajustadas em Transparencia')

    # Remove permission on the root of the site
    portal.manage_permission(
        permission,
        roles=(),
    )


def install_legislative_process_integration(self):
    """Install interlegis.portalmodelo.pl package.

    We need to deffer the installation of this package until the structure is
    created to avoid having to move the folder to the right position.
    """
    profile = 'profile-interlegis.portalmodelo.pl:default'
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runAllImportStepsFromProfile(profile)


def populate_cover(site):
    """Populate site front page. The layout is composed by 3 rows:

    1. 1 carousel tile
    2. 1 collection tiles
    3. TODO: 1 parlamientarians tile

    Populate and configure those tiles.
    """
    from cover import set_tile_configuration
    from plone.uuid.interfaces import IUUID

    cover = site['pagina-inicial']
    # first row
    tiles = cover.list_tiles('collective.cover.carousel')
    obj = site['sobre-a-camara']['noticias']['primeira-noticia']
    uuid = IUUID(obj)
    data = dict(uuids=[uuid])
    cover.set_tile_data(tiles[0], **data)
    set_tile_configuration(cover, tiles[0], image={'scale': 'large'})
    # second row
    tiles = cover.list_tiles('collective.cover.collection')
    obj = site['sobre-a-camara']['noticias']['agregador']
    assert obj.portal_type == 'Collection'
    uuid = IUUID(obj)
    data = dict(header=u'Notícias', footer=u'Mais…', uuid=uuid)
    cover.set_tile_data(tiles[0], **data)
    set_tile_configuration(
        cover, tiles[0], image=dict(order=0, scale='thumb'), date=dict(order=1))


def set_site_default_page(site):
    """Set front page as site default page."""
    site.setDefaultPage('pagina-inicial')
    logger.info(u'Visão padrão do site estabelecida')


def get_collection_default_kwargs(portal_type):
    """Return default values used to create a collection with a query
    for certain portal types specified.

    :param portal_type: portal types to be listed in the collection
    :type portal_type: a string or a list of strings
    :returns: dictionary with defaults
    """
    assert isinstance(portal_type, str) or isinstance(portal_type, list)
    defaults = dict(
        sort_reversed=True,
        sort_on=u'created',
        limit=100,
        tableContents=False,
        customViewFields=(
            u'CreationDate',
            u'Title',
            u'review_state',
            u'EffectiveDate',
        ),
        query=[
            dict(
                i='portal_type',
                o='plone.app.querystring.operation.selection.is',
                v=portal_type,
            ),
            dict(
                i='path',
                o='plone.app.querystring.operation.string.relativePath',
                v='../',
            ),
        ],
    )
    return defaults


def set_solgemafullcalendar_view(obj):
    """Set solgemafullcalendar_view as default view on object."""
    obj.setLayout('solgemafullcalendar_view')
    logger.info(u'Visão de calendario estabelecida para {0}'.format(obj.title))


def set_galleria_view(obj):
    """Set galleria_view as default view on object."""
    obj.setLayout('galleria_view')
    logger.info(u'Visão de galeria estabelecida para {0}'.format(obj.title))


def set_atct_album_view(obj):
    """Set atct_album_view as default view on object."""
    obj.setLayout('atct_album_view')
    logger.info(u'Visão de miniaturas estabelecida para {0}'.format(obj.title))


def import_images(site):
    """Import all images inside the "static" folder of the package and import
    them inside the "Banco de imagens" folder. We are assuming the folder
    contains only valid image files so no validation is done.
    """
    from StringIO import StringIO
    import os
    image_bank = site['imagens']
    # look inside "static" folder and import all files
    path = os.path.dirname(os.path.abspath(__file__)) + '/browser/static/'
    logger.info(u'Importando imagens')
    for name in os.listdir(path):
        with open(path + name) as f:
            image = StringIO(f.read())
        api.content.create(image_bank, type='Image', id=name, image=image)
        logger.debug(u'    {0} importada'.format(name))


def set_default_view_on_folder(folder, object_id=''):
    """Create and publish a Document (or other content type) inside a folder
    and set it as the default view of that folder.
    """
    assert folder.portal_type == 'Folder'
    id = folder.id
    title = folder.title
    object_id = object_id or id

    #kwargs = {
    #    'description': u'',
    #    'creators': (u'Programa Interlegis', ),
    #}
    #if type == 'Collection':
    #    assert portal_type is not None
    #    kwargs = get_collection_default_kwargs('News Item')
    #obj = api.content.create(folder, type=type, title=title, **kwargs)
    #api.content.transition(obj, 'publish')

    folder.setDefaultPage(object_id)
    logger.info(u'Visão padrão criada e estabelecida para {0}'.format(title))
    #return obj


def miscelaneous_house_folder(site):
    """Set various adjustments on site content on "Sobre a Câmara" folder:

    - Set default views on subfolders
    - Set solgemafullcalendar_view view on "Eventos"
    - Set galleria_view view on "Fotos"
    - Set atct_album_view view on "Banco de Imagens"
    """
    folder = site['sobre-a-camara']
    set_default_view_on_folder(folder['acesso'], object_id='pagina-padrao')
    set_default_view_on_folder(folder['historia'], object_id='pagina-padrao')
    set_default_view_on_folder(folder['funcao-e-definicao'], object_id='pagina-padrao')
    set_default_view_on_folder(folder['estrutura'], object_id='pagina-padrao')
    set_default_view_on_folder(folder['noticias'], object_id='agregador')

    set_solgemafullcalendar_view(folder['eventos'])
    set_galleria_view(folder['fotos'])
    set_atct_album_view(site['imagens'])


def import_registry_settings(site):
    """Import registry settings; we need to do this before other stuff here,
    like using a cover layout defined there.

    XXX: I don't know if there is other way to do this on ZCML or XML.
    """
    PROFILE_ID = 'profile-interlegis.portalmodelo.policy:default'
    setup = api.portal.get_tool('portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')


def create_feedback_poll(site):
    """Create a feedback poll."""
    folder = site['enquetes']
    poll = api.content.create(
        folder,
        'collective.polls.poll',
        title=u'Gostou do novo portal?',
        options=[
            dict(option_id=0, description=u'Sim'),
            dict(option_id=1, description=u'Não'),
            dict(option_id=2, description=u'Pode melhorar'),
        ]
    )
    api.content.transition(poll, 'open')
    logger.debug(u'Enquete inicial criada e publicada')


def setup_various(context):
    marker_file = '{0}.txt'.format(PROJECTNAME)
    if context.readDataFile(marker_file) is None:
        return

    portal = api.portal.get()
    import_registry_settings(portal)
    delete_default_content(portal)
    delete_default_portlets(portal)
    create_site_structure(portal, SITE_STRUCTURE)
    setup_csvdata_permissions(portal)
    install_legislative_process_integration(portal)
    set_site_default_page(portal)
    miscelaneous_house_folder(portal)
    import_images(portal)
    populate_cover(portal)
    create_feedback_poll(portal)


def fix_image_links_in_static_portlet(context):
    """Fix image links in "redes-sociais" portlet. To make this independent of
    portal site name we need to use `resolveuid/UID` as source of images
    instead of using a fixed URL. This is called after import of portlets.xml.
    """

    def get_image_uid(image):
        """Return image UID."""
        folder = portal['imagens']
        if image in folder:
            return folder[image].UID()

    marker_file = '{0}.txt'.format(PROJECTNAME)
    if context.readDataFile(marker_file) is None:
        return

    portal = api.portal.get()
    manager = getUtility(IPortletManager, name='plone.rightcolumn', context=portal)
    mapping = getMultiAdapter((portal, manager), IPortletAssignmentMapping)
    assert 'redes-sociais' in mapping

    portlet = mapping['redes-sociais']
    images = ['ico-facebook.png', 'ico-twitter.png', 'ico-instagram.png', 'ico-youtube.png', 'ico-pinterest.png']
    for i in images:
        uid = 'resolveuid/' + get_image_uid(i)
        portlet.text = portlet.text.replace(i, uid)
    logger.debug(u'Links substituidos no portlet de redes sociais')
