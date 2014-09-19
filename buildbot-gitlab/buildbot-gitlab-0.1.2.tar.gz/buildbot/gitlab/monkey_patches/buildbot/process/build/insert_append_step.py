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

import buildbot.process
from twisted.python import log

import re

""" functions to add to the buildstep list during a build"""

def appendStep(self, step):

    """
    adds a buildstep to the end of the list of pending steps for an already in progress build.

    :param step: step to be added
    :return: None
    """

    self.insertStep(len(self.steps), step)


def insertStep(self, index, step):

    """
    inserts a buildstep to the list of pending steps for an already in progress build at
    the specified index.

    :param step: step to be added
    :param index: the location at which to insert the step
    :return: None
    """

    step.setBuild(self)
    step.setBuildSlave(self.slavebuilder.slave)
    # TODO: remove once we don't have anything depending on setDefaultWorkdir
    if callable(self.workdir):
        step.setDefaultWorkdir(self.workdir(self.sources))
    else:
        step.setDefaultWorkdir(self.workdir)

    #the step needs to have a unique name
    #check if this step.name is registered multiple times (i.e. with a _count following it)
    reStepName = re.compile(r'(^' + step.name + '_)([0-9]+)')
    matched = False
    for n in self.progress.steps.keys():
        match = reStepName.match(n)

        if match is not None:
            log.msg("matched: " + n)
            matched = True
            name = match.group(1)
            count = int(match.group(2))
            step.name = step.name + "_%d" % (count + 1)

    #didnt match a name_x now check if name alone exists
    if not matched:
        if step.name in self.progress.steps.keys():
            log.msg("addstep: no name_ matches, but name exists, appending _1")
            step.name = step.name + "_1"

    # tell the BuildStatus about the step. This will create a
    # BuildStepStatus and bind it to the Step.
    step_status = self.build_status.addStepWithName(step.name)
    step.setStepStatus(step_status)

    self.steps.insert(index, step)

    log.msg(" step '%s' inserted at %d" % (step.name, index))

    # update progress to consider new step
    if self.useProgress:
        sp = step.setupProgress()
        self.progress.updateExpectations(sp)


@buildbot.gitlab.run_once
def apply():
    log.msg("applying Build.addStep functionality patch")
    buildbot.process.build.Build.appendStep = appendStep
    buildbot.process.build.Build.insertStep = insertStep


apply()
