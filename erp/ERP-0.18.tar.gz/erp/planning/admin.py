__author__ = 'cltanuki'
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from . import models


class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')

# Register your models here.
admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(models.TaskTemplate)
admin.site.register(models.ProjectTemplate)
admin.site.register(models.Task)
admin.site.register(models.Project)