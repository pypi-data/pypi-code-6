#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, errno
import re
import sys
import time
import datetime
import gzip
import glob

import Image, ExifTags
from ExifTags import TAGS

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.template import Context, Template
from django.conf import settings as conf
import rgallery.models as mymodels
from datetime import datetime
from pprint import pprint

from sorl.thumbnail import get_thumbnail


def get_exif(fn):
    """
    data = get_exif('img/2013-04-13 12.17.09.jpg')
    print data
    """
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    try:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
    except:
        now = datetime.now()
        ret['DateTimeOriginal'] = now.strftime("%Y:%m:%d %H:%M:%S")

    try:
        str(ret['DateTimeOriginal'])
    except:
        now = datetime.now()
        ret['DateTimeOriginal'] = now.strftime("%Y:%m:%d %H:%M:%S")

    return ret


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def img_rotate(im2):
    try:
        # Rotar si es necesario
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(im2._getexif().items())
        if exif[orientation] == 3:
            im2=im2.rotate(180, expand=True)
        elif exif[orientation] == 6:
            im2=im2.rotate(270, expand=True)
        elif exif[orientation] == 8:
            im2=im2.rotate(90, expand=True)
    except:
        pass

    return im2


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
                '--type',
                dest='type',
                default='photos',
                help='Type: photos|videos'
            ),
            make_option(
                '--debug',
                dest='debug',
                default=0,
                help='Verbosity information'
            ),
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
        debug = options['debug']
        storage = options['storage']
        source = options['source']
        repetidas = 0
        descargadas = 0
        total = 0
        thumbs = [200, 750, 1000]
        if storage == 'dropbox':
            srcdir = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'dropbox')
        if storage == 'file':
            srcdir = source
        destdir = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'photos')
        if os.path.exists(destdir) == False:
            mkdir_p(destdir)

        # Handle connection with the backend (Dropbox in this case)
        if storage == 'dropbox':
            from backend_dropbox import get_contents, get_images, download
        if storage == 'file':
            from backend_file import get_contents, get_images, download

        # Handle connection with the backend
        client, bucket = get_contents(srcdir, debug)

        print "-"*80
        print "[***] Importing..."
        print ""

        for file in bucket:
            #import pdb; pdb.set_trace()
            try:
                filepath = file['path']
            except:
                filepath = file.path

            try:
                im = mymodels.Photo.objects.get(origen=os.path.basename(filepath))
                repetidas += 1
                print "%04d - Repetida: %s" % (repetidas, os.path.basename(filepath))
            except:
                print "%04d - La imagen %s No esta en bd, descargar y agregar a bbdd y hacer thumb" % (total, os.path.basename(filepath))
                #import pdb; pdb.set_trace()
                nombre_imagen = "%s%s" % (slugify(str(os.path.splitext(os.path.basename(filepath))[0]).replace('/', '').replace(' ','_').replace(':','-')),
                                        str(os.path.splitext(os.path.basename(filepath))[1]))

                # Descargar original a img (si ya existe _1.jpg)
                if os.path.exists(destdir + '/' + nombre_imagen) == True:
                    nombre_imagen = "%s_1%s" % (slugify(str(os.path.splitext(os.path.basename(filepath))[0]).replace('/', '').replace(' ','_').replace(':','-')),
                                                     str(os.path.splitext(os.path.basename(filepath))[1]))
                    print "      Duplicada en disco, cambiado nombre a: %s" % nombre_imagen
                    descargadas += 1
                img = download(client, file, nombre_imagen, srcdir, destdir, debug)
                print "      Guardada: %s/%s" % (destdir, nombre_imagen)


                # Datos EXIF
                data_image = get_exif(img)
                capture_data = datetime.strptime(str(data_image['DateTimeOriginal']), "%Y:%m:%d %H:%M:%S")

                # Agregamos a BD
                im = mymodels.Photo(image="uploads/photos/" + nombre_imagen,
                                    origen=os.path.basename(filepath),
                                    insert_date=datetime.now(),
                                    capture_date=capture_data,
                                    status=True)
                im.save()
                print "      Agregada a bbdd (%s)" % im.origen

                # Abrimos imagen para modificaciones
                im2 = Image.open(img) # Abrir
                im2 = img_rotate(im2) # Rotar
                im2.save(destdir + '/' + nombre_imagen)

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
            c = Context({'image': p})
            t = Template('{% load thumbnail %}{% thumbnail image "200x200" crop="top" as img %}{{ img.url }}{% endthumbnail %}')
            t.render(c)

            for thumb in thumbs:
                im = get_thumbnail(p, "%sx%s" % (thumb, thumb))

        print ""
        print "-"*80
        print ""
        print "[***] Resumen"
        print ""
        print "[***] Repetidas en db: %s" % repetidas
        print "[***] Repetidas en disco: %s" % descargadas
        print "[***] Total: %s" % total
        print ""
        print "-"*80
