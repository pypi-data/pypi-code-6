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

from buildbot.process.buildstep import LoggingBuildStep, BuildStep
from buildbot.process.buildstep import BuildStepFailed
from buildbot.process.buildstep import RemoteCommand
from buildbot.process.factory import BuildFactory

# apply patches
from buildbot.gitlab.monkey_patches.buildbot.process.build import insert_append_step
from buildbot.gitlab.monkey_patches.buildbot.process.build import insert_append_step
from buildbot.gitlab.monkey_patches.buildbot.status.progress import update_expectations

from buildbot.steps.shell import ShellCommand

class FileBranch(LoggingBuildStep):

    """ FileBranch is a build step which selects the next step to be executed based on the presence
    of files located in the root checkout of the build.
    """

    name = "FileBranch"
    description = "Performing build step based upon files detected in root dir of checkout"

    def __init__(self, fileBranchDictionary, **kwargs):

        """
        __init__ requires a dictionary of filenames mapped to either a BuildStep or a BuildFactory, additional args are passed
        to the base class; LoggingBuildStep.

        :param fileBranchDictionary: a list of key-value pairs mapping file names to either a single BuildStep or
        a BuildFactory containing one or more steps
        if the file (the key) is detected in the root checkout of the build, then the associated step(s) will be run
        :param kwargs: additional arguments that will be passed directly to the base LoggingBuildStep
        :return: none
        """

        LoggingBuildStep.__init__(self, **kwargs)

        self.fileBranchDictionary = fileBranchDictionary
        self.fileFound = None

        # failure of this step should cause build to fail
        # we could set these based on all possible sub commands (i.e. if any registered commands have these set
        # then we set them else leave them as false).
        self.haltOnFailure = True
        self.flunkOnFailure = True

    def start(self):
        """
        this function sends the listdir command to the buildslave using the root of the checkout as the directory
         to return a list of files, used to determine the next buildstep.
        :return: none
        """

        cmd = RemoteCommand('listdir', {'dir': self.build.workdir})
        self.startCommand(cmd)


    def setStatus(self, cmd, results):

        """
        Update the status with the result of the stepBranch, i.e. what file was
        matched or if none where found

        :param cmd: The deferred command object defined in start
        :param results: Integer representing SUCCESS, FAILURE
        :return: none
        """

        if not self.fileFound:
            self.step_status.setText("No files matched")

            if self.haltOnFailure or self.flunkOnFailure:
                self.step_status.setText2("FileStepBranch: No files matched")

        else:
            self.step_status.setText("Matched " + self.fileFound)

    def commandComplete(self, cmd):

        """
        callback used upon completion of the ls command that was run on the buildslave
        expected to receive a list of files as the result.

        :param cmd: The deferred command object defined in start
        :return: none
        """

        if cmd.didFail():
            self.step_status.setText(["listdir command failed."])

            if self.haltOnFailure or self.flunkOnFailure:
                self.step_status.setText2(["listdir command failed."])

            raise BuildStepFailed()

        filelist = cmd.updates["files"][-1]

        # debug stuff, output results of step selection attempt
        debuglog = self.addLog("debug")

        debuglog.addStdout("Detected files in root:\n\n" + "\n".join(filelist) + "\n\n")

        # if build file exists in root dir, add the correct buildstep
        # if multiple files exist which match different buildsteps only the first is added
        for key, value in self.fileBranchDictionary.items():
            debuglog.addStdout("searching for %r in result\n" % key)

            if key in filelist:
                debuglog.addStdout("found: %r at %r\n\n" % (key, filelist.index(key)))

                # get steps to add from either the single specified step or the
                # steps from the buildfactory
                steps = getattr(value, "steps", [])
                steps = [s.buildStep() for s in steps]
                steps = steps or [value]

                for step in steps:
                    self.build.insertStep(0, step)
                    debuglog.addStdout("added buildstep %r for: %r\n\n" % (step.name, key))

                self.fileFound = key

                break

        # fail if no recognised file, as the build will not continue
        if not self.fileFound:
            debuglog.addStdout("No files matched")
            raise BuildStepFailed()

        debuglog.finish()

class WafCommand(ShellCommand):

    def __init__(self, command, **kwargs):

        """
        Creates a buildstep that executes a waf command.

        :param command: a string or list of string representing the parameters to pass to waf.
        :param kwargs: additional args to be passed to ShellCommand
        :return: None
        """

        if not isinstance(command, list):
            command = [command]

        ShellCommand.__init__(self, command=["waf"] + command, **kwargs)
