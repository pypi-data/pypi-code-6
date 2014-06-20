__author__ = 'cltanuki'
from planning import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType


class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')

# Register your models here.
admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(models.TaskTemplate)
admin.site.register(models.ProjectTemplate)
admin.site.register(models.Task)
admin.site.register(models.Project)