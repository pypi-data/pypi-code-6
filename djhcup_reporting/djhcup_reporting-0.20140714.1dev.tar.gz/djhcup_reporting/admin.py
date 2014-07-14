from django.contrib import admin

#import local models
from djhcup_reporting.models import FilterGroup, Filter, Column, ReportingTable, LookupTable, Universe

#Register models
admin.site.register(FilterGroup)
admin.site.register(Filter)
admin.site.register(Column)
admin.site.register(ReportingTable)
admin.site.register(LookupTable)
admin.site.register(Universe)
