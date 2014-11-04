# -*- coding: utf-8 -*-

import os
import json
import Image
from StringIO import StringIO
from datetime import datetime

from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib.sites.models import Site
from django.contrib import messages
import models as mymodels
import forms as myforms

from sorl.thumbnail import get_thumbnail
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from taggit.models import Tag

from django.conf import settings as conf

from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import ProcessFormView

from management.commands.utils import *
from forms import PhotoForm


class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class Photos(TagMixin, ListView):

    template_name = "rgallery/photos.html"
    context_object_name = "photos"
    paginate_by = 150

    def get_queryset(self):
        return mymodels.Photo.objects.all().filter(status=1, folder__isnull=True).order_by('-capture_date')

    def get_context_data(self, **kwargs):
        context = super(Photos, self).get_context_data(**kwargs)
        folders = mymodels.Folder.objects.filter(status=1)
        form = PhotoForm

        context.update({
            'title': _(u'Photos'),
            'form': form,
            'folders': folders,
        })
        return context


class PhotosFolder(ListView):

    template_name = "rgallery/photos.html"
    context_object_name = "photos"

    def get_queryset(self):
        folder = mymodels.Folder.objects.get(slug=self.kwargs['folder'])
        return mymodels.Photo.objects.all().filter(status=1, folder=folder).order_by('-capture_date')

    def get_context_data(self, **kwargs):
        context = super(PhotosFolder, self).get_context_data(**kwargs)

        context.update({
            'title': _(u'Photos'),
        })
        return context


class PhotosTag(ListView):

    template_name = "rgallery/photos.html"
    model = mymodels.Photo
    context_object_name = "photos"
    paginate_by = 100

    def get_queryset(self):
        return mymodels.Photo.objects.filter(status=1,
            tags__slug=self.kwargs.get('slug', None)).order_by('-capture_date')


class PhotoAddTag(LoginRequiredMixin, SuperuserRequiredMixin, ListView):

    model = mymodels.Photo

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax() and self.request.method == 'POST':
            pk = json.loads(self.request.POST.get('pk', None))
            tags = json.loads(self.request.POST.get('tags', None))
            photo = get_object_or_404(mymodels.Photo, pk=pk)
            photo.tags.clear()
            if len(tags) > 0:
                for tag in tags:
                    try:
                        t = Tag.objects.get(slug=tag)
                        photo.tags.add(t)
                    except:
                        photo.tags.add(tag)
            photo.save()
            rendered = render_to_string('rgallery/_listags.html',
                                        {'record': photo.tags.all()})
        return HttpResponse(rendered);


class PhotoAdd(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):

    model = mymodels.Photo
    form_class = PhotoForm
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Name (if exists in database)
        try:
            im = mymodels.Photo.objects.get(origen=os.path.basename(form.files['file'].name))
        except:
            nombre_imagen = str(os.path.basename(form.files['file'].name)).replace('/', '').replace(' ','_').replace(':','-')

            # Extracting Exif data
            data_image = img_get_exif(form.files['file'])
            capture_data = datetime.strptime(str(data_image['DateTimeOriginal']), "%Y:%m:%d %H:%M:%S")

            # Name (if exists in disk)
            destdir = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'photos')
            if os.path.exists(os.path.join(destdir, nombre_imagen)) == True:
                nombre_imagen = str(os.path.basename(form.files['file'].name)).replace('/', '').replace(' ','_').replace(':','-').replace('.jpg','') + '_1.jpg'
            data = ""
            for c in form.files['file'].chunks():
                data += c
            imagefile  = StringIO(data)
            img = Image.open(imagefile)
            img = img_rotate(img)

            # Save
            img.save(os.path.join(destdir, nombre_imagen), img.format)

            # Add to database
            im = mymodels.Photo(image="uploads/photos/" + nombre_imagen,
                                origen=form.files['file'].name,
                                insert_date=datetime.now(),
                                capture_date=capture_data,
                                status=True)
            im.save()

            # Thumbs
            thumbs = [200, 750, 1000]
            for thumb in thumbs:
                im = get_thumbnail(im, "%sx%s" % (thumb, thumb))

        return HttpResponseRedirect(self.get_success_url())


class PhotoDelete(LoginRequiredMixin, SuperuserRequiredMixin, ListView):

    model = mymodels.Photo
    template_name = "rgallery/photo_delete.html"

    def get_context_data(self, **kwargs):
        if self.request.is_ajax() and self.request.method == 'GET':
            pk = json.loads(self.request.GET.get('pk', None))
            photo = get_object_or_404(mymodels.Photo, pk=pk)
            photo.delete()
            return True


class PhotoGetVideo(LoginRequiredMixin, ListView):

    model = mymodels.Photo

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax() and self.request.method == 'POST':
            pk = json.loads(self.request.POST.get('pk', None))
            photo = get_object_or_404(mymodels.Photo, pk=pk)
            rendered = render_to_string('rgallery/_video.html',
                                        {'video': photo.video})
        return HttpResponse(rendered);


class Videos(ListView):

    template_name = "rgallery/videos.html"
    context_object_name = "videos"
    paginate_by = 6

    def get_queryset(self):
        vid = mymodels.Video.objects.all().filter(status=1, folder__isnull=True).order_by('-capture_date')
        print vid
        return vid

    def get_context_data(self, **kwargs):
        context = super(Videos, self).get_context_data(**kwargs)
        context.update({
            'title': _(u'Videos'),
        })
        return context