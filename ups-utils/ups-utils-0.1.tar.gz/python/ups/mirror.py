#!/usr/bin/env python
'''
Interact with a UPS package mirror
'''

# FIXME: make a generic mirror object that can have specifics given in a configuration file.


import os
import shelve
import urllib

from . import manifest
from . import util




class Oink(object):
    '''
    The "oink" mirror.
    '''

    tarball_urlpat = 'http://oink.fnal.gov/distro/packages/{name}/{tarball}'
    manifest_urlpat = 'http://oink.fnal.gov/distro/manifest/{suite}/{version}/{manifest}'
    manifest_binpat = '{suite}-{version_dotted}-{flavor}-{quals_dashed}_MANIFEST.txt'
    manifest_srcpat = '{suite}-{version_dotted}-source_MANIFEST.txt'

    def __init__(self, cachedir = '~/.ups-util/cache/'):
        cachedir = os.path.expanduser(os.path.expandvars(cachedir))
        if not os.path.exists(cachedir):
            os.makedirs(cachedir)
        self._shelf = shelve.open(os.path.join(cachedir, 'ups-mirror-oink'))
        self.mfs = dict()
        self.mes = set()
        for mfname, mftext in self._shelf.items():
            self._add_manifest_nocache(mfname, mftext)

    def _add_manifest_nocache(self, mfname, mftext):
        mflist = manifest.parse_text(mftext)
        self.mfs[mfname] = mflist
        for me in mflist:
            self.mes.add(me)
        return mflist

    # api
    def add_manifest(self, mfname, mftext):
        '''
        Add a manifest named <mfname> and consisting of text <mftext>.
        '''
        mflist = self._add_manifest_nocache(mfname, mftext)
        self._shelf[mfname] = mftext
        return mflist

    def manifest_name(self, suite, version, flavor, quals = ''):
        '''
        Return the manifest file name.
        '''
        assert version.startswith('v')
        version_dotted = version[1:].replace('_','.')
        quals_dashed = quals.replace(':','-')
        if flavor == 'source':
            return self.manifest_srcpat.format(**locals())
        return self.manifest_binpat.format(**locals())

    def manifest_url(self, suite, version, flavor, quals = ''):
        '''
        Return URL to the manifest file.
        '''
        mfname = self.manifest_name(suite, version, flavor, quals)
        return self.manifest_urlpat.format(manifest=mfname, **locals())
        
    # api
    def load_manifest(self, suite, version, flavor, quals=''):
        '''
        Load a manifest, return list of ManifestElements
        '''
        mfname = self.manifest_name(suite, version, flavor, quals)
        mf = self.mfs.get(mfname)
        if mf: return mf

        url = self.manifest_url(suite, version, flavor, quals)
        print 'Downloading manifest: "%s"' % url
        mftext = manifest.download(url)
        if not mftext: 
            raise RuntimeError, 'Failed to download: %s' % url 
            return

        mflist = self.add_manifest(mfname, mftext)
        return mflist

    # api
    def avail(self, mfname = None):
        '''Return known available entries for manifest named <mfname>.  

        If no name is given, all are returned.
        '''
        if not mfname:
            return self.mes
        return self.mfs.get(mfname)


    def download(self, me, path, force = False):
        target = os.path.join(path, me.tarball)
        if os.path.exists(target):
            if force:
                os.remove(target)
            else:
                return target
        url = self.tarball_urlpat.format(name=me.name, tarball=me.tarball)
        return util.download(url, target)
        


def make(name = 'oink', *args, **kwds):
    if name == 'oink':
        return Oink(*args, **kwds)
    KeyError, 'Unknown ups mirror: "%s"' % name
