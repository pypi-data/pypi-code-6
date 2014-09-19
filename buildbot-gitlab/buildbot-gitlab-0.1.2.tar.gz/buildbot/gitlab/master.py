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


from buildbot.gitlab.api import project as Project

from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers.forcesched import ForceScheduler
from buildbot.changes import filter

from buildbot.process.factory import BuildFactory
from buildbot.steps.source.git import Git
from buildbot.config import BuilderConfig
from buildbot.status import html
from buildbot.gitlab.api.resources import GitlabHtmlResource

def configure(config, builders, statusTargets, slaveBuilderFactory, projectJson, url):

    """
    configure constructs required schedulers and builders for working with gitlab
    to run specified factories

    :param config: A BuildmasterConfig instance. This will be updated to include the builders, schedules & status's required
    for gitlab integration. Anything already set will be removed.
    :param builders: Dictionary of builder names to a list of assigned slaves
    :param statusTargets: List of status targets
    :param slaveBuilderFactory: Dictionary of buildernames to a list of Key-Values mapping project names in the format
    namespace/project (where namespace is the gitlab containing folder for the project; this allows projects with the same name as
    they will reside in different gitlab namespaces) to a list of factories or buildsteps. This allows different projects
    to have different build factories.
    :param projectJson: json file containing a list of gitlab projects
    :param url: the url location of gitlab, use to determine checkout locations
    :return: Buildbot configuration

    This function is intended to be used in the 'master.cfg' to simplify the Buildbot/Gitlab integration, as the following
    example usage illustrates:

        #define builder dictionary in format: <builder-name> : [<slave name>]
        builders = {}
        builders['win7-builder'] = 'win7-buildslave'
        builders['multislave-builder'] = ["slave1", "slave2"]

        webStatus = html.WebStat(http_port=1=8080)

        # map different projects to either 1 or more build factories or build steps.
        # use '*' wildcard for either all projects in a namespaces or for all projects in all namespaces.
        slaveBuilderFactories['win7-builder' = {
            'gitlab/the-factory-project' : [FirstBuildFactory, SecondBuildFactory]
            'gitlab/the-steplist-project' : [FirstBuildstep, secondBuildstep]
            'gitlab/*' : [BuilderForOtherProjectsInGitlabFolder]
            '*' : [DefaultBuilder]
        }

        c = Configure(c, builders, [webStatus], slaveBuilderFactories, 'my_projects.json'
            'https://my-projects.com');

    """

    json = Project.Json(projectJson, url)

    #convert the namespace:projectlist dictionary to a list of (namespace,project) tuples
    projects = [(namespace,project) for namespace,projects in json.data.iteritems() for project in projects]

    config.setdefault('schedulers', [])
    config.setdefault('builders', [])
    config.setdefault('status', [])

    for namespace,project in projects:

        projectName = (namespace + "/" + project).encode('ascii')

        uniqueBuilders = { projectName + '-%s' % k : v for k,v in builders.items() }
        builderNames = [builder for builder in uniqueBuilders]
        slaveFactories = { projectName + '-%s' % k : v for k,v in slaveBuilderFactory.items() }

        #scheduler is triggered by a change source (from the gitlab web-hook in this case)
        #& applies filtering in order to select the appropriate builder
        #(i.e. the one with the git step that matches the repo url)
        config['schedulers'].append(SingleBranchScheduler(
                                 name=  projectName + ' all',
                                 change_filter=filter.ChangeFilter(branch='master', repository=json[namespace][project], project=projectName),
                                 treeStableTimer=None,
                                 builderNames=builderNames))

        config['schedulers'].append(ForceScheduler(
                                name= projectName + ' force',
                                builderNames=builderNames))


        # setup builder config for each slave/builder
        for index,buildername in enumerate(builderNames):

            factory = BuildFactory()

            factory.addStep(Git(
                repourl=json[namespace][project],
                mode='incremental'))

            factoryStepsOrList = slaveFactories[buildername].get(projectName,
                slaveFactories[buildername].get(namespace + "/*", slaveFactories[buildername]['*']))

            if isinstance(factoryStepsOrList, BuildFactory):
                factory.addSteps(factoryStepsOrList.steps)
            elif isinstance(factoryStepsOrList, list):
                for factorySteps in factoryStepsOrList:
                    factorySteps = getattr(factorySteps, "steps", []) or [factorySteps]
                    factory.addSteps(factorySteps)
            else:
                raise ValueError('failed to get either BuildFactory or list of steps in slaveFactories parameter')

            config['builders'].append(
                BuilderConfig(name=buildername,
                              slavenames=uniqueBuilders[buildername],
                              factory=factory))


    #if using WebStatus add the GitlabHtmlResource for modifying gitlab projects
    for statusTarget in statusTargets:
        if isinstance(statusTarget, html.WebStatus):
            statusTarget.putChild('gitlabapi', GitlabHtmlResource(projectJson))

        config['status'].append(statusTarget)

    return config
