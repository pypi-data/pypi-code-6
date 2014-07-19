from django.contrib import admin

from nanolog.models import Nanolog


class NanologAdmin(admin.ModelAdmin):
    list_display = ('log_type', 'details', 'note', 'created_date', 'ip', 'user', 'content_object', )
    search_fields = ('log_type', 'details', 'note', 'ip', 'user__username', 'user__first_name', 'user__last_name', )
    list_filter = ('log_type', )
    date_hierarchy = 'created_date'


admin.site.register(Nanolog, NanologAdmin)
