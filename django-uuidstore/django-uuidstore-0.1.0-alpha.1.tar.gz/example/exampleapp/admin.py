from django.contrib import admin
from .models import (
    ModelWithDenormalisedChar,
    ModelWithMonkeyPatchedUUID,
    ModelWithDenormalisedUUID,
    ModelWithDetatchedUUID
    )


class AdminWithUUID(admin.ModelAdmin):
    list_display = ('title', 'uuid')
    readonly_fields = ('uuid',)

admin.site.register(ModelWithDenormalisedChar, AdminWithUUID)
admin.site.register(ModelWithMonkeyPatchedUUID, AdminWithUUID)
admin.site.register(ModelWithDenormalisedUUID, AdminWithUUID)
admin.site.register(ModelWithDetatchedUUID)
