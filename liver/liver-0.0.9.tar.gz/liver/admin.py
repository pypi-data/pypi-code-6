from models import *

import logging
logger = logging.getLogger("liver.admin")

from django import forms
from django.contrib import admin
from django.db.models import Q

from django.utils.translation import ugettext_lazy, ugettext as _

def clone(modeladmin, request, queryset):
    for o in queryset:
        o.clone()
clone.short_description = _("Clone")

class RecordRuleInLine(admin.TabularInline):
        model = RecordRule
        extra = 1

class RecordMetadataInLine(admin.TabularInline):
        model = RecordMetadata
        extra = 1

class RecordJobMetadataInLine(admin.TabularInline):
        model = RecordJobMetadata
        extra = 1

class RecordSourceAdmin(admin.ModelAdmin):
    actions = [
            clone,
    ]

    inlines = [
                RecordRuleInLine,
                RecordMetadataInLine,
    ]

    list_display = [
            'sources_group',
            # 'insertion_date',
            'modification_date',
            'enabled',
            'enabled_since',
            'enabled_until',
            'edit_html',
    ]

    list_editable = [
            'sources_group',
            'enabled',
            'enabled_since',
            'enabled_until',

    ]

    list_display_links = ['edit_html']

    list_per_page = 200

    def edit_html(self, queryset):
        return '''<a href="%s/">Edit</a>''' % queryset.id
    edit_html.short_description = ''
    edit_html.allow_tags = True



class RecordJobAdmin(admin.ModelAdmin):
    actions = [
            clone,
    ]

    exclude = ["record_source"]
    readonly_fields = [
            'insertion_date',
            'modification_date',
            'execution_date',
            'completion_date',
    ]

    fieldsets = (
        (None, {
            'fields': (
                (
            'sources_group',
            'scheduled_start_date',
            'scheduled_duration',
            'enabled',
                ),

            )
        }),
        (_("Process"), {
            'fields': (
                (
            'status',
            'recorder',
            'result',
                ),
                (
            'insertion_date',
            'modification_date',
            'execution_date',
            'completion_date',
                ),

            )
        }),

    )

    list_filter = [
            "enabled",
            "status",
            "sources_group",
            "recorder",
    ]

    inlines = [
        RecordJobMetadataInLine,
    ]

class RecordAdmin(admin.ModelAdmin):
    ordering = ['-insertion_date']

    actions = [
            # clone,
    ]

    readonly_fields = [
            'name',
            'insertion_date',
            'modification_date',
            'record_job',
            'profiles',
            'metadata',
    ]

    fieldsets = (
        (None, {
            'fields': (
                (
            'name',
            'insertion_date',
            'modification_date',
                ),

            )
        }),
        (_("Information"), {
            'fields': (
                (
            'profiles',
            'metadata',
                ),
            )
        }),

    )


    list_display = [
            'name',
            'insertion_date',
            'modification_date',
            'profiles',
            'metadata',
    ]

    list_per_page = 200

    def has_add_permission(self, request):
        return False

    def queryset(self, request):
        qs = super(RecordAdmin, self).queryset(request)
        return qs.filter(Q(to_delete=False))


class SourceInLine(admin.TabularInline):
    model = Source
    fk_name = 'sources_group'
    extra = 0

class SourcesGroupAdmin(admin.ModelAdmin):
    actions = [
            clone,
    ]
    ordering = ['name']

    readonly_fields = [
            'insertion_date',
            'modification_date',
    ]

    fieldsets = (
        (None, {
            'fields': (
                (
            'name',
            'external_id',
                ),

            )
        }),
        (None, {
            'fields': (
                (
            'insertion_date',
            'modification_date',
                ),

            )
        }),
        (None, {
            'fields': (
                (
            'default_offset_start',
            'default_offset_end',
            'default_availability_window',
                ),

            )
        }),
    )

    inlines = [
      SourceInLine,
    ]


class RecorderAdmin(admin.ModelAdmin):
    ordering = ['name','token']

# admin.site.register(Source)
admin.site.register(SourcesGroup,SourcesGroupAdmin)
admin.site.register(Recorder,RecorderAdmin)
admin.site.register(RecordSource,RecordSourceAdmin)
admin.site.register(RecordJob,RecordJobAdmin)
admin.site.register(Record,RecordAdmin)

