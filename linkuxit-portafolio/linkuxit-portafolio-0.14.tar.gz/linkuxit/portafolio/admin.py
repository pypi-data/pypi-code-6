from modeltranslation.admin import TranslationAdmin
from modeltranslation.admin import TranslationStackedInline

from .models import TeamMember
from .models import SocialLink
from .models import Service
from .models import Client
from .models import Country
from .models import Project
from .models import Image
from .models import Team
from .models import Testimonial

from django.contrib import admin


class SocialLinkInline(admin.StackedInline):
    model = SocialLink


class ImageInline(TranslationStackedInline):
    model = Image


class TeamMemberAdmin(TranslationAdmin):
    inlines = [SocialLinkInline]
    list_display = ['full_name', 'position', 'is_active']
    prepopulated_fields = {'slug': ('full_name',)}

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class TeamAdmin(TranslationAdmin):
    filter_horizontal = ('members',)
    prepopulated_fields = {'slug': ('name_en',)}

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class ClientAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'is_featured']

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class ProjectAdmin(TranslationAdmin):
    inlines = [ImageInline]
    filter_horizontal = ('developers', 'services')
    prepopulated_fields = {'slug': ('name',)}

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class ServiceAdmin(TranslationAdmin):
    list_display = ['title', 'is_featured']
    prepopulated_fields = {'slug': ('title_es', 'title_en')}

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class CountryAdmin(TranslationAdmin):

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }



class TestimonialAdmin(TranslationAdmin):

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
