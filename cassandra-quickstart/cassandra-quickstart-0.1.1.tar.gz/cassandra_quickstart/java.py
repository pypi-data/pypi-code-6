import subprocess
import re
import os
from distutils.version import LooseVersion
import platform
import hashlib
from zipfile import ZipFile
import copy
import shutil

from cassandra_quickstart.util import download, DownloadError, makedirs
from cassandra_quickstart import config

class NoSuitableJavaException(Exception):
    pass

PLATFORM_JAVA = {
    "openjdk-1.7.0-u60": {
        'Linux_64bit': {
            'url':'https://bitbucket.org/alexkasko/openjdk-unofficial-builds/downloads/openjdk-1.7.0-u60-unofficial-linux-amd64-image.zip', 
            'sha256':'707c48420a2f81a377cdd3899ca6e083a9016047f1696ab08f311e92e25fb971'
        },
        'Linux_32bit': {
            'url':'https://bitbucket.org/alexkasko/openjdk-unofficial-builds/downloads/openjdk-1.7.0-u60-unofficial-linux-i586-image.zip', 
            'sha256':'70691d01a3448d718a9319107fc9ab04cd86020869827573f93df89289258289'
        },
        'Windows_64bit': {
            'url':'https://bitbucket.org/alexkasko/openjdk-unofficial-builds/downloads/openjdk-1.7.0-u60-unofficial-windows-amd64-image.zip', 
            'sha256':'a84e4ab93092577cdc45116f5a1b241ba44b4cf23bc9798b997d28476f45d96a'
        },
        'Windows_32bit': {
            'url':'https://bitbucket.org/alexkasko/openjdk-unofficial-builds/downloads/openjdk-1.7.0-u60-unofficial-windows-i586-image.zip',
            'sha256': '70691d01a3448d718a9319107fc9ab04cd86020869827573f93df89289258289'
        },
        'Darwin_64bit': {
            'url':'https://bitbucket.org/alexkasko/openjdk-unofficial-builds/downloads/openjdk-1.7.0-u60-unofficial-macosx-x86_64-image.zip', 
            'sha256':'b494bdacc8f00f9c12fe257fbdfb3671023af67ef9f902d97ecb32bc9a0ecbeb'
        }
    }
}

def setup_java(min_version='openjdk-1.7.0-u60'):
    """Return JAVA_HOME of the embedded OpenJDK.
    Download a package if none exists""" 

    cfg = config.Config.open()
    new_java = False
    try:
        java_home = cfg.get('java','java_home')
        sha = cfg.get('java','pkg_sha')
        version = cfg.get('java','version')
        if LooseVersion(version) < LooseVersion(min_version):
            new_java = True
    except config.NoOptionError:
        new_java = True

    if new_java:
        # Download new java:
        java_pkg = download_install_java(min_version)
        java_home = java_pkg['java_home']
        sha = java_pkg['sha256']
        version = java_pkg['version']        
        cfg.set('java','java_home', java_home)
        cfg.set('java','pkg_sha', sha)
        cfg.set('java','version', version)
        cfg.save()

    return java_home

def download_install_java(version, cqs_home=None):
    if cqs_home is None:
        cqs_home = os.path.join(os.path.expanduser("~"),'.cassandra-quickstart')
    jre_root = os.path.join(cqs_home,'java')
    sys_platform = platform.system() + "_" + platform.architecture()[0]
    
    try:
        java_pkg = PLATFORM_JAVA[version][sys_platform]
    except KeyError:
        raise AssertionError("Could not find a suitable java download for platform: {sys_platform}".format(sys_platform=sys_platform))

    makedirs(jre_root)
    java_home = os.path.join(jre_root, version)
    download_path = java_home + '.zip'
    # Delete any previous installs :
    try:
        shutil.rmtree(java_home)
        os.delete(download_path)
    except OSError:
        pass
    # Download:
    download(java_pkg['url'], download_path, show_progress=True)

    # Check sha256sum of downloaded java package:
    with open(download_path) as f:
        if hashlib.sha256(f.read()).hexdigest() != java_pkg['sha256']:
            raise AssertionError(
                'Java zip file from {download_url} did not have '
                'expected SHA256: {sha}. Not installing.'.format(
                    download_url=java_pkg['url'], sha=java_pkg['sha256']))

    # Extract java zip file to home dir:
    with ZipFile(download_path) as z:
        z.extractall(jre_root)
        try:
            java_pkg_dir = [d for d in z.namelist() if d.startswith(version) and '/' in d][0].strip('/')
        except:
            raise AssertionError('Could not find java directory name inside package: {download_path}'.format(**locals()))
        extracted_java_dir = os.path.join(jre_root, java_pkg_dir)
        os.rename(extracted_java_dir, java_home)
    # Set executable bits:
    for path in os.listdir(os.path.join(java_home,'bin')):
        os.chmod(os.path.join(java_home,'bin',path), 0o755)
    for path in os.listdir(os.path.join(java_home,'jre','bin')):
        os.chmod(os.path.join(java_home,'jre','bin',path), 0o755)

    # Write the sha of the original package we installed:
    with open(os.path.join(java_home, 'SHA.txt'), 'w') as f:
        f.write(java_pkg['sha256'])

    meta = {'java_home':java_home, 'version':version}
    meta.update(java_pkg)
    return meta
    
