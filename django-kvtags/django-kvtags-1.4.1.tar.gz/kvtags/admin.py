from django.contrib import admin
from kvtags.models import *


class KeyValueInline(admin.TabularInline):
    model = KeyValue


class TagAdmin(admin.ModelAdmin):
    inlines = [
        KeyValueInline,
    ]


admin.site.register(Tag, TagAdmin)
admin.site.register(TaggedItem)