#from django.conf.urls import *
from django.conf.urls import patterns
import quant.regexps
from quant.soleInstance import application

contractAttrNames = []
for contractType in application.registry.contractTypes:
    try:
        attrName = contractType.getExtensionRegistryAttrName()
    except ImportError:
        pass
    else:
        contractAttrNames.append(attrName)

contractpattern = '|'.join(contractAttrNames)

urlpatterns = patterns('quant.djangoapp.apps.eui.views',

    #   Remote Procedure Call
    ##
    
    (r'^rpc/(?P<viewName>(.*))/$',
        'rpc.view'),


    #
    ##  Application Home Page

    (r'^$',
        'welcome.welcome'),

    #
    ##  Help Page

    (r'^help/$',
        'welcome.welcome'),

    #
    ##  Trades Page

    (r'^trades/$',
        'welcome.trades'),

    #
    ##  Codes Page

    (r'^codes/$',
        'welcome.codes'),

    #
    ##  User Authentication

    (r'^login/(?P<returnPath>(.*))$',
        'accesscontrol.login'),
        
    (r'^logout(?P<redirect>(.+))$',
        'accesscontrol.logout'),

    (r'^persons/home/$',
        'welcome.user'),

    #
    ##  Access Control
    
    (r'^accessDenied/(?P<deniedPath>(.*))$',
        'welcome.accessDenied'),

    #
    ##  Administration
    
    (r'^admin/model/create/(?P<className>(\w*))/$',
        'admin.create'),

    (r'^admin/model/update/(?P<className>(\w*))/(?P<objectKey>([^/]*))/$',
        'admin.update'),

    (r'^admin/model/delete/(?P<className>(\w*))/(?P<objectKey>([^/]*))/$',
        'admin.delete'),

    (r'^admin/model/(?P<className>([^/]*))/(?P<objectKey>([^/]*))/(?P<hasMany>([^/]*))/$',
        'admin.listHasMany'),

    (r'^admin/model/create/(?P<className>([^/]*))/(?P<objectKey>([^/]*))/(?P<hasMany>([^/]*))/$',
        'admin.createHasMany'),

    (r'^admin/model/(?P<className>([^/]*))/(?P<objectKey>([^/]*))/(?P<hasMany>([^/]*))/(?P<attrKey>([^/]*))/$',
        'admin.readHasMany'),

    (r'^admin/model/update/(?P<className>([^/]*))/(?P<objectKey>([^/]*))/(?P<hasMany>([^/]*))/(?P<attrKey>([^/]*))/$',
        'admin.updateHasMany'),

    (r'^admin/model/delete/(?P<className>([^/]*))/(?P<objectKey>([^/]*))/(?P<hasMany>([^/]*))/(?P<attrKey>([^/]*))/$',
        'admin.deleteHasMany'),

    (r'^admin/model/(?P<className>([^/]*))/(?P<objectKey>([^/]*))/$',
        'admin.read'),

    (r'^admin/model/(?P<className>([^/]*))/$',
        'admin.list'),

    (r'^admin/model/$',
        'admin.model'),

    (r'^admin/$',
        'admin.index'),


    #
    ##  Registry Welcome
    
    (r'^registry/$',
        'welcome.registry'),

    #
    ##  Person

    (r'^persons/create/(?P<returnPath>(.*))$',
        'person.create'),

    (r'^persons/pending/$',
        'person.pending'),

    (r'^persons/$',
        'person.list'),

    (r'^persons/find/(?P<startsWith>[\w\d]+)/$',
        'person.search'),

    (r'^persons/find/$',
        'person.search'),

    (r'^persons/search/$',
        'person.search'),

    (r'^persons/home/$',
        'person.read'),

    (r'^persons/(?P<personName>%s)/$' % quant.regexps.personName,
        'person.read'),

    (r'^persons/(?P<personName>%s)/home/$' % quant.regexps.personName,
        'person.read'),

    (r'^persons/(?P<personName>%s)/update/$' % quant.regexps.personName,
        'person.update'),

    (r'^persons/(?P<personName>%s)/delete/$' % quant.regexps.personName,
        'person.delete'),

    (r'^persons/(?P<personName>%s)/approve/$' % quant.regexps.personName,
        'person.approve'),

    (r'^persons/(?P<personName>%s)/apikey/$' % quant.regexps.personName,
        'person.apikey'),


    #
    ## Registry views

    (r'^(?P<registryPath>(symbols|markets|priceProcesses|contractTypes|pricers|pricerPreferences|'+contractpattern+r'|books|images|results)(/.*)?)/(?P<actionName>(find))/(?P<actionValue>[\w\d]*)/$',
        'registry.view'),

    (r'^(?P<registryPath>(symbols|markets|priceProcesses|contractTypes|pricers|pricerPreferences|'+contractpattern+r'|books|images|results)(/.*)?)/(?P<actionName>(create|update|delete|read|search|undelete|purge))/$',
        'registry.view'),

    (r'^(?P<registryPath>(symbols|markets|priceProcesses|contractTypes|pricers|pricerPreferences|'+contractpattern+r'|books|images|results)(/.*)?)/$',
        'registry.view'),



    #
    ##  API
   
    (r'^api.*$',
        'api.api'),
    #
    ## Specialized views

    (r'^calculator/$',
        'calculator.calculator'),


    #
    ##  Not Found
   
    (r'^.*$',
        'welcome.pageNotFound'),
)

