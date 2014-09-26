import os.path
import shutil

from Server import Server
from Installer import Installer
from xl_helper.FileUtils import FileUtils


# class Updater:
#
#     def __init__(self, config):
#         self.config = config
#         self.installer = Installer(config)
#
#     def server(self, dist, location, start=False):
#         backup_location = location + '_old'
#         FileUtils.delete_dirs(backup_location)
#         shutil.copytree(location, backup_location)
#         FileUtils.delete_contents(location)
#
#         new_version_dir = self.installer.server(dist, os.path.join(location, os.path.pardir), start)
#
#         print "new_version_dir: " + new_version_dir
#
#         FileUtils.copy_contents(new_version_dir, location)
#
#         FileUtils.copy_contents(os.path.join(backup_location, 'repository'), os.path.join(location, 'repository'))
#         FileUtils.copy_contents(os.path.join(backup_location, 'plugins'), os.path.join(location, 'plugins'))
#         FileUtils.copy_contents(os.path.join(backup_location, 'conf'), os.path.join(location, 'conf'))
#
#         FileUtils.delete_dirs(backup_location, new_version_dir)
#         pass
