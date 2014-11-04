#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, errno
import re
import sys
import time
import datetime
import gzip
import glob
from datetime import datetime
from pprint import pprint

import Image, ExifTags
from ExifTags import TAGS

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.template import Context, Template
from django.conf import settings as conf
from sorl.thumbnail import get_thumbnail

import rgallery.models as mymodels
from utils import *


# Class MUST be named 'Command'
class Command(BaseCommand):

    # Displayed from 'manage.py help mycommand'
    help = """
    Tool that tries to download and parse photos from a source bucket,
    saving it on the database and converting the photos to fit the web:

    ./manage.py mediasync

    1.- First time it connects with the bucket and if it's Dropbox, stores the
        token information in a token_file
    2.- Next times it read the token from file to connect (only Dropbox)
    3.- Go to the shared folder and check if the image is already on database
    4.- If not, this script download the image, converting it to fit the web and
        save a record in the database.

    To run this script from a crontab task we should do something like this:

    */30 * * * * cd /path/to/rgallery-project/ ; source env/bin/activate ; cd src ; python manage.py mediasync > /dev/null

    Options:
        --storage=[dropbox|file]
        --source=/path/to/photos (only when storage=file)

    """

    option_list = BaseCommand.option_list + (
            make_option(
                '--storage',
                dest='storage',
                default='dropbox',
                help='Backend storage where the photos are'
            ),
            make_option(
                '--source',
                dest='source',
                default='/Users/oscar/Desktop/Peques/',
                help='Where the photos are in --storage=file'
            ),
        )


    def handle(self, *app_labels, **options):
        """
        The command itself
        """

        # Vars and folders
        storage = options['storage']
        source = options['source']
        img_duped = 0
        vid_duped = 0
        img_total = 0
        vid_total = 0
        total = 0
        thumbs = [60, 200, 750, 1000]

        # Handle connection with the backend (dinamically importing backend)
        # backend_file, backend_dropbox...
        backend = __import__('rgallery.management.commands.backend_%s' % storage, fromlist='*')

        # Set dirs (src, dest)
        srcdir, photodestdir, videodestdir = backend.set_dirs(source)

        # Handle connection with the backend
        client, bucket = backend.get_contents(srcdir)

        print "-"*80
        print "[***] Importing..."
        print ""

        for file in bucket:
            filepath = backend.filepath(file)
            if backend.is_image(file):
                try:
                    im = mymodels.Photo.objects.get(origen=os.path.basename(filepath))
                    img_duped += 1
                    print "%04d - Duped: %s" % (img_duped, os.path.basename(filepath))
                except:
                    # Downloading
                    print "%04d - Image %s not in database, downlaoding, thumbing and adding to database" % (total, os.path.basename(filepath))
                    nombre_imagen = namedup(filepath, photodestdir) # If duped adds '_1' to the name
                    img = backend.download(client, file, nombre_imagen, srcdir, photodestdir)
                    print "      Saved: %s/%s" % (photodestdir, nombre_imagen)

                    # Reading EXIF Data
                    data_image = img_get_exif(img)
                    capture_data = datetime.strptime(str(data_image['DateTimeOriginal']), "%Y:%m:%d %H:%M:%S")

                    # Adding to database
                    im = mymodels.Photo(image="uploads/photos/" + nombre_imagen,
                                        origen=os.path.basename(filepath),
                                        insert_date=datetime.now(),
                                        capture_date=capture_data,
                                        status=True)
                    im.save()
                    img_total += 1
                    print "      Added to database (%s)" % im.origen

                    # Open image to modify
                    im2 = Image.open(img) # Open
                    im2 = img_rotate(im2) # Rotate
                    im2.save(os.path.join(photodestdir, nombre_imagen))

                    # Creating thumbs
                    for thumb in thumbs:
                        print "      Thumb %sx%s" % (thumb, thumb)
                        c = Context({'image': im, 'thumb': "%sx%s" % (thumb, thumb)})
                        t = Template('{% load thumbnail %}{% thumbnail image thumb crop="top" as img %}{{ img.url }}{% endthumbnail %}')
                        t.render(c)
                        get_thumbnail(im, "%sx%s" % (thumb, thumb))

            if backend.is_video(file):
                try:
                    im = mymodels.Photo.objects.get(origen=os.path.basename(filepath))
                    vid_duped += 1
                    print "%04d - Duped: %s" % (vid_duped, os.path.basename(filepath))
                except:
                    # Downloading
                    print "%04d - Video %s not in database, downloading, thumbing and adding to database" % (total, os.path.basename(filepath))
                    video_name = namedup(filepath, videodestdir) # If duped adds '_1' to the name
                    video = backend.download(client, file, video_name, srcdir, videodestdir)
                    print "      Saved: %s/%s" % (videodestdir, video_name)

                    # Reading EXIF Data
                    rotate, data_video = video_get_exif(video)
                    capture_data = datetime.strptime(str(data_video), "%Y-%m-%d %H:%M:%S")

                    # Converting + thumb
                    thumbname = video_convert(video, file, srcdir, videodestdir, video_name, rotate)

                    # Adding to database
                    vid = mymodels.Photo(title=capture_data,
                                         image="uploads/videos/" + thumbname,
                                         video="uploads/videos/" + video_name,
                                         origen=os.path.basename(filepath),
                                         insert_date=datetime.now(),
                                         capture_date=capture_data,
                                         status=True)
                    vid.save()
                    vid_total += 1
                    print "      Added to database (%s)" % vid.origen

                    # Creating thumbs of image-video (poster)
                    for thumb in thumbs:
                        print "      Thumb %sx%s" % (thumb, thumb)
                        get_thumbnail(vid.image, "%sx%s" % (thumb, thumb))


            total += 1


        print ""
        print "-"*80
        print ""
        print "[***] Making missing thumbs"
        print ""
        conf.THUMBNAIL_DEBUG = True
        allphotos = mymodels.Photo.objects.all()
        for i,p in enumerate(allphotos):
            print "%04d - %s" % (i, p)
            for thumb in thumbs:
                c = Context({'image': p, 'thumb': "%sx%s" % (thumb, thumb)})
                t = Template('{% load thumbnail %}{% thumbnail image thumb crop="top" as img %}{{ img.url }}{% endthumbnail %}')
                t.render(c)
                get_thumbnail(p, "%sx%s" % (thumb, thumb))

        print ""
        print "-"*80
        print ""
        print "[***] Resume images"
        print ""
        print "[***] Duped images (ddbb): %s" % img_duped
        print "[***] Total images: %s" % img_total
        print ""
        print "[***] Resume videos"
        print ""
        print "[***] Duped videos (ddbb): %s" % vid_duped
        print "[***] Total videos: %s" % vid_total
        print ""
        print "[***] TOTAL: %s" % total
        print ""
        print "-"*80
