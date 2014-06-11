from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Flatpage
from .forms import FlatpageForm


class FlatpageAdmin(admin.ModelAdmin):
    form = FlatpageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('template_name',)}),
    )
    list_display = ('url', 'title')
    search_fields = ('url', 'title')

admin.site.register(Flatpage, FlatpageAdmin)
