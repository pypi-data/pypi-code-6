# -*- coding: utf-8 -*-

import os.path
from django.contrib import admin
from django.utils.safestring import mark_safe

import models as mymodels


class StampAdmin(admin.ModelAdmin):
    list_display = ('customer', 'start', 'end', 'customer', 'action')
    search_fields = ('customer', 'action', )


admin.site.register(mymodels.Stamp, StampAdmin)
admin.site.register(mymodels.Customer)
