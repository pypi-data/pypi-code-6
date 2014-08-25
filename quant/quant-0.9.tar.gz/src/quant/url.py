"""
Gets URLs for Services, and other DomainObjects.
"""

import os.path
import dm.ioc
import dm.exceptions

class UrlBuilderBase(object):
    
    def __init__(self):
        self.dictionary = dm.ioc.RequiredFeature('SystemDictionary')
        self.webRoot = self.dictionary['www.document_root']
    
    def getWebRoot(self):
        """
        Get the directory to use as the base directory for the web directory
        (the value used for DocumentRoot in Apache).
        """
        return os.path.join(self.webRoot, self.getTypeCode())
    
    def getFqdn(self):
        """
        Get the fully qualified domain name, e.g. x.y.com
        """
        return self.getTypeCode() + '.' + self.dictionary['domain_name']
    
    def getTypeCode(self):
        "The name of the address scheme."
        raise Exception('AbstractMethod')
    
    def getProjectPath(self, project):
        raise Exception('AbstractMethod')
    
    def getServicePath(self, service):
        "Get the url path for service (will be of form /a/b/c)."
        # self.unknownUrlBuilderBaseError(UrlBuilderBase)
        raise Exception('Unknown address scheme')
    
    def getServiceUrl(self, service):
        """
        Get the full url for the service.
        Currently defaults to using http:// (not https://)
        """
        url = 'http://' + self.getFqdn()
        if self.dictionary['www.port_http'] != '80':
            url += ":" + self.dictionary['www.port_http']
        url += self.getServicePath(service)
        return url
    
    def makeUrlPath(self, pathComponents):
        """
        Return url path made by concatenating path components with / as
        seperator.
        Makes path absolute if not already
        """
        makeAbsolute = True
        path = '/'.join(pathComponents)
        if makeAbsolute and not path.startswith('/'):
            path = '/' + path
        return path
    
    def getDefaultUrlBuilder(self):
        """
        Returns the default url builder by referring to the system dictionary.
        """
        default = self.dictionary['address_scheme_default']
        if default == 'admin':
            return UrlBuilderAdmin()
        elif default == 'project':
            return UrlBuilderProject()
        else:
            raise Exception, 'The address scheme specified as a default: %s, is not recognized' % default
    
    getDefaultUrlBuilder = classmethod(getDefaultUrlBuilder)
    
class UrlBuilderAdmin(UrlBuilderBase):
    def getTypeCode(self):
        return 'admin'
    
    def getProjectPath(self, project):
        components = [
            'project',
            project.name,
        ]
        return self.makeUrlPath(components)
    
    def getServicePath(self, service):
        components = [
            'project',
            service.project.name,
            #service.plugin.name,
            service.name
        ]
        return self.makeUrlPath(components)

class UrlBuilderProject(UrlBuilderBase):
    def getTypeCode(self):
        return 'project'
    
    def getProjectPath(self, project):
        components = [ 
            project.name,
        ]
        return self.makeUrlPath(components)
    
    def getServicePath(self, service):
        """
        Returns the url path for the service.
        """
        # exceptional case: www service (if it exists) is put at project root
        if service.plugin.name == 'www':
            return self.getProjectPath(service.project)
        
        maxServices = service.plugin.getSystem().getMaxServicesPerProject()
        # maxServices is None for normal service plugins
        if not maxServices or maxServices == 1:
            components = [
                service.project.name, 
                #service.plugin.name, 
                service.name
            ]
            return self.makeUrlPath(components)
        # elif maxServices == 1: # then a single service plugin
        #   return self.makeUrlPath([service.project.name, service.plugin.name])
        elif maxServices == 0:
            msg = 'Won\'t make servicePath for %s non-service plugin' % service
            raise dm.exceptions.KforgeError(msg)
    
    def decodeServicePath(self, urlPath):
        """
        Decode a url for a service into the project name and service name
        
        @return tuple (projectName, serviceName)
        """
        pathSegments = urlPath.split('/')
        projectName = ''
        serviceName = ''
        # urlPath starts with '/' so first segment is empty string
        projectName = pathSegments[1]
        serviceName = pathSegments[2]
        return (projectName, serviceName)

"""
URL Layout
**********

URL layout defines a view onto the underlying system data.
This primarily consists of two types:
    1. Core data: projects and persons/users
    2. Data for services

There are 2 main url addressing schemes:
    1. Admin view: primary view quantd by the kforge system)
    2. Project view: for non-administrative access to project resources

Defn: domainname is the site domain name such as kforge.net or
test.kforge.net it is to this that any hosts such as www or svn will be
prepended. Throughout we shall use kforge.net for illustration purposes
but this could be replaced by any valid domain name

Defn: **primary** view denotes the view presented at the default site url
i.e. kforge.net and www.kforge.net (we shall assume that usually these
resolve to the same thing)

Remarks on Service Addressing
=============================

Services are uniquely identified by:
    1. plugin_type, project, service_name
    2. service_id

And over-identified by:
    plugin_type, project, service_name, service_id

Therefore to address via a url we must either:
    1. Combine all 3 items into the url in some manner.
    2. Use service_id

It will be normal for service_name or service_id to come last in the url
string as these are the least significant pieces of info. However it is
unclear which should come first out of project and plugin_type. To
distinguish these two approaches we shall label them respectively:

    project addressing
    plugin addressing

Examples are:

Project Addressing:
    
    ${project}.kforge.net/${plugin}/${service_name}
    e.g. ukparse.kforge.net/wiki/wiki

Plugin addressing:
    ${plugin}.kforge.net/${project}/${service_name}
    e.g. wiki.kforge.net/ukparse/wiki
    
    or
    xxx.kforge.net/${plugin}/${project}/${service_id}

Remark: In general the service name will default to the plugin name. Thus
you will may end up with urls of the form  ..../wiki/wiki or /svn/svn.

This may seem a little annoying. If it were known that there were only
going to be one instance of that plugin per project then we could remove
the repetition and have /wiki or /svn. This adds an extra level of
complexity in that:
    1. Different projects have different url naming schemes
    2. One must specify in advance whether a project will allow multiple
    instances of a plugin and it will be difficult or impossible to change
    this once the decision has been taken

Thus this option will not be supported. (It was also suggested that one
could have some way to specify a default instance which would then be
served at the root plugin url e.g. /wiki/wiki/ would be available at /wiki/
or /svn/svn/ would be available at /svn/. However this is clearly
problematic as pages get served under this and these might conflict with
the names for other plugin instances e.g. often have project names at the
base of a svn repository and it is possible that you might have a project
in the repository /and/ another subversion instance in which case these
would both appear at /svn/project-name. Thus this case only works in the
situation in which there will be a single instance of the plugin).

Admin Virtual Host
==================

By default admin view will be the primary view.
It will also be available at admin.kforge.net
This is dealt with in greater detail elsewhere (e.g. the front controller
of the kforge user interface (kui) so it will only be sketched here and the
description is prescriptive rather than normative [[TODO: give explicit
location]].

admin.kforge.net/
    project/${project_name}/
        create
        delete
        service/
            ${service_name}
    person/${user_name}/
    ...
    

Projects Virtual Host
=====================

Available at projects.kforge.net
May also be a primary view.

Provides project priority addressing but with a fixed subdomain, i.e.
    
    projects.kforge.net/${project}/${plugin}/${service_name}
    projects.kforge.net/${project}/
        -- quant access to project web pages

Project Virtual Host
====================

Can *not* be a primary view as there are several and none have priority
Project priority addressing with project name as subdomain, i.e.

${project}.kforge.net/
    WEB ONLY -- No services?

Main use is to allow for this to direct to a site outside of kforge that is
run by project owner.

Extending
*********

You can implement your own url or directory layout by simply extending this
class and overriding the relevant methods.
Note however that this class uses data from the SystemDictionary
(kforge.system module) and variables defined therein.
"""


