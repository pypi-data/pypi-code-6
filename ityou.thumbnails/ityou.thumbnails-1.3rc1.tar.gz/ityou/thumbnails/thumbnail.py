# -*- coding: utf-8 -*-
import os
import urllib2
from datetime import datetime, date
import magic
import re

from time import time

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from ityou.thumbnails.interfaces import IThumbnailSettings

from Acquisition import aq_inner
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from zope.component.hooks import getSite

from . import THUMBNAIL_HOME, INSTANCE_PATH, TMP_FOLDER_LOCATION, HTML_TMPL
from . import THUMBNAIL_SUFFIX, LARGE_THUMBNAIL_SUFFIX, LISTING_THUMBNAIL_SUFFIX, CONVERTABLE_DOCTYPES

from browser.show_thumbnail import ShowThumbnail

import logging

try:
    os.mkdir(THUMBNAIL_HOME)
except OSError:
    logging.info("%s already exists. No need to create." % THUMBNAIL_HOME)

try:
    os.mkdir(TMP_FOLDER_LOCATION)
except OSError:
    logging.info("%s already exists. No need to create." % TMP_FOLDER_LOCATION)

class ThumbnailManager():
    """
    The thumbnail manager manages the thumbnails. The functions of the class generates them
    and deliver them to templates 
    """
    
    def getThumbnail(self, obj, size = ""):
        """
        This function checks if the document has already a new thumbnail or if a thumbnail
        has to be generated. If not it returns the URL of the thumbnail (link to show_thumbnail view
        on document). If a thumbnail has to be generated it calls the _createTmpFile() function.
        """
        obj_uid = obj.UID()
        t1 = time()
        tmp_file = None
                 
        if obj.portal_type == "Image":
            if not size:
                return obj.absolute_url() + '/image_thumb'
            elif size == "large":
                return obj.absolute_url() + '/image_large'
            elif size == "listing":
                return obj.absolute_url() + "/image_thumb"

        tn_path  = THUMBNAIL_HOME + '/' + obj_uid[0:2] + '/'
        tn       = tn_path + obj_uid + THUMBNAIL_SUFFIX[1]
        tn_large = tn_path + obj_uid + LARGE_THUMBNAIL_SUFFIX[1]
        tn_listing = tn_path + obj_uid + LISTING_THUMBNAIL_SUFFIX[1]
        
        obj_modified = obj.modification_date.millis() / 1000
        
        if not os.path.isfile(tn) or not os.path.isfile(tn_large):
            tmp_file = self._createTmpFile(obj, tn)
            if tmp_file:
                if not os.path.isfile(tn):
                    self._createThumbnail(tmp_file, tn_path, tn, size=THUMBNAIL_SUFFIX[0])
                if not os.path.isfile(tn_large):
                    self._createThumbnail(tmp_file, tn_path, tn_large, size=LARGE_THUMBNAIL_SUFFIX[0])
                if not os.path.isfile(tn_listing):
                    self._createThumbnail(tmp_file, tn_path, tn_listing, size=LISTING_THUMBNAIL_SUFFIX[0])
        
        if os.path.isfile(tn):                
            if obj_modified > int(os.path.getmtime(tn)):
                tmp_file = self._createTmpFile(obj, tn)
                if tmp_file:
                    self._createThumbnail(tmp_file, tn_path, tn, size=THUMBNAIL_SUFFIX[0])
                    self._createThumbnail(tmp_file, tn_path, tn_large, size=LARGE_THUMBNAIL_SUFFIX[0])
                    self._createThumbnail(tmp_file, tn_path, tn_listing, size=LISTING_THUMBNAIL_SUFFIX[0])
            
        if tmp_file:
            self._removeFile(tmp_file)
        
        print "\t\tDAUER    getThumbnails (ms): ", (time()-t1)*1000
        return obj.absolute_url() + '/@@show_thumbnail?size=' + size
    
    @memoize
    def getCachedThumbnail(self, uid, size = ""):
        """ Get Thumbnail in cached version
        """
        return self.getThumbnail(uid, size)
    
    def _removeFile(self,tmp_file):
        """Removes a file form the filesystem
        """
        os.system('rm -f %s' % tmp_file)
        return 

    def _createTmpFile(self, obj, tn):
        """Function creates a html file or other file which ImageMagic 
        can convert. The Thumbnail is saved in /var/thumbnails/...
        """
        obj_uid = obj.UID()
        doc_type = obj.portal_type

        tf = TMP_FOLDER_LOCATION + '/' + obj_uid
        #try:
        if doc_type == "File":
            doc_type = obj.getFilename().split('.')[-1]
            tmp_file = tf + '.' + doc_type 
            f = open(tmp_file, 'w')            
            input = obj.getFile()
            f.write(str(input))
            f.close()
            try:
                # if unoconv is running:
                if doc_type in CONVERTABLE_DOCTYPES:
                    print "OK!!! %s is Convertable!" % doc_type
                    res = os.system("unoconv -f pdf %s" % tmp_file)
                    os.system(  'rm -f %s' % tmp_file  )
                    print "RESULT:", res
                    tmp_file = tf + '.pdf'
            except:
                logging.info('uniconv is not running - no thumbnail of "%s" documents can be generated' % obj_uid)

        elif doc_type == "Link":
            # first check if url is valid!
            if not self._is_valid_url(obj.getRemoteUrl()):
                logging.warn('URL "%s" is not valid!' % obj.getRemoteUrl() )
                return

            tmp_file = tf + ".png"
            f = open(tmp_file, 'w')
            if getUtility(IRegistry).forInterface(IThumbnailSettings).cutycapt_installed: 
                tmp_file_to_crop = INSTANCE_PATH + '/var/tmp/' + obj_uid + 'CROP.png'
                os.system(  "xvfb-run --auto-servernum --server-args='-screen 0, 800x600x24' /usr/local/bin/CutyCapt --url=%s --out=%s" % (obj.getRemoteUrl(), tmp_file_to_crop) )
                os.system(  'convert "%s" -crop 1000x1333+0+0 +repage "%s"' % (tmp_file_to_crop, tmp_file)  )
                os.system(  'rm -f %s' % tmp_file_to_crop  )
            else:
                url_site = urllib2.urlopen(obj.getRemoteUrl())
                input = url_site.read()
                html_input = input[str(input).find("<html"):-1]
                f.write(str(html_input))
                f.close()

        elif doc_type in ["Document","Event", "News Item"]:
            tmp_file = tf + ".html"
            f = open(tmp_file, 'w')            

            title = obj.title_or_id().decode('utf-8').encode('iso-8859-15', 'ignore')
            text  = obj.getText().decode('utf-8').encode('iso-8859-15', 'ignore')
            description = obj.Description().decode('utf-8').encode('iso-8859-15', 'ignore')

            if doc_type == "Event":
                event_content = "\n" #TODO Event-Felder !iso-8859-15 
                text += event_content
            elif doc_type == "News Item":
                news_content = "\n" # TODO News-Felder !iso-8859-15 
                text += news_content

            data =  HTML_TMPL % (title, title, description, text)
            f.write(data)
            f.close()
        else:
            tmp_file = None
        
        return tmp_file
        #except:
        #    logging.warning("Warning: Could not create tmp_file for %s" % obj_uid)

    
    def _createThumbnail(self, tmp_file, tn_path, tn, size=THUMBNAIL_SUFFIX[0]):
        """Creates a thumnail
        tmp_file: Location of the temporary file
        tn: Location of the generated thumbnail
        """
        os.system('mkdir -p %s' % tn_path)
        
        try:
            if os.path.isfile(tmp_file):
                logging.info("Create Thumbnail (Path): %s", tn)
                os.system('convert -thumbnail %s "%s"[0] "%s"' % (size, tmp_file, tn))
        except:
            logging.warning("Warning: Could not create thumbnail for %s" % tn)        

        return

    def _is_valid_url(self, url):
        regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return url is not None and regex.search(url)



