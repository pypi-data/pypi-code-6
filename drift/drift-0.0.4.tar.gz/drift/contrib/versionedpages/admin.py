from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Page, Version 


class PageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Page, PageAdmin)
admin.site.register(Version)
