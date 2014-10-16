from django.contrib import admin
from .models import ObjectUUID


class ObjectUUIDAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'content_type', 'object_id')
    readonly_fields = ('content_object', 'uuid')

admin.site.register(ObjectUUID, ObjectUUIDAdmin)
