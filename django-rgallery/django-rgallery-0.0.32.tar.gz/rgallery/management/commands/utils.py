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
from subprocess import Popen, PIPE

from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.template import Context, Template
from django.conf import settings as conf

import Image, ExifTags
from ExifTags import TAGS
from sorl.thumbnail import get_thumbnail
from shutil import copyfile

# GENERAL **********************************************************************

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def namedup(filepath, photodestdir):
    nombre_imagen = "%s%s" % (slugify(str(os.path.splitext(os.path.basename(filepath))[0]).replace('/', '').replace(' ','_').replace(':','-')),
                            str(os.path.splitext(os.path.basename(filepath))[1]))

    # Descargar original a img (si ya existe _1.jpg)
    if os.path.exists(os.path.join(photodestdir, nombre_imagen)) == True:
        nombre_imagen = "%s_1%s" % (slugify(str(os.path.splitext(os.path.basename(filepath))[0]).replace('/', '').replace(' ','_').replace(':','-')),
                                         str(os.path.splitext(os.path.basename(filepath))[1]))
        print "      Duped in disk, name changed to: %s" % nombre_imagen
    return nombre_imagen


# IMAGES ***********************************************************************

def img_get_exif(fn):
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


# VIDEOS ***********************************************************************

def video_get_exif(fn):
    # data = get_exif('img/2013-04-13 12.17.09.jpg')
    # print data

    rotate = '0'
    creation = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    process = Popen([conf.FFPROBE, '-show_streams', str(fn)],
                    stdout=PIPE,
                    stderr=PIPE)
    stdout, stderr = process.communicate()

    for line in iter(stdout.splitlines()):
        if re.search(r'TAG:rotate', line):
            rotate = line.split('=')[1]
        if re.search(r'TAG:creation_time', line):
            creation = line.split('=')[1]

    return rotate, creation


def video_convert(video, file, srcdir, destdir, video_name, rotate):
    # Convertir con FFMPEG      (en principio no hace falta convertir...)
    # Hacer thumb               (...pero hace falta hacer thumb)

    # ffmpeg -i [sourcefile.avi] -acodec mp3 -ar 22050 -ab 32 -f flv -s 320×240 [destfile.flv]
    # flvtool2 -U [flvfile]
    # ffmpeg -y -i [videofile] -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s 320×240 [thumbnailimage.png]
    #
    # convertvideo = "%s -i %s -acodec %s -ar 22050 -ab 32 -f flv -s %s %s" % (conf.ZERO14_FFMPEG, src,
    #                                                 conf.ZERO14_FFMPEG_ACODEC, conf.ZERO14_FFMPEG_VIDEO_SIZE,
    #                                                 flvfile)
    # MarcosBL:
    # ffmpeg -vstats_file /tmp/vstats -i "$1" -f mp4 -vcodec libx264 -r 25 -b 560000 -ab 64 -ar 44100 -threads 0 "$2" 2>/dev/null &

    try:
        src = file.path
    except:
        src = video
    dst = os.path.join(destdir, video_name)
    thumbname = "%s%s" % (slugify(str(os.path.splitext(os.path.basename(video_name))[0])),'.png')
    thumb = os.path.join(destdir, thumbname)

    rotate, data_video = video_get_exif(dst)

    transpose = ''
    size = conf.FFMPEG_THUMB_SIZE
    if rotate == '90':
        transpose = '-vf "transpose=1"'
        size = conf.FFMPEG_THUMB_SIZE_INVERSE

    # Conf
    # FFPROBE='/opt/local/bin/ffprobe'
    # FFMPEG='/opt/local/bin/ffmpeg'
    # FFMPEG_VCODEC_THUMB='png'
    # FFMPEG_THUMB_SIZE='444x250'
    # FFMPEG_THUMB_SIZE_INVERSE='250x444'

    grabimage = "%s -y -i '%s' -vframes 1 -ss 00:00:00 -an -vcodec %s -f rawvideo -s %s %s %s " % (conf.FFMPEG, src,
                                                                                              conf.FFMPEG_VCODEC_THUMB,
                                                                                              size,
                                                                                              transpose,
                                                                                              thumb)
    #os.system(convertvideo)
    #print "      [%s]" % grabimage
    os.system(grabimage)

    # Copy file to dest
    copyfile(src, dst)

    return thumbname