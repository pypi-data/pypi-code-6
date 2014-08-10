from __future__ import absolute_import

from django.contrib import admin

from .models import Inventory, ItemTemplate, Location, Log, Supplier


class ItemTemplateAdmin(admin.ModelAdmin):
    filter_horizontal = ('supplies', 'suppliers')


admin.site.register(Location)
admin.site.register(Log)
admin.site.register(ItemTemplate, ItemTemplateAdmin)
admin.site.register(Inventory)
admin.site.register(Supplier)
