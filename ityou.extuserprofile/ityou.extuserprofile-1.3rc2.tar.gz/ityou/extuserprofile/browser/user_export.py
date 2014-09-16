# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

from Products.CMFCore.utils import getToolByName
from ityou.extuserprofile.dbapi import DBApi
import csv
import urllib

from cStringIO import StringIO
from datetime import datetime

import tarfile
import os
import logging

class UserExport(BrowserView):
    """ View which exports members (memberdata + extuserprofile) as a .tar file
    """
    
    def __call__(self):
        """ Userdata are migrated to a .csv file and with the portraits packed to .tar
        File is downloadable for the user at the end
        """
        timestamp = str(datetime.now()).replace(":", "-").replace(".", "-")
        TMP_FOLDER = '/'.join(INSTANCE_HOME.split('/')[:-2]) + "/var/tmp/user_export" + timestamp
        TMP_FOLDER_PATH = "var/tmp/user_export" + timestamp
        CSV_FILE = TMP_FOLDER + "/exportlist.csv"

        try:
            os.mkdir(TMP_FOLDER)
        except OSError:
            logging.info("%s already exists. No need to create." % TMP_FOLDER)
        context = aq_inner(self.context)
        dbapi = DBApi()
        mt= getToolByName(context,"portal_membership")
        exportlist = open(CSV_FILE, "w")
        
        csvwriter = csv.writer(exportlist, delimiter=',', quotechar='"')
        
        prop_key_list = ["salutation", "acadtitle", "firstname", "lastname", "birthdate", "homecity", "leasure", "like", \
                         "dislike", "education", "profession", "phone", "fax", "skype", "xing", "linkedin", "fb", \
                         "twitter", "icq", "street", "city", "country", "department", "position", "superior", "demands", "offers"]
        
        member_ids = mt.listMemberIds()
        for member_id in member_ids:
            member = mt.getMemberById(member_id)
            member_csv = []
            member_csv.append(member_id)
            member_csv.append(member.getProperty("fullname", ""))
            member_csv.append(member.getProperty("email", ""))
            member_csv.append(member.getProperty("homepage", ""))
            try:
                image = urllib.urlopen(str(mt.getPersonalPortrait(member_id, size="original")).split("src=")[1].split('"')[1]).read()
            except:
                image = urllib.urlopen(str(mt.getPersonalPortrait(member_id)).split("src=")[1].split('"')[1]).read()
            f = open(TMP_FOLDER + "/" + member_id, 'w')
            f.write(image)
            f.close()
            ext_profile = dbapi.getExtendedProfile(member_id)
            for key in prop_key_list:
                val = ext_profile.__getattribute__(key)
                if type(val) == "str":
                    member_csv.append(val.encode("utf-8"))
                if not val:
                    member_csv.append("")
                else:
                    member_csv.append(str(val).encode("utf-8"))
            csvwriter.writerow(member_csv)
            
        exportlist.close()
        packed_file_name = "export" + timestamp + ".tar"
        packed_file_path = TMP_FOLDER + "/" + packed_file_name 
        file = tarfile.open(packed_file_path, 'w')
        file.add(TMP_FOLDER_PATH)
        file.close()

        packed_file = open(packed_file_path, "rb")
        context.REQUEST.response.setHeader("Content-Type", "application/octet-stream")
        context.REQUEST.response.setHeader("Content-Disposition", 'attachment; filename="%s"' % packed_file_name)
        context.REQUEST.response.setHeader("Content-Length", packed_file.__sizeof__())
        return packed_file.read()