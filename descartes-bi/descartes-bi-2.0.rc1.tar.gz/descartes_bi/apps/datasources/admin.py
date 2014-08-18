from django.contrib import admin

from .models import Datasource, Host


class DatasourceAdmin(admin.ModelAdmin):
    list_display = ('label', 'host', 'data_format', 'python_enabled')
    list_editable = ('host',)


class HostAdmin(admin.ModelAdmin):
    list_display = ('label', 'netloc')
    list_editable = ('netloc',)


admin.site.register(Datasource, DatasourceAdmin)
admin.site.register(Host, HostAdmin)
