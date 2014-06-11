# -*- coding: utf-8 -*-
from five import grok
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from Products.CMFPlone import interfaces as st_interfaces
from zope.interface import implements

PROJECTNAME = 'brasil.gov.portal'

REDES = [
    {'id': 'facebook',
     'title': 'Facebook',
     'url': 'http://facebook.com/%s'},
    {'id': 'twitter',
     'title': 'Twitter',
     'url': 'https://twitter.com/%s'},
    {'id': 'youtube',
     'title': 'YouTube',
     'url': 'http://youtube.com/%s'},
    {'id': 'flickr',
     'title': 'Flickr',
     'url': 'http://flickr.com/%s'},
    {'id': 'googleplus',
     'title': 'Google+',
     'url': 'http://plus.google.com/%s'},
    {'id': 'slideshare',
     'title': 'Slideshare',
     'url': 'http://slideshare.com/%s'},
    {'id': 'soundcloud',
     'title': 'SoundCloud',
     'url': 'http://soundcloud.com/%s'},
    {'id': 'rss',
     'title': 'RSS',
     'url': '%s'},
    {'id': 'instagram',
     'title': 'Instagram',
     'url': 'http://instagram.com/%s'},
    {'id': 'tumblr',
     'title': 'Thumblr',
     'url': 'http://%s.tumblr.com'},
]

SHOW_DEPS = [
    'brasil.gov.agenda',
    'brasil.gov.barra',
    'brasil.gov.tiles',
    'brasil.gov.vcge',
    'collective.cover',
    'collective.nitf',
    'collective.polls',
    'sc.embedder',
    'sc.social.like',
]

DEPS = [
    'archetypes.querywidget',
    'brasil.gov.agenda.upgrades.v2000',
    'brasil.gov.agenda.upgrades.v3000',
    'brasil.gov.agenda.upgrades.v4000',
    'brasil.gov.portal.upgrades.v1000',
    'brasil.gov.portal.upgrades.v10300',
    'brasil.gov.portal.upgrades.v2000',
    'brasil.gov.portal.upgrades.v3000',
    'brasil.gov.portal.upgrades.v4000',
    'brasil.gov.portal.upgrades.v5000',
    'brasil.gov.tiles.upgrades.v2000',
    'brasil.gov.vcge.at',
    'brasil.gov.vcge.dx',
    'brasil.gov.vcge.upgrades.v2000',
    'collective.googleanalytics',
    'collective.js.galleria',
    'collective.js.jqueryui',
    'collective.oembed',
    'collective.portlet.calendar',
    'collective.upload',
    'collective.z3cform.datetimewidget',
    'collective.z3cform.widgets',
    'plone.app.blocks',
    'plone.app.collection',
    'plone.app.contenttypes',
    'plone.app.dexterity',
    'plone.app.drafts',
    'plone.app.intid'
    'plone.app.intid',
    'plone.app.iterate',
    'plone.app.jquery',
    'plone.app.jquerytools',
    'plone.app.querystring',
    'plone.app.relationfield',
    'plone.app.theming',
    'plone.app.tiles',
    'plone.app.versioningbehavior',
    'plone.formwidget.autocomplete',
    'plone.formwidget.contenttree',
    'plone.formwidget.querystring',
    'plone.resource',
    'plone.session',
    'plonetheme.classic',
    'Products.Doormat',
    'Products.PloneFormGen',
    'raptus.autocompletewidget',
]

HIDDEN_PROFILES = [
    'archetypes.querywidget:default',
    'brasil.gov.agenda:default',
    'brasil.gov.agenda.upgrades.v2000:default',
    'brasil.gov.agenda.upgrades.v3000:default',
    'brasil.gov.agenda.upgrades.v4000:default',
    'brasil.gov.barra:default',
    'brasil.gov.barra.upgrades.v1002:default',
    'brasil.gov.barra.upgrades.v1010:default',
    'brasil.gov.portal:default',
    'brasil.gov.portal:initcontent',
    'brasil.gov.portal.upgrades.v1000:default',
    'brasil.gov.portal.upgrades.v2000:default',
    'brasil.gov.portal.upgrades.v3000:default',
    'brasil.gov.portal.upgrades.v4000:default',
    'brasil.gov.portal.upgrades.v5000:default',
    'brasil.gov.portal.upgrades.v10300:default',
    'brasil.gov.portal:testfixture',
    'brasil.gov.portal:uninstall',
    'brasil.gov.tiles:default',
    'brasil.gov.tiles:uninstall',
    'brasil.gov.tiles.upgrades.v2000:default',
    'brasil.gov.vcge:default',
    'brasil.gov.vcge.at:default',
    'brasil.gov.vcge.dx:default',
    'brasil.gov.vcge:uninstall',
    'brasil.gov.vcge.upgrades.v2000:default',
    'collective.cover:default',
    'collective.cover:testfixture',
    'collective.cover:uninstall',
    'collective.js.galleria:default',
    'collective.js.jqueryui:default',
    'collective.nitf:default',
    'collective.oembed:default',
    'collective.polls:default',
    'collective.portlet.calendar:default',
    'collective.portlet.calendar:uninstall',
    'collective.upload:default',
    'collective.upload:testfixture',
    'collective.upload:uninstall',
    'collective.z3cform.widgets:1_to_2',
    'collective.z3cform.widgets:default',
    'collective.z3cform.widgets:test',
    'collective.z3cform.widgets:uninstall',
    'collective.z3cform.widgets:upgrade_1_to_2',
    'plone.app.blocks:default',
    'plone.app.contenttypes:default',
    'plone.app.contenttypes:plone-content',
    'plone.app.dexterity:default',
    'plone.app.drafts:default',
    'plone.app.iterate:plone.app.iterate',
    'plone.app.openid:default',
    'plone.app.jquerytools:default',
    'plone.app.querystring:default',
    'plone.app.relationfield:default',
    'plone.app.theming:default',
    'plone.app.tiles:default',
    'plone.app.versioningbehavior:default',
    'plone.formwidget.autocomplete:default',
    'plone.formwidget.contenttree:default',
    'plone.formwidget.querystring:default',
    'Products.Doormat:default',
    'Products.Doormat:uninstall',
    'Products.PloneFormGen:default',
    'raptus.autocompletewidget:default',
    'raptus.autocompletewidget:uninstall',
    'sc.embedder:default',
    'sc.embedder:uninstall',
    'sc.social.like:default',
    'sc.social.like:to2000',
    'sc.social.like:uninstall',
]


class HiddenProducts(grok.GlobalUtility):
    """ Oculta produtos do QuickInstaller """
    implements(qi_interfaces.INonInstallable)

    def getNonInstallableProducts(self):
        products = []
        products = [p for p in DEPS]
        return products


class HiddenProfiles(grok.GlobalUtility):
    """ Oculta profiles da tela inicial de criacao do site """
    implements(st_interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        return HIDDEN_PROFILES
