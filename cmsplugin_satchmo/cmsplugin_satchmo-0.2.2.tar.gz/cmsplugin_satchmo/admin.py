# -*- coding: utf-8 -*- 
from django.contrib import admin

from cmsplugin_satchmo.models import SatchmoSiteSetting

class SatchmoSiteSettingAdmin(admin.ModelAdmin):
	list_display = ['site', 'product_url_path', 'category_url_path',]
	list_filter = ['site',]
	search_fields = ['site__name', 'shop_base', 'product_slug', 'category_slug']

admin.site.register(SatchmoSiteSetting, SatchmoSiteSettingAdmin)
