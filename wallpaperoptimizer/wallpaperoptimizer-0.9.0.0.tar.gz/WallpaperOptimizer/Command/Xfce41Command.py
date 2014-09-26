# -*- coding: utf-8 -*-

import subprocess
import re

from WallpaperOptimizer.Command.Command import Command


class Xfce41Command(Command):

    class Settings(object):
        def isPrimary(self):
            return self.Primary

        def setPrimary(self):
            self.Primary = True

        def __init__(self):
            self.mid = ""
            self.Primary = False
            self.CycleEnable = False
            self.CyclePeriod = 0
            self.CycleRandom = False
            self.CycleTimer = 0
#            self.ColorStyle = 0
            self.ImageStyle = 0
            self.lastImage = ""

    def setWall(self, path):
        self.ret = subprocess.call(
            [self.command,
                "-c",
                "xfce4-desktop",
                "-p",
                "/backdrop/screen0/monitor" +
                self.monitor0.mid +
                "/workspace0/last-image",
                "-t",
                "string",
                "-s",
                path]
        )
        return self.ret

    def setView(self):
        self.ret = None

        if self.wspMode is False:
            self.ret = subprocess.call(
                [self.command,
                    "-c",
                    "xfce4-desktop",
                    "-p",
                    "/backdrop/single-workspace-mode",
                    "-t",
                    "Boolean",
                    "-T"]
            )

        if self.monitor0.ImageStyle != 6:
            self.ret = subprocess.call(
                [self.command,
                    "-c",
                    "xfce4-desktop",
                    "-p",
                    "/backdrop/screen0/monitor" +
                    self.monitor0.mid +
                    "/workspace0/image-style",
                    "-t",
                    "int",
                    "-s",
                    "6"]
            )

        if self.monitor0.CycleEnable is False:
            self.ret = subprocess.call(
                [self.command,
                    "-c",
                    "xfce4-desktop",
                    "-p",
                    "/backdrop/screen0/monitor" +
                    self.monitor0.mid +
                    "/workspace0/backdrop-cycle-enable",
                    "-t",
                    "Boolean",
                    "-T"]
            )

            self.ret = subprocess.call(
                [self.command,
                    "-c",
                    "xfce4-desktop",
                    "-p",
                    "/backdrop/screen0/monitor" +
                    self.monitor0.mid +
                    "/workspace0/backdrop-cycle-period",
                    "-t",
                    "int",
                    "-s",
                    self.monitor0.CyclePeriod]
            )

            self.ret = subprocess.call(
                [self.command,
                    "-c",
                    "xfce4-desktop",
                    "-p",
                    "/backdrop/screen0/monitor" +
                    self.monitor0.mid +
                    "/workspace0/backdrop-cycle-timer",
                    "-t",
                    "Integer",
                    self.monitor0.CycleTimer]
            )

            if self.monitor0.CycleRandom is True:
                self.ret = subprocess.call(
                    [self.command,
                        "-c",
                        "xfce4-desktop",
                        "-p",
                        "/backdrop/screen0/monitor" +
                        self.monitor0.mid +
                        "/workspace0/backdrop-cycle-random-order",
                        "-t",
                        "Boolean",
                        "-T"]
                )

        return self.ret

    def getWall(self):
        self.current = subprocess.Popen(
            [self.command,
                "-c",
                "xfce4-desktop",
                "-p",
                "/backdrop/screen0/monitor" +
                self.monitor0.mid +
                "/workspace0/last-image"],
            stdout=subprocess.PIPE
        ).communicate()[0].rstrip()
        return self.current

    def setOption(self, option):
        self.monitor0.CycleEnable = True
        self.monitor0.CyclePeriod = 0
#         self.monitor0.CycleRandom = False
        self.monitor0.CycleTimer = option.getInterval()

    def __init__(self):
        self.command = "xfconf-query"
        self.monitor0 = self.Settings()
        self.monitor1 = self.Settings()
        self.wspMode = False
#         self.wspNumber = 0

        # channlel: displays
        displays = subprocess.Popen(
            ["grep", "^.*\-0$"],
            stdin=subprocess.Popen(
                [self.command,
                 "-c",
                 "displays",
                 "-l"], stdout=subprocess.PIPE
                ).stdout,
            stdout=subprocess.PIPE
        ).communicate()[0].rstrip().splitlines()

        for display in displays:
            (ppath, mid) = display.rsplit("/", 1)
            prisec = subprocess.Popen(
                [self.command,
                    "-c",
                    "displays",
                    "-p",
                    ppath + "/" + mid + "/Primary"], stdout=subprocess.PIPE
            ).communicate()[0].rstrip()
            if prisec == "true":
                self.monitor0.mid = mid
                self.monitor0.setPrimary()
            else:
                self.monitor1.mid = mid

        # channlel: xfce4-desktop
        kvptn = re.compile('^(.+)\s+(.+)$')
        for mon in (self.monitor0, self.monitor1):
            propertys = subprocess.Popen(
                ["grep", mon.mid],
                stdin=subprocess.Popen(
                    [self.command,
                     "-c",
                     "xfce4-desktop",
                     "-lv"], stdout=subprocess.PIPE
                    ).stdout,
                stdout=subprocess.PIPE
            ).communicate()[0].rstrip().splitlines()

            for prop in propertys:
                val = kvptn.split(prop)[2].rstrip()
                if (kvptn.split(prop)[1].rfind("cycle-enable") > 0):
                    if (val == "true"):
                        mon.CycleEnable = True
                    else:
                        mon.CycleEnable = False
                elif (kvptn.split(prop)[1].rfind("cycle-period") > 0):
                    mon.CyclePeriod = int(val)
                elif (kvptn.split(prop)[1].rfind("cycle-random-order") > 0):
                    if (val == "true"):
                        mon.CycleRandom = True
                    else:
                        mon.CycleRandom = False
                elif (kvptn.split(prop)[1].find("cycle-timer") > 0):
                    mon.CycleTimer = int(val)
#                 elif (kvptn.split(prop)[1].find("color-style") > 0):
#                     mon.ColorStyle = val
                elif (kvptn.split(prop)[1].find("image-style") > 0):
                    mon.ImageStyle = int(val)
                elif (kvptn.split(prop)[1].find("last-image") > 0):
                    mon.lastImage = val

        wspSettings = subprocess.Popen(
            ["grep", "single-workspace"],
            stdin=subprocess.Popen(
                [self.command,
                 "-c",
                 "xfce4-desktop",
                 "-lv"], stdout=subprocess.PIPE
                ).stdout,
            stdout=subprocess.PIPE
        ).communicate()[0].rstrip().splitlines()

        for wspSetting in wspSettings:
            val = kvptn.split(wspSetting)[2].rstrip()
            if (kvptn.split(wspSetting)[1].rfind("mode") > 0):
                if (val == "true"):
                    self.wspMode = True
                else:
                    self.wspMode = False
#             elif (kvptn.split(wspSetting)[1].rfind("number") > 0):
#                 self.wspNumber = val
