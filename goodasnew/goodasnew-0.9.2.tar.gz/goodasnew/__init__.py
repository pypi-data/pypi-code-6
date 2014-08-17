# Copyright (c) 2012, Wide Open Technologies. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer. Redistributions in
# binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution. THIS SOFTWARE IS
# PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging
import os
import platform
import shutil
import sys
import tempfile
import urllib
import urllib2
import xml.etree.ElementTree

from ftplib import FTP
from xml.dom import minidom
from xml.etree import ElementTree as ET

manifest_filename = "updates.xml"
thisarch = platform.architecture()[0]

def xml2d(e):
    """
    convert XML output to dictionary format
    """
    def _xml2d(e):
        if e.text:
            text = e.text.strip()
            if text != "":
                return text
            else:
                kids = {}
                for c in e:
                    kids[c.tag] = _xml2d(c)
                    
                return kids
    return { e.tag : _xml2d(e) }

# 
def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            
def version_to_int_list(version):
    version_int = []
    for num in version.split("."):
        try:
            version_int.append(int(num))
        except:
            raise
        
    return version_int

class Updater(object):
    """
    Updater is used to find and download any available updates,
    then start a separate process that performs the actual installation
    and restarts the app.
    """
    
    def __init__(self, update_dir_url):
        """
        Initializes the updater.
        
        update_url: A url to a directory containing zip files with available
        updates, and a updates.xml file, mapping versions to updates
        and providing update description and details.
        """
        self.update_dir_url = update_dir_url
        self.updates = []
        self.tempdir = tempfile.mkdtemp()
        url = update_dir_url + "/updates.xml"
        xml = urllib2.urlopen(url)
        if xml.geturl().endswith("updates.xml"):
            tempxml = open(os.path.join(self.tempdir, "updates.xml"), 'wb')
            tempxml.write(xml.read())
            tempxml.close()
        self.manifest = UpdatesManifest(self.tempdir)
        
    def cleanup(self):
        """
        Cleans up any temp files or temporary objects created by the updater.
        """
        try:
            shutil.rmtree(self.tempdir)
        except:
            # the OS should clean up on reboot if we can't do it
            pass
            
    def find_latest_update(self, version, name=None, platform=sys.platform, arch=thisarch):
        """
        Finds the latest update available for the given version, name, platform and arch.
        Returns a dict with update info if found, or None if no update has been found.
        """
        
        update = self.manifest.find_latest_update(version, name, platform, arch)
        if not "url" in update:
            # we're up-to-date, so just run cleanup and return None
            self.cleanup()
            return None
        
        return update
        
    def download_update(self, update_filename, callback=None):
        update_url = self.update_dir_url + '/' + update_filename
        urllib.urlretrieve(update_url, filename=os.path.join(self.tempdir, update_filename), reporthook=callback)
        print "%r downloaded!" % update_url
        
    def get_xml_as_dict(self, url):
        answer = {}
        try:
            et = ET.XML(urllib2.urlopen(url).read())
            answer = xml2d(et)
        except ET.ParseError, e:
            log = logging.getLogger("goodasnew")
            log.error("Error parsing response from server. The data returned is:")
            log.error(repr(e))
        
        return answer

class UpdatesManifest(object):
    """
    UpdatesManifest is used to manage the updater's XML manifest, containing a list of
    products, versions and descriptions."
    """
    
    def __init__(self, manifest_dir, ftp_host=None, ftp_dir=None, ftp_user=None, ftp_pass=None):
        """
        Initialize the UpdatesManifest.
        
        manifest_dir: The path on disk to the directory containing the updates.xml file.
        
        """
        
        self.manifest_dir = manifest_dir
        self.manifest_fn = os.path.join(manifest_dir, manifest_filename)
        self.manifest = None # this will be an ElementTree structure after load()
        
        self.ftp_host = ftp_host
        self.ftp_dir = ftp_dir
        self.ftp_user = ftp_user
        self.ftp_pass = ftp_pass
        
        if self.ftp_host is not None and self.ftp_dir is not None:
            self.fetch_manifest()
        
        self.load()
        
    def fetch_manifest(self):
        # if this fails, there is most likely no manifest on the server, and load
        # will create one in that case.
        try:
            ftp = FTP(self.ftp_host)
            if self.ftp_user is not None and self.ftp_pass is not None:
                ftp.login(self.ftp_user, self.ftp_pass)
            ftp_path = '%s/%s' % (self.ftp_dir, manifest_filename)
            if ftp.size(ftp_path) is not None:
                f = open(self.manifest_fn, 'wb')
                try:
                    ftp.retrbinary('RETR ' + ftp_path, f.write)
                except:
                    pass
                f.close()
        except:
            pass

    def load(self):
        """
        Loads the manifest from the directory specified by manifest_dir.
        """
        if os.path.exists(self.manifest_fn):
            self.manifest = ET.ElementTree(file=self.manifest_fn)
        else:
            updates = ET.Element("Updates")
            self.manifest = ET.ElementTree(updates)
        
    def save(self):
        """
        Saves the manifest to the directory specified by manifest_dir.
        """
        indent(self.manifest.getroot())
        self.manifest.write(self.manifest_fn)
        
    def find_latest_update(self, version, name=None, platform=sys.platform, arch=thisarch):
        """
        Finds the latest update available for the current application version, platform, 
        and CPU architecture. Also checks the application name if name is set.
        """
        
        log = logging.getLogger("goodasnew")
        result = {}
        version_tuple = version_to_int_list(version)
        latest_update = None
        for update in self.manifest.getroot():
            update_version = update.get('version')
            # if we're checking the app name, make sure it matches first
            if name is not None and not update.get(name) == name:
                continue
                
            if update_version and version_to_int_list(update_version) > version_tuple:
                if latest_update is not None:
                    if version_to_int_list(update_version) > version_to_int_list(latest_update.get('version')):
                        latest_update = update
                else:
                    latest_update = update
                    
        # okay, we've found a new version, now let's find the right platform and arch
        release_name = ''
        if latest_update is not None:
            result["version"] = latest_update.get('version')
            result["name"] = latest_update.get('name')
            for release in latest_update.find('Releases'):
                if release.get('platform') == platform and release.get('arch') == arch:
                    release_name = "%s-%s-%s-%s" % (name, version, platform, arch)
                    result["url"] = release.get('url')
                    hashtag = release.find('Hash')
                    if hashtag is None:
                        log.error("Could not find release hash for %s. Please check the XML manifest." % release_name)
                    else:
                        result["hash"] = hashtag.text
        if not "url" in result or result["url"] is None:
            log.debug("No valid update URL for %s. Please check the XML manifest." % release_name)
            
        return result
                
    def add_update(self, name, version, url, zipfile, hash, platform=sys.platform, arch=thisarch, description=None):
        """
        Adds a new update to the manifest. If an update of the same name and version exists,
        it simply updates the existing element with the data passed in. 
        """
        update = None
        for update_elem in self.manifest.getroot():
            if update_elem.get("version") == version and update_elem.get("name") == name:
                update = update_elem
                break

        if update is None:
            update = ET.SubElement(self.manifest.getroot(), "Update")
        update.set("name", name)
        update.set("version", version)
        desc = update.find('Description')
        if desc is None:
            desc = ET.SubElement(update, "Description")
            desc.text = 'Insert description here.'
        
        if description:
            desc.text = description
        else:
            log = logging.getLogger("goodasnew")
            log.warning("No description specified. Please enter a description before uploading.")
        releases = update.find('Releases')
        if releases is None:
            releases = ET.SubElement(update, "Releases")

        release = None
                    
        for thisrelease in releases:
            if thisrelease.get('url') == url:
                release = thisrelease
                break

        if release is None:
            release = ET.SubElement(releases, "Release")

        release.set("url", url)
        release.set("platform", platform)
        release.set("arch", arch)
        hashtag = release.find('Hash')
        if hashtag is None:
            hashtag = ET.SubElement(release, "Hash")
        hashtag.text = hash
        
        self.save()
        destfile = os.path.join(self.manifest_dir, os.path.basename(zipfile))
        if os.path.exists(destfile):
            os.remove(destfile)
        shutil.copy(zipfile, destfile)
        
    def upload_files(self):
        ftp = FTP(self.ftp_host)
        if self.ftp_user is not None and self.ftp_pass is not None:
            ftp.login(self.ftp_user, self.ftp_pass)
        ftp.cwd(self.ftp_dir)
        
        files = os.listdir(self.manifest_dir)
        for afile in files:
            fullpath = os.path.join(self.manifest_dir, afile)
            if os.path.exists(fullpath) and os.path.isfile(fullpath) and not afile.startswith('.'):                
                f = open(fullpath, 'rb')
                print("Uploading %s, this may take a while..." % afile)
                ftp.storbinary('STOR ' + afile, f)
                f.close()
