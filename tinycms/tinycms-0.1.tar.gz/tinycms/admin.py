from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from models import *

class ContentInline(admin.StackedInline):
    model = Content

class PageAdmin(MPTTModelAdmin):
    inlines = [ContentInline]

#admin.site.register(Page,MPTTModelAdmin)
admin.site.register(Page,PageAdmin)

class ContentAdmin(admin.ModelAdmin):
    list_display  = ['page','value_name']
admin.site.register(Content,ContentAdmin)




