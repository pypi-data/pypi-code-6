from models import *
from django.contrib import admin
class OptionAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    filter_horizontal = ['data_lists', 'relative_links', 'absolute_links', 'email_links', 'images', 'illustrations', 'lists', 'media_boxes', 'downloads', 'tables']
    fieldsets = (
    ('Data List', {
							'classes': ('collapse',),
							'fields':('data_lists',)}),
	
    ('List', {
							'classes': ('collapse',),
							'fields':('lists',)}),
	
    ('Relative Link', {
							'classes': ('collapse',),
							'fields':('relative_links',)}),
	
    ('Absolute Link', {
							'classes': ('collapse',),
							'fields':('absolute_links',)}),
	
    ('Email Link', {
							'classes': ('collapse',),
							'fields':('email_links',)}),
	('Image', {
							'classes': ('collapse',),
							'fields':('images',)}),
							
    ('Illustration', {
							'classes': ('collapse',),
							'fields':('illustrations',)}),
							
	('Media Box', {
							'classes': ('collapse',),
							'fields':('media_boxes',)}),
	
    ('Downloads', {
							'classes': ('collapse',),
							'fields':('downloads',)}),
    ('Table', {
							'classes': ('collapse',),
							'fields':('tables',)}),

    )
class ParagraphAdmin(admin.ModelAdmin):
    date_hierarchy = 'publish_date'
    search_fields = ['name', 'text']
    save_on_top = True
    save_as = True        
    filter_horizontal = ['options']  
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = 'publish_date'
    search_fields = ['title']
    filter_horizontal = ['paragraphs']
    save_on_top = True
    save_as = True
    
class ChapterAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = 'ts'
    filter_horizontal = ['pages']
    save_on_top = True
    save_as = True
    
class IllustrationAdmin(admin.ModelAdmin):
    search_fields = ['title',]
    save_on_top = True

class RelativeLinkAdmin(admin.ModelAdmin):
    search_fields = ['text',]
    save_on_top = True

class AbsoluteLinkAdmin(admin.ModelAdmin):
    search_fields = ['text',]
    save_on_top = True

class EmailLinkAdmin(admin.ModelAdmin):
    search_fields = ['text',]
    save_on_top = True
    
class ImageAdmin(admin.ModelAdmin):
    search_fields = ['title',]
    save_on_top = True

class ListAdmin(admin.ModelAdmin):
    save_on_top = True
    filter_horizontal = ['list_items']
    
class ListItemAdmin(admin.ModelAdmin):
    search_fields = ['name','text']
    save_on_top = True
    save_as = True
    filter_horizontal = ['options']  

class DataListAdmin(admin.ModelAdmin):
    filter_horizontal = ['data_titles']
    save_on_top = True
    
class DataListTitleAdmin(admin.ModelAdmin):
    filter_horizontal = ['data_items']
    save_on_top = True
    
class DataListDataAdmin(admin.ModelAdmin):
    search_fields = ['name','text']
    save_on_top = True
    save_as = True
    filter_horizontal = ['options']  
    
admin.site.register(MetaTag)

admin.site.register(Option, OptionAdmin)
admin.site.register(Paragraph, ParagraphAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(ChapterClass)
admin.site.register(PageClass)
admin.site.register(ParagraphClass)
admin.site.register(IllustrationClass)
admin.site.register(ImageClass)
admin.site.register(LinkClass)
admin.site.register(Illustration)
admin.site.register(Image, ImageAdmin)
admin.site.register(AbsoluteLink, AbsoluteLinkAdmin)
admin.site.register(RelativeLink)
admin.site.register(EmailLink, EmailLinkAdmin)
admin.site.register(MediaBox)
admin.site.register(List, ListAdmin)
admin.site.register(ListItem, ListItemAdmin)
admin.site.register(DataList, DataListAdmin)
admin.site.register(DataListData, DataListDataAdmin)
admin.site.register(DataListTitle, DataListTitleAdmin)
admin.site.register(DefaultClass)
admin.site.register(ListClass)
admin.site.register(Download)