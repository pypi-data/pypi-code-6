# -*- coding: utf-8 -*-
import csv
import urllib2
import tarfile
import os
import logging
import hashlib

from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from datetime import datetime
from ZPublisher.HTTPRequest import FileUpload
from crop_portrait import FieldStorage

from ityou.extuserprofile.dbapi import DBApi
from .. import INSTANCE_PATH

dbapi = DBApi()

class UserImport(BrowserView):
    """ View to import data which was exported with @@user-export before
    """
    
    def __call__(self):
        """ View must be called with the context of the packed file.
        Users are added if not exist. Restores Extended User Profiles and
        Personal Portraits.
        """
        context = aq_inner(self.context)
        pr= getToolByName(context,"portal_registration")
        mt= getToolByName(context,"portal_membership")

        do_import_users   =  context.REQUEST.get('users')
        do_import_groups  =  context.REQUEST.get('groups')
        if not do_import_users and not do_import_groups:
            return "Please us like this: @@user-export?users=1&groups=1"
        
        try:
            os.mkdir("var/tmp/import")
        except OSError:
            logging.info("var/tmp/import already exists. No need to create.")

        FILE_NAME = context.getFilename()
        FILE_IDENTIFIER = FILE_NAME.split(".")[0] 
        FILE_PATH = "var/tmp/import/" + FILE_NAME
        EXTRACTED_PATH = "var/tmp/import/" + FILE_IDENTIFIER + "/"
        
        online_file = context.getFile()
        file = open(FILE_PATH, "w")
        file.write(str(online_file))
        file.close()
        file = tarfile.open(FILE_PATH, 'r')
        file.extractall(path=EXTRACTED_PATH)

        # 1. USERS IMPORT =============================================
        if do_import_users: 
            core_props = ['uid','password','fullname','email']
            ext_props  = ["salutation", "acadtitle", "firstname", "lastname", \
                          "homecity", "education", "profession", \
                          "phone", "mobile", \
                          "city", "department", "position", "specialist_education_in", "medical_specialist_designation", "focus", "career_progression"]
            group_props = ['groups']
            props       = core_props + ext_props + group_props
        
        
            f = open("var/tmp/import/" + FILE_IDENTIFIER + "/EXPORT_USERS.CSV")
            data = csv.reader(f)

            for row in data:
                print "import: ", row
                uid =           row[0]
                fullname =      row[1]
                password =      row[2]
                email =         row[3]

                domains =   ""
                roles =     ("Member",)

                properties = {
                    "username":  uid,
                    "fullname":  fullname,
                    "email":     email,
                }  
                m = hashlib.md5()
                m.update(uid)
                m.update(str(datetime.now()))
                try:
                    pr.addMember(uid, m.hexdigest(), roles, domains, properties=properties)
                except:
                    print "Could not member with uid:", uid
                finally:
                    member = mt.getMemberById(uid)
                    member.setFullname(fullname)
                    try:
                        personal_portrait = open("var/tmp/user_" + FILE_IDENTIFIER + "/" + uid, "r")
                        portrait = FileUpload(FieldStorage(personal_portrait))
                        mt.changeMemberPortrait(portrait, uid=uid)
                        personal_portrait.close()
                    except:
                        pass

                    extented_properties = {}
                    i = 4
                    for prop in ext_props:
                        if prop == 'birthdate':
                            extented_properties[prop] = str(row[i])
                        else:
                            extented_properties[prop] = row[i].decode('utf-8')
                        i += 1
                    
                    dbapi.setExtendedProfile(uid, **extented_properties)

            ###os.system("rm %s" % FILE_PATH.replace(" ", "\ "))
            ###os.system("rm %s -R" % EXTRACTED_PATH.replace(" ", "\ "))            
            return "OK"
        # / USERS IMPORT ===============================================

