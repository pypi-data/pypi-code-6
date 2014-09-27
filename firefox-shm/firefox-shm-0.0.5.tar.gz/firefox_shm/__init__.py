# Copyright (C) 2014 Jens Kasten. All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# 

"""
Package to put firefox profile on tmpfs.

Copyright (C) Jens Kasten. All Rights Reserved.
"""

__author__  = "Jens Kasten <jens@kasten-edv.de>"
__status__  = "beta"
__date__    = "4 August 2014"

__all__ = ["MOZ_PROFILES_DIR", "ProfileConfig", "ProfileArchive"]


import os
import configparser
import shutil
import logging
from subprocess import Popen, PIPE

logging.basicConfig(format='%(levelname)s:%(name)s:line %(lineno)s: %(message)s')
log = logging.getLogger(__name__)

# default directory to search for firefox profiles.ini 
MOZ_PROFILES_DIR = os.path.join(os.environ["HOME"], ".mozilla", "firefox")


class ProfileConfig(object):
    """Class to obtain firefox profile info."""

    def __init__(self):
        self.profiles = {}
        self.profiles_dir = MOZ_PROFILES_DIR
        self.profile_ini =  os.path.join(self.profiles_dir, "profiles.ini")

    def set_log_level(self):
        log.setLevel(logging.DEBUG)

    def read(self):
        config = configparser.ConfigParser()
        log.info("read config: %s" % self.profile_ini)
        config.read(self.profile_ini)
        for section in config.sections():
            if section.startswith("Profile"):
                self.profiles[config.get(section, "name")] = {
                    "path": config.get(section, "path"),
                    "isrelative": config.get(section, "isrelative"),
                }
                try:
                    self.profiles[config.get(section, "name")]["default"] = config.get(section, "default")
                except configparser.NoOptionError as error:
                    pass
        if len(self.profiles) >= 1:
            return True

    def default(self):
        """get default profile"""
        for key, value in self.profiles.items():
            if len(self.profiles) == 1:
                return key
            if "default" in value and value["default"] == "1":
                return key
         
    def path(self, profile):
        try:
            if ("isrelative" in self.profiles[profile] and 
                    self.profiles[profile]["isrelative"] == "1"):
                path = os.path.join(self.profiles_dir,
                    self.profiles[profile]["path"])
                return path
            else:
                return self.profiles[profile]["path"]
        except KeyError as error:
            pass


class ProfileArchive(object):

    def __init__(self, compress="bztar"):
        suffix = {
            "gztar": "tar.gz",
            "bztar": "tar.bz2",
            "zip": "zip"
        }
        self.compress = compress
        self.suffix = suffix[self.compress]

    def set_log_level(self):
        log.setLevel(logging.DEBUG)

    def set_runtime_vars(self, profile_path):
        if not profile_path:
            return False
        self.profile_path = profile_path
        self.profile_name = profile_path.split("/")[-1]
        self.profile_path_new = ".".join([self.profile_path, "new"])
        self.profile_path_shm = os.path.join("/dev/shm", os.environ["USER"],
            "firefox", self.profile_name)
        self.profile_path_archive = ".".join([self.profile_path, "archive"])

    def move_profile_to_new(self):
        try:
            if os.path.islink(self.profile_path):
                return False
            log.info("move %s to %s" % (self.profile_path, 
                self.profile_path_new))
            shutil.move(self.profile_path, self.profile_path_new)
            return True
        except OSError as error:
            log.error(error)

    def copy_profile_to_shm(self):
        try:
            if not os.path.isdir(self.profile_path_shm):
                log.info("create %s" % self.profile_path_shm)
                os.makedirs(self.profile_path_shm)
                log.info("chmod 700 %s" % self.profile_path_shm)
                os.chmod(self.profile_path_shm, 0o700)
            cmd = ["rsync", "-r", "--delete", "--exclude", "lock", 
                    self.profile_path_new + "/", self.profile_path_shm]
            log.info(" ".join(cmd))
            process = Popen(cmd, stdin=PIPE, stderr=PIPE)
            output, error = process.communicate()
        except OSError as error:
            log.error(error)

    def link_shm_profile(self):
        try:
            log.info("ln -sf %s %s" % (self.profile_path_shm, 
                self.profile_path))
            os.symlink(self.profile_path_shm, self.profile_path)
        except OSError as error:
            log.error(error)
            
    def sync_profile(self):
        try:
            if not os.path.isdir(self.profile_path_shm):
                return False
            cmd = ["rsync", "-r", "--delete", "--exclude", "lock",
                    self.profile_path_shm + "/", self.profile_path_new]
            log.info(" ".join(cmd))
            process = Popen(cmd, stdout=PIPE, stderr=PIPE)
            output, error = process.communicate()
        except OSError as error:
            log.error(error)

    def backup_profile(self):
        try:
            if not os.path.isdir(self.profile_path_archive):
                os.mkdir(self.profile_path_archive)
            cmd = ["rsync", "-r", "--delete", "--exclude", "lock",
                    self.profile_path + "/", self.profile_path_archive]
            log.info(" ".join(cmd))
            process = Popen(cmd, stdout=PIPE, stderr=PIPE)
            output, error = process.communicate()
        except OSError as error:
            log.error(error)

    def restore_profile(self):
        try:
            if not os.path.isdir(self.profile_path_new):
                log.info("Nothing to do. Not exists: %s" % self.profile_path_new)
                return False
            if os.path.islink(self.profile_path):
                log.info("Remove symlink: %s" % self.profile_path)
                os.remove(self.profile_path)
            log.info("move %s %s" % (self.profile_path_new + "/", 
                self.profile_path))
            shutil.move(self.profile_path_new, self.profile_path)
            if os.path.isdir(self.profile_path_shm):
                shutil.rmtree(self.profile_path_shm)
        except OSError as error:
            log.error(error)

