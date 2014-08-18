from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import (ChartJSBarWidget, ChartJSDoughnutWidget, ChartJSLineWidget,
                     ChartJSPieWidget, ChartJSRadarWidget, ExpressionWidget,
                     JustgageWidget, MessageWidget, NovusLineChartWidget,
                     WebsiteWidget)


class WidgetdAdmin(admin.ModelAdmin):
    list_display = ('label', 'datasource', 'python_enabled', 'javascript_enabled')
    list_editable = ('datasource', 'python_enabled', 'javascript_enabled')


admin.site.register(ChartJSBarWidget, WidgetdAdmin)
admin.site.register(ChartJSDoughnutWidget, WidgetdAdmin)
admin.site.register(ChartJSLineWidget, WidgetdAdmin)
admin.site.register(ChartJSPieWidget, WidgetdAdmin)
admin.site.register(ChartJSRadarWidget, WidgetdAdmin)
admin.site.register(ExpressionWidget, WidgetdAdmin)
admin.site.register(JustgageWidget, WidgetdAdmin)
admin.site.register(MessageWidget, WidgetdAdmin)
admin.site.register(NovusLineChartWidget, WidgetdAdmin)
admin.site.register(WebsiteWidget, WidgetdAdmin)
