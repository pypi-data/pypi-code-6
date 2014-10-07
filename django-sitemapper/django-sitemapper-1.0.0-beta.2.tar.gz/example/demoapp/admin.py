from django.contrib import admin
from .models import Demo

# Step 1: You'll need to import the admin-inline
from sitemapper.admin import SitemapEntryInline


class DemoAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'modified')
    readonly_fields = ('modified',)
    prepopulated_fields = {'slug': ('title',)}

    # Step 2: Add the admin-inline to the inlines of your admin class
    inlines = [SitemapEntryInline]

admin.site.register(Demo, DemoAdmin)
