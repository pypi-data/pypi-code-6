import string
import sys
import os.path

from suds.client import Client
from suds.cache import FileCache

from pyrannosaurus import get_package_dir
from pyrannosaurus.clients.base import BaseClient
from pyrannosaurus.utils import package_to_dict, zip_to_binary

class MetadataClient(BaseClient):

    def __init__(self, wsdl='wsdl/metadata.xml', cacheDuration = 0, **kwargs):
        super(MetadataClient, self).__init__()
        #TODO: clean this up
        wsdl = get_package_dir(wsdl)
        if ':///' not in wsdl:
            if os.path.isfile(wsdl):
                wsdl = 'file:///' + os.path.abspath(wsdl)

        if cacheDuration > 0:
            cache = FileCache()
            cache.setduration(seconds = cacheDuration)
        else:
            cache = None

        self._client = Client(wsdl, cache = cache)

        headers = {'User-Agent': 'Salesforce/' + self._product + '/' + '.'.join(str(x) for x in self._version)}
        self._client.set_options(headers = headers)

    def generateHeader(self, sObjectType):
        try:
          return self._client.factory.create(sObjectType)
        except:
          print 'There is not a SOAP header of type %s' % sObjectType

    def login(self, username, password, token='', is_production=False, name='default'):
        lr, header = super(MetadataClient, self)._login(username, password, token, is_production)
        #replace the metadata 'm' with the apex 's'
        self._connections[name] = self.Connection(header, lr.serverUrl, lr.metadataServerUrl)
        if name == 'default':
            self._setEndpoint(lr.metadataServerUrl)
            super(MetadataClient, self)._setEndpoint(lr.serverUrl, base=True)
            super(MetadataClient, self).setSessionHeader(self._sessionHeader)

    def set_active_connection(self, name):
        conn = self._connections.get(name)
        if conn:
            self.setSessionHeader(conn.session_header)
            self._setEndpoint(conn.metadata_url, base=False)
            super(MetadataClient, self).set_active_connection(name)
        else:
            #TODO:replace this with real exception
            print "Connection not found"

    def deploy(self, file_path, **kwargs):
        self._setHeaders('retrieve')
        deploy_options = self._client.factory.create('DeployOptions')
        deploy_options.allowMissingFiles = False
        deploy_options.autoUpdatePackage = False
        deploy_options.checkOnly = False
        deploy_options.ignoreWarnings = False
        deploy_options.performRetrieve = False
        deploy_options.purgeOnDelete = False
        deploy_options.rollbackOnError = True
        deploy_options.runAllTests = False
        deploy_options.runTests = []
        deploy_options.singlePackage = True
        if kwargs:
            for k, v in kwargs.iteritems():
                    if k in deploy_options.__keylist__:
                        deploy_options.__setattr__(k, v)

        res = self._client.service.deploy(zip_to_binary(file_path), deploy_options)
        return res

    def check_deploy_status(self, id, include_details=False):
        self._setHeaders('checkDeployStatus')
        return self._client.service.checkDeployStatus(id,include_details)

    def cancel_deploy(self, id):
        self._setHeaders('cancelDeploy')
        if id:
            cancel_deploy_result = self._client.service.cancelDeploy(id)
            return cancel_deploy_result
        else:
            #TODO: probably should impl this as exception
            return 'Must specify id for cancel deploy call.'

    def retrieve(self, package_manifest, api_version=29.0, api_access='Unrestricted', singlePackage=True):
        self._setHeaders('retrieve')
        retrieve_request = self._client.factory.create('RetrieveRequest')
        retrieve_request.apiVersion = api_version
        retrieve_request.singlePackage = singlePackage
        retrieve_request.unpackaged.apiAccessLevel.value = api_access
        package_dict = package_to_dict(package_manifest)

        for name,members in package_dict.iteritems():
            pkg_mem = self._client.factory.create('PackageTypeMembers')
            pkg_mem.name = name
            for m in members:
                pkg_mem.members.append(m)

        retrieve_request.unpackaged.types.append(pkg_mem)
        retrieve_response = self._client.service.retrieve(retrieve_request)

        return retrieve_response

    def check_retrieve_status(self, id):
        self._setHeaders('checkRetrieveStatus')
        zip_response = self._client.service.checkRetrieveStatus(id)
        return zip_response

    def check_status(self, id):
        self._setHeaders('checkStatus')
        if id:
            async_result = self._client.service.checkStatus(id)
            return async_result
        else:
            #TODO: probably should impl this as exception
            return 'Must specify id for check status call.'
