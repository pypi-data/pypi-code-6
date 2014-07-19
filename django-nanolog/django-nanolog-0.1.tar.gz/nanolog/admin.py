from django.contrib import admin

from nanolog.models import Nanolog


class NanologAdmin(admin.ModelAdmin):
    list_display = ('details', 'note', 'created_date', 'ip', )
    search_fields = ('log_type', 'details', 'note', 'ip', )
    list_filter = ('log_type', )
    date_hierarchy = 'created_date'


admin.site.register(Nanolog, NanologAdmin)
