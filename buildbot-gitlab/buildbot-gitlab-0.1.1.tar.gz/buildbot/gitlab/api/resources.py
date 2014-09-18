#!/usr/bin/env python
# encoding: utf-8


# Copyright (c) 2014, VCA Technology. All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from twisted.web.resource import ErrorPage
from twisted.python import log
from buildbot.status.web.base import HtmlResource
from buildbot.status.web.status_json import JsonResource

from buildbot.gitlab.api import project as GitlabAPI

import twisted.web._responses as HTTPResponse

import sys, traceback

def ExtractProjectNameFromUri(prepath):

    """
    given a list containing uri elements, returns the project name.
    expected uri format <address>/gitlabapi/projects/<namespace>/<project>
    :param: list object from request.prepath
    :return: unicode string of the project name
    """

    return unicode(prepath[3], 'utf-8')
#extracts the namespace from a uri
def ExtractNamespaceFromUri(prepath):

    """
    given a list containing uri elements, returns the namespace name.
    expected uri format <address>/gitlabapi/projects/<namespace>/<project>
    :param: list object from request.prepath
    :return: unicode string of the namespace name
    """

    return unicode(prepath[2], 'utf-8')

def GetExceptionDetail():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    err = "".join(lines)
    return err

class GitlabHtmlResource(HtmlResource):

    """
    GitlabHtmlResource - Root api page for gitlab api setups child Json resources
    when requested.
    """

    def __init__(self, filename):
        HtmlResource.__init__(self)

        self.filename = filename

        #define valid child resources here
        self.apichildren = {
            'projects': GitlabProjectsJsonResource,
        }

    def getChild(self, path, request):
        status = self.getStatus(request)

        #lookup child resources, if exist, instantiate & return, else error
        if path in self.apichildren.keys():
            return self.apichildren[path](status, self.filename)
        elif path:
            #if path not empty and we get here, requested undefined api page, 404
            return ErrorPage(HTTPResponse.NOT_FOUND, '404 - Not Found', 'Gitlab API Method "' + path + '" is not defined').render(request)
        else:
            return self

    def getPageTitle(self, request):
        return 'buildbot - Gitlab Integration'

    def body(self, ctx):
        return 'Gitlab integration home'


class GitlabErrorJsonResource(JsonResource):

    """
    Json resource for returning error codes/messages from API
    """

    def __init__(self, status, filename, status_code, message, detail, namespace, project):
        JsonResource.__init__(self, status)
        self.filename = filename
        self.status_code = status_code
        self.namespace = namespace
        self.message = message
        self.detail = detail
        self.project = project

    def getChild(self, path, request):
        return self

    def asDict(self, request):
        result = {}
        result['error'] = {}
        result['error']['filename'] = self.filename
        result['error']['status_code'] = self.status_code
        result['error']['message'] = self.message
        result['error']['detail'] = self.detail
        result['error']['namespace'] = self.namespace
        result['error']['project'] = self.project

        request.setResponseCode(self.status_code)

        return result

class GitlabProjectsJsonResource(JsonResource):

    """
    Json resource for accessing projects
    """

    def __init__(self, status, filename, baseRepoUrl):
        JsonResource.__init__(self, status)
        self.filename = filename
        self.baseRepoUrl = baseRepoUrl

    def getChild(self, path, request):
        namespace = ExtractNamespaceFromUri(request.prepath)

        try:
            #verify that the namespace exists
            json = GitlabAPI.Json(self.filename, self.baseRepoUrl)

            if request.method == 'PUT':
                json += namespace

            return GitlabProjectNamespaceJsonResource(self.status, self.filename, self.baseRepoUrl, namespace)
        except:
            request.method = 'GET'
            return GitlabErrorJsonResource(self.status, self.filename, HTTPResponse.NOT_FOUND,
                                           'The namespace was not found', GetExceptionDetail(), namespace, '')

    def asDict(self, request):
        json = GitlabAPI.Json(self.filename, self.baseRepoUrl)
        return json.data


class GitlabProjectNamespaceJsonResource(JsonResource):

    """
    Json Resource for all projects within a group/namespace
    """

    def __init__(self, status, filename, baseRepoUrl, namespace):
        JsonResource.__init__(self, status)

        self.filename = filename
        self.namespace = namespace
        self.baseRepoUrl = baseRepoUrl

    def getChild(self, path, request):
        if request.method == 'GET' or request.method == 'DELETE':
            try:
                #load projects from file
                project = ExtractProjectNameFromUri(request.prepath)
                json = GitlabAPI.Json(self.filename, self.baseRepoUrl)

                #ensure the project exists by attempting to access it
                json[self.namespace][project]

                log.msg('accessing project: %r, from: %r' % (project, self.namespace))

                request.setResponseCode(HTTPResponse.OK)
                return GitlabProjectJsonResource(self.status, self.filename, self.baseRepoUrl, self.namespace, project)

            except:
                return GitlabErrorJsonResource(self.status, self.filename, HTTPResponse.NOT_FOUND, 'The project was not found in the specified namespace',
                                               GetExceptionDetail(), self.namespace, project)

        elif request.method == 'PUT':
            project = ExtractProjectNameFromUri(request.prepath)
            return GitlabProjectJsonResource(self.status, self.filename, self.baseRepoUrl, self.namespace, project)

    def asDict(self, request):
        json = GitlabAPI.Json(self.filename, self.baseRepoUrl)

        try:
            return json.data[self.namespace]
        except:
            request.setResponseCode(HTTPResponse.NOT_FOUND)
            return GitlabErrorJsonResource(self.status, self.filename, HTTPResponse.NOT_FOUND, "The namespace was not found",
                               GetExceptionDetail(), self.namespace, "").asDict(request)

    def render_DELETE(self, request):

        """
        REST call:
        DELETE <address>/gitlabapi/projects/<namespace>
        """

        log.msg('deleting %r' % self.namespace)

        try:
            projectJson = GitlabAPI.Json(self.filename, self.baseRepoUrl)

            del projectJson[self.namespace]

            request.setResponseCode(HTTPResponse.ACCEPTED)
            request.method = 'GET'

            return GitlabProjectsJsonResource(self.status, self.filename, self.baseRepoUrl).render(request)
        except:
            print 'exception %r' % GetExceptionDetail()
            request.method = 'GET'
            return GitlabErrorJsonResource(self.status, self.filename, HTTPResponse.NOT_FOUND, 'The namespace was not found',
                                           GetExceptionDetail(), self.namespace, '').render(request)



class GitlabProjectJsonResource(JsonResource):

    """
    Json Resource for a specific project, handles HTTP PUT and DELETE
    requests for adding/deleting
    """

    def __init__(self, status, filename, baseRepoUrl, namespace, project):
        JsonResource.__init__(self, status)

        self.filename = filename
        self.baseRepoUrl = baseRepoUrl
        self.namespace = namespace
        self.project = project

    def render_PUT(self, request):

        """
        REST call:
        PUT <address>/gitlabapi/projects/<namespace>/<project>
        """

        try:
            projectName = ExtractProjectNameFromUri(request.prepath)
            namespace = ExtractNamespaceFromUri(request.prepath)

            projectJson = GitlabAPI.Json(self.filename, self.baseRepoUrl)

            projectJson[namespace] += projectName

            request.setResponseCode(HTTPResponse.ACCEPTED)
            request.method = 'GET'

            return GitlabProjectsJsonResource(self.status, self.filename).render(request)

        except:
            request.method = 'GET'
            return GitlabErrorJsonResource(self.status, self.filename, HTTPResponse.BAD_REQUEST, 'Failed to create the project as the specified namespace',
                                           GetExceptionDetail(), self.namespace, projectName).render(request)

    def render_DELETE(self, request):

        """
        REST call:
        DELETE <address>/gitlabapi/projects/<namespace>/<project>
        """

        projectName = ExtractProjectNameFromUri(request.prepath)
        namespace = ExtractNamespaceFromUri(request.prepath)

        if projectName and namespace:

            try:
                projectJson = GitlabAPI.Json(self.filename, self.baseRepoUrl)
                del projectJson[namespace][projectName]

                request.setResponseCode(HTTPResponse.ACCEPTED)
                request.method = 'GET'

                return GitlabProjectsJsonResource(self.status, self.filename).render(request)

            except:
                request.method = 'GET'
                return GitlabErrorJsonResource(self.status, self.filename, HTTPResponse.NOT_FOUND, "Failed to delete project",
                                               GetExceptionDetail(), self.namespace, projectName).render(request)

        else:
            #failed to find projects in url, this shouldnt happen
            #has the page moved?
            return GitlabErrorJsonResource(self.status, self.filename, HTTPResponse.INTERNAL_SERVER_ERROR,
                                                   'The uri did not contain both a project and a namespace, should not have been able to get this far',
                                                   '', self.namespace, projectName).render(request)

    def asDict(self, request):
        result = {}

        json = GitlabAPI.Json(self.filename, self.baseRepoUrl)

        result['Namespace'] = self.namespace
        result['Name'] = self.project
        result['repourl'] = json[self.namespace][self.project]

        return result
