from django.contrib import admin

#import local models
from djhcup_integration.models import Edition, IntegrationTable, Definition, Column, ColumnName

#Register models
admin.site.register(Edition)
admin.site.register(IntegrationTable)
admin.site.register(Definition)
admin.site.register(Column)
admin.site.register(ColumnName)
