from django.contrib import admin

from django_tiniest_cms.models import Content


class ContentAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Content, ContentAdmin)
